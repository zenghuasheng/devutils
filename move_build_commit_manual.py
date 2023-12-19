import os
import subprocess
import sys

if __name__ == '__main__':
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("缺少 commit 信息")
        sys.exit(1)

    message = sys.argv[1]
    main_dir = '/Users/xhs/go/src/github.com/bangwork/bang-api-gomod'
    os.chdir(main_dir)
    build_command = '/Users/xhs/go1.17/go1.20.1/bin/go build  -o /tmp/'

    # 执行构建命令
    build_result = subprocess.run(build_command, shell=True, check=False)

    # 检查构建结果
    if build_result.returncode == 0:
        # 构建成功，自动提交修改
        # git_commit_command = f'git add . && git commit -m ""'
        git_commit_command = f"git add . && git commit -m \"{message}\""
        commit_result = subprocess.run(git_commit_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if commit_result.returncode != 0 and "nothing to commit, working tree clean" not in commit_result.stdout.decode("utf-8"):
            print(f'Commit failed, Please check the modifications.')
            exit(1)
    else:
        print(f'Build failed, Please check the modifications.')