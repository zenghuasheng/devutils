import argparse
import json
import os
import subprocess
import sys


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
    parser.add_argument("--ip", help="remote server ip", required=False)
    parser.add_argument("--port", help="ssh port, default is 8122", required=False, default="8122")
    parser.add_argument("--only-restart", action="store_true", help="Only restart the service")
    parser.add_argument("--ssh", action="store_true", help="Show ssh connection info")
    parser.add_argument("--only-log", action="store_true", help="Only show log")

    args = parser.parse_args()

    return args


log_tips = "docker exec -i $(docker ps -q --filter 'publish=80') /bin/bash -c " \
           "'tail -f /usr/local/ones-ai-project-api/nohup.out'"
replace_bin_tips = f"sh /tmp/debug_tool/debug.sh && {log_tips}"


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
            sys.exit(0)
        ip = args.ip
        port = args.port
        if ip is None:
            ip = get_ip(env_name)
        else:
            # TODO 先测试 IP 是否可用
            update_ip_in_env_infos(env_name, ip)

        if args.ssh:
            print(f"ssh -p {port} root@{ip}")
            sys.exit(0)

        if args.only_log:
            subprocess.run(["ssh", "-p", port, f"root@{ip}", log_tips])
            sys.exit(0)

        if not args.only_restart:
            build_and_package()
            # 执行 scp 和 ssh 命令
            scp_command = f"scp -P {port} bin/ones-ai-api-core.tar.gz root@{ip}:/tmp/ones-ai-api-core.tar.gz"
            print(scp_command)
            check_result = subprocess.run(scp_command, shell=True)
            if check_result.returncode != 0:
                exit_with_error("Upload failed.")
        check_result = subprocess.run(["ssh", "-p", port, f"root@{ip}", replace_bin_tips])
        if check_result.returncode != 0:
            exit_with_error("start debug failed.")
    except ScriptError as e:
        print(f"Error: {e}")
        sys.exit(1)
