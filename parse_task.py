import json
import requests


def extract_task_uuids(file_path):
    task_uuids = []
    with open(file_path, 'r') as f:
        data = json.load(f)
        buckets = data['data']['buckets']
        for bucket in buckets:
            tasks = bucket['tasks']
            for task in tasks:
                task_uuids.append(task['uuid'])
    return task_uuids


def send_request(ids: []):
    try:
        response = requests.post(
            url="http://ext.ones.pro:10075/project/api/project/team/FWdNetPL/tasks/info",
            headers={
                "Host": "ext.ones.pro:10075",
                "Connection": "keep-alive",
                "Content-Length": "47",
                "Accept": "application/json, text/plain, */*",
                "X-CSRF-TOKEN": "dc0d12761a78a6d7665a39e2bd4b9126ff4f18f92212b3c47c344b5d5fb11b37",
                "Accept-Language": "zh",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                "Content-Type": "application/json;charset=UTF-8",
                "Origin": "http://ext.ones.pro:10075",
                "Referer": "http://ext.ones.pro:10075/project/",
                "Accept-Encoding": "gzip, deflate",
                "Cookie": "language=zh; ones-uid=5zmkNmmT; ones-lt=CCsGNBlWnwjI12AjgMYpa88BE2wpXtJVXDtu21THLSFUJKDdhhxQ35XBKRZnH5iA; timezone=Asia/Shanghai; ct=dc0d12761a78a6d7665a39e2bd4b9126ff4f18f92212b3c47c344b5d5fb11b37; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22R9o8QgKu%22%2C%22first_id%22%3A%22181ae269bf5cf6-02d82d82d82d82e-37796305-1296000-181ae269bf61a2e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiJSOW84UWdLdSIsIiRpZGVudGl0eV9jb29raWVfaWQiOiIxODFhZTI2OWJmNWNmNi0wMmQ4MmQ4MmQ4MmQ4MmUtMzc3OTYzMDUtMTI5NjAwMC0xODFhZTI2OWJmNjFhMmUifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22R9o8QgKu%22%7D%2C%22%24device_id%22%3A%22181ae269bf5cf6-02d82d82d82d82e-37796305-1296000-181ae269bf61a2e%22%7D",
            },
            data=json.dumps({
                "ids": ids
            })
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


if __name__ == "__main__":
    json_file_path = "/Users/xhs/Downloads/ext.ones.pro_08-04-2023-10-36-41.json"
    task_uuids = extract_task_uuids(json_file_path)
    # 发30个请求
    for i in range(300):
        send_request(task_uuids)
    # print("Task UUIDs:")
    # for uuid in task_uuids:
    #     print(f"\"{uuid}\",")
