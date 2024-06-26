import os
import re
from collections import defaultdict

from flask import Flask, request, jsonify
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

# tenant = 'saas/'
tenant = 'lanwang/'

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
def split_goroutine_logs(file_path):
    pattern = re.compile(r'^goroutine \d+ \[.*\]:$')
    current_log = []
    goroutine_logs = []

    with open(file_path, 'r') as file:
        for line in file:
            if pattern.match(line):
                if current_log:
                    goroutine_logs.append(''.join(current_log).strip())
                    current_log = []
            current_log.append(line)

        if current_log:
            goroutine_logs.append(''.join(current_log).strip())

    # 去掉第一个 goroutine 日志，因为它是 panic 信息
    goroutine_logs = goroutine_logs[1:]
    return goroutine_logs


# 函数：解析 goroutine ID 和 created by 属性
def parse_goroutine_log(log):
    goroutine_id_match = re.match(r'^goroutine (\d+)', log)
    created_by_match = re.search(r'created by (.*) in goroutine (\d+)', log)
    goroutine_id = goroutine_id_match.group(1) if goroutine_id_match else None
    created_by = created_by_match.group(1) if created_by_match else None
    return goroutine_id, created_by


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


# 路由：展示所有 goroutine 日志
@app.route('/logs', methods=['GET'])
def get_logs():
    logs = load_all_goroutine_logs()
    return jsonify(logs)


# 路由：全文搜索
@app.route('/search', methods=['GET'])
def search_logs():
    query_str = request.args.get('q', '')
    results = []
    total_hits = 0

    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        search_results = searcher.search(query, limit=None)  # 获取所有匹配结果

        total_hits = len(search_results)  # 获取总匹配记录数

        # 获取前10条结果
        top_results = search_results[:10]

        # 从文件中读取匹配的内容
        for result in top_results:
            log_path = result["log_path"]
            with open(log_path, 'r') as log_file:
                content = log_file.read()
            results.append({
                "goroutine_id": result["goroutine_id"],
                "created_by": result["created_by"],
                "log_path": result["log_path"],
                "content": content
            })

    response = {
        "total_results": total_hits,
        "results": results
    }

    return jsonify(response)


# 路由：按 created_by 分组并返回各自的数量
@app.route('/group_by_created_by', methods=['GET'])
def group_by_created_by():
    # 创建一个默认字典来存储分组结果
    created_by_count = defaultdict(int)

    with ix.searcher() as searcher:
        # 获取所有文档
        results = searcher.documents()
        for result in results:
            created_by = result.get("created_by", "Unknown")
            created_by_count[created_by] += 1

    # 将字典转换为数组并按数量降序排序
    sorted_created_by_count = sorted(created_by_count.items(), key=lambda item: item[1], reverse=True)

    # 转换为数组并返回
    sorted_created_by_count_list = [{"created_by": k, "count": v} for k, v in sorted_created_by_count]

    return jsonify(sorted_created_by_count_list)


# 运行 Flask 应用
if __name__ == "__main__":
    # log_file_path = '/Users/xhs/task/panic问题/SaaS的project-api.log'  # 替换为实际日志文件路径
    # log_file_path = '/Users/xhs/task/panic问题/蓝网的project-api.log'
    # main(log_file_path)
    app.run(host='0.0.0.0', port=5050)
    print('Flask app running')
