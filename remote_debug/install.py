#!/usr/bin/env python
import argparse
import os
import subprocess
import sys


class ScriptError(Exception):
    pass


def exit_with_error(message):
    raise ScriptError(message)


def download_debug_tool():
    debug_tool_url = "http://112.74.98.121:8080/debug_tool.tar.gz"
    debug_tool_path = "/tmp/debug_tool.tar.gz"

    if os.path.isfile(debug_tool_path):
        exit_with_error("debug_tool.tar.gz already exists. If you want to update, please remove the existing one.")

    subprocess.call(["curl", "-o", debug_tool_path, debug_tool_url])


def extract_debug_tool():
    subprocess.call(["tar", "-zxvf", "/tmp/debug_tool.tar.gz", "-C", "/tmp"])


def replace_container():
    subprocess.call(["sh", "/tmp/debug_tool/replace_container.sh"])


def configure_ssh(public_key, port):
    authorized_keys_path = os.path.expanduser("~/.ssh/authorized_keys")

    with open(authorized_keys_path, "a") as auth_keys_file:
        auth_keys_file.write(public_key + "\n")

    sed_command = 'sed -i -e "/^#Port 22/a Port {0}" -e "s/^#Port 22/Port 22/" /etc/ssh/sshd_config'.format(port)
    subprocess.call(sed_command, shell=True)

    subprocess.call(["systemctl", "restart", "sshd"])


def get_local_ip():
    ip_address = subprocess.check_output(["curl", "-s", "ip.me"]).strip()
    return ip_address


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="install debug tool.")
    parser.add_argument("public_key", help="public key used for ssh")
    parser.add_argument("--port", help="ssh listen port, default is 8122, your can use 9200, 9001, 9002, 8123",
                        required=False, default="8122")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    try:
        os.chdir("/tmp")
        args = parse_command_line_args()
        public_key = args.public_key
        port = args.port

        download_debug_tool()
        extract_debug_tool()
        replace_container()
        configure_ssh(public_key, port)

        ip_address = get_local_ip()

        print("The tool package has been downloaded to the /tmp/debug_tool directory.")
        print("Please download the compile and package script locally and execute it.")
        print("Download command: ")
        print("curl -o build_deploy.py http://112.74.98.121:8080/build_deploy.py")
        print("Execute command: ")
        print("python build_deploy.py replace_your_env_name --ip {} --port {}".format(ip_address, port))
    except ScriptError as e:
        print("Error: {0}".format(e))
        sys.exit(1)
