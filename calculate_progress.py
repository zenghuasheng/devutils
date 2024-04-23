import json
import re
from datetime import datetime


def calculate_days_between_dates(date1_str, date2_str):
    # 将日期字符串转换为 datetime 对象
    date1 = datetime.strptime(date1_str, "%Y-%m-%d")
    date2 = datetime.strptime(date2_str, "%Y-%m-%d")

    # 计算日期之间的间隔天数
    delta = abs(date2 - date1)
    days = delta.days

    return days


def parse_task_info(result_string):
    # 定义正则表达式模式
    pattern = r"\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|"

    # 使用正则表达式提取每一行的数据
    rows = re.findall(pattern, result_string)

    # 将每一行的数据解析成字典，并存入任务信息字典
    task_info_map = {}
    for row in rows:
        task_uuid, field_uuid, field_type, value, number_value, status = row
        if task_uuid not in task_info_map:
            task_info_map[task_uuid] = {}
        if field_uuid == "field027":
            task_info_map[task_uuid]["start_date"] = value
        elif field_uuid == "field028":
            task_info_map[task_uuid]["end_date"] = value
        elif field_uuid == "field033":
            task_info_map[task_uuid]["progress"] = number_value

    return task_info_map


def parse_task_results(result_string):
    # 定义正则表达式模式
    pattern = r"\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|"

    # 使用正则表达式提取每一行的数据
    rows = re.findall(pattern, result_string)

    # 将每一行的数据解析成字典，并存入列表
    tasks = []
    for row in rows:
        uuid, number, create_time, summary, path = row
        task = {
            "uuid": uuid,
            "number": int(number),
            "create_time": int(create_time),
            "summary": summary.strip(),
            "path": path.strip()
        }
        tasks.append(task)

    return tasks


def parse_progress():
    file_path = "/Users/xhs/task/迭代进度计算/124.71.228.121_04-22-2024-17-42-51.json"
    with open(file_path, 'r') as file:
        data = json.load(file)
    # {
    #   "data": {
    #     "buckets": [
    #       {
    #         "key": "bucket.0.__all",
    #         "pageInfo": {
    #           "count": 33,
    #           "endCursor": "e3hl5zHLe4kgAAAAdGFzay1GNGhkOGdpY25XdGRUNjNv",
    #           "endPos": 32,
    #           "hasNextPage": false,
    #           "preciseCount": 0,
    #           "startCursor": "e3hl5zHLe4kAAAAAdGFzay1BVnBYV0N4eFU5RkFaU3ZS",
    #           "startPos": 0,
    #           "totalCount": 33
    #         },
    #         "tasks": [
    #           {
    task_info = {}
    for bucket in data['data']['buckets']:
        for task in bucket['tasks']:
            task_info[task['uuid']] = task
    return task_info


def build_task_tree(tasks, task_info_mysql, task_info_graphql):
    # 构建任务树字典，以任务路径为键，任务对象为值
    task_tree = {}
    in_sprint = {}
    print(len(tasks))
    for task in tasks:
        task_tree[task["path"]] = task
        in_sprint[task["uuid"]] = True

    # 递归打印任务树
    def print_task_tree(task_path, task_tree, depth=0):
        # 获取当前任务
        current_task = task_tree.get(task_path)
        if not current_task:
            current_task = {
                "uuid": task_path,
                "summary": ""
            }
        # 打印当前任务，缩进表示层级
        # 加上任务信息
        start_date, end_date, progress = get_task_info(current_task['uuid'], task_info_mysql, task_info_graphql)
        # print("  " * depth + f"{current_task['uuid']}")
        print(
            "  " * depth + f"{current_task['uuid']} {current_task['summary']} {start_date} {end_date} {progress / 100000} {in_sprint.get(current_task['uuid'], False)}")
        # 递归打印子任务
        # children_paths = [path for path in task_tree.keys() if path.startswith(task_path + "-")]
        new_task_tree = {}
        # 去掉 task_path 前缀
        children_paths = []
        for path in task_tree:
            if path.startswith(task_path):
                key = path[len(task_path) + 1:]
                if key == "":
                    continue
                new_task_tree[key] = task_tree[path]
                path = key.split("-", 1)[0]
                if path not in children_paths:
                    children_paths.append(path)
        for child_path in children_paths:
            print_task_tree(child_path, new_task_tree, depth + 1)

    # 打印任务树的根节点
    # root_tasks = [task["path"] for task in tasks if "-" not in task["path"]]
    root_tasks = []
    for task in tasks:
        if "-" not in task["path"]:
            root_tasks.append(task["path"])
        else:
            parent_path = task["path"].split("-", 1)[0]
            if parent_path not in root_tasks:
                root_tasks.append(parent_path)
    for root_task_path in root_tasks:
        print_task_tree(root_task_path, task_tree)


