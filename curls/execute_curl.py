import os
import time
import uuid


def generate_random_uuid():
    a_uuid = str(uuid.uuid4())
    # 取前8个字符
    return a_uuid[:8]


if __name__ == "__main__":
    curl_command_tpl = '''
curl 'https://memory.k3s-dev.myones.net/project/api/project/team/WA7zYRTi/tasks/add3' \
-X POST \
-H 'Host: memory.k3s-dev.myones.net' \
-H 'Connection: keep-alive' \
-H 'sec-ch-ua: "Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"' \
-H 'X-CSRF-TOKEN: 38113a906bf0e86d4b63358cf8bcfc69c79261ace31bee6de4b4af7e564375c4' \
-H 'Accept-Language: zh' \
-H 'sec-ch-ua-mobile: ?0' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36' \
-H 'Accept: application/json, text/plain, */*' \
-H 'sec-ch-ua-platform: "macOS"' \
-H 'Origin: https://memory.k3s-dev.myones.net' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Sec-Fetch-Mode: cors' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Referer: https://memory.k3s-dev.myones.net/project/' \
-H 'Content-Type: application/json' \
--cookie 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190153ebf0eeb-065d450a0b18cac-1a525637-2073600-190153ebf0f23a7%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMTUzZWJmMGVlYi0wNjVkNDUwYTBiMThjYWMtMWE1MjU2MzctMjA3MzYwMC0xOTAxNTNlYmYwZjIzYTcifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190153ebf0eeb-065d450a0b18cac-1a525637-2073600-190153ebf0f23a7%22%7D; ct=38113a906bf0e86d4b63358cf8bcfc69c79261ace31bee6de4b4af7e564375c4; language=zh; ones-uid=MpC3gsRq; ones-lt=NwIJh6AqUzEYpep45mica6R91q3mphOD9joVIPviAVBQYDD7UKmLo9vHGUrvAaot; timezone=Asia/Shanghai' \
--data-raw '{"tasks":[{"uuid":"MpC3gsRqj3fexqw2","assign":"MpC3gsRq","summary":"ddd","parent_uuid":"","field_values":[{"field_uuid":"field004","type":8,"value":"MpC3gsRq"},{"field_uuid":"field012","type":1,"value":"VKRyagaX"},{"field_uuid":"field011","type":7,"value":null},{"field_uuid":"field001","type":2,"value":"ddd"},{"field_uuid":"field016","type":20,"value":null}],"issue_type_uuid":"3CuiffW7","project_uuid":"MpC3gsRqQJ89CDtq","watchers":["MpC3gsRq"],"add_manhours":[]}]}'
'''
    curl_command_tpl = '''
    curl 'https://memory.k3s-dev.myones.net/project/api/project/team/WA7zYRTi/items/graphql?t=group-task-data' \
-X POST \
-H 'Host: memory.k3s-dev.myones.net' \
-H 'Connection: keep-alive' \
-H 'sec-ch-ua: "Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"' \
-H 'X-CSRF-TOKEN: cbf1addf8c6ba86f84eb131949d16d3f9f5a8f8433218436a5167d181954401e' \
-H 'Accept-Language: zh' \
-H 'sec-ch-ua-mobile: ?0' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36' \
-H 'Accept: application/json, text/plain, */*' \
-H 'sec-ch-ua-platform: "macOS"' \
-H 'Origin: https://memory.k3s-dev.myones.net' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Sec-Fetch-Mode: cors' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Referer: https://memory.k3s-dev.myones.net/project/' \
-H 'Content-Type: application/json;charset=UTF-8' \
--cookie 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190153ebf0eeb-065d450a0b18cac-1a525637-2073600-190153ebf0f23a7%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMTUzZWJmMGVlYi0wNjVkNDUwYTBiMThjYWMtMWE1MjU2MzctMjA3MzYwMC0xOTAxNTNlYmYwZjIzYTcifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190153ebf0eeb-065d450a0b18cac-1a525637-2073600-190153ebf0f23a7%22%7D; language=zh; ones-uid=MpC3gsRq; ones-lt=NwIJh6AqUzEYpep45mica6R91q3mphOD9joVIPviAVBQYDD7UKmLo9vHGUrvAaot; timezone=Asia/Shanghai; ct=cbf1addf8c6ba86f84eb131949d16d3f9f5a8f8433218436a5167d181954401e' \
--data-raw '{"query":"{\n    buckets (\n      groupBy: $groupBy\n      orderBy: $groupOrderBy\n      pagination: $pagination\n      filter: $groupFilter\n    ) {\n      key\n      \n      tasks (\n        filterGroup: $filterGroup\n        orderBy: $orderBy\n        limit: 1000\n        \n      includeAncestors:{pathField:\"path\"}\n      orderByPath: \"path\"\n    \n      ) {\n        \n    key\n    name\n    uuid\n    serverUpdateStamp\n    number\n    path\n    subTaskCount\n    subTaskDoneCount\n    position\n    status {\n      uuid\n      name\n      category\n    }\n    deadline(unit: ONESDATE)\n    subTasks {\n      uuid\n    }\n    issueType {\n      uuid\n      manhourStatisticMode\n    }\n    subIssueType {\n      uuid\n      manhourStatisticMode\n    }\n    project {\n      uuid\n    }\n    parent {\n      uuid\n    }\n    estimatedHours\n    remainingManhour\n    totalEstimatedHours\n    totalRemainingHours\n    issueTypeScope {\n      uuid\n    }\n\n        \n      importantField{\n        bgColor\n        color\n        name\n        value\n        fieldUUID\n      }\n    \n      }\n      pageInfo {\n        count\n        totalCount\n        startPos\n        startCursor\n        endPos\n        endCursor\n        hasNextPage\n        preciseCount\n      }\n    }\n    __extensions\n  }","variables":{"groupBy":{"tasks":{}},"groupOrderBy":null,"orderBy":{"position":"ASC","createTime":"DESC"},"filterGroup":[{"assign_in":["${currentUser}"]}],"search":null,"pagination":{"limit":50,"preciseCount":false}}}'
    '''
    # 替换为新的 uuid
    while True:
        # new_uuid = generate_random_uuid()
        new_uuid = ""
        curl_command = curl_command_tpl.replace("j3fexqw2", new_uuid)
        curl_command = curl_command.replace("ddd", new_uuid)
        os.system(f"{curl_command}")
        # time.sleep(0.1)
