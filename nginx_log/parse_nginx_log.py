from flask import Flask, request, jsonify
import os
import re
import hashlib
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh import index
from whoosh.qparser import QueryParser, AndGroup, MultifieldParser
from collections import defaultdict
from datetime import datetime
import tempfile

from whoosh.sorting import FieldFacet

app = Flask(__name__)

# Define the log directory and index directory
log_dir = "logs"
index_dir = "indexdir"

# Ensure the directories exist
os.makedirs(log_dir, exist_ok=True)
os.makedirs(index_dir, exist_ok=True)


# Function to create a dynamic schema based on the provided fields
def create_schema(fields):
    schema_fields = {}
    for field, field_type in fields.items():
        if field_type == "TEXT":
            schema_fields[field] = TEXT(stored=True, sortable=True)
        elif field_type == "ID":
            schema_fields[field] = ID(stored=True, sortable=True)
        elif field_type == "NUMERIC":
            schema_fields[field] = NUMERIC(stored=True, sortable=True)
    return Schema(**schema_fields)


def project_api_format_fields(match, schema_fields):
    line_map = {}
    for i, field in enumerate(schema_fields):
        field_value = match.group(i + 1)
        if schema_fields[field] == "NUMERIC":
            # parsed_lines.append({field: int(field_value)})
            # 尝试转为 int,如果失败，转为 float
            if field == "response_time":
                # 带有单位，比如 1.23µs 1.23ms 1.23s 1min2s
                if "µs" in field_value:
                    field_value = field_value.replace("µs", "")
                    field_value = float(field_value)
                    field_value = int(field_value)
                elif "ms" in field_value:
                    field_value = field_value.replace("ms", "")
                    field_value = float(field_value)
                    field_value = int(field_value)
                elif "s" in field_value:
                    field_value = field_value.replace("s", "")
                    field_value = float(field_value)
                    field_value = int(field_value * 1000)
                elif "min" in field_value:
                    field_value = field_value.replace("min", "")
                    field_value = field_value.split("s")
                    field_value = int(field_value[0]) * 60 + int(field_value[1])
                line_map[field] = field_value
            else:
                try:
                    field_value = int(field_value)
                    line_map[field] = field_value
                except ValueError:
                    field_value = float(field_value)
                    field_value = int(field_value * 1000)
                    line_map[field] = field_value
        else:
            line_map[field] = field_value
    return line_map


# Function to parse the log file based on the provided regex pattern
def parse_log_file(file_path, log_pattern, schema_fields, format_fields, limit=0):
    compiled_pattern = re.compile(log_pattern)
    parsed_lines = []
    lines = []
    with open(file_path, 'r', encoding='utf-8') as log_file:
        i = 0
        for line in log_file:
            lines.append(line)
            i += 1
            if 0 < limit < i:
                break
            match = compiled_pattern.match(line.strip())
            if match:
                # parsed_lines.append({field: match.group(i + 1) for i, field in enumerate(schema_fields)})
                groups = match.groups()
                if len(groups) != len(schema_fields):
                    # 遍历 groups, 把目前的解析结果返回
                    error_string = f"Error parsing line: {line.strip()}"
                    for i, g in enumerate(groups):
                        error_string += f"\nGroup {i}: {g}"
                    return [], error_string
                line_map = format_fields(match, schema_fields)
                parsed_lines.append(line_map)
    if len(parsed_lines) == 0:
        return [], "parse error, please check the log pattern.\n" + "\n".join(lines)
    return parsed_lines, ""




# Function to calculate MD5 of a file
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    # Get first 100 lines and last 100 lines
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        first_100_lines = lines[:100]
        last_100_lines = lines[-100:]
        for line in first_100_lines + last_100_lines:
            hash_md5.update(line.encode('utf-8'))
    return hash_md5.hexdigest()


