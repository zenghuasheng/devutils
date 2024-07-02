from whoosh.fields import Schema, TEXT, ID, NUMERIC
import os
import re
import hashlib
from whoosh import index
from whoosh.qparser import QueryParser, AndGroup
from flask import Flask, jsonify, request
from collections import defaultdict
from datetime import datetime, timedelta, timezone

# Define the Whoosh schema
schema = Schema(
    ip_address=ID(stored=True),
    timestamp=TEXT(stored=True),
    method=TEXT(stored=True),
    endpoint=TEXT(stored=True),
    status=NUMERIC(stored=True),
    size=NUMERIC(stored=True),
    referer=TEXT(stored=True),
    user_agent=TEXT(stored=True),
    request_ip=ID(stored=True),
    response_time=NUMERIC(stored=True),
    log_path=ID(stored=True)
)

# Define paths and directories
log_dir = "logs"
index_dir = "indexdir"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
if not os.path.exists(index_dir):
    os.makedirs(index_dir)

# Initialize or open the Whoosh index
if not index.exists_in(index_dir):
    ix = index.create_in(index_dir, schema)
else:
    ix = index.open_dir(index_dir)

# Regex pattern for nginx log format
log_pattern = re.compile(r'^(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" "(.*?)" "([\d\.]+)"$')


# Function to parse a single nginx log line
def parse_nginx_log_line(line):
    match = log_pattern.match(line.strip())
    if match:
        ip_address = match.group(1)
        timestamp = match.group(2)
        method = match.group(3).split()[0]  # Extract HTTP method (GET, POST, etc.)
        endpoint = match.group(3).split()[1]  # Extract request endpoint
        status = int(match.group(4))
        size = int(match.group(5))
        referer = match.group(6)
        user_agent = match.group(7)
        request_ip = match.group(8)
        response_time = float(match.group(9))
        return ip_address, timestamp, method, endpoint, status, size, referer, user_agent, request_ip, response_time
    return None


# Function to store and index nginx log data
def store_and_index_nginx_log(writer, ip_address, timestamp, method, endpoint, status, size, referer, user_agent,
                              request_ip, response_time, log_path):
    writer.add_document(
        ip_address=ip_address,
        timestamp=timestamp,
        method=method,
        endpoint=endpoint,
        status=status,
        size=size,
        referer=referer,
        user_agent=user_agent,
        request_ip=request_ip,
        response_time=response_time,
        log_path=log_path
    )


# Function to read nginx logs, parse them, and index into Whoosh
def index_nginx_logs(log_file_path):
    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        for line in log_file:
            log_data = parse_nginx_log_line(line.strip())
            if log_data:
                ip_address, timestamp, method, endpoint, status, size, referer, user_agent, request_ip, response_time = log_data
                store_and_index_nginx_log(writer, ip_address, timestamp, method, endpoint, status, size, referer,
                                          user_agent, request_ip, response_time, log_file_path)


app = Flask(__name__)


# Route for searching logs
@app.route('/search', methods=['GET'])
def search_logs():
    query_str = request.args.get('q', '')
    size = int(request.args.get('size', 10))

    results = []
    total_hits = 0

    with ix.searcher() as searcher:
        query = QueryParser("endpoint", ix.schema, group=AndGroup).parse(query_str)
        search_results = searcher.search(query, limit=None)
        total_hits = len(search_results)

        for result in search_results[:size]:
            results.append({
                "ip_address": result["ip_address"],
                "timestamp": result["timestamp"],
                "method": result["method"],
                "endpoint": result["endpoint"],
                "status": result["status"],
                "size": result["size"],
                "referer": result["referer"],
                "user_agent": result["user_agent"],
                "response_time": result["response_time"]
            })

    response = {
        "total_results": total_hits,
        "results": results
    }

    return jsonify(response)


# Route for aggregating logs by timestamp range
@app.route('/aggregate_by_timestamp', methods=['GET'])
def aggregate_by_timestamp():
    start_time_str = request.args.get('start_time', '')
    end_time_str = request.args.get('end_time', '')

    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

    with ix.searcher() as searcher:
        results = []
        for doc in searcher.documents():
            timestamp = datetime.strptime(doc['timestamp'], "%d/%b/%Y:%H:%M:%S %z")
            if start_time <= timestamp <= end_time:
                results.append({
                    "ip_address": doc["ip_address"],
                    "timestamp": doc["timestamp"],
                    "method": doc["method"],
                    "endpoint": doc["endpoint"],
                    "status": doc["status"],
                    "size": doc["size"],
                    "referer": doc["referer"],
                    "user_agent": doc["user_agent"],
                    "response_time": doc["response_time"]
                })

        sorted_results = sorted(results, key=lambda x: x['response_time'])

    return jsonify(sorted_results)


# Route for aggregating logs by request count
@app.route('/aggregate_by_request_count', methods=['GET'])
def aggregate_by_request_count():
    with ix.searcher() as searcher:
        results = []
        query = QueryParser("endpoint", ix.schema, group=AndGroup).parse('*:*')
        search_results = searcher.search(query, limit=None)

        count_dict = defaultdict(int)
        for result in search_results:
            count_dict[result['endpoint']] += 1

        sorted_results = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)

        for result in sorted_results:
            results.append({
                "endpoint": result[0],
                "request_count": result[1]
            })

    return jsonify(results)


# 写一个函数，按请求时长排序
@app.route('/aggregate_by_response_time', methods=['GET'])
def aggregate_by_response_time():
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
            if average_response_time > 10:
                results.append({
                    "endpoint": result[0],
                    "average_response_time": average_response_time
                })

    return jsonify(results)


# Run Flask app
if __name__ == '__main__':
    # Example usage to index nginx logs
    # log_file_path = '/Users/xhs/task/panic问题/云路/project-web.log'
    # with ix.writer() as writer:
    #     index_nginx_logs(log_file_path)

    app.run(host='0.0.0.0', port=5050)
