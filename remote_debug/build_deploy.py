import argparse
import json
import os
import subprocess
import sys
import requests


class UploadFile:
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

    def get_task(self):
        # Query for the first task
        tasks_url = f'{self.domain}/project/api/project/team/{self.team_uuid}/items/graphql?t=group-task-data'
        headers_tasks = {
            'Host': self.host,
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
        if first_task['uuid'] is None:
            raise Exception('No task found')
        self.task_uuid = first_task['uuid']

    def upload_file(self):
        # First API endpoint for obtaining upload information
        upload_url = f"{self.domain}/project/api/project/team/{self.team_uuid}/res/attachments/upload"
        # print(upload_url)
        headers = {
            'Host': self.host,
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
            print(response.text)
            raise Exception('Upload failed')
        upload_info = response.json()

        # Second API endpoint for actual file upload
        file_upload_url = upload_info['upload_url']
        file_headers = {
            'Host': self.host,
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
        print(f"文件已上传到 /data/ones/files/private/{file_info['hash']}")


def login_ones(host, domain):
    # Login API
    login_url = f'{domain}/project/api/project/auth/v2/login'
    headers_login = {
        'Host': host,
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


class ScriptError(Exception):
    pass


def exit_with_error(message):
    raise ScriptError(message)


env_info_path = os.path.join(os.path.expanduser("~"), "env_infos.json")


def comment_code():
    # Run git status and capture the output
    status_output = subprocess.getoutput('git status')

    # Check if "working tree clean" is in the output
    if "working tree clean" in status_output or "app/init.go" not in status_output:
        # If "working tree clean" is found, comment out the specified line with "github.com/bangwork/ones-anti-piracy/pkg/apis/runtime"
        with open('app/init.go', 'r') as file:
            lines = file.readlines()

        with open('app/init.go', 'w') as file:
            flag = 0
            for line in lines:
                if 'github.com/bangwork/ones-anti-piracy/pkg/apis/runtime' in line:
                    file.write('// ' + line)
                elif 'err := runtime.RegisterInstanceRuntime(db.RedisPool(), "")' in line:
                    file.write('// ' + line)
                    # 接下来的 3 行也注释掉，先标记
                    flag = 1
                elif 0 < flag < 4:
                    file.write('// ' + line)
                    flag += 1
                else:
                    file.write(line)

        print("Code commented out in app/init.go")
    else:
        print(
            "Working tree is not clean, 请手动注释 app/init.go 里的 err := runtime.RegisterInstanceRuntime 后再执行一次, "
            "不用或已经注释请忽略")


def update_ip_in_env_infos(env_name, new_ip):
    if not os.path.exists(env_info_path):
        exit_with_error("找不到 env_infos.json 文件，请确保文件存在并包含正确的环境信息")

    with open(env_info_path, "r") as json_file:
        env_infos = json.load(json_file)

    if env_name not in env_infos:
        env_infos[env_name] = {}

    env_infos[env_name]["public_ip"] = new_ip

    with open(env_info_path, "w") as json_file:
        json.dump(env_infos, json_file, indent=2)

    print(f"已更新环境 {env_name} 的 IP 为 {new_ip}")


def get_ip(env_name):
    if not os.path.exists(env_info_path):
        exit_with_error("找不到 env_infos.json 文件，请确保文件存在并包含正确的环境信息")
    with open(env_info_path, "r") as json_file:
        env_infos = json.load(json_file)
    if env_name not in env_infos or "public_ip" not in env_infos[env_name]:
        exit_with_error(f"找不到环境 {env_name} 的 IP，请手动输入")
    return env_infos[env_name]['public_ip']


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="build and deploy for remote debug.")

    # 添加位置参数
    parser.add_argument("--env_name", help="Name of the environment", required=False)
    parser.add_argument("--only-upload", action="store_true", help="Only upload bin file")

    args = parser.parse_args()

    return args


log_tips = "docker exec -i $(docker ps -q --filter 'publish=80') /bin/bash -c " \
           "'tail -f /usr/local/ones-ai-project-api/nohup.out'"
replace_bin_tips = f"sh /tmp/debug_tool/debug.sh && {log_tips}"
replace_bin_tips2 = f"sh /tmp/debug_tool/debug2.sh && {log_tips}"


def build_and_package():
    # 检查当前目录是否为项目根目录，有 go.mod 文件，或者有 vendor 目录
    if not (os.path.isfile('go.mod') or os.path.isdir('vendor')):
        exit_with_error("不是 bang-api 项目根目录，请先切换到项目根目录。")

    comment_code()

    # 编译 Go 项目
    # env={'CGO_ENABLED': '0', 'GOOS': 'linux', 'GOARCH': 'amd64'}
    # 获取当前 shell 的环境变量
    current_env = os.environ.copy()
    current_env['CGO_ENABLED'] = '0'
    current_env['GOOS'] = 'linux'
    current_env['GOARCH'] = 'amd64'
    check_result = subprocess.run(
        ['go', 'build', '-o', 'bin/ones-ai-api-core', '-gcflags', 'all=-N -l'],
        env=current_env
    )

    # 检查编译是否成功
    if check_result.returncode != 0:
        exit_with_error("Go build failed.")
    check_result = subprocess.run(['tar', '-czvf', 'bin/ones-ai-api-core.tar.gz', 'bin/ones-ai-api-core'])
    if check_result.returncode != 0:
        exit_with_error("Compression failed.")
    print("Compression and packaging successful.")
    md5_output = subprocess.getoutput('md5 bin/ones-ai-api-core')
    print(md5_output)
    # 输出压缩包绝对路径
    print("二进制已经压缩放在:", os.path.realpath('bin/ones-ai-api-core.tar.gz'))


if __name__ == '__main__':
    try:
        # 检查参数
        args = parse_command_line_args()
        # 如果未提供 IP，检查 env_infos.json 文件
        env_name = args.env_name
        if env_name is None:
            build_and_package()
            print("请手动上传 bin/ones-ai-api-core.tar.gz 到服务器，然后执行以下命令：")
            print(replace_bin_tips)
        else:
            if not args.only_upload:
                build_and_package()
            host = f"{env_name}.dev.myones.net"
            domain = f"https://{host}"
            user_uuid, team_uuid, token = login_ones(host, domain)
            if user_uuid == '' or team_uuid == '' or token == '':
                exit_with_error("登录失败")
            upload_file = UploadFile(user_uuid, team_uuid, token, host)
            upload_file.get_task()
            upload_file.upload_file()
            print(replace_bin_tips2)
    except ScriptError as e:
        print(f"Error: {e}")
        sys.exit(1)
