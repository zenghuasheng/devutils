import argparse
import os
import subprocess


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Script to move go file or directory.")
    parser.add_argument("source", help="")
    parser.add_argument("target", help="")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # dir 需要 main_dir 回到上一级目录 + repo_dir
    args = parse_command_line_args()
    find_dir = "/Users/xhs/go/src/github.com/bangwork/bang-api-gomod"
    # 去掉 source 和 target 两边的 "
    args.source = args.source.strip('"')
    args.target = args.target.strip('"')
    # TODO
    replace_commands = [
        f"find {find_dir} -type f -name '*.go' -exec sed -i '' 's|\"{args.source}\"|\"{args.target}\"|g' {{}} +",
        f"find {find_dir} -type f -name '*.go' -exec sed -i '' 's|\"{args.source}/|\"{args.target}/|g' {{}} +",
    ]
    for replace_command in replace_commands:
        print(replace_command)
        subprocess.run(replace_command, shell=True)
