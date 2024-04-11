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
    parser.add_argument("--forward-port", help="本地的哪个端口转发到远程的 10086", required=False)

    args = parser.parse_args()
    return args


def check_sync_status():
    consecutive_success = 0
    while True:
        time.sleep(1)
        status_output = subprocess.run(["okteto", "status", "--info"], capture_output=True, text=True)
        status = status_output.stdout
        if "Synchronization status: 100.00%" in status:
            consecutive_success += 1
            if consecutive_success >= 2:
                return True
        else:
            consecutive_success = 0
            # print(status)


def port_forward(pod, forward_port):
    print(f"开始端口转发，将本地 {forward_port} 端口转发到远程 10086 端口")
    subprocess.Popen(
        ["kubectl", "-n", "ones", "port-forward", pod, f"{forward_port}:10086"]
    )


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


def get_debug_pod(service_name):
    # 执行 kubectl 命令并捕获输出
    result = subprocess.run(
        ["kubectl", "-n", "ones", "get", "pod"],
        capture_output=True,
        text=True
    )

    # 解析输出，找到匹配的 Pod 名称
    pod_name = None
    if result.returncode == 0:
        output = result.stdout.strip()
        lines = output.split("\n")
        for line in lines:
            if not "okteto" in line:
                continue
            if line.startswith(service_name):
                pod_name = line.split()[0]
                break

    return pod_name


if __name__ == '__main__':
    try:
        print("执行这个脚本前，请确认是否执行了 okteto up 命令")
        # 获取当前 shell 的环境变量
        current_env = os.environ.copy()
        # 检查参数
        args = parse_command_line_args()
        service_name = get_service_name_from_path()
        if not service_name:
            exit_with_error("没传 IP，也无法根据路径找到服务名，请检查参数")
        ssh_config = parse_ssh_config()
        service_path_name_map = {
            "bang-api-gomod": "project-api",
        }
        if service_name in service_path_name_map:
            service_name = service_path_name_map[service_name]
        print(f"service_name: {service_name}")
        ip = ssh_config.get(service_name)
        if not ip:
            exit_with_error("无法根据服务名找到 ssh 配置，请检查 ~/.ssh/config 文件。")
        bin_name = 'debug_bin'
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
            check_sync_status()
            print("二进制已同步完成")
        # 重启
        print("正在重启服务，重启后即可点击 Goland debug 进行远程调试")
        # 先杀死原来的 dlv 进程
        username = 'root'
        print("执行 pkill dlv")
        subprocess.run(["ssh", f"{username}@{ip}", "pkill dlv"])
        print("\n")
        # 重新建立端口转发
        # kubectl -n ones port-forward project-api-deployment-okteto-6f58dfc8b8-ffj4z 10086:10086
        pod = get_debug_pod(service_name)
        print(f"自动找到开发容器：{pod}")
        forward_port = args.forward_port
        if not forward_port:
            # 根据服务名找到对应的端口
            service_port_map = {
                "project-api": 10086,
                "ones-project-api": 10087,
                "audit-log-sync": 10088,
            }
            forward_port = service_port_map.get(service_name)
        if not forward_port:
            exit_with_error("无法根据服务名找到对应转发的端口，请传入 forward-port 参数。")
        port_forward(pod, forward_port)
        # 重启服务
        subprocess.run(["ssh", f"{username}@{ip}",
                        f"/go/bin/dlv --listen=:10086 --headless=true --accept-multiclient --api-version=2 exec {bin_name}"])
    except ScriptError as e:
        print(f"Error: {e}")
        sys.exit(1)
