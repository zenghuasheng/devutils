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
        self.reference_path = parts[0]
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


def search_import(search):
    # grep -r "github\.com/bangwork/bang-api/app/services" --include='*.go' /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/project-api/
    cmd = f'grep -r "{search}" --include=\'*.go\' /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/project-api/'
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
    for item in imports:
        print(f'{item.package_path} {item.reference_path}')


if __name__ == '__main__':
    searches = [
        # 'github\.com/bangwork/bang-api/app/services',
        # 'github\.com/bangwork/bang-api/app/models',
        'github\.com/bangwork/bang-api/app',
    ]
    for search in searches:
        search_import(search)
