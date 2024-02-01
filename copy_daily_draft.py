import os
import shutil
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

        # Create a backup file name
        backup_name = f"{os.path.basename(file_path)}.{timestamp}"

        # Copy the file with the backup name
        shutil.copy(file_path, os.path.join(os.path.dirname(file_path), backup_name))

        print(f"Backup created: {backup_name}")

        # Clear the content of the original file
        with open(file_path, 'w') as file:
            file.write("")

        print(f"Original file content cleared: {file_path}")
    else:
        print(f"File content is empty. No backup created.")


if __name__ == "__main__":
    # Specify the file path
    file_to_backups = [
        "/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/tmp/tmp.txt",
        "/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/tmp/tmp.sql",
    ]

    # Perform the backup operation
    for file_to_backup in file_to_backups:
        backup_file(file_to_backup)
