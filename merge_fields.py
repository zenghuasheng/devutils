import json


def merge_data(filename):
    # 读取project_list.json文件数据
    with open('/Users/xhs/Downloads/project_list.json', 'r') as file:
        project_list_data = json.load(file)

    # 读取product_management.json文件数据
    with open(f'/Users/xhs/Downloads/{filename}.json', 'r') as file:
        product_management_data = json.load(file)

    # 将product_management.json的数据放在前面，is_hide改为false
    merged_data = []
    uuid_set = set()
    for item in product_management_data:
        item['is_hide'] = False
        merged_data.append(item)
        uuid_set.add(item['uuid'])

    # 将project_list.json的数据放在后面，如果uuid已经出现过，则跳过，且is_hide改为true
    for item in project_list_data:
        if item['uuid'] not in uuid_set:
            item['is_hide'] = True
            merged_data.append(item)
            uuid_set.add(item['uuid'])

    # Swap the order of status and assign elements in merged_data
    status_index = next((index for index, item in enumerate(merged_data) if item["uuid"] == "status"), None)
    assign_index = next((index for index, item in enumerate(merged_data) if item["uuid"] == "assign"), None)

    if status_index is not None and assign_index is not None:
        merged_data[status_index], merged_data[assign_index] = merged_data[assign_index], merged_data[status_index]

    # 将合并后的数据写入新的JSON文件
    with open(f'category/{filename}_merged_data.json', 'w') as file:
        # json.dump(merged_data, file, indent=4)
        json.dump(merged_data, file)


if __name__ == '__main__':
    a_list = [
        'business_management',
        'development_project',
        'product_management',
        'project_category',
    ]
    for filename in a_list:
        merge_data(filename)
