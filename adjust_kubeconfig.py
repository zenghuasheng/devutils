import argparse
import subprocess

import requests
import yaml
import os


def adjust_kubeconfig(config_file, target_path, new_ip):
    if new_ip is None:
        print("No new IP address provided, skip adjusting kubeconfig")
        return
    # 读取 YAML 文件内容
    # 判断 config_file 是否存在
    if not os.path.exists(config_file):
        raise Exception(f"File not found: {config_file}")
    with open(config_file, 'r') as f:
        kubeconfig = yaml.safe_load(f)

    # 调整 certificate-authority-data 部分为 insecure-skip-tls-verify: true
    for cluster in kubeconfig['clusters']:
        cluster['cluster']['insecure-skip-tls-verify'] = True
        if 'certificate-authority-data' in cluster['cluster']:
            del cluster['cluster']['certificate-authority-data']

        # 替换 server 中的 IP
        cluster['cluster']['server'] = f"https://{new_ip}:6443"

    # 写入新的 YAML 文件
    with open(target_path, 'w') as f:
        yaml.dump(kubeconfig, f, default_flow_style=False)

    print(f"Kubeconfig adjusted and saved as {target_path}")


def copy_config(config_path):
    # 拷贝到同目录的 config 文件
    config_dir = os.path.dirname(config_path)
    os.system(f"cp {config_path} {config_dir}/config")


def verify_kubeconfig(ip):
    if ip is None:
        cmd = "kubectl cluster-info"
    else:
        cmd = f"kubectl cluster-info | grep {ip}"
    result = os.system(cmd)
    if result != 0:
        raise Exception("Kubeconfig verification failed")


def get_k8s_pod():
    # 执行 kubectl 命令并捕获输出
    # kubectl -n ones-installer get pod | grep installer-api
    cmd = "kubectl -n ones-installer get pod | grep installer-api"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        # installer-api-5fd55cc66c-l2pw4   1/1     Running   0             10m
        return result.stdout.split()[0]
    else:
        raise Exception("Failed to get pod name")


def modify_api_common_config(file_path):
    with open(file_path, 'r') as f:
        config_data = yaml.safe_load(f)

    # 修改 check_service_health 内容
    config_data['spec']['gomplate']['templates']['ones-esn-sidecar-sh'] = """
        #!/bin/bash

        retry_interval=30
        retry_threshold=4

        # 检查服务是否健康：
        #   尝试3次, 每次间隔20秒，检查端口是否监听。
        #   如果连续3次检查通过，则返回0，否则返回1

        check_service_health() {
          echo 0
          return
        }


        # 循环检查服务是否健康，如果检查不通过的次数超过阈值，则删除pod
        loop_check_service_health() {
          local port="$1"
          local count=0
          while true; do
            status=$(check_service_health $port)
            echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S%z') service_status: " $status ", retries_count: " $count
            if [ "$status" == 1 ]; then
              count=$((count + 1))
            else
              count=0
            fi
            if [ $count -ge $retry_threshold ]; then
              echo "[WARN] $(date '+%Y-%m-%d %H:%M:%S%z') service is not healthy, delete pod"
              kubectl -n $POD_NAMESPACE delete pods $POD_NAME
            fi
            sleep $retry_interval
          done
        }


        {{ if eq $config.isDev "true" }}
        sleep infinity
        {{ else }}
        loop_check_service_health $@
        {{ end }}
"""

    # 写回原文件
    with open(file_path, 'w') as f:
        yaml.dump(config_data, f)

    print("api-common-config.yaml 文件已修改")


