# curl -o install.py http://112.74.98.121:8080/debug_tool/install.py && python install.py
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

    subprocess.run(["curl", "-o", debug_tool_path, debug_tool_url])


def extract_debug_tool():
    subprocess.run(["tar", "-zxvf", "/tmp/debug_tool.tar.gz"], cwd="/tmp")


def replace_container():
    subprocess.run(["sh", "/tmp/debug_tool/replace_container.sh"])


def configure_ssh(public_key):
    authorized_keys_path = os.path.expanduser("~/.ssh/authorized_keys")

    with open(authorized_keys_path, "a") as auth_keys_file:
        auth_keys_file.write(public_key + "\n")

    subprocess.run(["sed", "-i", "-e", "/^#Port 22/a Port 18443", "-e", "s/^#Port 22/Port 22/", "/etc/ssh/sshd_config"])

    subprocess.run(["systemctl", "restart", "sshd"])


def get_local_ip():
    ip_address = subprocess.getoutput("curl -s ip.me").strip()
    return ip_address


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="install debug tool.")

    parser.add_argument("public_key", help="public key used for ssh")
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    try:
        os.chdir("/tmp")
        args = parse_command_line_args()
        public_key = args.public_key

        download_debug_tool()
        extract_debug_tool()
        replace_container()

        configure_ssh(public_key)

        ip_address = get_local_ip()

        print(f"The tool package has been downloaded to the /tmp/debug_tool directory. "
              f"Please download the compile and package script locally and execute it.")
        print(f"Download command: ")
        print(f"curl -o build_deploy.py http://112.74.98.121:8080/build_deploy.py")
    except ScriptError as e:
        print(f"Error: {e}")
    sys.exit(1)
