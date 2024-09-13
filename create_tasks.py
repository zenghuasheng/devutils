import time

import requests
import random
import string
import uuid
import json


# 生成随机的 8 个字符
def generate_random_suffix(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# 生成符合要求的 UUID
def generate_uuid():
    return 'XuP7g899' + generate_random_suffix()


# 递归创建任务并生成二叉树
def create_tasks(level, max_level, parent_uuid, project_uuid, issue_type_uuid, sub_issue_type_uuid, summary_prefix):
    if level > max_level:
        return []

    tasks = []
    # num_tasks = 2 ** (level - 1)

    for i in range(1, 3):
        task_uuid = generate_uuid()
        summary = f"{summary_prefix}{level}层{i}"
        task = {
            "uuid": task_uuid,
            "assign": "XuP7g899",
            "summary": summary,
            "parent_uuid": parent_uuid,
            "project_uuid": project_uuid,
            "issue_type_uuid": issue_type_uuid,
            "sub_issue_type_uuid": sub_issue_type_uuid,
            "owner": "XuP7g899",
            "desc_rich": None,
            "field_values": [
                {
                    "field_uuid": "field011",
                    "type": 7,
                    "value": "MTgrBco2"
                }
            ],
            "layout_type": 2,
            "add_manhours": []
        }
        tasks.append(task)
        tasks += create_tasks(level + 1, max_level, task_uuid, project_uuid, issue_type_uuid, sub_issue_type_uuid,
                              summary_prefix)

    return tasks


def main():
    # 初始父任务 UUID 和项目 UUID
    root_uuid = 'XuP7g899gJoueY8k'
    project_uuid = 'XuP7g8996jry6h9s'
    issue_type_uuid = "U1nLXzS2"
    sub_issue_type_uuid = "U1nLXzS2"

    # 创建二叉树层级的任务
    max_level = 9  # 可以根据需要调整层数
    tasks = create_tasks(1, max_level, root_uuid, project_uuid, issue_type_uuid, sub_issue_type_uuid, "第")

    # 发送 HTTP 请求
    url = 'https://plugin.k3s-dev.myones.net/project/api/project/team/DSsFH9nr/tasks/add3'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg2ZTljZGY1LTIxZjItNDBmNi02YTVjLTJlYzExZTQxZTY5YiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsib25lcy52MSJdLCJjbGllbnRfaW5mbyI6eyJjbGllbnRfaXAiOiIyMTguMTcuMjE1LjE4In0sImV4cCI6MTcyMjk0MDgxOSwiaWF0IjoxNzIyOTM2OTE5LCJpc3MiOiJodHRwOi8vcGx1Z2luLmszcy1kZXYubXlvbmVzLm5ldC8iLCJqdGkiOiJlOTllYjM3OS0yZTAwLTRiMTItNTc4ZC1kYTQ5Y2MwYTE2NzIiLCJsb2dpbl90aW1lIjoxNzIyODMwODkzOTYxLCJuYmYiOjE3MjI5MzY5MTksIm9yZ191c2VyX3V1aWQiOiJYdVA3Zzg5OSIsIm9yZ191dWlkIjoiRnZGVDkyY2IiLCJyZWdpb25fdXVpZCI6ImRlZmF1bHQiLCJzY29wZXMiOlsib3BlbmlkIiwib2ZmbGluZV9hY2Nlc3MiLCJvbmVzOm9yZzpkZWZhdWx0OkZ2RlQ5MmNiOlh1UDdnODk5Il0sInNpZCI6IjY1NmM3ZGQxLWVjMTQtNDE3Yy02ZDQ4LTE3ZGI3YzdkOWI2ZSIsInN1YiI6IjZkZmNQTHpDOmRlZmF1bHQ6RnZGVDkyY2I6WHVQN2c4OTkifQ.gl7GIje16OLgJiLGTqdzYf6ecChXLLCGUXpxMFkS-cRdX0wyIyzCDxh-zeKJFLafoZNTFT2wIUjCZx1S4Sf-a_HwChQcdcnnu7RmGz_lly0hdcbVbwQtwcmE1r-SLvY7G-ukrKID53IeSUedzTIa1P7RpypHyoyPHLIeah1pl1Sxgq6Q58svMBXGOpLB5piTsPhTa2qxIwabOVOUe99UOYxCCmSy_8V34VCM2ibaIpGYYG7BHCgNPx6hq4I6_p_Z0VhTty5USlnyOZvCBXGa7ACxf4Ua2RjGNkCOtS43IqvVom-QlCRRACGg7WnYeZR6Oh_wCsIAbWxL8lWT28fcZQ',
        'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190baaa1d1d6a8-00c9a3b6ad31ef9-19525637-2073600-190baaa1d1e28fb%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwYmFhYTFkMWQ2YTgtMDBjOWEzYjZhZDMxZWY5LTE5NTI1NjM3LTIwNzM2MDAtMTkwYmFhYTFkMWUyOGZiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190baaa1d1d6a8-00c9a3b6ad31ef9-19525637-2073600-190baaa1d1e28fb%22%7D; ones-tz=Asia%2FShanghai; ones-region-uuid=default; ones-org-uuid=FvFT92cb; timezone=Asia/Shanghai; ones-ids-sid=f8def544-0c1d-4cd6-54d8-dfb300631e4d; ones-lang=zh; ct=6617887edab0da28f77b69cdbbadb8bd9cbf916663fa2f00d130e5fed2893298; ones-lt=eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg2ZTljZGY1LTIxZjItNDBmNi02YTVjLTJlYzExZTQxZTY5YiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsib25lcy52MSJdLCJjbGllbnRfaW5mbyI6eyJjbGllbnRfaXAiOiIyMTguMTcuMjE1LjE4In0sImV4cCI6MTcyMjk0MDgxOSwiaWF0IjoxNzIyOTM2OTE5LCJpc3MiOiJodHRwOi8vcGx1Z2luLmszcy1kZXYubXlvbmVzLm5ldC8iLCJqdGkiOiJlOTllYjM3OS0yZTAwLTRiMTItNTc4ZC1kYTQ5Y2MwYTE2NzIiLCJsb2dpbl90aW1lIjoxNzIyODMwODkzOTYxLCJuYmYiOjE3MjI5MzY5MTksIm9yZ191c2VyX3V1aWQiOiJYdVA3Zzg5OSIsIm9yZ191dWlkIjoiRnZGVDkyY2IiLCJyZWdpb25fdXVpZCI6ImRlZmF1bHQiLCJzY29wZXMiOlsib3BlbmlkIiwib2ZmbGluZV9hY2Nlc3MiLCJvbmVzOm9yZzpkZWZhdWx0OkZ2RlQ5MmNiOlh1UDdnODk5Il0sInNpZCI6IjY1NmM3ZGQxLWVjMTQtNDE3Yy02ZDQ4LTE3ZGI3YzdkOWI2ZSIsInN1YiI6IjZkZmNQTHpDOmRlZmF1bHQ6RnZGVDkyY2I6WHVQN2c4OTkifQ.gl7GIje16OLgJiLGTqdzYf6ecChXLLCGUXpxMFkS-cRdX0wyIyzCDxh-zeKJFLafoZNTFT2wIUjCZx1S4Sf-a_HwChQcdcnnu7RmGz_lly0hdcbVbwQtwcmE1r-SLvY7G-ukrKID53IeSUedzTIa1P7RpypHyoyPHLIeah1pl1Sxgq6Q58svMBXGOpLB5piTsPhTa2qxIwabOVOUe99UOYxCCmSy_8V34VCM2ibaIpGYYG7BHCgNPx6hq4I6_p_Z0VhTty5USlnyOZvCBXGa7ACxf4Ua2RjGNkCOtS43IqvVom-QlCRRACGg7WnYeZR6Oh_wCsIAbWxL8lWT28fcZQ',
    }
    data = {
        "tasks": tasks
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Tasks created successfully:")
        print(response.json())
    else:
        print(f"Failed to create tasks. Status code: {response.status_code}")
        print(response.text)


def create_task2():
    # curl 'https://x1065-k3s-3.k3s-dev.myones.net/project/api/project/team/JGcrF2yM/tasks/add3' \
    # -X POST \
    # -H 'Host: x1065-k3s-3.k3s-dev.myones.net' \
    # -H 'Connection: keep-alive' \
    # -H 'sec-ch-ua: "Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"' \
    # -H 'X-CSRF-TOKEN: 9cc07459ffda05457aab4251859d07ba78d3ce88053d956af37a56e9109a3f7c' \
    # -H 'Accept-Language: zh' \
    # -H 'sec-ch-ua-mobile: ?0' \
    # -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjU5Y2M2MzFiLTNmMmUtNGVlZi01ODAyLTMyNDI0MTM3MGY2NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsib25lcy52MSJdLCJjbGllbnRfaW5mbyI6eyJjbGllbnRfaXAiOiI1OC42MS4xNjEuMTQ0In0sImV4cCI6MTcyMzYzMDEyMCwiaWF0IjoxNzIzNjI2MjIwLCJpc3MiOiJodHRwOi8veDEwNjUtazNzLTMuazNzLWRldi5teW9uZXMubmV0LyIsImp0aSI6IjRlZDZlYzExLTA3OWMtNGQ2Yi00NDE1LTY4NmUyMmFlZDkyZiIsImxvZ2luX3RpbWUiOjE3MjM2MjMyMTg5MDgsIm5iZiI6MTcyMzYyNjIyMCwib3JnX3VzZXJfdXVpZCI6IlhQOEFMSDloIiwib3JnX3V1aWQiOiJUTXoydzVGOCIsInJlZ2lvbl91dWlkIjoiZGVmYXVsdCIsInNjb3BlcyI6WyJvcGVuaWQiLCJvZmZsaW5lX2FjY2VzcyIsIm9uZXM6b3JnOmRlZmF1bHQ6VE16Mnc1Rjg6WFA4QUxIOWgiXSwic2lkIjoiNjliMGJhZTItNzExZC00MzlmLTQ4YzctZjM5YWUxOTI0NzJjIiwic3ViIjoiR3RhTFR6c1g6ZGVmYXVsdDpUTXoydzVGODpYUDhBTEg5aCJ9.E47JWM9qZXP3hlF9cg3yW4udao2y2-XhnEa_ecbkcDed7MoA_9wBLtDlk6ngARJH_QijB_9TO0O5xTRsUwMiPPplBiUzP0BQePsiRWwRaon98MxHI4VRq4jaXApqhSGJmuYdk_hanUTcV4FTtLAQTP4rjWIeu1Ke0SAvsnLywmqL_Iak6E_GIHkeZjKwnUT7AxBjYskhTogePzJM2q7N1_MkqLLe7xcVn5DuJ_5FsEWVJCljaVnKsxs6HrCL3UaFqxfH4rxa7Wl-Kw1qWPB7n6eg_H5QuxPVTLNRAH_TYfKf4fDl2Z_swcOsG1KFRMumD1uAiPlr--82tIljbMwYgA' \
    # -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36' \
    # -H 'Accept: application/json, text/plain, */*' \
    # -H 'sec-ch-ua-platform: "macOS"' \
    # -H 'Origin: https://x1065-k3s-3.k3s-dev.myones.net' \
    # -H 'Sec-Fetch-Site: same-origin' \
    # -H 'Sec-Fetch-Mode: cors' \
    # -H 'Sec-Fetch-Dest: empty' \
    # -H 'Referer: https://x1065-k3s-3.k3s-dev.myones.net/project/' \
    # -H 'Content-Type: application/json' \
    # --cookie 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190baaa1d1d6a8-00c9a3b6ad31ef9-19525637-2073600-190baaa1d1e28fb%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwYmFhYTFkMWQ2YTgtMDBjOWEzYjZhZDMxZWY5LTE5NTI1NjM3LTIwNzM2MDAtMTkwYmFhYTFkMWUyOGZiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190baaa1d1d6a8-00c9a3b6ad31ef9-19525637-2073600-190baaa1d1e28fb%22%7D; ones-ids-sid=306c9495-7cca-44dd-7d8b-5e46890f3df1; ones-lang=zh; ones-tz=Asia%2FShanghai; ones-region-uuid=default; ones-org-uuid=TMz2w5F8; timezone=Asia/Shanghai; ones-lt=eyJhbGciOiJSUzI1NiIsImtpZCI6IjU5Y2M2MzFiLTNmMmUtNGVlZi01ODAyLTMyNDI0MTM3MGY2NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsib25lcy52MSJdLCJjbGllbnRfaW5mbyI6eyJjbGllbnRfaXAiOiI1OC42MS4xNjEuMTQ0In0sImV4cCI6MTcyMzYzMDEyMCwiaWF0IjoxNzIzNjI2MjIwLCJpc3MiOiJodHRwOi8veDEwNjUtazNzLTMuazNzLWRldi5teW9uZXMubmV0LyIsImp0aSI6IjRlZDZlYzExLTA3OWMtNGQ2Yi00NDE1LTY4NmUyMmFlZDkyZiIsImxvZ2luX3RpbWUiOjE3MjM2MjMyMTg5MDgsIm5iZiI6MTcyMzYyNjIyMCwib3JnX3VzZXJfdXVpZCI6IlhQOEFMSDloIiwib3JnX3V1aWQiOiJUTXoydzVGOCIsInJlZ2lvbl91dWlkIjoiZGVmYXVsdCIsInNjb3BlcyI6WyJvcGVuaWQiLCJvZmZsaW5lX2FjY2VzcyIsIm9uZXM6b3JnOmRlZmF1bHQ6VE16Mnc1Rjg6WFA4QUxIOWgiXSwic2lkIjoiNjliMGJhZTItNzExZC00MzlmLTQ4YzctZjM5YWUxOTI0NzJjIiwic3ViIjoiR3RhTFR6c1g6ZGVmYXVsdDpUTXoydzVGODpYUDhBTEg5aCJ9.E47JWM9qZXP3hlF9cg3yW4udao2y2-XhnEa_ecbkcDed7MoA_9wBLtDlk6ngARJH_QijB_9TO0O5xTRsUwMiPPplBiUzP0BQePsiRWwRaon98MxHI4VRq4jaXApqhSGJmuYdk_hanUTcV4FTtLAQTP4rjWIeu1Ke0SAvsnLywmqL_Iak6E_GIHkeZjKwnUT7AxBjYskhTogePzJM2q7N1_MkqLLe7xcVn5DuJ_5FsEWVJCljaVnKsxs6HrCL3UaFqxfH4rxa7Wl-Kw1qWPB7n6eg_H5QuxPVTLNRAH_TYfKf4fDl2Z_swcOsG1KFRMumD1uAiPlr--82tIljbMwYgA; ct=9cc07459ffda05457aab4251859d07ba78d3ce88053d956af37a56e9109a3f7c' \
    # --data-raw '{"tasks":[{"uuid":"XP8ALH9hujePWTF6","assign":"XP8ALH9h","summary":"的4","parent_uuid":"","field_values":[{"field_uuid":"field004","type":8,"value":"XP8ALH9h"},{"field_uuid":"field012","type":1,"value":"8DwYpYbr"},{"field_uuid":"field011","type":7,"value":null},{"field_uuid":"field001","type":2,"value":"的4"},{"field_uuid":"field016","type":20,"value":null}],"issue_type_uuid":"Qtto2r6q","project_uuid":"XP8ALH9hCRDNpRW8","watchers":["XP8ALH9h"],"add_manhours":[]}]}' \
    # --proxy http://localhost:9090
    # #1 工作项1、#2 工作项2、...、#100 工作项100、#101 工作项101
    url = 'https://x1065-k3s-3.k3s-dev.myones.net/project/api/project/team/JGcrF2yM/tasks/add3'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjU5Y2M2MzFiLTNmMmUtNGVlZi01ODAyLTMyNDI0MTM3MGY2NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsib25lcy52MSJdLCJjbGllbnRfaW5mbyI6eyJjbGllbnRfaXAiOiI1OC42MS4xNjEuMTQ0In0sImV4cCI6MTcyMzYzMDEyMCwiaWF0IjoxNzIzNjI2MjIwLCJpc3MiOiJodHRwOi8veDEwNjUtazNzLTMuazNzLWRldi5teW9uZXMubmV0LyIsImp0aSI6IjRlZDZlYzExLTA3OWMtNGQ2Yi00NDE1LTY4NmUyMmFlZDkyZiIsImxvZ2luX3RpbWUiOjE3MjM2MjMyMTg5MDgsIm5iZiI6MTcyMzYyNjIyMCwib3JnX3VzZXJfdXVpZCI6IlhQOEFMSDloIiwib3JnX3V1aWQiOiJUTXoydzVGOCIsInJlZ2lvbl91dWlkIjoiZGVmYXVsdCIsInNjb3BlcyI6WyJvcGVuaWQiLCJvZmZsaW5lX2FjY2VzcyIsIm9uZXM6b3JnOmRlZmF1bHQ6VE16Mnc1Rjg6WFA4QUxIOWgiXSwic2lkIjoiNjliMGJhZTItNzExZC00MzlmLTQ4YzctZjM5YWUxOTI0NzJjIiwic3ViIjoiR3RhTFR6c1g6ZGVmYXVsdDpUTXoydzVGODpYUDhBTEg5aCJ9.E47JWM9qZXP3hlF9cg3yW4udao2y2-XhnEa_ecbkcDed7MoA_9wBLtDlk6ngARJH_QijB_9TO0O5xTRsUwMiPPplBiUzP0BQePsiRWwRaon98MxHI4VRq4jaXApqhSGJmuYdk_hanUTcV4FTtLAQTP4rjWIeu1Ke0SAvsnLywmqL_Iak6E_GIHkeZjKwnUT7AxBjYskhTogePzJM2q7N1_MkqLLe7xcVn5DuJ_5FsEWVJCljaVnKsxs6HrCL3UaFqxfH4rxa7Wl-Kw1qWPB7n6eg_H5QuxPVTLNRAH_TYfKf4fDl2Z_swcOsG1KFRMumD1uAiPlr--82tIljbMwYgA',
        'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190baaa1d1d6a8-00c9a3b6ad31ef9-19525637-2073600-190baaa1d1e28fb%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwYmFhYTFkMWQ2YTgtMDBjOWEzYjZhZDMxZWY5LTE5NTI1NjM3LTIwNzM2MDAtMTkwYmFhYTFkMWUyOGZiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190baaa1d1d6a8-00c9a3b6ad31ef9-19525637-2073600-190baaa1d1e28fb%22%7D; ones-ids-sid=306c9495-7cca-44dd-7d8b-5e46890f3df1; ones-lang=zh; ones-tz=Asia%2FShanghai; ones-region-uuid=default; ones-org-uuid=TMz2w5F8; timezone=Asia/Shanghai; ones-lt=eyJhbGciOiJSUzI1NiIsImtpZCI6IjU5Y2M2MzFiLTNmMmUtNGVlZi01ODAyLTMyNDI0MTM3MGY2NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsib25lcy52MSJdLCJjbGllbnRfaW5mbyI6eyJjbGllbnRfaXAiOiI1OC42MS4xNjEuMTQ0In0sImV4cCI6MTcyMzYzMDEyMCwiaWF0IjoxNzIzNjI2MjIwLCJpc3MiOiJodHRwOi8veDEwNjUtazNzLTMuazNzLWRldi5teW9uZXMubmV0LyIsImp0aSI6IjRlZDZlYzExLTA3OWMtNGQ2Yi00NDE1LTY4NmUyMmFlZDkyZiIsImxvZ2luX3RpbWUiOjE3MjM2MjMyMTg5MDgsIm5iZiI6MTcyMzYyNjIyMCwib3JnX3VzZXJfdXVpZCI6IlhQOEFMSDloIiwib3JnX3V1aWQiOiJUTXoydzVGOCIsInJlZ2lvbl91dWlkIjoiZGVmYXVsdCIsInNjb3BlcyI6WyJvcGVuaWQiLCJvZmZsaW5lX2FjY2VzcyIsIm9uZXM6b3JnOmRlZmF1bHQ6VE16Mnc1Rjg6WFA4QUxIOWgiXSwic2lkIjoiNjliMGJhZTItNzExZC00MzlmLTQ4YzctZjM5YWUxOTI0NzJjIiwic3ViIjoiR3RhTFR6c1g6ZGVmYXVsdDpUTXoydzVGODpYUDhBTEg5aCJ9.E47JWM9qZXP3hlF9cg3yW4udao2y2-XhnEa_ecbkcDed7MoA_9wBLtDlk6ngARJH_QijB_9TO0O5xTRsUwMiPPplBiUzP0BQePsiRWwRaon98MxHI4VRq4jaXApqhSGJmuYdk_hanUTcV4FTtLAQTP4rjWIeu1Ke0SAvsnLywmqL_Iak6E_GIHkeZjKwnUT7AxBjYskhTogePzJM2q7N1_MkqLLe7xcVn5DuJ_5FsEWVJCljaVnKsxs6HrCL3UaFqxfH4rxa7Wl-Kw1qWPB7n6eg_H5QuxPVTLNRAH_TYfKf4fDl2Z_swcOsG1KFRMumD1uAiPlr--82tIljbMwYgA; ct=9cc07459ffda05457aab4251859d07ba78d3ce88053d956af37a56e9109a3f7c'
    }

    for i in range(1, 12):
        task_uuid = generate_uuid()
        # summary = f"工作项{i}"
        # 工作项a, 工作项b, ..., 工作项k
        summary = f"工作项{chr(96 + i)}"
        task = {
            "uuid": task_uuid,
            "assign": "XP8ALH9h",
            "summary": summary,
            "parent_uuid": "",
            "field_values": [
                {
                    "field_uuid": "field004",
                    "type": 8,
                    "value": "XP8ALH9h"
                },
                {
                    "field_uuid": "field012",
                    "type": 1,
                    "value": "8DwYpYbr"
                },
                {
                    "field_uuid": "field011",
                    "type": 7,
                    "value": None
                },
                {
                    "field_uuid": "field001",
                    "type": 2,
                    "value": summary
                },
                {
                    "field_uuid": "field016",
                    "type": 20,
                    "value": None
                },
            ],
            "issue_type_uuid": "Qtto2r6q",
            "project_uuid": "XP8ALH9ha45eRXFT",
            "watchers": [
                "XP8ALH9h"
            ],
            "add_manhours": []
        }
        tasks = [task]
        data = {
            "tasks": tasks
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Tasks created successfully:")
            print(response.json())
        else:
            print(f"Failed to create tasks. Status code: {response.status_code}")
            print(response.text)
        time.sleep(0.3)


if __name__ == "__main__":
    # main()
    create_task2()
