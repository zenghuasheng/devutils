import random
import string
from datetime import datetime

import requests


# 生成随机的 8 个字符
def generate_random_suffix(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# 生成符合要求的 UUID
def generate_uuid(user_uuid):
    return user_uuid + generate_random_suffix()


class DependencyTest():
    base_url = ''
    user_uuid = ''
    team_uuid = ''
    cookie = ''
    plugin_uuid = ''
    project_uuid = ''
    authorization = ''
    number = 0

    def __init__(self, base_url, user_uuid, team_uuid, plugin_uuid, cookie, authorization, project_uuid):
        self.base_url = base_url + '/project/api/project'
        self.user_uuid = user_uuid
        self.team_uuid = team_uuid
        self.plugin_uuid = plugin_uuid
        self.cookie = cookie
        self.authorization = authorization
        self.project_uuid = project_uuid

    def get_standard_headers(self):
        # 请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.authorization,
            'Cookie': self.cookie
        }
        return headers

    def get_headers(self):
        # 请求头
        headers = {
            'ones-plugin-id': self.plugin_uuid,
            'ones-check-id': self.team_uuid,
            'ones-check-point': 'team',
            'Content-Type': 'application/json',
            'Cookie': self.cookie
        }
        return headers

    def fetch_tasks(self):
        # url = "https://ppm.k3s-dev.myones.net/project/api/project/team/EJ2nRZH6/ppm/tasks/list"
        url = f"{self.base_url}/team/{self.team_uuid}/ppm/tasks/list"
        # 请求体
        data = {
            "project_uuid": self.project_uuid,
            "field_uuids": [
                "field001",
                "field004",
                "field012",
                "field005",
                "field017",
                "field003",
                "field011"
            ]
        }

        # 发送请求
        response = requests.post(url, json=data, headers=self.get_headers())

        # 检查响应状态码是否为200
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        # 将响应的 JSON 数据解析为字典
        result = response.json()

        print(result)

        # 检查返回的 success 字段是否为 True
        assert result["data"]["success"] == True, "Expected success to be True, but it is False"

        # 检查 tasks 列表是否不为空
        tasks = result["data"]["tasks"]
        assert len(tasks) > 0, "Expected at least one task, but got an empty list"

        return result

    def save_dependency_by_relate(self, source_uuid, target_uuid, dependency_type="FS"):
        url = f"{self.base_url}/team/{self.team_uuid}/task/{source_uuid}/related_tasks"
        data = {
            "task_uuids": [
                target_uuid
            ],
            "task_link_type_uuid": f"PPM000{dependency_type}",
            "link_desc_type": "link_out_desc"
        }
        response = requests.post(url, json=data, headers=self.get_standard_headers())
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    def save_dependency(self, source_uuid, target_uuid, dependency_type="FS", is_asap=True, delay_days=0, is_add=True):
        url = f"{self.base_url}/team/{self.team_uuid}/ppm/save-dependency"
        data = {
            "project_uuid": self.project_uuid,
            "dependency_type": dependency_type,
            "source_uuid": source_uuid,
            "target_uuid": target_uuid,
            "is_asap": is_asap,
            "delay_days": delay_days,
            "is_add": is_add
        }
        response = requests.post(url, json=data, headers=self.get_headers())
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        # result = response.json()
        # assert result["data"]["success"] == True, "Expected success to be True, but it is False"
        # # 遍历 tasks 列表，找到 uuid 为 source_uuid 的任务，检查其 context.successors 列表是否包含 target_uuid
        # tasks = result["data"]["tasks"]
        # source_task = next(task for task in tasks if task["uuid"] == source_uuid)
        # successors = source_task["context"]["successors"]
        # # [{'uuid': '2auLpYfT0wgEkBA1', 'dependency_type': 'FS', 'create_time': 1725963753.921, 'number': 51, 'is_asap': True, 'delay_days': 0, 'errors': [], 'is_key_path': True}]
        # # assert target_uuid in successors, f"Expected {target_uuid} to be in successors, but it is not"
        # # 验证 target_uuid 是否在 successors 列表中，要用 uuid 字段进行比较
        # assert any(dep["uuid"] == target_uuid for dep in successors), f"Expected {target_uuid} to be in successors, but it is not"
        # # dependency_type, is_asap, delay_days 也要一致
        # dependency = next(dep for dep in successors if dep["uuid"] == target_uuid)
        # assert dependency[
        #            "dependency_type"] == dependency_type, f"Expected dependency_type {dependency_type}, but got {dependency['dependency_type']}"
        # assert dependency["is_asap"] == is_asap, f"Expected is_asap {is_asap}, but got {dependency['is_asap']}"
        # assert dependency[
        #            "delay_days"] == delay_days, f"Expected delay_days {delay_days}, but got {dependency['delay_days']}"

    def update_field_value(self, task_uuid, **kwargs):
        url = f"{self.base_url}/team/{self.team_uuid}/ppm/update-field-value"

        # 构建请求数据
        data = {
            "project_uuid": self.project_uuid,
            "uuid": task_uuid,
        }

        # 动态添加字段，仅处理用户显式提供的参数
        if 'start_date' in kwargs:
            data["start_date"] = kwargs['start_date']

        if 'end_date' in kwargs:
            data["end_date"] = kwargs['end_date']

        if 'duration' in kwargs:
            duration = kwargs['duration']
            assert isinstance(duration, (int, float)) and duration > 0, "Duration must be a positive number"
            data["duration"] = duration

        # 发送请求
        response = requests.post(url, json=data, headers=self.get_headers())

        # 验证响应状态码
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        # 验证结果
        result = response.json()
        assert result["data"]["success"] == True, "Expected success to be True, but it is False"

    def add_task(self, name):
        url = f"{self.base_url}/team/{self.team_uuid}/tasks/add3"
        task_uuid = generate_uuid(self.user_uuid)
        data = {
            "tasks": [
                {
                    "uuid": task_uuid,
                    "assign": self.user_uuid,
                    "summary": name,
                    "parent_uuid": "",
                    "field_values": [
                        {
                            "field_uuid": "field004",
                            "type": 8,
                            "value": self.user_uuid
                        },
                        {
                            "field_uuid": "field012",
                            "type": 1,
                            "value": "2KeLxkuV"
                        },
                        {
                            "field_uuid": "field011",
                            "type": 7,
                            "value": None
                        },
                        {
                            "field_uuid": "field001",
                            "type": 2,
                            "value": name
                        },
                        {
                            "field_uuid": "field016",
                            "type": 20,
                            "value": None
                        }
                    ],
                    "issue_type_uuid": "EH285Jnd",
                    "project_uuid": self.project_uuid,
                    "watchers": [],
                }
            ]
        }
        response = requests.post(url, json=data, headers=self.get_standard_headers())
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        result = response.json()
        print(result)
        return task_uuid
    def set_wbs_parent(self, uuid, parent_uuid):
        url = f"{self.base_url}/team/{self.team_uuid}/tasks/update3"
        data = {
            "tasks": [
                {
                    "uuid": uuid,
                    "field_values": [
                        {
                            "field_uuid": "SizPxmz4",
                            "type": 1001,
                            "value": parent_uuid
                        }
                    ]
                }
            ],
            "must_all_succeed": False
        }
        response = requests.post(url, json=data, headers=self.get_standard_headers())
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        result = response.json()
        print(result)

    def generate_name(self):
        # 当前的日期和时间
        now = datetime.now()
        ch = chr(ord('A') + self.number)
        self.number += 1
        return f"T{now.strftime('%m%d_%H%M%S')}_{ch}"

    def add_dependency_between_tasks(self):
        # 添加两个任务
        task1_uuid = self.add_task(self.generate_name())
        task2_uuid = self.add_task(self.generate_name())
        # 设置任务的开始时间、结束时间
        self.update_field_value(task1_uuid, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(task2_uuid, start_date="2024-09-11", end_date="2024-09-11")
        # 保存两个任务之间的依赖关系
        self.save_dependency(task1_uuid, task2_uuid)
        # return task1_uuid, task2_uuid
        # 获取任务列表，检查依赖关系是否正确
        result = self.fetch_tasks()
        print(result)

    def test_autoschedule(self):
        # 添加两个任务
        task1_uuid = self.add_task(self.generate_name())
        task2_uuid = self.add_task(self.generate_name())
        task3_uuid = self.add_task(self.generate_name())
        # 设置任务的开始时间、结束时间
        self.update_field_value(task1_uuid, start_date="2024-09-11", end_date="2024-09-11")
        self.update_field_value(task2_uuid, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(task3_uuid, start_date="2024-09-11", end_date="2024-09-11")
        # 保存两个任务之间的依赖关系
        self.save_dependency(task1_uuid, task2_uuid)
        self.save_dependency(task3_uuid, task2_uuid)

    def test_four_dependencies(self):
        task1_uuid = self.add_task(self.generate_name())
        task2_uuid = self.add_task(self.generate_name())
        task3_uuid = self.add_task(self.generate_name())
        task4_uuid = self.add_task(self.generate_name())
        task5_uuid = self.add_task(self.generate_name())
        task6_uuid = self.add_task(self.generate_name())
        task7_uuid = self.add_task(self.generate_name())
        task8_uuid = self.add_task(self.generate_name())
        self.update_field_value(task1_uuid, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(task2_uuid, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(task3_uuid, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(task4_uuid, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(task5_uuid, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(task6_uuid, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(task7_uuid, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(task8_uuid, start_date="2024-09-10", end_date="2024-09-10")
        self.save_dependency(task1_uuid, task2_uuid, dependency_type='SS')
        self.save_dependency(task3_uuid, task4_uuid, dependency_type='SF')
        self.save_dependency(task5_uuid, task6_uuid, dependency_type='FS')
        self.save_dependency(task7_uuid, task8_uuid, dependency_type='FF')

    def test_collect(self):
        uuid1 = self.add_task(self.generate_name())
        # uuid2 = self.add_task(self.generate_name())
        # uuid3 = self.add_task(self.generate_name())
        # self.set_wbs_parent(uuid2, uuid1)
        # self.set_wbs_parent(uuid3, uuid1)

    def test_multi_predecessors(self):
        uuid1 = self.add_task(self.generate_name())
        uuid2 = self.add_task(self.generate_name())
        uuid3 = self.add_task(self.generate_name())
        uuid4 = self.add_task(self.generate_name())
        self.update_field_value(uuid1, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(uuid2, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(uuid3, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(uuid4, start_date="2024-09-10", end_date="2024-09-10")
        self.save_dependency(uuid2, uuid1)
        self.save_dependency(uuid3, uuid1)
        self.save_dependency(uuid4, uuid1)

    def test_have_cycle(self):
        uuid1 = self.add_task(self.generate_name())
        uuid2 = self.add_task(self.generate_name())
        uuid3 = self.add_task(self.generate_name())
        uuid4 = self.add_task(self.generate_name())
        self.update_field_value(uuid1, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(uuid2, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(uuid3, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(uuid4, start_date="2024-09-10", end_date="2024-09-10")
        self.save_dependency_by_relate(uuid1, uuid2)
        self.save_dependency_by_relate(uuid2, uuid3)
        self.save_dependency_by_relate(uuid3, uuid1)
        self.save_dependency_by_relate(uuid1, uuid4)
    def test_have_repeat_dependency(self):
        uuid1 = self.add_task(self.generate_name())
        uuid2 = self.add_task(self.generate_name())
        uuid3 = self.add_task(self.generate_name())
        self.update_field_value(uuid1, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(uuid2, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(uuid3, start_date="2024-09-10", end_date="2024-09-10")
        self.save_dependency_by_relate(uuid1, uuid2, dependency_type='FS')
        self.save_dependency_by_relate(uuid1, uuid2, dependency_type='SS')
        self.save_dependency_by_relate(uuid2, uuid3)

    def test_have_parent(self):
        uuid1 = self.add_task(self.generate_name())
        uuid2 = self.add_task(self.generate_name())
        uuid3 = self.add_task(self.generate_name())
        self.update_field_value(uuid1, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(uuid2, start_date="2024-09-10", end_date="2024-09-10")
        self.update_field_value(uuid3, start_date="2024-09-10", end_date="2024-09-10")
        self.set_wbs_parent(uuid2, uuid1)
        self.set_wbs_parent(uuid3, uuid2)


    def test_request_number(self):
        task1_uuid = self.add_task(self.generate_name())
        self.update_field_value(task1_uuid, start_date="2024-09-10", end_date="2024-09-10")

refresh_token_file = "refresh_token.txt"

def read_refresh_token():
    # 从文件中读取 refresh token
    with open(refresh_token_file, "r") as file:
        return file.read().strip()

def get_token(base_url, cookie):
    url = f"{base_url}/identity/oauth/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': read_refresh_token(),
        'client_id': 'ones.v1'
    }
    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    result = response.json()
    # 写入 refresh token 到文件
    with open(refresh_token_file, "w") as file:
        file.write(result['refresh_token'])
    return result['access_token']

# 调用函数并测试
if __name__ == "__main__":
    base_url = "https://ppm.k3s-dev.myones.net"
    user_uuid = "2auLpYfT"
    team_uuid = "EJ2nRZH6"
    project_uuid = "2auLpYfTYRCwH6wC"
    plugin_uuid = "bd67187c"
    cookie = 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190baaa1d1d6a8-00c9a3b6ad31ef9-19525637-2073600-190baaa1d1e28fb%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwYmFhYTFkMWQ2YTgtMDBjOWEzYjZhZDMxZWY5LTE5NTI1NjM3LTIwNzM2MDAtMTkwYmFhYTFkMWUyOGZiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190baaa1d1d6a8-00c9a3b6ad31ef9-19525637-2073600-190baaa1d1e28fb%22%7D; ones-lang=zh; ones-tz=Asia%2FShanghai; ones-region-uuid=default; ones-org-uuid=AKeDv8P8; timezone=Asia/Shanghai; ones-ids-sid=1a9e3ef7-9b61-408e-7175-ede03fabf1e5; ones-lt=eyJhbGciOiJSUzI1NiIsImtpZCI6IjNmY2NkNzkxLTBmNWMtNDA2Yy03ZDA1LTEwMTJiMzZhM2E5YSIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsib25lcy52MSJdLCJjbGllbnRfaW5mbyI6eyJjbGllbnRfaXAiOiI1OC42MS4xNjEuMTQ0In0sImV4cCI6MTcyNTk2MzQ3OSwiaWF0IjoxNzI1OTU5NTc5LCJpc3MiOiJodHRwOi8vcHBtLmszcy1kZXYubXlvbmVzLm5ldC8iLCJqdGkiOiI4NzJjZjM3OC1lMDFiLTQyZWUtNmYyNy03YWI2NDI3ZDUwNTYiLCJsb2dpbl90aW1lIjoxNzI1ODYwNDE2NTg0LCJuYmYiOjE3MjU5NTk1NzksIm9yZ191c2VyX3V1aWQiOiIyYXVMcFlmVCIsIm9yZ191dWlkIjoiQUtlRHY4UDgiLCJyZWdpb25fdXVpZCI6ImRlZmF1bHQiLCJzY29wZXMiOlsib3BlbmlkIiwib2ZmbGluZV9hY2Nlc3MiLCJvbmVzOm9yZzpkZWZhdWx0OkFLZUR2OFA4OjJhdUxwWWZUIl0sInNpZCI6IjVjY2MwNTllLWQ3ZDctNGQ3YS01YmFiLTQxNzRhMWI3ZjM5OSIsInN1YiI6IlZUd3hhaGNOOmRlZmF1bHQ6QUtlRHY4UDg6MmF1THBZZlQifQ.hQZ9_eaKRgRBafnIzSAEvowVLdxAp9hMwx15wQt8YgDQKRl0HgciwQjRxSleb8kwumkW9tByP0TfT8zwYz9VYJ10YZnO0ak8DlswXv2xhjJMiYs5jywoWybvQX3q11TOCeP9cGZlK8UTMjIsVn2wcP7_hDGWQfizBqFoRIhJ3B0lRE8k-iaDX-UmzkY_wrDCiVR-M3lNIKfYndTBBLIpz9_ksTAKsbAPuNeLhrsvggUdeUlmecwH2qAfiZcybSf7XFlDJRrLT4d89WC6az-mX5auWoXuPpy19meU9ZA6v2p1DlT83JgAuFaYU2aiooH_kZ27jdQ46CAxOLojQy-TxA; ct=3a2e8254f06f11372c0ea10f0af7a0dbd802f87ab8a881cae2645a18e7e7dded'
    token = get_token(base_url, cookie)
    authorization = f'Bearer {token}'
    test = DependencyTest(base_url, user_uuid, team_uuid, plugin_uuid, cookie, authorization, project_uuid)
    # test.fetch_tasks()
    # task_uuid = test.add_task("A1")
    # test.add_dependency_between_tasks()
    # test.test_autoschedule()
    # test.test_four_dependencies()
    # test.test_collect()
    # test.test_multi_predecessors()
    # test.test_have_cycle()
    # test.test_have_repeat_dependency()
    test.test_have_parent()