def get_task_info(uuid, task_info_mysql, task_info_graphql):
    if uuid in task_info_graphql:
        progress = task_info_graphql[uuid]['progress']
        # planStartDate
        start_date = task_info_graphql[uuid]['planStartDate']
        # planEndDate
        end_date = task_info_graphql[uuid]['planEndDate']
    else:
        progress = task_info_mysql[uuid].get('progress', 0)
        # 把字符串转换为数字
        progress = int(progress)
        start_date = task_info_mysql[uuid].get('start_date', None)
        end_date = task_info_mysql[uuid].get('end_date', None)
    return start_date, end_date, progress


if __name__ == "__main__":
    result_string = """
+------------------+--------+------------------+-----------------------------------------------------------+----------------------------------------------------+
| uuid             | number | create_time      | summary                                                   | path                                               |
+------------------+--------+------------------+-----------------------------------------------------------+----------------------------------------------------+
| 4GmJoN3Z4xlV3mVa |  23913 | 1712642366227106 | 网络优先级配置                                            | AVpXWCxxQpjyoq8X-AVpXWCxxbGECmZCY-4GmJoN3Z4xlV3mVa |
| 4GmJoN3Z9iJSjRIW |  23953 | 1712643181395789 | 配置项导出                                                | AVpXWCxxQpjyoq8X-AVpXWCxxLNJgYTXL-4GmJoN3Z9iJSjRIW |
| 4GmJoN3Zc29l5QoC |  23949 | 1712643111251619 | 配置项导入                                                | AVpXWCxxQpjyoq8X-AVpXWCxxLNJgYTXL-4GmJoN3Zc29l5QoC |
| 88DEiNVEV7gCG1Gi |  24028 | 1712740424170610 | web端日志接口                                             | AVpXWCxxQpjyoq8X-AVpXWCxxaYOt2SUE-88DEiNVEV7gCG1Gi |
| 88DEiNVExwEv3Dy1 |  23990 | 1712663867188399 | 服务端日志实现                                            | AVpXWCxxQpjyoq8X-AVpXWCxxaYOt2SUE-88DEiNVExwEv3Dy1 |
| 9awfuL9Lr16QaJCC |  23858 | 1712565864599314 | 摄像头配置                                                | AVpXWCxxQpjyoq8X-AVpXWCxxEgbkwZ1s-9awfuL9Lr16QaJCC |
| AVpXWCxx2zcvTkWa |  23413 | 1712057732592707 | 云平台升级管理和推送（暂时使用鸿湖云）                    | AVpXWCxxNR4Z7sGV-AVpXWCxxVzeapQkJ-AVpXWCxx2zcvTkWa |
| AVpXWCxx7J451PMv |  23585 | 1712124285741159 | web页面所有配置项全部重置                                 | AVpXWCxxNR4Z7sGV-AVpXWCxxe6PLlYxv-AVpXWCxx7J451PMv |
| AVpXWCxx8ArfWKC8 |  23422 | 1712057732647670 | IPv6                                                      | AVpXWCxxNR4Z7sGV-AVpXWCxx8ArfWKC8                  |
| AVpXWCxxD8hCPy3b |  23411 | 1712057732579501 | OTA升级服务                                               | AVpXWCxxNR4Z7sGV-AVpXWCxxVzeapQkJ-AVpXWCxxD8hCPy3b |
| AVpXWCxxHk5S4chf |  23421 | 1712057732641566 | 网络优先级设置                                            | AVpXWCxxNR4Z7sGV-AVpXWCxxHk5S4chf                  |
| AVpXWCxxJHy5UQ6A |  23423 | 1712057732653868 | PIR唤醒                                                   | AVpXWCxxNR4Z7sGV-AVpXWCxxJHy5UQ6A                  |
| AVpXWCxxJdtWMSs6 |  23410 | 1712057732572883 | OTA拍包（全量包）                                         | AVpXWCxxNR4Z7sGV-AVpXWCxxVzeapQkJ-AVpXWCxxJdtWMSs6 |
| AVpXWCxxLNJgYTXL |  23624 | 1712125183249552 | 配置导入、导出                                            | AVpXWCxxQpjyoq8X-AVpXWCxxLNJgYTXL                  |
| AVpXWCxxQCj2EbvG |  23414 | 1712057732598911 | 手动升级接口                                              | AVpXWCxxNR4Z7sGV-AVpXWCxxVzeapQkJ-AVpXWCxxQCj2EbvG |
| AVpXWCxxR1gmKjcS |  23403 | 1712057732530745 | License功能                                               | AVpXWCxxNR4Z7sGV-AVpXWCxxR1gmKjcS                  |
| AVpXWCxxSpBvXHEE |  23644 | 1712125598882331 | 系统安全                                                  | AVpXWCxxU9FAZSvR-AVpXWCxxSpBvXHEE                  |
| AVpXWCxxaYOt2SUE |  23633 | 1712125311345058 | 日志管理                                                  | AVpXWCxxQpjyoq8X-AVpXWCxxaYOt2SUE                  |
| AVpXWCxxe6PLlYxv |  23578 | 1712124033762337 | 恢复出厂设置                                              | AVpXWCxxNR4Z7sGV-AVpXWCxxe6PLlYxv                  |
| AVpXWCxxjONp51sf |  23589 | 1712124352516699 | OH系统默认全部重置项                                      | AVpXWCxxNR4Z7sGV-AVpXWCxxe6PLlYxv-AVpXWCxxjONp51sf |
| BbTzfPG1noKM7r26 |  24291 | 1713270901811526 | 适配ec200a并搭建4g代码框架                                | AVpXWCxxNR4Z7sGV-AVpXWCxxW7Y9MmPG-BbTzfPG1noKM7r26 |
| F4hd8gicCIlgkeVp |  23941 | 1712642826234094 | TF卡本地升级                                              | AVpXWCxxQpjyoq8X-AVpXWCxxYlr9PUCC-F4hd8gicCIlgkeVp |
| F4hd8gicnWtdT63o |  24198 | 1713170414142009 | 支持GB28181                                               | AVpXWCxxQpjyoq8X-PvJhcAy9WGe3RoTO-F4hd8gicnWtdT63o |
| PvJhcAy9Ks6Vojga |  24092 | 1712839194757710 | 流量统计                                                  | PvJhcAy9Ks6Vojga                                   |
| PvJhcAy9eeO5Pbin |  24093 | 1712840164409969 | 测试                                                      | PvJhcAy9eeO5Pbin                                   |
| Vep4anuWnYwEKi58 |  23804 | 1712495380187880 | license和主要服务耦合                                     | AVpXWCxxNR4Z7sGV-AVpXWCxxR1gmKjcS-Vep4anuWnYwEKi58 |    
    """
    tasks = parse_task_results(result_string)
    value_string = """
+------------------+------------+------+------------+--------------+--------+
| task_uuid        | field_uuid | type | value      | number_value | status |
+------------------+------------+------+------------+--------------+--------+
| 4GmJoN3Z4xlV3mVa | field033   |    4 | 0          |            0 |      1 |
| 4GmJoN3Z9iJSjRIW | field033   |    4 | 0          |            0 |      1 |
| 4GmJoN3Zc29l5QoC | field033   |    4 | 0          |            0 |      1 |
| 88DEiNVEV7gCG1Gi | field033   |    4 | 0          |            0 |      1 |
| 88DEiNVExwEv3Dy1 | field033   |    4 | 0          |            0 |      1 |
| 9awfuL9Lr16QaJCC | field033   |    4 | 0          |            0 |      1 |
| AVpXWCxx7J451PMv | field033   |    4 | 0          |            0 |      1 |
| AVpXWCxxLNJgYTXL | field028   |    5 | 1713182400 |   1713182400 |      1 |
| AVpXWCxxSpBvXHEE | field028   |    5 | 1713441600 |   1713441600 |      1 |
| AVpXWCxxjONp51sf | field033   |    4 | 0          |            0 |      1 |
| BbTzfPG1noKM7r26 | field033   |    4 | 0          |            0 |      1 |
| F4hd8gicCIlgkeVp | field033   |    4 | 0          |            0 |      1 |
| F4hd8gicnWtdT63o | field033   |    4 | 0          |            0 |      1 |
| PvJhcAy9Ks6Vojga | field033   |    4 | 10000000   |     10000000 |      1 |
| PvJhcAy9eeO5Pbin | field028   |    5 | 1712923200 |   1712923200 |      1 |
| PvJhcAy9eeO5Pbin | field033   |    4 | 10000000   |     10000000 |      1 |
| Vep4anuWnYwEKi58 | field033   |    4 | 0          |            0 |      1 |
+------------------+------------+------+------------+--------------+--------+
"""
    task_info1 = parse_task_info(value_string)
    # 按照 path 排序
    task_info2 = parse_progress()
    need_do = 0
    finished = 0
    build_task_tree(tasks, task_info1, task_info2)
    # for task in tasks:
    #     print(task['uuid'], task['path'])
    #     uuid = task['uuid']
    #     if uuid in task_info2:
    #         progress = task_info2[uuid]['progress']
    #         # planStartDate
    #         start_date = task_info2[uuid]['planStartDate']
    #         # planEndDate
    #         end_date = task_info2[uuid]['planEndDate']
    #     else:
    #         progress = task_info1[uuid].get('progress', 0)
    #         # 把字符串转换为数字
    #         progress = int(progress)
    #         start_date = task_info1[uuid].get('start_date', None)
    #         end_date = task_info1[uuid].get('end_date', None)
    #     if not start_date or not end_date:
    #         current_need_do = 1
    #     else:
    #         current_need_do = calculate_days_between_dates(start_date, end_date)
    #     current_finished = ((progress / 100000) / 100) * current_need_do
    #     need_do += 1
    #     finished += current_finished
    # print(f"Need do: {need_do}, Finished: {finished}, Progress: {finished / need_do}")


def calculate_progress(root):
    # 判断是否是叶子任务，如果是叶子任务，直接返回进度
    # 如果不是叶子任务，递归计算子任务的进度
    pass
