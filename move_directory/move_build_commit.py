import os
import subprocess
from replace_code import replace_text_in_file, add_import


def move_and_replace_imports(main_dir, module_map):
    os.chdir(main_dir)

    # TODO 改成文件目录映射
    # mvc_dirs = ['app/models', 'app/services', 'app/controllers', 'app/services/common']
    mvc_dirs = ['app/models']
    for module_dir in mvc_dirs:
        # 去掉 app
        module = module_dir.replace('app/', '')
        source_dir = os.path.join(main_dir, module_dir)

        # 遍历子目录
        for dirpath, dirnames, filenames in os.walk(source_dir):
            for filename in filenames:
                # 检查是否有映射关系
                # 把 filename 拆分成文件名和后缀
                name, file_extension = os.path.splitext(filename)
                if name not in module_map:
                    # print(f"No mapping for {filename}, skipping...")
                    continue

                repo, target = module_map[name]
                if repo == "" or target == "":
                    print(f"No mapping for {filename}, skipping...")
                    continue
                if repo == "biz-common":
                    continue
                target_module = f'{repo}/{target}/{module}/{filename}'
                print(f'Moving {filename} to {target_module}')
                target_file = os.path.join(main_dir, target_module)

                # 这是绝对路径了
                package_name = os.path.dirname(target_file)
                # 创建父级目录
                os.makedirs(package_name, exist_ok=True)

                # 移动文件
                subprocess.run(['mv', os.path.join(dirpath, filename), target_file])

                # controllers 文件内容替换
                replace_text_in_file(target_file)

                # 添加 import
                add_import(target_file, "github.com/bangwork/bang-api/app/utils/httpsvc")

                # 看这个文件暴露了哪些函数，找到引用的地方，替换成新的引用

                # 替换 import
                # find /Users/xhs/go/src/github.com/bangwork/bang-api-gomod -type f -name '*.go' -exec sed -i '' 's|github\.com/bangwork/bang-api/app/models/commoncomment|github\.com/bangwork/bang-api/project-lib/task/models/commoncomment|g' {} +
                # replace_command = f"find {main_dir} -type f -name '*.go' -exec sed -i '' 's|github\.com/bangwork/bang-api/app/{module}/{filename}|github\.com/bangwork/bang-api/project-lib/{target}/{module}/{filename}|g' {{}} +"
                # subprocess.run(replace_command, shell=True)

                # 执行构建命令
                build_command = '/Users/xhs/go1.17/go1.20.1/bin/go build  -o /tmp/'
                build_result = subprocess.run(build_command, shell=True, check=False)

                # 检查构建结果
                if build_result.returncode == 0:
                    # 构建成功，自动提交修改
                    git_commit_command = f'git add . && git commit -m "{target_file}"'
                    commit_result = subprocess.run(git_commit_command, shell=True, stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE)
                    if commit_result.returncode != 0 and "nothing to commit, working tree clean" not in commit_result.stdout.decode(
                            "utf-8"):
                        print(f'Commit failed, Please check the modifications.')
                        exit(1)
                else:
                    print(f'Build failed, Please check the modifications.')
                    exit(1)
            for dirname in dirnames:
                # 检查是否有映射关系
                if dirname not in module_map:
                    # print(f"No mapping for {dirname}, skipping...")
                    continue

                repo, target = module_map[dirname]
                if repo == "" or target == "":
                    print(f"No mapping for {dirname}, skipping...")
                    continue

                if module == "controllers":
                    continue
                target_module = f'{repo}/{target}/{module}/{dirname}'
                print(f'Moving {dirname} to {target_module}')
                target_file = os.path.join(main_dir, target_module)

                # 创建父级目录
                os.makedirs(os.path.dirname(target_file), exist_ok=True)

                # 移动子目录
                move_command = " ".join(['mv', os.path.join(dirpath, dirname), os.path.dirname(target_file)])
                print(move_command)
                move_result = subprocess.run(move_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if move_result.returncode != 0:
                    print(f'Move failed, Please check the modifications.')
                    exit(1)

                # 替换 import
                # find /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/app/services/common/organization -type f -name '*.go' -exec sed -i '' 's|"github\.com/bangwork/bang-api/app/models/user"|"github\.com/bangwork/bang-api/biz-common/user/models/user"|g' {} +
                replace_commands = [
                    f"find {main_dir} -type f -name '*.go' -exec sed -i '' 's|\"github\.com/bangwork/bang-api/app/{module}/{dirname}\"|\"github\.com/bangwork/bang-api/{repo}/{target}/{module}/{dirname}\"|g' {{}} +",
                    f"find {main_dir} -type f -name '*.go' -exec sed -i '' 's|\"github\.com/bangwork/bang-api/app/{module}/{dirname}/|\"github\.com/bangwork/bang-api/{repo}/{target}/{module}/{dirname}/|g' {{}} +",
                ]
                for replace_command in replace_commands:
                    print(replace_command)
                    subprocess.run(replace_command, shell=True)

                # 执行构建命令
                build_command = '/Users/xhs/go1.17/go1.20.1/bin/go build  -o /tmp/'
                build_result = subprocess.run(build_command, shell=True, check=False)

                # 检查构建结果
                if build_result.returncode == 0:
                    # 构建成功，自动提交修改
                    git_commit_command = f'git add . && git commit -m "{target_module}"'
                    commit_result = subprocess.run(git_commit_command, shell=True, stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE)
                    if commit_result.returncode != 0 and "nothing to commit, working tree clean" not in commit_result.stdout.decode(
                            "utf-8"):
                        print(f'Commit failed, Please check the modifications.')
                        exit(1)
                else:
                    print(f'Build failed, Please check the modifications.')
                    exit(1)
            # 不继续递归
            break


if __name__ == '__main__':
    # TODO 改成配置
    main_directory = '/Users/xhs/go/src/github.com/bangwork/bang-api-gomod'
    module_mapping = {
        # 例如
        # "app/services/activity": ("project-api", "ppm"),
        "app/services_refactor/product": ("", ""),
        "app/services_refactor/task": ("", ""),
        "app/services_refactor/workflow_refactor": ("", ""),
        "app/core/test_case": ("", ""),
        "app/core/objectlink": ("", ""),
        "app/core/collector": ("", ""),
        "app/core/wiki": ("", ""),
        "app/core/utils": ("", ""),
        "app/core/user": ("", ""),
        "app/core/scope": ("", ""),
        "app/core/product": ("", ""),
        "app/core/project": ("", ""),
        "app/core/issuetype": ("", ""),
        "app/core/workflow": ("", ""),
        "app/core/task": ("", ""),
        "app/core/publish_version": ("", ""),
        "app/core/resource": ("", ""),
        "app/core/sprint": ("", ""),
        "app/utils/tree": ("", ""),
        "app/utils/performanceutils": ("", ""),
        "app/utils/unique": ("", ""),
        "app/utils/explain": ("", ""),
        "app/utils/numbers": ("", ""),
        "app/utils/context": ("", ""),
        "app/utils/timezone": ("", ""),
        "app/utils/paymentutils": ("", ""),
        "app/utils/cache": ("", ""),
        "app/utils/license": ("", ""),
        "app/utils/identity": ("", ""),
        "app/utils/test": ("", ""),
        "app/utils/limit": ("", ""),
        "app/utils/file": ("", ""),
        "app/utils/swagger": ("", ""),
        "app/utils/config": ("", ""),
        "app/utils/httpsvc": ("", ""),
        "app/utils/routine": ("", ""),
        "app/utils/date": ("", ""),
        "app/utils/telesign": ("", ""),
        "app/utils/listloader": ("", ""),
        "app/utils/gid": ("", ""),
        "app/utils/wikiutils": ("", ""),
        "app/utils/rabbitmq": ("", ""),
        "app/utils/language": ("", ""),
        "app/utils/user": ("", ""),
        "app/utils/audit_log": ("", ""),
        "app/utils/app_platform": ("", ""),
        "app/utils/image": ("", ""),
        "app/utils/env": ("", ""),
        "app/utils/ratelimit": ("", ""),
        "app/utils/redislock": ("", ""),
        "app/utils/json": ("", ""),
        "app/utils/http": ("", ""),
        "app/utils/kafka": ("", ""),
        "app/utils/csv": ("", ""),
        "app/utils/queue": ("", ""),
        "app/utils/format": ("", ""),
        "app/utils/stripeutils": ("", ""),
        "app/utils/log": ("", ""),
        "app/utils/mime": ("", ""),
        "app/utils/cmdproxy": ("", ""),
        "app/utils/retrycounter": ("", ""),
        "app/utils/base58": ("", ""),
        "app/utils/errors": ("", ""),
        "app/utils/safemap": ("", ""),
        "app/utils/timestamp": ("", ""),
        "app/utils/i18n": ("", ""),
        "app/utils/metric": ("", ""),
        "app/utils/encrypt": ("", ""),
        "app/utils/uuid": ("", ""),
        "app/utils/signal": ("", ""),
        "app/utils/constraint": ("", ""),
        "app/utils/oldtimetransfer": ("", ""),
        "app/utils/syncmap": ("", ""),
        "app/utils/flow": ("", ""),
        "app/utils/router": ("", ""),
        "app/models/organization": ("", ""),
        "app/models/commoncomment": ("", ""),
        "app/models/pipeline": ("", ""),
        "app/models/testcase": ("", ""),
        "app/models/taskrelation": ("", ""),
        "app/models/issue_type_scope_field_constraint": ("", ""),
        "app/models/authconfig": ("", ""),
        "app/models/noticerules": ("", ""),
        "app/models/menu.v2": ("", ""),
        "app/models/devops": ("", ""),
        "app/models/role": ("", ""),
        "app/models/importer": ("", ""),
        "app/models/commonmessage": ("", ""),
        "app/models/objectcount": ("", ""),
        "app/models/oauth": ("", ""),
        "app/models/usergroup": ("", ""),
        "app/models/license": ("", ""),
        "app/models/noticeconfig": ("", ""),
        "app/models/accountnotice": ("", ""),
        "app/models/copilot": ("", ""),
        "app/models/import_rule": ("", ""),
        "app/models/config": ("", ""),
        "app/models/auth": ("", ""),
        "app/models/notification": ("", ""),
        "app/models/deliverable": ("", ""),
        "app/models/activity": ("", ""),
        "app/models/whiteAppEmailRecord": ("", ""),
        "app/models/objectlink": ("", ""),
        "app/models/layout": ("", ""),
        "app/models/team_scm": ("", ""),
        "app/models/marketplace": ("", ""),
        "app/models/related": ("", ""),
        "app/models/publishVersion": ("", ""),
        "app/models/login_notice": ("", ""),
        "app/models/plugin": ("", ""),
        "app/models/template": ("", ""),
        "app/models/milestone": ("", ""),
        "app/models/observer": ("", ""),
        "app/models/component": ("", ""),
        "app/models/field_cal": ("", ""),
        "app/models/message": ("", ""),
        "app/models/utils": ("", ""),
        "app/models/user": ("", ""),
        "app/models/userguide": ("", ""),
        "app/models/department": ("", ""),
        "app/models/audit_log": ("", ""),
        "app/models/status": ("", ""),
        "app/models/app_platform": ("", ""),
        "app/models/product": ("", ""),
        "app/models/field": ("", ""),
        "app/models/manhour": ("", ""),
        "app/models/quickaction": ("", ""),
        "app/models/captcha": ("", ""),
        "app/models/notice": ("", ""),
        "app/models/search": ("", ""),
        "app/models/importerbase": ("", ""),
        "app/models/workorder": ("", ""),
        "app/models/project": ("", ""),
        "app/models/channel": ("", ""),
        "app/models/authenticatorinfo": ("", ""),
        "app/models/dashboard": ("", ""),
        "app/models/container": ("", ""),
        "app/models/common": ("", ""),
        "app/models/ganttchart": ("", ""),
        "app/models/action": ("", ""),
        "app/models/region": ("", ""),
        "app/models/condition": ("", ""),
        "app/models/team": ("", ""),
        "app/models/version": ("", ""),
        "app/models/issuetype": ("", ""),
        "app/models/batch": ("", ""),
        "app/models/item": ("", ""),
        "app/models/custom_language": ("", ""),
        "app/models/style.v2": ("", ""),
        "app/models/smsconfig": ("", ""),
        "app/models/workflow": ("", ""),
        "app/models/kanban": ("", ""),
        "app/models/geolocation": ("", ""),
        "app/models/objectlinktype": ("", ""),
        "app/models/task": ("", ""),
        "app/models/sso.v2": ("", ""),
        "app/models/migrate_notice": ("", ""),
        "app/models/onesapp": ("", ""),
        "app/models/program": ("", ""),
        "app/models/queue": ("", ""),
        "app/models/db": ("", ""),
        "app/models/layout_field": ("", ""),
        "app/models/bot": ("", ""),
        "app/models/stamp": ("", ""),
        "app/models/report": ("", ""),
        "app/models/miniapp": ("", ""),
        "app/models/automation": ("", ""),
        "app/models/workordernotice": ("", ""),
        "app/models/kilob": ("", ""),
        "app/models/es": ("", ""),
        "app/models/filter": ("", ""),
        "app/models/setting": ("", ""),
        "app/models/resource": ("", ""),
        "app/models/performance": ("", ""),
        "app/models/space": ("", ""),
        "app/models/i18n": ("", ""),
        "app/models/ppmtask": ("", ""),
        "app/models/permission": ("", ""),
        "app/models/rank": ("", ""),
        "app/models/sprint": ("", ""),
        "app/models/ip_resolver": ("", ""),
        "app/models/pages": ("", ""),
        "app/models/tabconfig": ("", ""),
        "app/models/thirdparty": ("", ""),
        "app/models/resource_management": ("", ""),
        "app/openapi/middlewares": ("", ""),
        "app/openapi/utils": ("", ""),
        "app/openapi/controllers": ("", ""),
        "app/openapi/consts": ("", ""),
        "app/openapi/services": ("", ""),
        "app/openapi/router": ("", ""),
        "app/controllers_refactor/task": ("", ""),
        "app/controllers/organization": ("", ""),
        "app/controllers/testcase": ("", ""),
        "app/controllers/devops": ("", ""),
        "app/controllers/role": ("", ""),
        "app/controllers/importer": ("", ""),
        "app/controllers/usergroup": ("", ""),
        "app/controllers/desk": ("", ""),
        "app/controllers/license": ("", ""),
        "app/controllers/file": ("", ""),
        "app/controllers/copilot": ("", ""),
        "app/controllers/admin": ("", ""),
        "app/controllers/org_config": ("", ""),
        "app/controllers/message": ("", ""),
        "app/controllers/department": ("", ""),
        "app/controllers/notice": ("", ""),
        "app/controllers/project": ("", ""),
        "app/controllers/issuetype": ("", ""),
        "app/controllers/item": ("", ""),
        "app/controllers/task": ("", ""),
        "app/controllers/automation": ("", ""),
        "app/controllers/user_view": ("", ""),
        "app/controllers/account": ("", ""),
        "app/controllers/resource": ("", ""),
        "app/controllers/sprint": ("", ""),
        "app/controllers/auditlog": ("", ""),
        "app/services/organization": ("", ""),
        "app/services/demo": ("", ""),
        "app/services/webhook": ("", ""),
        "app/services/encryption": ("", ""),
        "app/services/notify": ("", ""),
        "app/services/commoncomment": ("", ""),
        "app/services/pipeline": ("", ""),
        "app/services/testcase": ("", ""),
        "app/services/risk_detection": ("", ""),
        "app/services/authconfig": ("", ""),
        "app/services/eventbus": ("", ""),
        "app/services/noticerules": ("", ""),
        "app/services/menu.v2": ("", ""),
        "app/services/devops": ("", ""),
        "app/services/batch_refactor": ("", ""),
        "app/services/role": ("", ""),
        "app/services/importer": ("", ""),
        "app/services/commonmessage": ("", ""),
        "app/services/context": ("", ""),
        "app/services/card": ("", ""),
        "app/services/trace": ("", ""),
        "app/services/oauth": ("", ""),
        "app/services/timezone": ("", ""),
        "app/services/usergroup": ("", ""),
        "app/services/desk": ("", ""),
        "app/services/scope_field_config": ("", ""),
        "app/services/app": ("", ""),
        "app/services/license": ("", ""),
        "app/services/noticeconfig": ("", ""),
        "app/services/accountnotice": ("", ""),
        "app/services/plugin-platform": ("", ""),
        "app/services/permissionrule": ("", ""),
        "app/services/copilot": ("", ""),
        "app/services/import_rule": ("", ""),
        "app/services/sms": ("", ""),
        "app/services/config": ("", ""),
        "app/services/auth": ("", ""),
        "app/services/activity": ("", ""),
        "app/services/mail": ("", ""),
        "app/services/objectlink": ("", ""),
        "app/services/layout": ("", ""),
        "app/services/marketplace": ("", ""),
        "app/services/related": ("", ""),
        "app/services/publishVersion": ("", ""),
        "app/services/login_notice": ("", ""),
        "app/services/plugin": ("", ""),
        "app/services/template": ("", ""),
        "app/services/scope_field": ("", ""),
        "app/services/amqp": ("", ""),
        "app/services/component": ("", ""),
        "app/services/message": ("", ""),
        "app/services/user": ("", ""),
        "app/services/userguide": ("", ""),
        "app/services/agent": ("", ""),
        "app/services/audit_log": ("", ""),
        "app/services/status": ("", ""),
        "app/services/app_platform": ("", ""),
        "app/services/product": ("", ""),
        "app/services/field": ("", ""),
        "app/services/manhour": ("", ""),
        "app/services/operations": ("", ""),
        "app/services/captcha": ("", ""),
        "app/services/lua": ("", ""),
        "app/services/notice": ("", ""),
        "app/services/search": ("", ""),
        "app/services/workorder": ("", ""),
        "app/services/project": ("", ""),
        "app/services/channel": ("", ""),
        "app/services/dashboard": ("", ""),
        "app/services/org_initializer": ("", ""),
        "app/services/container": ("", ""),
        "app/services/push": ("", ""),
        "app/services/open-platform-services": ("", ""),
        "app/services/common": ("", ""),
        "app/services/ganttchart": ("", ""),
        "app/services/region": ("", ""),
        "app/services/sso": ("", ""),
        "app/services/object": ("", ""),
        "app/services/team": ("", ""),
        "app/services/version": ("", ""),
        "app/services/issuetype": ("", ""),
        "app/services/batch": ("", ""),
        "app/services/item": ("", ""),
        "app/services/custom_language": ("", ""),
        "app/services/style.v2": ("", ""),
        "app/services/smsconfig": ("", ""),
        "app/services/cert": ("", ""),
        "app/services/workflow": ("", ""),
        "app/services/kanban": ("", ""),
        "app/services/ones_task": ("", ""),
        "app/services/objectlinktype": ("", ""),
        "app/services/task": ("", ""),
        "app/services/sso.v2": ("", ""),
        "app/services/program": ("", ""),
        "app/services/queue": ("", ""),
        "app/services/environment": ("", ""),
        "app/services/stamp": ("", ""),
        "app/services/report": ("", ""),
        "app/services/miniapp": ("", ""),
        "app/services/teamscm": ("", ""),
        "app/services/automation": ("", ""),
        "app/services/filter": ("", ""),
        "app/services/scm": ("", ""),
        "app/services/account": ("", ""),
        "app/services/service": ("", ""),
        "app/services/setting": ("", ""),
        "app/services/script_field": ("", ""),
        "app/services/resource": ("", ""),
        "app/services/performance": ("", ""),
        "app/services/tzconfig": ("", ""),
        "app/services/permission": ("", ""),
        "app/services/bind": ("", ""),
        "app/services/rank": ("", ""),
        "app/services/fieldcal": ("", ""),
        "app/services/sprint": ("", ""),
        "app/services/userdomain": ("", ""),
        "app/services/tz": ("", ""),
        "app/services/tabconfig": ("", ""),
        "app/services/event": ("", ""),
        "app/services/resource_management": ("", ""),
        "app/services/com": ("", ""),
        "app/services/project_field": ("", ""),
        "app/services/membership": ("", ""),
        "app/services/cron": ("", ""),
        "app/services/privacy_policy": ("", ""),
        "app/services/stripe": ("", ""),
    }
    move_and_replace_imports(main_directory, module_mapping)
