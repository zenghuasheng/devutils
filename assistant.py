import os


def convert_to_exclude_pattern():
    a_str = '''
github.com/bangwork/bang-api/app/models/custom_language.BatchAddOrUpdateMultiLanguage
'''
    # 分行，去掉空行，每行按 . 分割，把最后一个元素替换为 *，输出
    a_list = a_str.split('\n')
    a_list = [i for i in a_list if i != '']
    a_list = [i.split('.') for i in a_list]
    a_list = [i[:-1] + ['*'] for i in a_list]
    a_list = ['.'.join(i) for i in a_list]
    # 打印
    a_list = list(set(a_list))
    for i in a_list:
        print(f"\"{i}\",")


def unique_array(a_array):
    a_array = list(set(a_array))
    # 排序
    a_array.sort()
    for i in a_array:
        print(f"\"{i}\",")


def parse_directory_path(path):
    # /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/app/services/filter
    # app/services/filter
    # 按 / 分割，倒着找到第一个包含 app 的，然后取后面的
    parts = path.split("/")
    for i in range(len(parts) - 1, -1, -1):
        if "app" in parts[i]:
            return "/".join(parts[i:])

def check_model_dir():
    dir_str = '''
    activity
agent
batch
batch_refactor
card
commoncomment
component
container
dashboard
desk
field
filter
ganttchart
import_rule
importer
issuetype
kanban
layout
object
objectlink
objectlinktype
ones_task
operations
product
program
project
project_field
publishVersion
rank
related
report
role
scope_field
scope_field_config
sprint
status
tabconfig
task
version
workflow
workorder
    '''
    dir_list = dir_str.split('\n')
    dir_list = [i.strip() for i in dir_list if i != '']
    exclude_map = {}
    for dir in dir_list:
        # /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/app/models/
#     "app/services/role": PROJECT_COMMON_EXCLUDE_PATTERNS + [
#         "github.com/bangwork/bang-api/app/models/role.*",
#     ]
        k = f"app/services/{dir}"
        # 先校验对应的 models 目录是否存在
        models_dir = f"/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/app/models/{dir}"
        if not os.path.exists(models_dir):
            print(f"models dir not exists: {models_dir}")
            continue
        # 放入 map
        exclude_map[k] = [
            f"github.com/bangwork/bang-api/app/models/{dir}.*",
        ]
    # 打印
    for k, v in exclude_map.items():
        print(f"\"{k}\": [")
        for i in v:
            print(f"    \"{i}\",")
        print("],")


if __name__ == "__main__":
    check_model_dir()