def replace_esn_shell():
    po = get_k8s_pod()
    # kubectl cp ones-installer/installer-api-5fbd76fffb-pmf5m:/data/ones/ones-ai-k8s/apps/ones/v1/base/k8s-v1.16/api-common-config.yaml ./api-common-config.yaml
    cmd = f"kubectl cp ones-installer/{po}:/data/ones/ones-ai-k8s/apps/ones/v1/base/k8s-v1.16/api-common-config.yaml " \
          f"/Users/xhs/go_workspace/aidemo/api-common-config.yaml "
    os.system(cmd)
    cmd = f"kubectl cp ones-installer/{po}:/data/ones/ones-ai-k8s/apps/ones/v1/base/k8s-v1.16/api-common-config.yaml " \
          f"/Users/xhs/go_workspace/aidemo/api-common-config_bak.yaml "
    os.system(cmd)
    # 修改 api-common-config.yaml 文件
    modify_api_common_config("/Users/xhs/go_workspace/aidemo/api-common-config.yaml")
    # 复制回去
    cmd = f"kubectl cp /Users/xhs/go_workspace/aidemo/api-common-config.yaml ones-installer/{po}:/data/ones/ones-ai-k8s/apps/ones/v1/base/k8s-v1.16/api-common-config.yaml"
    os.system(cmd)
    # 在容器执行 make setup-ones
    cmd = f"kubectl exec -it {po} -n ones-installer -- make setup-ones"
    os.system(cmd)
    # 删除 api-common-config.yaml 文件
    os.system("rm /Users/xhs/go_workspace/aidemo/api-common-config.yaml")


def get_available_envs(config_dir):
    available_envs = []
    for filename in os.listdir(config_dir):
        if filename.endswith(".yaml"):
            env_name = os.path.splitext(filename)[0]
            available_envs.append(env_name)
    return available_envs


def parse_command_line_args(kubeconfig_dir):
    parser = argparse.ArgumentParser(description="Adjust kubeconfig file")
    parser.add_argument("env_name", nargs="?", type=str, help="env_name")
    parser.add_argument("--ip", type=str, required=False, help="IP address")
    parser.add_argument("--only-connect", action="store_true", help="Only connect to the environment")
    # 从远程获取
    parser.add_argument("--remote", action="store_true", help="Get IP address from remote")
    args = parser.parse_args()

    if not args.env_name:
        available_envs = get_available_envs(kubeconfig_dir)
        print("Available environments:")
        for env in available_envs:
            print(f"- {env}")
        exit()

    return args


# def copy_remote_kubeconfig(remote_path, local_path):
# remote_kubeconfig_path = os.getenv("REMOTE_KUBECONFIG_PATH")
#     remote_host = os.getenv("SYNC_KUBECONFIG_HOST")
#     command = ["rsync", "-a", f"{remote_host}:{remote_path}", local_path]
#     subprocess.run(command, check=True)
#     print("Kubeconfig files copied successfully.")

def copy_remote_kubeconfig(local_path):
    auth_id = os.getenv("THINK_ID")
    if not auth_id:
        print("Please set THINK_ID")
        exit(1)
    url = f"http://task.xiaohuasheng.cc/api/think?id={auth_id}&page=1&search="
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'http://task.xiaohuasheng.cc/',
    }
    response = requests.get(url, headers=headers, verify=False)
    json_data = response.json()
    # 遍历 list，找出 name: 开头的记录
    kube_configs = {}
    for item in json_data['data']['list']:
        if not item['content'].startswith("name:"):
            continue
        contentParts = item['content'].split('\n')
        namePart = contentParts[0]
        ipPart = contentParts[1]
        configPart = contentParts[2:]
        name = namePart.split(":")[1].strip()
        ip = ipPart.split(":")[1].strip()
        # 如果有相同名字的，取 item['create_time'] 较大的一个
        if name not in kube_configs or item['create_time'] > kube_configs[name]['create_time']:
            kube_configs[name] = {
                "id": item['id'],
                "ip": ip,
                "config": "\n".join(configPart),
                "create_time": item['create_time']
            }
    # 遍历 kube_configs，写入 local_path
    # 120.79.159.211_p1109-k3s-5
    for name, config in kube_configs.items():
        with open(f"{local_path}/{config['ip']}_{name}", 'w') as f:
            f.write(config['config'])
            print(f"Kubeconfig file {config['ip']}_{name} saved to {local_path}")
            # 删除远程记录
            delete_remote_kubeconfig(auth_id, config['id'])
    print("Kubeconfig files copied successfully.")


