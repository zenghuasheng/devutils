import paramiko
import sys

import paramiko
import sys


def ssh_interactive_shell(host, port, username, private_key_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 使用私钥进行连接
        private_key = paramiko.RSAKey(filename=private_key_path)
        client.connect(host, port=port, username=username, pkey=private_key)
        print(f"Connected to {host}:{port} as {username}")

        # 打开一个交互式的 shell
        shell = client.invoke_shell()

        # 设置 shell 的超时时间
        shell.settimeout(0.1)

        # 读取并打印输出
        while True:
            output = shell.recv(1024).decode()
            if not output:
                break
            print(output, end='')

        # 用户输入并发送到 shell
        print("here")
        while True:
            user_input = input("Enter command (or 'exit' to quit): ")

            if user_input.lower() == 'exit':
                break

            shell.send(user_input + '\n')

            # 读取并打印输出
            while True:
                output = shell.recv(1024).decode()
                if not output:
                    break
                print(output, end='')

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ssh.py env_name")
        sys.exit(1)

    env_name = sys.argv[1]

    # 根据 env_name 获取对应的 IP 和 Port
    # 这里以示例的方式直接写死，你需要根据实际情况修改
    if env_name == "mydebug":
        host = "120.79.190.189"
        port = 8122
        username = "root"
        private_key_path = "/Users/xhs/.ssh/id_rsa"
        # command = "docker exec -it ones_dup bash"
        command = ""
    else:
        print(f"Environment '{env_name}' not found.")
        sys.exit(1)

    ssh_interactive_shell(host, port, username, private_key_path)
