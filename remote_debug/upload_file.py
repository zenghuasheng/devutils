import os

import requests


class UploadFile:
    user_uuid = ''
    team_uuid = ''
    token = ''
    cookies_next_request = {}
    task_uuid = ''

    def __init__(self, user_uuid, team_uuid, token):
        self.user_uuid = user_uuid
        self.team_uuid = team_uuid
        self.token = token
        # Set cookies for the next request
        self.cookies_next_request = {
            'language': 'zh',
            'ajs_user_id': 'Suye9AjK',
            'ajs_anonymous_id': '8c86cff4-4787-4bb6-91c4-c4f23ba25ced',
            'sensorsdata2015jssdkcross': '...',
            'timezone': 'Asia/Shanghai',
            'ones-uid': user_uuid,
            'ones-lt': token,
        }

    def get_task(self):
        # Query for the first task
        tasks_url = 'https://mydebug.dev.myones.net/project/api/project/team/{}/items/graphql?t=group-task-data'.format(
            self.team_uuid)
        headers_tasks = {
            'Host': 'mydebug.dev.myones.net',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            # Add other headers as needed
        }
        data_tasks = {
            'query': '{\n    buckets (\n      groupBy: $groupBy\n      orderBy: $groupOrderBy\n      pagination: $pagination\n      filter: $groupFilter\n    ) {\n      key\n      \n      tasks (\n        filterGroup: $filterGroup\n        orderBy: $orderBy\n        limit: 1000\n        \n      includeAncestors:{pathField:\"path\"}\n      orderByPath: \"path\"\n    \n      ) {\n        \n    key\n    name\n    uuid\n    serverUpdateStamp\n    number\n    path\n    subTaskCount\n    subTaskDoneCount\n    position\n    status {\n      uuid\n      name\n      category\n    }\n    deadline(unit: ONESDATE)\n    subTasks {\n      uuid\n    }\n    issueType {\n      uuid\n      manhourStatisticMode\n    }\n    subIssueType {\n      uuid\n      manhourStatisticMode\n    }\n    project {\n      uuid\n    }\n    parent {\n      uuid\n    }\n    estimatedHours\n    remainingManhour\n    totalEstimatedHours\n    totalRemainingHours\n    issueTypeScope {\n      uuid\n    }\n\n        \n      importantField{\n        bgColor\n        color\n        name\n        value\n        fieldUUID\n      }\n      issueTypeScope {\n        uuid\n        currentLayout {\n          uuid\n          hasViewManhourTab\n        }\n      }\n    \n      }\n      pageInfo {\n        count\n        totalCount\n        startPos\n        startCursor\n        endPos\n        endCursor\n        hasNextPage\n        preciseCount\n      }\n    }\n    \n  }',
            # Add the GraphQL query here
            'variables': {
                'groupBy': {'tasks': {}},
                'groupOrderBy': None,
                'orderBy': {'position': 'ASC', 'createTime': 'DESC'},
                'filterGroup': [],
                'search': None,
                'pagination': {'limit': 1, 'preciseCount': False},
            },
        }
        response_tasks = requests.post(tasks_url, headers=headers_tasks, json=data_tasks,
                                       cookies=self.cookies_next_request)
        if response_tasks.status_code != 200:
            raise Exception('Query failed')
        tasks_info = response_tasks.json()

        # Extract the first task
        first_task = tasks_info['data']['buckets'][0]['tasks'][0]
        self.task_uuid = first_task['uuid']

    def upload_file(self):
        # First API endpoint for obtaining upload information
        upload_url = f"https://mydebug.dev.myones.net/project/api/project/team/f{self.team_uuid}/res/attachments/upload"
        headers = {
            'Host': 'mydebug.dev.myones.net',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            # Add other headers as needed
        }
        data = {
            'type': 'attachment',
            'name': 'ones-ai-api-core.tar.gz',
            'ref_id': self.task_uuid,
            'ref_type': 'task',
            'description': '',
            'ctype': ''
        }
        response = requests.post(upload_url, headers=headers, json=data, cookies=self.cookies_next_request)
        if response.status_code != 200:
            raise Exception('Upload failed')
        upload_info = response.json()

        # Second API endpoint for actual file upload
        file_upload_url = upload_info['upload_url']
        file_headers = {
            'Host': 'mydebug.dev.myones.net',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            # Add other headers as needed
        }
        file_data = {
            'token': upload_info['token']
        }
        if not os.path.exists('bin/ones-ai-api-core.tar.gz'):
            raise Exception('File not found')
        files = {
            'file': ('ones-ai-api-core.tar.gz', open('bin/ones-ai-api-core.tar.gz', 'rb'))
        }
        file_response = requests.post(file_upload_url, headers=file_headers, data=file_data,
                                      cookies=self.cookies_next_request,
                                      files=files)
        if file_response.status_code != 200:
            raise Exception('File upload failed')
        file_info = file_response.json()
        print("文件已上传到 /data/ones/files/private")
        print(file_info)


def login_ones():
    # Login API
    login_url = 'https://mydebug.dev.myones.net/project/api/project/auth/v2/login'
    headers_login = {
        'Host': 'mydebug.dev.myones.net',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        # Add other headers as needed
    }
    data_login = {
        'password': 'Test1234',
        'captcha': '',
        'email': 'marsdev@ones.ai',
    }
    cookies_login = {
        # Add your cookies here
    }
    response_login = requests.post(login_url, headers=headers_login, json=data_login, cookies=cookies_login)
    if response_login.status_code != 200:
        raise Exception('Login failed')
    login_info = response_login.json()

    # Extract user information
    user_uuid = login_info['user']['uuid']
    team_uuid = login_info['teams'][0]['uuid']
    token = login_info['user']['token']
    return user_uuid, team_uuid, token


if __name__ == '__main__':
    user_uuid, team_uuid, token = login_ones()
    upload_file = UploadFile(user_uuid, team_uuid, token)
    upload_file.get_task()
    upload_file.upload_file()
