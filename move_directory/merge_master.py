import os.path
import subprocess

if __name__ == '__main__':
    files_path_map = [
        ("app/models/message/message.go", "ones-api-biz-common", "notification/message/models/bizMessage/message.go"),
        ("app/models/sprint/sprint.go", "ones-project-api", "app/project/models/sprint/sprint.go"),
        ("app/openapi/controllers/project/issue_field.go", "bang-api-gomod",
         "app/openapi/controllers/project/issue_field.go"),
        ("app/openapi/router/router.go", "bang-api-gomod", "app/openapi/router/router.go"),
        ("app/openapi/services/common/types.go", "bang-api-gomod", "app/openapi/services/common/types.go"),
        ("app/openapi/services/project/issue_field/error.go", "bang-api-gomod",
         "app/openapi/services/project/issue_field/error.go"),
        ("app/openapi/services/project/issue_field/issue_field.go", "bang-api-gomod",
         "app/openapi/services/project/issue_field/issue_field.go"),
        ("app/openapi/services/project/issue_field/types.go", "bang-api-gomod",
         "app/openapi/services/project/issue_field/types.go"),
        ("app/openapi/utils/date/date.go", "bang-api-gomod", "app/openapi/utils/date/date.go"),
        ("app/openapi/utils/graphql/consts.go", "bang-api-gomod", "app/openapi/utils/graphql/consts.go"),
        ("app/openapi/utils/graphql/paging_query.go", "bang-api-gomod", "app/openapi/utils/graphql/paging_query.go"),
        ("app/openapi/utils/graphql/simple_paging_query.go", "bang-api-gomod",
         "app/openapi/utils/graphql/simple_paging_query.go"),
        ("app/services/message/discussion.go", "ones-project-api", "app/task/services/message/discussion.go"),
        ("app/services/sprint/export_sprints.go", "ones-project-api", "app/project/services/sprint/export_sprints.go"),
        ("app/services/sprint/list.go", "ones-project-api", "app/project/services/sprint/list.go"),
        ("go.mod", "bang-api-gomod", "go.mod"),
    ]

    bangwork_dir = '/Users/xhs/go/src/github.com/bangwork'
    old_project_path = '/Users/xhs/go/src/github.com/bangwork/bang-api-docker'
    have_not_deal_files = []
    for ft in files_path_map:
        f = ft[0]
        # 拼上新项目目录，看文件是否存在
        new_file = os.path.join(bangwork_dir, ft[1], ft[2])
        new_dir = os.path.dirname(new_file)
        if not os.path.exists(new_file):
            print(ft)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        # 文件存在，从旧项目目录拷贝到新项目目录
        old_file = os.path.join(old_project_path, f)
        # cp
        cp_cmd = f'cp {old_file} {new_file}'
        # 执行
        # move_result = subprocess.run(move_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = subprocess.run(cp_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print(f'Error: {res.stderr.decode("utf-8")}')
