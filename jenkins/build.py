import argparse
import os

import requests
from requests.auth import HTTPBasicAuth

# Jenkins 服务器信息
jenkins_url = 'https://jenkins.myones.net/'
job_name = 'ones-k3s-single-deploy/job/ones-k3s-single-deploy-start'  # 替换成你的流水线名称
username = 'zenghuasheng@ones.cn'  # 替换成你的 Jenkins 用户名


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="start machine")

    parser.add_argument("env_name", help="env name")
    api_token = os.getenv("JENKINS_API_TOKEN")

    parser.add_argument("--token", type=str, default=api_token, help="jenkins api token")

    args = parser.parse_args()
    return args


args = parse_command_line_args()

if not args.token:
    raise ValueError("请设置 JENKINS_API_TOKEN 环境变量或使用 --token 参数指定 Jenkins API Token")

if not args.env_name:
    raise ValueError("请指定环境名称")

# 参数设置
parameters = {
    'env_name': args.env_name,  # 环境名称（例如，${itemKey}）
    'notify_user_email': 'zenghuasheng@ones.cn'  # 通知用户的邮箱（例如，${notifyUserEmail}）
}

# 请求 URL
# https://jenkins.myones.net/job/ones-k3s-single-deploy/job/ones-k3s-single-deploy-start/build?delay=0sec
url = f'{jenkins_url}job/{job_name}/buildWithParameters'

# 进行 POST 请求，触发流水线
response = requests.post(url, params=parameters, auth=HTTPBasicAuth(username, args.token))

# 检查响应状态
if response.status_code == 201:
    print("流水线已成功触发!")
else:
    print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
