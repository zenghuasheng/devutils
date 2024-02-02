import os
import re
import sys


def count_go_lines(directory):
    total_lines = 0

    # 定义匹配 Go 代码行的正则表达式
    go_code_pattern = re.compile(r'^\s*[^//]*[^/\s].*$')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".go"):
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                    # 使用正则表达式匹配 Go 代码行
                    go_lines = [line for line in lines if go_code_pattern.match(line)]

                    # 统计代码行数
                    total_lines += len(go_lines)

    return total_lines


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python code_lines.py <project_directory>")
        sys.exit(1)

    project_directory = sys.argv[1]
    lines = count_go_lines(project_directory)

    print(f"Total lines of Go code (excluding comments and blank lines): {lines}")
