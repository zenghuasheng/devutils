import hashlib
import os
import re
from collections import defaultdict

from flask import Flask, request, jsonify
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser, AndGroup

# tenant = 'saas/'
# tenant = 'lanwang/'
tenant = 'saas_normal/'

# 全局变量
log_dir = tenant + "logs"
index_dir = tenant + "indexdir"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
if not os.path.exists(index_dir):
    os.makedirs(index_dir)

# 定义 Whoosh schema
schema = Schema(goroutine_id=ID(stored=True), created_by=TEXT(stored=True), content=TEXT, log_path=ID(stored=True))

# 创建或打开索引
if not index.exists_in(index_dir):
    ix = index.create_in(index_dir, schema)
else:
    ix = index.open_dir(index_dir)


# 函数：分割堆栈日志
# def split_goroutine_logs(file_path):
#     pattern = re.compile(r'^goroutine \d+ \[.*\]:$')
#     current_log = []
#     goroutine_logs = []
#
#     with open(file_path, 'r') as file:
#         for line in file:
#             if pattern.match(line):
#                 if current_log:
#                     goroutine_logs.append(''.join(current_log).strip())
#                     current_log = []
#             current_log.append(line)
#
#         if current_log:
#             goroutine_logs.append(''.join(current_log).strip())
#
#     # 去掉第一个 goroutine 日志，因为它是 panic 信息
#     goroutine_logs = goroutine_logs[1:]
#     return goroutine_logs

def split_goroutine_logs(file_path):
    goroutine_logs = []
    with open(file_path, 'r') as file:
        content = file.read()
        # 将日志按空行分割
        raw_logs = content.split('\n\n')

        for log in raw_logs:
            if log.strip():  # 过滤掉空白日志
                goroutine_logs.append(log)

    return goroutine_logs


# 函数：解析 goroutine ID 和 created by 属性
# def parse_goroutine_log(log):
#     goroutine_id_match = re.match(r'^goroutine (\d+)', log)
#     created_by_match = re.search(r'created by (.*) in goroutine (\d+)', log)
#     goroutine_id = goroutine_id_match.group(1) if goroutine_id_match else None
#     created_by = created_by_match.group(1) if created_by_match else None
#     return goroutine_id, created_by
def parse_goroutine_log(log):
    # 计算 goroutine_id 为日志内容的 MD5 哈希值
    log_md5 = hashlib.md5(log.encode('utf-8')).hexdigest()

    # 解析 created_by 信息，这里假设日志中没有 created_by 信息
    created_by = ""

    return log_md5, created_by


# 函数：存储堆栈日志为文件并索引
def store_and_index_goroutine_log(writer, goroutine_id, created_by, log):
    log_file_path = os.path.join(log_dir, f"goroutine_{goroutine_id}.txt")
    with open(log_file_path, 'w') as log_file:
        log_file.write(log)
    writer.add_document(goroutine_id=goroutine_id, created_by=created_by, content=log, log_path=log_file_path)


# 函数：加载所有堆栈日志文件
def load_all_goroutine_logs():
    logs = []
    for filename in os.listdir(log_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(log_dir, filename), 'r') as log_file:
                logs.append(log_file.read())
    return logs


# 主函数
def main(log_file_path):
    goroutine_logs = split_goroutine_logs(log_file_path)

    with ix.writer() as writer:
        for log in goroutine_logs:
            goroutine_id, created_by = parse_goroutine_log(log)
            if goroutine_id:
                store_and_index_goroutine_log(writer, goroutine_id, created_by, log)
                print(f"Stored and indexed goroutine {goroutine_id} log, created by: {created_by}")


# Flask 应用
app = Flask(__name__)


# 路由：全文搜索
@app.route('/search', methods=['GET'])
def search_logs():
    # 收集所有搜索词参数
    query_params = [request.args.get(f'q{i}', '') for i in range(10) if request.args.get(f'q{i}', '')]

    # 如果没有提供任何搜索词，返回空结果
    if not query_params:
        return jsonify({"total_results": 0, "results": [], "tenant": tenant})

    size = request.args.get('size', 10)
    size = int(size)  # 转为整数
    results = []
    total_hits = 0

    with ix.searcher() as searcher:
        # 构建组合查询
        parser = QueryParser("content", ix.schema, group=AndGroup)
        combined_query = " AND ".join(query_params)
        query = parser.parse(combined_query)

        search_results = searcher.search(query, limit=None)  # 获取所有匹配结果
        total_hits = len(search_results)  # 获取总匹配记录数

        # 获取前size条结果
        top_results = search_results[:size]

        # 从文件中读取匹配的内容
        for result in top_results:
            log_path = result["log_path"]
            if log_path.startswith(tenant):
                log_path = log_path
            else:
                log_path = tenant + log_path
            with open(log_path, 'r') as log_file:
                content = log_file.read()
            # 转换 content，按行分割为数组，\t 换成4个空格
            content_lines = content.split('\n')
            content_lines = [line.replace('\t', '    ') for line in content_lines]
            results.append({
                "goroutine_id": result["goroutine_id"],
                "created_by": result["created_by"],
                "log_path": result["log_path"],
                "content": content_lines
            })

    response = {
        "total_results": total_hits,
        "results": results,
        "tenant": tenant
    }

    return jsonify(response)

# 路由：按 created_by 分组并返回各自的数量
@app.route('/group_by_created_by', methods=['GET'])
def group_by_created_by():
    # 创建一个默认字典来存储分组结果
    created_by_count = defaultdict(int)

    with ix.searcher() as searcher:
        # 获取所有文档
        total_progress = searcher.doc_count_all()
        results = searcher.documents()
        for result in results:
            created_by = result.get("created_by", "Unknown")
            created_by_count[created_by] += 1

    # 将字典转换为数组并按数量降序排序
    sorted_created_by_count = sorted(created_by_count.items(), key=lambda item: item[1], reverse=True)

    # 转换为数组并返回
    # 计算百分比, v / total_progress 格式化为 %.2f
    # sorted_created_by_count_list = [{"created_by": k, "count": v, "percentage": v / total_progress} for k, v in
    #                                 sorted_created_by_count]
    sorted_created_by_count_list = [{"created_by": k, "count": v, "percentage": "%.2f%%" % (v / total_progress * 100)}
                                    for k, v in
                                    sorted_created_by_count]

    # 统计哪些包含 sarama 的，计算总数和占比
    sarama_count = 0
    for k, v in sorted_created_by_count:
        if "sarama" in k:
            sarama_count += v
    sarama_percentage = "%.2f%%" % (sarama_count / total_progress * 100)
    res = {
        "total_progress": total_progress,
        "created_by_count": sorted_created_by_count_list,
        "tenant": tenant,
        "sarama_count": sarama_count,
        "sarama_percentage": sarama_percentage
    }
    return jsonify(res)


# 运行 Flask 应用
if __name__ == "__main__":
    # log_file_path = '/Users/xhs/task/panic问题/SaaS的project-api.log'  # 替换为实际日志文件路径
    # log_file_path = '/Users/xhs/task/panic问题/蓝网的project-api.log'
    # log_file_path = '/Users/xhs/task/panic问题/saas正常的协程堆栈_part.log'
    # main(log_file_path)
    app.run(host='0.0.0.0', port=5050)
    print('Flask app running')
