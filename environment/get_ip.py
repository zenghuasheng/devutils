import argparse
import yaml
import sys
import requests


class Ones:
    domain = ''
    host = ''
    user_uuid = ''
    team_uuid = ''
    token = ''
    cookies_next_request = {}
    task_uuid = ''

    def __init__(self, user_uuid, team_uuid, token, host):
        self.host = host
        self.domain = f"https://{host}"
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

    def get_task(self, task_name):
        # Query for the first task
        tasks_url = f'{self.domain}/project/api/project/team/{self.team_uuid}/items/graphql?t=group-task-data'
        headers_tasks = {
            'Host': self.host,
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            # Add other headers as needed
        }
        data_tasks = {
            'query': '{\n    buckets (\n      groupBy: $groupBy\n      orderBy: $groupOrderBy\n      pagination: $pagination\n      filter: $groupFilter\n    ) {\n      key\n      \n      tasks (\n        filterGroup: $filterGroup\n        orderBy: $orderBy\n        limit: 1000\n        \n      includeAncestors:{pathField:\"path\"}\n      orderByPath: \"path\"\n    \n      ) {\n        \n    key\n    name\ndescriptionText\n        description\n    uuid\n    serverUpdateStamp\n    number\n    path\n    subTaskCount\n    subTaskDoneCount\n    position\n    status {\n      uuid\n      name\n      category\n    }\n    deadline(unit: ONESDATE)\n    subTasks {\n      uuid\n    }\n    issueType {\n      uuid\n      manhourStatisticMode\n    }\n    subIssueType {\n      uuid\n      manhourStatisticMode\n    }\n    project {\n      uuid\n    }\n    parent {\n      uuid\n    }\n    estimatedHours\n    remainingManhour\n    totalEstimatedHours\n    totalRemainingHours\n    issueTypeScope {\n      uuid\n    }\n\n        \n      importantField{\n        bgColor\n        color\n        name\n        value\n        fieldUUID\n      }\n      issueTypeScope {\n        uuid\n        currentLayout {\n          uuid\n          hasViewManhourTab\n        }\n      }\n    \n      }\n      pageInfo {\n        count\n        totalCount\n        startPos\n        startCursor\n        endPos\n        endCursor\n        hasNextPage\n        preciseCount\n      }\n    }\n    \n  }',
            # Add the GraphQL query here
            'variables': {
                'groupBy': {'tasks': {}},
                'groupOrderBy': None,
                'orderBy': {'position': 'ASC', 'createTime': 'DESC'},
                'filterGroup': [
                    {
                        'name_equal': task_name,
                    }
                ],
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
        if first_task['uuid'] is None:
            raise Exception('No task found')
        self.task_uuid = first_task['uuid']
        return first_task


def login_ones(host, domain, username, password):
    # Login API
    login_url = f'{domain}/project/api/project/auth/v2/login'
    headers_login = {
        'Host': host,
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        # Add other headers as needed
    }
    data_login = {
        'password': password,
        'captcha': '',
        'email': username,
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


def update_kubeconfig(config_path, name, ip):
    # Read the Kubernetes configuration file
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Find the cluster with the given name and update its server address
    for cluster in config['clusters']:
        if cluster['name'] == name:
            cluster['cluster']['server'] = f'https://{ip}:6443'
            break

    # Write the updated configuration back to the file
    with open(config_path, 'w') as file:
        yaml.dump(config, file)

    print(f"Updated cluster '{name}' server address to 'https://{ip}:6443'.")


class ScriptError(Exception):
    pass


def exit_with_error(message):
    raise ScriptError(message)


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="get k3s machine ip")

    # 添加位置参数
    parser.add_argument("env_name", help="Name of the environment, for example p1109-k3s-2")
    # config_path = '/Users/xhs/kubeconfig/config'
    parser.add_argument("--config-path", help="Path to the Kubernetes configuration file", required=False,
                        default='/Users/xhs/kubeconfig/config')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    try:
        # 检查参数
        args = parse_command_line_args()
        env_name = args.env_name
        host = f"{env_name}.k3s-dev.myones.net"
        domain = f"https://{host}"
        username = "blue@ones.cn"
        password = "Test1234@"
        user_uuid, team_uuid, token = login_ones(host, domain, username, password)
        if user_uuid == '' or team_uuid == '' or token == '':
            exit_with_error("登录失败")
        print(f"登录成功: user_uuid: {user_uuid}, team_uuid: {team_uuid}, token: {token}")
        upload_file = Ones(user_uuid, team_uuid, token, host)
        task_name = "k3s_machine_ip"
        task = upload_file.get_task(task_name)
        # task['descriptionText']
        print(f"ip: {task['descriptionText']}")
        # Example usage
        if task['descriptionText'] == '':
            exit_with_error("获取 ip 失败")
        update_kubeconfig(args.config_path, env_name, task['descriptionText'])
    except ScriptError as e:
        print(f"Error: {e}")
        sys.exit(1)
