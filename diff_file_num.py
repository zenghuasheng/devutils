import subprocess
import os
from datetime import datetime


def count_changed_files():
    # 进入目录
    # os.chdir("/Users/xhs/go/src/github.com/bangwork/bang-api-gomod")
    # 打印当前目录
    print(os.getcwd())

    # 获取指定时间之后的 commit 记录
    since_date = "Tue Feb 27 10:59:06 2024 +0800"
    log_output = subprocess.run(["git", "log", "--oneline", f"--since='{since_date}'"], capture_output=True, text=True)
    commits = log_output.stdout.split("\n")

    # 打印每个 commit 和最新 commit 的改动文件数对比
    for commit in commits:
        if len(commit.split()) == 0:
            continue
        commit_hash = commit.split()[0]
        diff_output = subprocess.run(["git", "diff", "--name-status", commit_hash], capture_output=True, text=True)
        changed_files = diff_output.stdout.split("\n")
        changed_files_count = len(changed_files)
        print(f"Commit {commit_hash}: {changed_files_count} changed files")


if __name__ == "__main__":
    count_changed_files()
