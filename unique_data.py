import json

# 读取 JSON 文件
with open('/Users/xhs/Downloads/ones.cpgroup.cn_12-09-2023-17-56-49.json', 'r') as file:
    data = json.load(file)

# 获取所有任务
all_tasks = [task for bucket in data['data']['buckets'] for task in bucket.get('tasks', [])]

# 去重
unique_tasks = []
seen_uuids = set()

for task in all_tasks:
    uuid = task['uuid']
    if uuid not in seen_uuids:
        unique_tasks.append(task)
        seen_uuids.add(uuid)

# 构造新的 JSON 数据
print(len(unique_tasks))
unique_data = {'data': {'buckets': [{'tasks': unique_tasks}]}}

# 将去重后的 JSON 数据写入新文件
output_filename = 'unique_tasks.json'
with open(output_filename, 'w') as output_file:
    json.dump(unique_data, output_file, indent=2)

print(f"去重后的数据已保存到文件: {output_filename}")