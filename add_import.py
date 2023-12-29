import re

def add_import(file_path, package_name):
    with open(file_path, 'r') as file:
        content = file.read()

    # 正则表达式匹配 import() 语句
    import_pattern = r'\bimport\s*\(\s*([^)]+)\s*\)\s*'

    # 查找 import() 语句
    import_match = re.search(import_pattern, content)

    if import_match:
        existing_imports = import_match.group(1)

        # 检查 package_name 是否已存在
        if package_name in existing_imports:
            print(f'Package "{package_name}" already exists in {file_path}')
            return

        # 在 import() 语句中添加新的包
        new_import = f'"{package_name}"'
        modified_imports = f'{existing_imports}\n\t{new_import}'

        # 检查是否有其他函数或代码紧随在 import() 语句后面
        after_import = content[import_match.end():]
        match_after_import = re.search(r'^\s*\)', after_import)
        if match_after_import:
            modified_content = content[:import_match.start()] + f'import (\n\t{modified_imports}\n)\n\n{after_import[match_after_import.end():]}'
        else:
            modified_content = content[:import_match.start()] + f'import (\n\t{modified_imports}\n)\n{after_import}'

        with open(file_path, 'w') as file:
            file.write(modified_content)

        print(f'Package "{package_name}" added to {file_path}')
    else:
        print('Error: import() statement not found in the file')

# 用法示例
file_path = '/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/project-api/task/controllers/version.go'
package_name = 'github.com/your/new/package'

add_import(file_path, package_name)
