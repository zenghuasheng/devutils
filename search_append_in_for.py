import os
import re


def search_append_in_for(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".go"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = re.findall(r'for\s+\w+\s*:=\s*range\s*\w+\s*\{[^}]*append\(', content)
                    for match in matches:
                        print(f"File: {filepath}")
                        print(f"Code:\n{match}\n")


if __name__ == "__main__":
    base_directory = "/Users/xhs/go/src/github.com/bangwork/ones-project-api"  # 修改为你的目标目录
    search_append_in_for(base_directory)
