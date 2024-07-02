import os


def read_ignore_list(ignore_file_path):
    """读取 .stignore 文件的内容并按行分割为 ignoreList"""
    with open(ignore_file_path, 'r') as file:
        ignore_list = [line.strip() for line in file if line.strip()]
    return ignore_list


def get_template_files(template_dir):
    """获取 template 目录下的所有文件和目录"""
    template_files = []
    for root, dirs, files in os.walk(template_dir):
        for name in dirs + files:
            template_files.append(os.path.relpath(os.path.join(root, name), template_dir))
    return template_files


def main():
    # 定义路径
    base_path = "/Users/xhs/go/src/github.com/bangwork/bang-api-gomod"
    ignore_file_path = os.path.join(base_path, ".stignore")
    template_dir = os.path.join(base_path, "template")

    # 读取 ignoreList
    ignore_list = read_ignore_list(ignore_file_path)

    # 获取 template 目录下的所有文件和目录
    template_files = get_template_files(template_dir)

    # 检查是否包含在 ignoreList 中并打印出来
    should_not_ignore = []
    for file in template_files:
        if file in ignore_list:
            should_not_ignore.append(file)
            print(f"Ignored: {file}")
    new_ignore_list = set(ignore_list) - set(should_not_ignore)
    a_str = "\n".join(new_ignore_list)
    print(f"New ignore list:\n{a_str}")


if __name__ == "__main__":
    main()
