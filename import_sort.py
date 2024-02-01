import argparse
import os.path
import subprocess
import sys


class Import:
    reference_path = ''
    alias = ''
    package_path = ''

    def __init__(self, raw_import: str):
        # 切分开，引用路径、别名、包路径
        raw_import = raw_import.strip()
        # 先按 : 切分
        parts = raw_import.split(':')
        self.reference_path = parts[0].split('bang-api-gomod')[1].strip('/').replace('//', '/')
        # 再按空格切分
        # 有的有别名，有的没有
        parts = parts[1].strip().split(' ')
        if len(parts) == 1:
            self.package_path = parts[0]
        elif len(parts) == 2:
            self.alias = parts[0]
            self.package_path = parts[1]
        elif len(parts) == 3:
            self.alias = parts[1]
            self.package_path = parts[2]
        else:
            print(f'Error: {raw_import}')
            sys.exit(1)


def search_import(search, in_path, owner_map):
    # grep -r "github\.com/bangwork/bang-api/app/services" --include='*.go' /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/project-api/
    cmd = f'grep -r "{search}" --include=\'*.go\' {in_path}'
    result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            encoding='utf-8')
    if result.returncode != 0:
        print(f'Error: {result.stderr}')
        sys.exit(1)
    lines = result.stdout.split('\n')
    # /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/project-api//ppm/controllers/activity.go:  itemCommon "github.com/bangwork/bang-api/app/services/item/common"
    # /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/project-api//ppm/controllers/activity.go:  "github.com/bangwork/bang-api/app/services/item/delegates/activity"
    # 切分开，引用路径、别名、包路径

    # lines = [
    #     '/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/project-api//task/services/task/common/span.go:import eventTypes "github.com/bangwork/bang-api/app/services/eventbus/types"',
    #     '/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/project-api//task/core/task/internal/domain/types/const.go:import _ "github.com/bangwork/bang-api/app/services/manhour/refactor"'
    # ]

    imports = []
    for line in lines:
        if len(line) == 0:
            continue
        imports.append(Import(line))

    # 按包路径排序，输出 包路径和引用路径
    imports.sort(key=lambda x: x.package_path)
    data = []
    # dirs = []
    for item in imports:
        print(f'{item.package_path} {item.reference_path}')
        d = item.reference_path.split('/')[1]
        # dirs.append(d)
        data.append(
            [item.package_path, item.reference_path, owner_map.get(d), ''])
    # dirs = list(set(dirs))
    # print('\n'.join(dirs))
    return data


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="search import")
    parser.add_argument("--search-path", help="search path", required=False,
                        default='/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/project-api/')
    parser.add_argument("--search-packages", nargs="*", help="List of packages", required=False,
                        default=['github\.com/bangwork/bang-api/app'])
    parser.add_argument("--save", help="save result to excel", required=False, default=False, action='store_true')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_command_line_args()
    # searches = [
    #     # 'github\.com/bangwork/bang-api/app/services',
    #     # 'github\.com/bangwork/bang-api/app/models',
    #     'github\.com/bangwork/bang-api/app',
    #     # 'github\.com/bangwork/bang-api/project-api',
    # ]
    # in_path = '/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/project-api/'
    # in_path = '/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/biz-common/'
    all_data = []
    all_data.append(["package", "path", "owner", "solution"])
    owner_map = {
        "es": "华生",
        "stamp": "宠善",
        "userdomain": "华生",
        "push": "华生",
        "batch": "宠善",
        "context": "华生",
        "utils": "华生",
        "permission": "梓恒",
        "license": "宠善",
        "user": "华生",
        "smsconfig": "华生",
        "team": "华生",
        "plugin-platform": "宠善",
        "resource": "梓恒",
    }
    for search in args.search_packages:
        data = search_import(search, args.search_path, owner_map)
        all_data.extend(data)
    if args.save:
        from move_directory.extract_go_info import write_data_to_excel

        output_name = os.path.basename(args.search_path)
        if output_name == '':
            output_name = 'result'
        column_widths = [60, 60, 15, 40]
        write_data_to_excel(all_data, column_widths, f"{output_name}.xlsx")
