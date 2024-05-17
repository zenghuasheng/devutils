import os

# 删除 /Users/xhs/go/src/github.com/bangwork/bang-api-gomod 下的 debug_bin 文件

if __name__ == "__main__":
    # Specify the file path
    file_to_remove = [
        "/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/debug_bin",
        "/Users/xhs/go/src/github.com/bangwork/ones-project-api/debug_bin",
    ]

    # Loop through each file path
    for file_path in file_to_remove:
        # Check if the file exists
        if os.path.exists(file_path):
            # Remove the file
            os.remove(file_path)
            print(f"File removed: {file_path}")
        else:
            print(f"File not found: {file_path}")
