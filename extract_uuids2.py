import json
import time


def task_uuids():
    # 读取 JSON 文件
    with open('/Users/xhs/go_workspace/aidemo/FeHelper-20231009182402.json', 'r') as json_file:
        data = json.load(json_file)

    # 提取 "tasks" 下的 UUID
    tasks_uuids = [task['uuid'] for task in data['data']['buckets'][0]['tasks']]

    # 打印 "tasks" 下的 UUID
    for uuid in tasks_uuids:
        print(uuid)


def task_uuids2():
    # 读取 JSON 文件
    with open('/Users/xhs/task/工作项增加模块属性/our.ones.pro_04-17-2024-17-06-20.json', 'r') as json_file:
        data = json.load(json_file)

    # 提取 "tasks" 下的 UUID
    tasks_uuids = [task['task_uuid'] for task in data['tasks']]

    # 每个 uuid 都加上双引号，以逗号分隔，形成一行打印出来
    print(','.join([f'"{uuid}"' for uuid in tasks_uuids]))


def category_uuids():
    # [{"uuid":"product_management","value":"产品管理","default_selected":false,"bg_color":"","color":"","desc":""},{"uuid":"development_project","value":"研发项目","default_selected":false,"bg_color":"","color":"","desc":""},{"uuid":"progress_management","value":"业务进度","default_selected":false,"bg_color":"","color":"","desc":""},{"uuid":"Nd8MQyAQ","value":"自定义项目类型","default_selected":false,"bg_color":"","color":"","desc":""},{"uuid":"TNctCqk7","value":"这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的项目类型这是自定义的","default_selected":false,"bg_color":"","color":"","desc":""},{"uuid":"92jXqsVL","value":"this is a new type","default_selected":false,"bg_color":"","color":"","desc":""},{"uuid":"WyTqBABa","value":"Change, a constant and inevitable force in our lives, often brings a mix of excitement, fear, and uncertainty. It's the engine of progress, pushing us out of our comfort zones and into new territories. Embracing change, rather than resisting it, can lead t","default_selected":false,"bg_color":"","color":"","desc":""}]
    # 读取 JSON 文件
    with open('/Users/xhs/go_workspace/aidemo/category.json', 'r') as json_file:
        data = json.load(json_file)
    uuids = [category['uuid'] for category in data]
    # 给SQL用的，打印成字符串
    print(','.join([f'"{uuid}"' for uuid in uuids]))


def project_create_time():
    #  ~/Downloads/ones.lango-tech.com_04-07-2024-13-50-15.json
    # {
    #   "data": {
    #     "buckets": [
    #       {
    #         "key": "bucket.0.1ep8pbbk5apif",
    #         "projects": [
    #           {
    #             "assign": {
    #               "avatar": "",
    #               "name": "谭俊英",
    #               "uuid": "9hCwVkBE"
    #             },
    #             "createTime": 1695624267610663,
    #             "doneTaskPercent": 12000,
    #             "isArchive": false,
    #             "isPin": false,
    #             "isSample": false,
    #             "key": "project-9hCwVkBELpRgqAMW",
    #             "name": "ONES问题和需求收集",
    # 读取 JSON 文件，提取所有 buckets 下的 projects 的 name 和 createTime
    with open('/Users/xhs/Downloads/ones.lango-tech.com_04-07-2024-13-50-15.json', 'r') as json_file:
        data = json.load(json_file)
    projects = []
    for bucket in data['data']['buckets']:
        for project in bucket['projects']:
            # print(project['name'], project['createTime'])
            projects.append((project['name'], project['createTime']))
    # 按 createTime 排序
    projects.sort(key=lambda x: x[1])
    # 打印所有 projects 的 name 和 createTime，以表格的形式，要对齐
    for project in projects:
        time_str = ''
        if project[1] < 1691390191608457:
            # 除以 1000，转换成秒，格式化成字符串
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(project[1] / 1000))
        else:
            # 除以 1000000，转换成秒，格式化成字符串
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(project[1] / 1000000))
        print(f'{project[1]:<40} {time_str} {project[0]}')


if __name__ == '__main__':
    # category_uuids()
    # project_create_time()
    task_uuids2()
