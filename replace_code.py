import os
import re
import sys
import fileinput

# 定义要查找和替换的文本映射
replacement_map = {
    "getOrganizationUUID": "httpsvc.GetOrganizationUUID",
    "getTeamUUID": "httpsvc.GetTeamUUID",
    "getUserID": "httpsvc.GetUserID",
    "getProjectUUID": "httpsvc.GetProjectUUID",
    "getSprintUUID": "httpsvc.GetSprintUUID",
    "getComponentUserViewUUID": "httpsvc.GetComponentUserViewUUID",
    "getComponentUUID": "httpsvc.GetComponentUUID",
    "BindJSON": "httpsvc.BindJSON",
    "RenderJSON": "httpsvc.RenderJSON",
    "getContainerType": "httpsvc.GetContainerType",
    "getContainerUUID": "httpsvc.GetContainerUUID",
    "getMessageUUID": "httpsvc.GetMessageUUID",
    "getTaskUUID": "httpsvc.GetTaskUUID",
    "getBatchUUID": "httpsvc.GetBatchUUID",
    "getJobType": "httpsvc.GetJobType",
    # getIssueTypeScopeUUID
    "getIssueTypeScopeUUID": "httpsvc.GetIssueTypeScopeUUID",
    "getIssueTypeUUID": "httpsvc.GetIssueTypeUUID",
    # getVersionSprintUUID
    # getVersionUUID
    # getProductUUID
    "getVersionSprintUUID": "httpsvc.GetVersionSprintUUID",
    "getVersionUUID": "httpsvc.GetVersionUUID",
    "getProductUUID": "httpsvc.GetProductUUID",
    "getUserToken": "httpsvc.GetUserToken",
    "getWorkOrderFormUUID": "httpsvc.GetWorkOrderFormUUID",
    "getLayoutUUID": "httpsvc.GetLayoutUUID",
    "GetRequestTimezone": "httpsvc.GetRequestTimezone",
    "GetRequestToken": "httpsvc.GetRequestToken",
}


def replace_text_in_file(file_path):
    try:
        with fileinput.FileInput(file_path, inplace=True) as file:
            for line in file:
                if "httpsvc" in line:
                    print(line, end='')
                else:
                    for key, value in replacement_map.items():
                        line = line.replace(key, value)
                    print(line, end='')

        print(f"文件 {file_path} 替换完成。")

    except FileNotFoundError:
        print(f"找不到文件: {file_path}")
    except Exception as e:
        print(f"发生错误: {str(e)}")


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
            modified_content = content[
                               :import_match.start()] + f'import (\n\t{modified_imports}\n)\n\n{after_import[match_after_import.end():]}'
        else:
            modified_content = content[:import_match.start()] + f'import (\n\t{modified_imports}\n)\n{after_import}'

        with open(file_path, 'w') as file:
            file.write(modified_content)

        print(f'Package "{package_name}" added to {file_path}')
    else:
        print('Error: import() statement not found in the file')


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".go"):
                file_path = os.path.join(root, file_name)
                replace_text_in_file(file_path)


if __name__ == '__main__':
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python replace_text.py <目录路径>")
        sys.exit(1)

    directory_path = sys.argv[1]

    # 判断是目录还是文件
    if os.path.isdir(directory_path):
        # 处理目录及子目录下的所有 .go 文件
        process_directory(directory_path)
    else:
        replace_text_in_file(directory_path)
        add_import(directory_path, "github.com/bangwork/bang-api/app/utils/httpsvc")