def delete_remote_kubeconfig(auth_id, think_id):
    url = f"http://task.xiaohuasheng.cc/api/think?id={auth_id}&think_id={think_id}"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'http://task.xiaohuasheng.cc',
        'Referer': 'http://task.xiaohuasheng.cc/',
    }
    response = requests.delete(url, headers=headers, verify=False)
    print("Kubeconfig files deleted successfully.")


def get_env_configs(directory, need_split=True):
    env_configs = {}
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if need_split:
                ip, env_name = filename.split("_")
            else:
                ip, env_name = None, filename
            env_name = env_name.split(".")[0]  # 去掉文件扩展名
            mtime = os.path.getmtime(filepath)
            if env_name not in env_configs or mtime > env_configs[env_name][0]:
                env_configs[env_name] = [mtime, filepath, ip]
    return env_configs


def get_server_public_ip(url):
    try:
        # 发送 HTTP GET 请求
        # 好像没用呀，因为 504 的时候不返回 IP
        response = requests.get(url)

        server_public_ip = response.headers.get('X-Server-Public-Ip')
        if server_public_ip:
            print(f"Server public IP: {server_public_ip}")
            return server_public_ip
        else:
            print("X-Server-Public-Ip not found in response headers.")
    except Exception as e:
        print(f"Error occurred: {e}")


# 目前我是用了自己的服务器存储 kubeconfig 文件
# 如果IP变了，需要在 jumpserver 同步
# scp -o StrictHostKeyChecking=no ~/.kube/config root@your_ip:/root/kubeconfig/$(curl -s ip.me)_p1103-k3s-2
if __name__ == "__main__":
    kubeconfig_dir = os.getenv("KUBECONFIG_DIR")
    local_kubeconfig_path = os.getenv("LOCAL_KUBECONFIG_PATH")
    # 如果读不到，退出
    if not kubeconfig_dir or not local_kubeconfig_path:
        print('''Please set KUBECONFIG_DIR, REMOTE_KUBECONFIG_PATH and LOCAL_KUBECONFIG_PATH
export KUBECONFIG_DIR=/Users/xhs/kubeconfig/
export REMOTE_KUBECONFIG_PATH=/root/kubeconfig
export LOCAL_KUBECONFIG_PATH=/Users/xhs/kubeconfig_remote/
        ''')
        exit(1)
    copy_remote_kubeconfig(local_kubeconfig_path)
    remote_env_configs = get_env_configs(local_kubeconfig_path)
    local_env_configs = get_env_configs(kubeconfig_dir, need_split=False)
    for env_name, config_info in remote_env_configs.items():
        # 取出本地的
        local_config_info = local_env_configs.get(env_name)
        # 如果本地为空或者远程的更新时间大于本地的，就拷贝过来
        if not local_config_info or config_info[0] > local_config_info[0]:
            target_path = os.path.join(kubeconfig_dir, f"{env_name}.yaml")
            if local_config_info:
                target_path = local_config_info[1]
            adjust_kubeconfig(config_info[1], target_path, config_info[2])
            print(f"{env_name} updated")
        else:
            print(f"{env_name} is up to date, skip updating")
    args = parse_command_line_args(kubeconfig_dir)

    config_path = f"/Users/xhs/kubeconfig/{args.env_name}.yaml"
    new_ip = None
    if args.ip:
        new_ip = args.ip
    # else:
    #     new_ip = get_server_public_ip(f"https://{args.env_name}.k3s-dev.myones.net")
    adjust_kubeconfig(config_path, config_path, new_ip)
    copy_config(config_path)
    verify_kubeconfig(new_ip)
    if not args.only_connect:
        replace_esn_shell()
        after_adjust_hook = os.getenv("AFTER_ADJUST_HOOK")
        if after_adjust_hook:
            print(f"Running after adjust hook: {after_adjust_hook}")
            os.system(after_adjust_hook)
    print("环境已准备好，请到项目下执行 okteto up --log-level=debug")
