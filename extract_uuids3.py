import json
import time

# 读取 JSON 文件
with open('/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/tmp/yunketang_es.json', 'r') as json_file:
    data = json.load(json_file)


# 提取 "tasks" 下的 UUID
for task in data['hits']['hits']:
    t = task['fields']['create_time'][0]
    # 把时间戳转为localtime
    time_local = time.localtime(t/1000000)
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    print(time_string, task['_id'], t)
