import json

# 读取 JSON 文件
with open('/Users/xhs/go_workspace/aidemo/FeHelper-20231009182402.json', 'r') as json_file:
    data = json.load(json_file)


# 提取 "tasks" 下的 UUID
tasks_uuids = [task['uuid'] for task in data['data']['buckets'][0]['tasks']]

# 打印 "tasks" 下的 UUID
for uuid in tasks_uuids:
    print(uuid)