import argparse
import os
import subprocess
import sys
import time


class ScriptError(Exception):
    pass


def exit_with_error(message):
    raise ScriptError(message)


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="build and deploy for remote debug.")

    # 添加位置参数
    parser.add_argument("--only-restart", action="store_true", help="Only restart the service")

    args = parser.parse_args()
    return args


def get_local_debug_bin_md5(bin_name):
    # 计算本地 debug_bin 文件的 MD5 值
    result = subprocess.run(["md5", bin_name], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip().split()[-1]
    else:
        return None


def get_remote_debug_bin_md5(bin_name, ip, username):
    # 在远程服务器上计算 debug_bin 文件的 MD5 值
    result = subprocess.run(["ssh", f"{username}@{ip}", "md5sum", bin_name], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip().split()[0]
    else:
        return None


def check_sync_status(bin_name, ip, username):
    local_md5 = get_local_debug_bin_md5(bin_name)
    print(f"local_md5: {local_md5}")
    while True:
        time.sleep(1)
        remote_md5 = get_remote_debug_bin_md5(bin_name, ip, username)
        print(f"remote_md5: {remote_md5}")
        if remote_md5 and local_md5 == remote_md5:
            return True


def parse_ssh_config():
    ssh_config_path = os.path.expanduser("~/.ssh/config")
    ssh_config = {}
    with open(ssh_config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("Host "):
                current_host = line.split(" ")[1]
                parts = current_host.split("-deployment.okteto")
                ssh_config[parts[0]] = current_host
    return ssh_config


def get_service_name_from_path():
    current_path = os.getcwd()
    parts = current_path.split(os.path.sep)
    # 找到 bangwork 后的部分
    for i, part in enumerate(parts):
        if part == "bangwork":
            return "-".join(parts[i + 1:])
    return None


if __name__ == '__main__':
    try:
        print("执行这个脚本前，请确认是否执行了 okteto up 命令，以及 okteto.yaml 配置了 forward")
        # 获取当前 shell 的环境变量
        current_env = os.environ.copy()
        # 检查参数
        args = parse_command_line_args()
        service_name = get_service_name_from_path()
        if not service_name:
            exit_with_error("无法根据路径找到服务名")
        ssh_config = parse_ssh_config()
        service_path_name_map = {
            "bang-api-gomod": "project-api",
        }
        if service_name in service_path_name_map:
            service_name = service_path_name_map[service_name]
        print(f"service_name: {service_name}")
        ip = ssh_config.get(service_name)
        if not ip:
            exit_with_error("无法根据服务名找到 ssh 配置，可能还没执行 okteto up，请检查 ~/.ssh/config 文件。")
        bin_name = 'debug_bin'
        username = 'root'
        if not args.only_restart:
            # 检查当前目录是否为项目根目录，有 go.mod 文件，或者有 vendor 目录
            if not (os.path.isfile('go.mod') or os.path.isdir('vendor')):
                exit_with_error("不是项目根目录，请先切换到项目根目录。")
            # 编译 Go 项目
            current_env['CGO_ENABLED'] = '0'
            current_env['GOOS'] = 'linux'
            current_env['GOARCH'] = 'amd64'
            check_result = subprocess.run(
                ['go', 'build', '-o', bin_name, '-gcflags', 'all=-N -l'],
                env=current_env
            )

            # 检查编译是否成功
            if check_result.returncode != 0:
                exit_with_error("Go build failed.")
            print("编译完成，准备同步")
            # 检测同步状态
            check_sync_status(bin_name, ip, username)
            print("二进制已同步完成")
        # 重启
        print("正在重启服务")
        # 先杀死原来的 dlv 进程
        print("执行 pkill dlv")
        subprocess.run(["ssh", f"{username}@{ip}", "pkill dlv"])
        print("")
        # 重启服务
        subprocess.run(["ssh", f"{username}@{ip}",
                        f"/go/bin/dlv --listen=:10086 --headless=true --accept-multiclient --api-version=2 exec {bin_name}"])
    except ScriptError as e:
        print(f"Error: {e}")
        sys.exit(1)