@app.route('/api/upload', methods=['POST'])
def upload_log():
    if 'logfile' not in request.files or 'log_pattern' not in request.form:
        return jsonify({"error": "No file or pattern provided"}), 400

    logfile = request.files['logfile']
    log_pattern = request.form['log_pattern']
    fields = request.form.get('fields')
    format_code = request.form.get('format_fields')

    if not fields:
        return jsonify({"error": "No fields provided"}), 400

    if not format_code:
        return jsonify({"error": "No format fields code provided"}), 400
    # Safely execute the format function
    try:
        exec_globals = {}
        exec_locals = {}
        exec(format_code, exec_globals, exec_locals)
        if 'format_fields' not in exec_locals:
            return jsonify({"error": "format_fields function not found in provided code"}), 400
        format_fields = exec_locals['format_fields']
    except Exception as e:
        return jsonify({"error": f"Failed to execute format function: {str(e)}"}), 400

    # Convert fields from string to dictionary
    schema_fields = {field.split(":")[0]: field.split(":")[1] for field in fields.split(",")}

    # Create a temporary file to store the uploaded log
    temp_file = tempfile.NamedTemporaryFile(delete=False, dir=log_dir)
    logfile.save(temp_file.name)

    # Calculate MD5 hash
    md5_hash = calculate_md5(temp_file.name)

    # Create sub-directory based on MD5 hash
    log_subdir = os.path.join(log_dir, md5_hash)
    os.makedirs(log_subdir, exist_ok=True)
    # index_dir
    index_subdir = os.path.join(index_dir, md5_hash)
    os.makedirs(index_subdir, exist_ok=True)

    # Move the temporary file to the final location
    final_log_path = os.path.join(log_subdir, md5_hash)
    os.rename(temp_file.name, final_log_path)

    # 保存文件名
    with open(os.path.join(log_subdir, "filename.txt"), "w") as f:
        f.write(str(logfile.filename))

    parsed_lines, error_string = parse_log_file(final_log_path, log_pattern, schema_fields, format_fields, limit=10)
    parsed_first_100 = parsed_lines[:10]

    return jsonify({
        "md5": md5_hash,
        "first_100_parsed": parsed_first_100,
        "error": error_string,
    })


@app.route('/api/confirm', methods=['POST'])
def confirm_parse():
    md5_hash = request.form['md5']
    log_pattern = request.form['log_pattern']
    fields = request.form['fields']
    format_code = request.form.get('format_fields')

    if not fields:
        return jsonify({"error": "No fields provided"}), 400

    if not format_code:
        return jsonify({"error": "No format fields code provided"}), 400
    # Safely execute the format function
    try:
        exec_globals = {}
        exec_locals = {}
        exec(format_code, exec_globals, exec_locals)
        if 'format_fields' not in exec_locals:
            return jsonify({"error": "format_fields function not found in provided code"}), 400
        format_fields = exec_locals['format_fields']
    except Exception as e:
        return jsonify({"error": f"Failed to execute format function: {str(e)}"}), 400

    index_subdir = os.path.join(index_dir, md5_hash)
    # 如果 index 存在，直接返回
    if index.exists_in(index_subdir):
        return jsonify({"status": "success"})

    # Convert fields from string to dictionary
    schema_fields = {field.split(":")[0]: field.split(":")[1] for field in fields.split(",")}
    schema = create_schema(schema_fields)

    log_subdir = os.path.join(log_dir, md5_hash)
    final_log_path = os.path.join(log_subdir, md5_hash)

    parsed_lines, error_string = parse_log_file(final_log_path, log_pattern, schema_fields, format_fields)

    # Initialize or open the Whoosh index
    if not index.exists_in(index_subdir):
        ix = index.create_in(index_subdir, schema)
    else:
        ix = index.open_dir(index_subdir)

    # Store parsed logs into Whoosh index
    with ix.writer() as writer:
        for line in parsed_lines:
            writer.add_document(**line)

    # 保存 schema 到 log_subdir 目录，之后查询时需要用到
    with open(os.path.join(log_subdir, "schema.txt"), "w") as f:
        f.write(str(fields))

    return jsonify({
        "status": "success",
        "total_lines_parsed": len(parsed_lines),
        "error": error_string,
    })


