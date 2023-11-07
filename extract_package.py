import sys
import re

# 检查命令行参数是否包含文件路径
if len(sys.argv) != 2:
    print("Usage: python extract_go_info.py <go_file_path>")
    sys.exit(1)

# 从命令行参数获取Go文件路径
go_file_path = sys.argv[1]

# 读取Go文件内容
with open(go_file_path, 'r') as file:
    go_code = file.read()

# 提取包名称
package_match = re.search(r'package\s+([\w\d_]+)', go_code)
if package_match:
    package_name = package_match.group(1)
    print(f'Package Name: {package_name}')

# 提取引用的包
import_match = re.findall(r'import\s+\((.*?)\)', go_code, re.DOTALL)
if import_match:
    import_block = import_match[0]
    import_lines = re.findall(r'\"(.*?)\"', import_block)
    print('Imported Packages:')
    for package in import_lines:
        print(package)

