import os
import sys
import fileinput


def replace_text_in_file(file_path, replacement_map):
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


def process_directory(directory_path, replacement_map):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".go"):
                file_path = os.path.join(root, file_name)
                replace_text_in_file(file_path, replacement_map)


if __name__ == '__main__':
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python replace_text.py <目录路径>")
        sys.exit(1)

    directory_path = sys.argv[1]

    # 定义要查找和替换的文本映射
    replacement_map = {
        "controllers.getOrganizationUUID": "httpsvc.GetOrganizationUUID",
        "controllers.getTeamUUID": "httpsvc.GetTeamUUID",
        "controllers.getUserID": "httpsvc.GetUserID",
        "controllers.getProjectUUID": "httpsvc.GetProjectUUID",
        "controllers.getSprintUUID": "httpsvc.GetSprintUUID",
        "controllers.getComponentUserViewUUID": "httpsvc.GetComponentUserViewUUID",
        "controllers.getComponentUUID": "httpsvc.GetComponentUUID",
        "controllers.BindJSON": "httpsvc.BindJSON",
        "controllers.RenderJSON": "httpsvc.RenderJSON",
        "controllers.getContainerType": "httpsvc.GetContainerType",
        "controllers.getContainerUUID": "httpsvc.GetContainerUUID",
        "controllers.getMessageUUID": "httpsvc.GetMessageUUID",
        "controllers.getTaskUUID": "httpsvc.GetTaskUUID",
        "controllers.getBatchUUID": "httpsvc.GetBatchUUID",
        "controllers.getJobType": "httpsvc.GetJobType",
        # getIssueTypeScopeUUID
        "controllers.getIssueTypeScopeUUID": "httpsvc.GetIssueTypeScopeUUID",
        "controllers.getIssueTypeUUID": "httpsvc.GetIssueTypeUUID",
    }

    # 处理目录及子目录下的所有 .go 文件
    process_directory(directory_path, replacement_map)
