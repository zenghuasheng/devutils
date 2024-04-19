import argparse
import subprocess

import yaml
import os


def adjust_kubeconfig(config_file, target_path, new_ip):
    if new_ip is None:
        print("No new IP address provided, skip adjusting kubeconfig")
        return
    # 读取 YAML 文件内容
    with open(config_file, 'r') as f:
        kubeconfig = yaml.safe_load(f)

    # 调整 certificate-authority-data 部分为 insecure-skip-tls-verify: true
    for cluster in kubeconfig['clusters']:
        cluster['cluster']['insecure-skip-tls-verify'] = True
        del cluster['cluster']['certificate-authority-data']

        # 替换 server 中的 IP
        cluster['cluster']['server'] = cluster['cluster']['server'].replace('127.0.0.1', new_ip)

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

        loop_check_service_health $@
    """

    # 写回原文件
    with open(file_path, 'w') as f:
        yaml.dump(config_data, f)

    print("api-common-config.yaml 文件已修改")


def replace_esn_shell():
    po = get_k8s_pod()
    # kubectl cp ones-installer/installer-api-5fbd76fffb-pmf5m:/data/ones/ones-ai-k8s/apps/ones/v1/base/k8s-v1.16/api-common-config.yaml ./api-common-config.yaml
    cmd = f"kubectl cp ones-installer/{po}:/data/ones/ones-ai-k8s/apps/ones/v1/base/k8s-v1.16/api-common-config.yaml " \
          f"./api-common-config.yaml "
    os.system(cmd)
    # 修改 api-common-config.yaml 文件
    modify_api_common_config("./api-common-config.yaml")
    # 复制回去
    cmd = f"kubectl cp ./api-common-config.yaml ones-installer/{po}:/data/ones/ones-ai-k8s/apps/ones/v1/base/k8s-v1.16/api-common-config.yaml"
    os.system(cmd)
    # 在容器执行 make setup-ones
    cmd = f"kubectl exec -it {po} -n ones-installer -- make setup-ones"
    os.system(cmd)
    # 删除 api-common-config.yaml 文件
    os.system("rm ./api-common-config.yaml")


def get_available_envs(config_dir):
    available_envs = []
    for filename in os.listdir(config_dir):
        if filename.endswith(".yaml"):
            env_name = os.path.splitext(filename)[0]
            available_envs.append(env_name)
    return available_envs


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Adjust kubeconfig file")
    parser.add_argument("env_name", nargs="?", type=str, help="env_name")
    parser.add_argument("--ip", type=str, required=False, help="IP address")
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


def copy_remote_kubeconfig(remote_host, remote_path, local_path):
    command = ["rsync", "-a", f"{remote_host}:{remote_path}", local_path]
    try:
        subprocess.run(command, check=True)
        print("Kubeconfig files copied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("Failed to copy kubeconfig files.")


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


kubeconfig_dir = "/Users/xhs/kubeconfig/"

if __name__ == "__main__":
    remote_host = "root@114.215.111.84"
    remote_path = "/root/kubeconfig"
    local_path = "/Users/xhs/kubeconfig_remote/"
    copy_remote_kubeconfig(remote_host, remote_path, local_path)
    remote_env_configs = get_env_configs(os.path.join(local_path, os.path.basename(remote_path)))
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
    args = parse_command_line_args()

    config_path = f"/Users/xhs/kubeconfig/{args.env_name}.yaml"
    adjust_kubeconfig(config_path, config_path, args.ip)
    copy_config(config_path)
    verify_kubeconfig(args.ip)
    replace_esn_shell()
    print("环境已准备好，请到项目下执行 okteto up --log-level=debug")
