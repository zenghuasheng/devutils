import os
import shutil
import subprocess
from datetime import datetime


def backup_file(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Check if the content is not empty
    if content:
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        ext = os.path.splitext(file_path)[1]
        # Create a backup file name
        backup_name = f"{os.path.basename(file_path)}.{timestamp}{ext}"
        # 取 file_path 的后缀

        # Copy the file with the backup name
        shutil.copy(file_path, os.path.join(os.path.dirname(file_path), backup_name))

        print(f"Backup created: {backup_name}")

        # Clear the content of the original file
        with open(file_path, 'w') as file:
            file.write("")
        git_commit_command = f'git add . && git commit -m "{backup_name}"'
        commit_result = subprocess.run(git_commit_command, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, cwd=os.path.dirname(file_path))
        if commit_result.returncode != 0 and "nothing to commit, working tree clean" not in commit_result.stdout.decode(
                "utf-8"):
            print(f'Commit failed, Please check the modifications.')
            exit(1)
        # push
        git_push_command = f'git push origin master'
        push_result = subprocess.run(git_push_command, shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, cwd=os.path.dirname(file_path))
        if push_result.returncode != 0:
            print(f'Push failed, Please check the modifications.')
            exit(1)

        print(f"Original file content cleared: {file_path}")
    else:
        print(f"File content is empty. No backup created.")


if __name__ == "__main__":
    # Specify the file path
    file_to_backups = [
        "/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/tmp/tmp.txt",
        # "/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/tmp/tmp.sql",
    ]

    # Perform the backup operation
    for file_to_backup in file_to_backups:
        backup_file(file_to_backup)
