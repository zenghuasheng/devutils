import json
import os
import subprocess
import sys

env_info_path = os.path.join(os.path.expanduser("~"), "env_infos.json")

def comment_code():
    # Run git status and capture the output
    status_output = subprocess.getoutput('git status')

    # Check if "working tree clean" is in the output
    if "working tree clean" in status_output:
        # If "working tree clean" is found, comment out the specified line with "github.com/bangwork/ones-anti-piracy/pkg/apis/runtime"
        with open('app/init.go', 'r') as file:
            lines = file.readlines()

        with open('app/init.go', 'w') as file:
            for line in lines:
                if 'github.com/bangwork/ones-anti-piracy/pkg/apis/runtime' in line:
                    file.write('// ' + line)
                elif 'err := runtime.RegisterInstanceRuntime(db.RedisPool(), "")' in line:
                    file.write('// ' + line)
                else:
                    file.write(line)

        print("Code commented out in app/init.go")
    else:
        print(
            "Working tree is not clean, 请手动注释 app/init.go 里的 err := runtime.RegisterInstanceRuntime 后再执行一次, "
            "不用或已经注释请忽略")


def update_ip_in_env_infos(env_name, new_ip):
    if not os.path.exists(env_info_path):
        print("找不到 env_infos.json 文件，请确保文件存在并包含正确的环境信息")
        exit(1)

    with open("env_infos.json", "r") as json_file:
        env_infos = json.load(json_file)

    if env_name not in env_infos or "public_ip" not in env_infos[env_name]:
        print(f"找不到环境 {env_name} 的 IP，请手动输入")
        env_infos[env_name] = {"public_ip": input("请输入 IP: ")}

    env_infos[env_name]["public_ip"] = new_ip

    with open("env_infos.json", "w") as json_file:
        json.dump(env_infos, json_file, indent=2)

    print(f"已更新环境 {env_name} 的 IP 为 {new_ip}")


def get_ip(env_name):
    if not os.path.exists(env_info_path):
        print("找不到 env_infos.json 文件，请确保文件存在并包含正确的环境信息")
        exit(1)
    with open("env_infos.json", "r") as json_file:
        env_infos = json.load(json_file)
    if env_name not in env_infos or "public_ip" not in env_infos[env_name]:
        print(f"找不到环境 {env_name} 的 IP，请手动输入")
    return env_infos[env_name]['public_ip']


if __name__ == '__main__':
    # 检查参数
    if len(sys.argv) < 2:
        print("请提供环境名称参数")
        exit(1)

    env_name = sys.argv[1]
    ip = sys.argv[2] if len(sys.argv) > 2 else None

    # 如果未提供 IP，检查 env_infos.json 文件
    if ip is None:
        ip = get_ip(env_name)
    else:
        update_ip_in_env_infos(env_name, ip)

    # 执行 scp 和 ssh 命令
    subprocess.run(["scp", "-P", "18443", "bin/ones-ai-api-core.tar.gz", f"root@{ip}:/tmp/ones-ai-api-core.tar.gz"])
    subprocess.run(["ssh", "-p", "18443", f"root@{ip}",
                    "sh /tmp/debug_tool/debug.sh && docker exec -i $(docker ps -q --filter 'publish=80') /bin/bash -c 'tail -f /usr/local/ones-ai-project-api/nohup.out'"])
    # 检查当前目录是否为项目根目录，有 go.mod 文件，或者有 vendor 目录
    if not (os.path.isfile('go.mod') or os.path.isdir('vendor')):
        print("不是 bang-api 项目根目录，请先切换到项目根目录。")
        exit(1)

    comment_code()

    # 编译 Go 项目
    check_result = subprocess.run(
        ['CGO_ENABLED=0', 'GOOS=linux', 'GOARCH=amd64', 'go', 'build', '-o', 'bin/ones-ai-api-core', '-gcflags',
         'all=-N -l'])

    # 检查编译是否成功
    if check_result.returncode != 0:
        print("Go build failed.")
        exit(1)
    check_result = subprocess.run(['tar', '-czvf', 'bin/ones-ai-api-core.tar.gz', 'bin/ones-ai-api-core'])
    if check_result.returncode != 0:
        print("Compression failed.")
        exit(1)
    print("Compression and packaging successful.")
    md5_output = subprocess.getoutput('md5 bin/ones-ai-api-core')
    print(md5_output)
    # 输出压缩包绝对路径
    print("二进制已经压缩放在:", os.path.realpath('bin/ones-ai-api-core.tar.gz'))
    check_result = subprocess.run(['scp', '-P', '18443', 'bin/ones-ai-api-core.tar.gz',
                                   'root@47.107.52.182:/tmp/ones-ai-api-core.tar.gz'])
    if check_result.returncode != 0:
        print("Upload failed.")
        exit(1)
    check_result = subprocess.run(['ssh', '-p', '18443', 'root@47.107.52.182', "sh /tmp/debug_tool/debug.sh"])
    if check_result.returncode != 0:
        print("重启失败")
        exit(1)
    # docker exec -i $(docker ps -q --filter 'publish=80') /bin/bash -c 'tail -f /usr/local/ones-ai-project-api/nohup.out'
