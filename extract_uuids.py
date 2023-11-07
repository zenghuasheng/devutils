import json

# 打开JSON文件
with open('xiaoneng_data.json', 'r') as file:
    data = json.load(file)

# 初始化一个空数组来存放所有的number值
numbers = []

# 遍历JSON数据，提取number字段值
for item in data:
    if 'number' in item:
        numbers.append(item['number'])

# 打开JSON文件
with open('filter_task.json', 'r') as file:
    data = json.load(file)

# 初始化一个空数组来存放所有的number值
numbers2 = []

# 遍历JSON数据，提取number字段值
for item in data:
    if 'number' in item:
        numbers2.append(item['number'])

set1 = set(numbers)
set2 = set(numbers2)

difference = set1 - set2

# 将差集转换回列表
result = list(difference)
# 打印提取出的number数组
print(result)
