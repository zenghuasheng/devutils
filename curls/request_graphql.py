import time

import requests

proxies = {
    'http': 'http://localhost:9090',
    'https': 'http://localhost:9090',
}

cookies = {
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22190153ebf0eeb-065d450a0b18cac-1a525637-2073600-190153ebf0f23a7%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMTUzZWJmMGVlYi0wNjVkNDUwYTBiMThjYWMtMWE1MjU2MzctMjA3MzYwMC0xOTAxNTNlYmYwZjIzYTcifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190153ebf0eeb-065d450a0b18cac-1a525637-2073600-190153ebf0f23a7%22%7D',
    'language': 'zh',
    'ones-uid': 'E2VDNNai',
    'ones-lt': '0eVh2h7q5hPrMH3s7yALcGGOvXWkmfT8ScXhfNaX7YaNcRoNDwhVrYQxaP6A8SmJ',
    'timezone': 'Asia/Shanghai',
    'ct': '4813f0c74e8983ef600e3be05175e3dc77cc210a1b58d228a3ea5c09e731a013',
}

headers = {
    'Host': 'podrestart.k3s-dev.myones.net',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'X-CSRF-TOKEN': '4813f0c74e8983ef600e3be05175e3dc77cc210a1b58d228a3ea5c09e731a013',
    'Accept-Language': 'zh',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua-platform': '"macOS"',
    'Origin': 'https://podrestart.k3s-dev.myones.net',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://podrestart.k3s-dev.myones.net/project/',
    'Content-Type': 'application/json;charset=UTF-8',
    # 'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190153ebf0eeb-065d450a0b18cac-1a525637-2073600-190153ebf0f23a7%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMTUzZWJmMGVlYi0wNjVkNDUwYTBiMThjYWMtMWE1MjU2MzctMjA3MzYwMC0xOTAxNTNlYmYwZjIzYTcifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190153ebf0eeb-065d450a0b18cac-1a525637-2073600-190153ebf0f23a7%22%7D; language=zh; ones-uid=E2VDNNai; ones-lt=0eVh2h7q5hPrMH3s7yALcGGOvXWkmfT8ScXhfNaX7YaNcRoNDwhVrYQxaP6A8SmJ; timezone=Asia/Shanghai; ct=4813f0c74e8983ef600e3be05175e3dc77cc210a1b58d228a3ea5c09e731a013',
}

params = {
    't': 'group-task-data',
}

json_data = {
    'query': '{\n         tasks (\n        filterGroup: $filterGroup\n         ) {\n        \n    key\n    name\n    uuid\n    serverUpdateStamp\n    number\n    path\n    subTaskCount\n    subTaskDoneCount\n    position\n    status {\n      uuid\n      name\n      category\n    }\n    deadline(unit: ONESDATE)\n    subTasks {\n      uuid\n    }\n    issueType {\n      uuid\n      manhourStatisticMode\n    }\n    subIssueType {\n      uuid\n      manhourStatisticMode\n    }\n    project {\n      uuid\n    }\n    parent {\n      uuid\n    }\n    estimatedHours\n    remainingManhour\n    totalEstimatedHours\n    totalRemainingHours\n    issueTypeScope {\n      uuid\n    }\n\n        \n        number\n      \n        name\n      \n        \n    priority {\n      bgColor\n      color\n      uuid\n      value\n      position\n    }\n  \n      \n        \n    status {\n      uuid\n      name\n    }\n  \n      \n        \n    assign {\n      key\n      uuid\n      name\n      avatar\n    }\n  \n      deadline(unit: ONESDATE)\n        estimatedHours\n      \n        totalManhour\n      \n        remainingManhour\n      \n        \n    owner {\n      key\n      uuid\n      name\n      avatar\n    }\n  \n      \n        }}',
    'variables': {
        'groupBy': {
            'tasks': {},
        },
        'groupOrderBy': None,
        'orderBy': {
            'position': 'ASC',
            'createTime': 'DESC',
        },
        'filterGroup': [
            {
                'uuid_in': [
                    'E2VDNNai1750cf16',
                ],
            },
        ],
        'search': None,
        'pagination': {
            'preciseCount': False,
        },
    },
}

if __name__ == '__main__':
    i = 0
    while True:
        response = requests.post(
            'https://podrestart.k3s-dev.myones.net/project/api/project/team/2QPVWPD5/items/graphql',
            params=params,
            cookies=cookies,
            headers=headers,
            json=json_data,
            # proxies=proxies,
        )
        print(response.status_code, i)
        print(response.text)
        i += 1
        if i > 1520:
            break
        # time.sleep(0.1)
