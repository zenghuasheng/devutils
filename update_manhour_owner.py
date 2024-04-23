import json
import requests


def update_manhour(owner_uuid, task_uuid, hours, key, start_time):
    url = 'https://our.ones.pro/project/api/project/team/RDjYMhKq/items/graphql?t=UpdateManhour'
    headers = {
        'Host': 'our.ones.pro',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'X-CSRF-TOKEN': 'ae95078ed8a7402db0039a3e0a9b36f961ad915868456112e8ff2504fd0c0385',
        'Accept-Language': 'zh',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua-platform': '"macOS"',
        'Origin': 'https://our.ones.pro',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://our.ones.pro/project/',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'language=zh; sajssdk_2015_cookie_access_test=1; ones-uid=R9o8QgKu; ones-lt=BrKFa7nsNIUolpM7wEm7Pn1rdvCHprQlpASbCcTWtKwGU8bigjo1p4Gy79St1WGf; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22R9o8QgKu%22%2C%22first_id%22%3A%22181ae269bf5cf6-02d82d82d82d82e-37796305-1296000-181ae269bf61a2e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiJSOW84UWdLdSIsIiRpZGVudGl0eV9jb29raWVfaWQiOiIxODFhZTI2OWJmNWNmNi0wMmQ4MmQ4MmQ4MmQ4MmUtMzc3OTYzMDUtMTI5NjAwMC0xODFhZTI2OWJmNjFhMmUifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22R9o8QgKu%22%7D%2C%22%24device_id%22%3A%22181ae269bf5cf6-02d82d82d82d82e-37796305-1296000-181ae269bf61a2e%22%7D; timezone=Asia/Shanghai; ct=ae95078ed8a7402db0039a3e0a9b36f961ad915868456112e8ff2504fd0c0385',
    }

    payload = {
        "query": """
            mutation UpdateManhour {
              updateManhour (
                mode: "detailed",
                task: "%s",
                owner: "%s",
                type: "estimated",
                hours: %d,
                key: "%s",
                start_time: "%s"
              ) {
                key
              }
            }
        """ % (task_uuid, owner_uuid, hours, key, start_time)
    }

    print(json.dumps(payload, indent=2))
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Manhour updated successfully.")
    else:
        print("Failed to update manhour.")


def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    json_file = "/Users/xhs/task/工作项增加模块属性/our.ones.pro_04-17-2024-17-21-39.json"
    data = read_json_file(json_file)
    manhours = data.get('data', {}).get('manhours', [])
    for manhour in manhours:
        owner_uuid = manhour.get('owner', {}).get('uuid')
        if owner_uuid == "R9o8QgKu":
            continue
        owner_uuid = "R9o8QgKu"
        task_uuid = manhour.get('task', {}).get('uuid')
        hours = manhour.get('hours')
        key = "manhour-" + manhour.get('uuid')
        start_time = "2024-03-20"  # 你需要修改为实际的时间
        update_manhour(owner_uuid, task_uuid, hours, key, start_time)
