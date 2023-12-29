import argparse
import os
import subprocess


def move_dir(main_dir, go_path, source, target):
    os.chdir(main_dir)
    print(f'Moving {source} to {target}')
    target_file = os.path.join(main_dir, target)
    # 判断 source 是否存在
    if not os.path.exists(os.path.join(main_dir, source)):
        print(f'Package "{source}" not exists')
        exit(1)

    # 判断 go_path 是否存在
    if not os.path.exists(go_path):
        print(f'go_path "{go_path}" not exists')
        exit(1)

    # 创建父级目录
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    # 移动子目录
    move_command = " ".join(['mv', os.path.join(main_dir, source), os.path.dirname(target_file)])
    print(move_command)
    move_result = subprocess.run(move_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if move_result.returncode != 0:
        print(f'Move failed, Please check the modifications.')
        exit(1)

    # 替换 import
    # find /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/app/services/common/organization -type f -name '*.go' -exec sed -i '' 's|"github\.com/bangwork/bang-api/app/models/user"|"github\.com/bangwork/bang-api/biz-common/user/models/user"|g' {} +
    replace_commands = [
        f"find {main_dir} -type f -name '*.go' -exec sed -i '' 's|\"github\.com/bangwork/bang-api/{source}\"|\"github\.com/bangwork/bang-api/{target}\"|g' {{}} +",
        f"find {main_dir} -type f -name '*.go' -exec sed -i '' 's|\"github\.com/bangwork/bang-api/{source}/|\"github\.com/bangwork/bang-api/{target}/|g' {{}} +",
    ]
    for replace_command in replace_commands:
        print(replace_command)
        subprocess.run(replace_command, shell=True)

    # 执行构建命令
    build_command = f'{go_path} build  -o /tmp/'
    build_result = subprocess.run(build_command, shell=True, check=False)

    # 检查构建结果
    if build_result.returncode == 0:
        # 构建成功，自动提交修改
        git_commit_command = f'git add . && git commit -m "move {source} to {target}"'
        commit_result = subprocess.run(git_commit_command, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        if commit_result.returncode != 0 and "nothing to commit, working tree clean" not in commit_result.stdout.decode(
                "utf-8"):
            print(f'Commit failed, Please check the modifications.')
            exit(1)
    else:
        print(f'Build failed, Please check the modifications.')
        exit(1)


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="move go package.")

    # 添加位置参数
    parser.add_argument("source", help="relative path of source package, like app/services/common/organization")
    parser.add_argument("target", help="relative path of target package, like biz-common/organization")
    parser.add_argument("--main_dir", help="directory path of bang-api", required=False,
                        default='/Users/xhs/go/src/github.com/bangwork/bang-api-gomod')
    # go path
    parser.add_argument("--go_path", help="go path", required=False, default='/Users/xhs/go1.17/go1.20.1/bin/go')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_command_line_args()
    move_dir(args.main_dir, args.go_path, args.source, args.target)