@app.route('/api/aggregate_by_response_time', methods=['GET'])
def aggregate_by_response_time():
    md5_id = request.args.get('id', '')
    index_subdir = os.path.join(index_dir, md5_id)
    ix = index.open_dir(index_subdir)
    with ix.searcher() as searcher:
        results = []
        query = QueryParser("endpoint", ix.schema, group=AndGroup).parse('*:*')
        search_results = searcher.search(query, limit=None)

        response_time_dict = defaultdict(list)
        for result in search_results:
            response_time_dict[result['endpoint']].append(result['response_time'])

        sorted_results = sorted(response_time_dict.items(), key=lambda x: sum(x[1]) / len(x[1]))

        for result in sorted_results:
            average_response_time = sum(result[1]) / len(result[1])
            results.append({
                "endpoint": result[0],
                "average_response_time": average_response_time
            })
    # 排序
    results = sorted(results, key=lambda x: x['average_response_time'], reverse=True)
    return jsonify(results)


@app.route('/api/list', methods=['GET'])
def list_logs():
    md5_hash = request.args.get('md5')
    query_str = request.args.get('q', '')
    sort_field = request.args.get('sort_field', '')
    is_reverse = request.args.get('is_reverse', 'false').lower() == 'true'
    limit = int(request.args.get('limit', 100))

    if not md5_hash:
        return jsonify({"error": "md5 parameter is required"}), 400

    index_subdir = os.path.join(index_dir, md5_hash)
    if not os.path.exists(index_subdir):
        return jsonify({"error": "Invalid md5 parameter"}), 400

    if not index.exists_in(index_subdir):
        return jsonify({"error": "Index does not exist"}), 400

    schema_file = os.path.join(log_dir, md5_hash, "schema.txt")
    if not os.path.exists(schema_file):
        return jsonify({"error": "Schema file does not exist"}), 400

    # Read schema file
    with open(schema_file, 'r') as f:
        schema_content = f.read().strip()

    # Parse schema fields
    schema_fields = {}
    for field in schema_content.split(','):
        name, field_type = field.split(':')
        schema_fields[name] = field_type

    searchable_fields = [name for name, field_type in schema_fields.items() if field_type in {"TEXT", "ID"}]

    ix = index.open_dir(index_subdir)

    results = []
    with ix.searcher() as searcher:
        if query_str:
            parser = MultifieldParser(searchable_fields, schema=ix.schema)
            query = parser.parse(query_str)
        else:
            # Select a field from schema_fields to perform a match-all query
            any_field = list(schema_fields.keys())[0]
            query = QueryParser(any_field, ix.schema).parse("*")

        if sort_field:
            facet = FieldFacet(sort_field, reverse=is_reverse)
            search_results = searcher.search(query, sortedby=facet, limit=limit)
        else:
            search_results = searcher.search(query, limit=limit)

        total_count = search_results.scored_length() if query_str else searcher.doc_count()

        for result in search_results:
            results.append(dict(result))

    return jsonify({
        "results": results,
        "total_count": total_count,
        "schema_fields": list(schema_fields.keys())
    })


@app.route('/api/parsed-log-list', methods=['GET'])
def parsed_log_list():
    log_list = []

    # Iterate through subdirectories in log_dir
    for hash_dir in os.listdir(log_dir):
        log_subdir = os.path.join(log_dir, hash_dir)
        if os.path.isdir(log_subdir):
            filename_path = os.path.join(log_subdir, "filename.txt")
            filename = ""
            if os.path.exists(filename_path):
                with open(filename_path, 'r') as f:
                    filename = f.read().strip()
            log_list.append({
                "hash": hash_dir,
                "filename": filename
            })

    return jsonify(log_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)
