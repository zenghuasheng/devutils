import json
from collections import Counter

# 读取 JSON 文件
with open('/Users/xhs/Downloads/ones.cpgroup.cn_12-09-2023-17-56-49.json', 'r') as file:
    data = json.load(file)

# 获取所有任务
all_tasks = [task for bucket in data['data']['buckets'] for task in bucket.get('tasks', [])]

# 查找重复的 uuid 和 name
seen_uuids = set()
duplicate_uuids = set()
duplicate_names = Counter()

for task in all_tasks:
    uuid = task['uuid']
    name = task['name']

    if uuid in seen_uuids:
        duplicate_uuids.add(uuid)
        duplicate_names[name] += 1
    else:
        seen_uuids.add(uuid)

# 输出重复的 uuid、任务名称和重复次数
if duplicate_uuids:
    for uuid in duplicate_uuids:
        name_counts = duplicate_names.most_common()  # 获取按次数降序排列的任务名称及次数
        for name, count in name_counts:
            if uuid in (task['uuid'] for task in all_tasks if task['name'] == name):
                print(f"UUID: {uuid}, 任务名称: {name}, 重复次数: {count}")
else:
    print("没有重复的 UUID。")