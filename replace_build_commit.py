import os
import subprocess

# 定义目标目录
main_dir = '/Users/xhs/go/src/github.com/bangwork/project-api'
target_directory = main_dir + '/app/controllers'


def replace_build_commit(subdir, f):
    # 构建完整的目录路径
    current_file = os.path.join(subdir, f)
    # 检查目录下的文件是否包含 'github.com/bangwork/project-lib'
    check_command = f'grep -r -q "github\.com\/bangwork\/project-lib" {current_file}'
    check_result = subprocess.run(check_command, shell=True)

    if check_result.returncode == 0:
        print(f'Directory {current_file} already contains "github.com/bangwork/project-lib". Skipping...')
        return

    # 构建查找并替换的 sed 命令
    sed_command = f'find {current_file} -type f -name "*.go" -exec sed -i \'\' ' \
                  f'\'s/github\.com\/bangwork\/project-api/github\.com\/bangwork\/project-lib/g\' {{}} +'

    # 执行 sed 命令
    print(sed_command)
    sed_result = subprocess.run(sed_command, shell=True, check=True)
    if sed_result.returncode != 0:
        print(f'Sed failed for directory: {current_file}. Please check the modifications.')
        exit(1)

    # 回到主目录并执行 go build
    os.chdir(main_dir)
    build_command = '/Users/xhs/go1.17/go1.20.1/bin/go build  -o /tmp/'

    # 执行构建命令
    build_result = subprocess.run(build_command, shell=True, check=False)

    # 检查构建结果
    if build_result.returncode == 0:
        # 构建成功，自动提交修改
        # git_commit_command = f'git add . && git commit -m ""'
        git_commit_command = f"git add . && git commit -m \"{current_file}\""
        commit_result = subprocess.run(git_commit_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if commit_result.returncode != 0 and "nothing to commit, working tree clean" not in commit_result.stdout.decode("utf-8"):
            print(f'Commit failed for directory: {current_file}. Please check the modifications.')
            exit(1)
    else:
        print(f'Build failed for directory: {current_file}. Please check the modifications.')
        # 执行 git reset 恢复修改
        git_reset_command = f'git reset --hard'
        reset_result = subprocess.run(git_reset_command, shell=True, check=True)
        if reset_result.returncode != 0:
            print(f'Reset failed for directory: {current_file}. Please check the modifications.')
            exit(1)

    # 返回上级目录，准备处理下一个子目录
    os.chdir(target_directory)

# 遍历一级子目录
for subdir, dirs, files in os.walk(target_directory):
    # for dir in dirs:
    #     if dir in ['task']:
    #         continue
    #     replace_build_commit(subdir, dir)
    for file in files:
        if file in ['notice.go']:
            continue
        replace_build_commit(subdir, file)