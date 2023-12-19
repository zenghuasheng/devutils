import os
import subprocess


def move_and_replace_imports(main_dir, module_map):
    os.chdir(main_dir)

    # mvc_dirs = ['app/models', 'app/services', 'app/controllers', 'app/services/common']
    mvc_dirs = ['app/services/common']
    for module_dir in mvc_dirs:
        # 去掉 app
        module = module_dir.replace('app/', '')
        source_dir = os.path.join(main_dir, module_dir)

        # 遍历子目录
        for dirpath, dirnames, filenames in os.walk(source_dir):
            # for filename in filenames:
            #     # 检查是否有映射关系
            #     # 把 filename 拆分成文件名和后缀
            #     name, file_extension = os.path.splitext(filename)
            #     if name not in module_map:
            #         # print(f"No mapping for {filename}, skipping...")
            #         continue
            #
            #     target = module_map[filename]
            #     target_file = os.path.join(main_dir, f'project-lib/{target}/{module}/{filename}')
            #
            #     # 创建父级目录
            #     os.makedirs(os.path.dirname(target_file), exist_ok=True)
            #
            #     # 移动文件
            #     subprocess.run(['mv', os.path.join(dirpath, filename), target_file])
            #
            #     # 替换 import
            #     # find /Users/xhs/go/src/github.com/bangwork/bang-api-gomod -type f -name '*.go' -exec sed -i '' 's|github\.com/bangwork/bang-api/app/models/commoncomment|github\.com/bangwork/bang-api/project-lib/task/models/commoncomment|g' {} +
            #     replace_command = f"find {main_dir} -type f -name '*.go' -exec sed -i '' 's|github\.com/bangwork/bang-api/app/{module}/{filename}|github\.com/bangwork/bang-api/project-lib/{target}/{module}/{filename}|g' {{}} +"
            #     subprocess.run(replace_command, shell=True)
            #
            #     # 执行构建命令
            #     build_command = '/Users/xhs/go1.17/go1.20.1/bin/go build  -o /tmp/'
            #     build_result = subprocess.run(build_command, shell=True, check=False)
            #
            #     # 检查构建结果
            #     if build_result.returncode == 0:
            #         # 构建成功，自动提交修改
            #         git_commit_command = f'git add . && git commit -m "{target_file}"'
            #         commit_result = subprocess.run(git_commit_command, shell=True, stdout=subprocess.PIPE,
            #                                        stderr=subprocess.PIPE)
            #         if commit_result.returncode != 0 and "nothing to commit, working tree clean" not in commit_result.stdout.decode(
            #                 "utf-8"):
            #             print(f'Commit failed, Please check the modifications.')
            #             exit(1)
            #     else:
            #         print(f'Build failed, Please check the modifications.')
            for dirname in dirnames:
                # 检查是否有映射关系
                if dirname not in module_map:
                    # print(f"No mapping for {dirname}, skipping...")
                    continue

                repo, target = module_map[dirname]
                if repo == "" or target == "":
                    print(f"No mapping for {dirname}, skipping...")
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
    main_directory = '/Users/xhs/go/src/github.com/bangwork/bang-api-gomod'
    module_mapping = {
        # services
        # "account": ("", ""),
        # "accountnotice": ("", ""),
        "activity": ("project-lib", "ppm"),
        # "agent": ("", ""),
        # "amqp": ("", ""),
        # "app": ("", ""),
        # "app_platform": ("", ""),
        # "audit_log": ("", ""),
        # "auth": ("", ""),
        # "authconfig": ("", ""),
        # "automation": ("", ""),
        # "batch": ("biz-common", "batch"),
        # "batch_refactor": ("", ""),
        # "bind": ("", ""),
        # "captcha": ("", ""),
        # "cert": ("", ""),
        # "channel": ("", ""),
        # "com": ("", ""),
        # "common": ("", ""),
        "commoncomment": ("biz-common", "comment"),
        "commonmessage": ("biz-common", "message"),
        # "config": ("", ""),
        "container": ("project-lib", "container"),
        "context": ("biz-common", "context"),
        # "copilot": ("", ""),
        # "cron": ("", ""),
        # "custom_language": ("", ""),
        # "demo": ("", ""),
        "desk": ("project-lib", "desk"),
        # "devops": ("", ""),
        # "encryption": ("", ""),
        "environment": ("biz-common", "environment"),
        # "event": ("", ""),
        # "eventbus": ("", ""),
        "field": ("project-lib", "task"),
        "fieldcal": ("project-lib", "task"),
        "filter": ("project-lib", "project"),
        "ganttchart": ("project-lib", "ppm"),
        # "import_rule": ("", ""),
        # "importer": ("", ""),
        # "init.go": ("", ""),
        "item": ("project-lib", "item"),
        "kanban": ("project-lib", "project"),
        "layout": ("project-lib", "task"),
        # "license": ("", ""),
        # "login_notice": ("", ""),
        "lua": ("biz-common", "lua"),
        # "mail": ("", ""),
        # "manhour": ("", ""),
        # "marketplace": ("", ""),
        # "membership": ("", ""),
        # "menu.v2": ("", ""),
        "message": ("biz-common", "message"),
        # "miniapp": ("", ""),
        # "notice": ("", ""),
        # "noticeconfig": ("", ""),
        # "noticerules": ("", ""),
        # "notify": ("", ""),
        # "oauth": ("", ""),
        # "object": ("", ""),
        "objectlink": ("project-lib", "task"),
        "objectlinktype": ("project-lib", "task"),
        # "ones_task": ("", ""),
        # "open-platform-services": ("", ""),
        # "operations": ("", ""),
        # "org_initializer": ("", ""),
        # "organization": ("", ""),
        # "performance": ("", ""),
        "permission": ("biz-common", "permission"),
        "permissionrule": ("biz-common", "permission"),
        # "pipeline": ("", ""),
        # "plugin": ("", ""),
        # "plugin-platform": ("", ""),
        # "privacy_policy": ("", ""),
        "product": ("project-lib", "project"),
        # "program": ("", ""),
        "publishVersion": ("project-lib", "task"),
        # "push": ("", ""),
        # "queue": ("", ""),
        "rank": ("project-lib", "project"),
        # "region": ("", ""),
        "related": ("biz-common", "related"),
        "report": ("project-lib", "project"),
        "resource": ("biz-common", "resource"),
        "resource_management": ("biz-common", "resource"),
        # "risk_detection": ("", ""),
        # "scm": ("", ""),
        "scope_field": ("project-lib", "task"),
        "scope_field_config": ("project-lib", "task"),
        # "script_field": ("", ""),
        "search": ("biz-common", "search"),
        # "service": ("", ""),
        # "setting": ("", ""),
        # "sms": ("", ""),
        # "smsconfig": ("", ""),
        # "sso": ("", ""),
        # "sso.v2": ("", ""),
        "stamp": ("biz-common", "stamp"),
        "status": ("project-lib", "task"),
        # "stripe": ("", ""),
        # "style.v2": ("", ""),
        # "tabconfig": ("", ""),
        # "team": ("", ""),
        # "teamscm": ("", ""),
        # "template": ("", ""),
        # "testcase": ("", ""),
        # "timezone": ("", ""),
        # "trace": ("", ""),
        # "tz": ("", ""),
        # "tzconfig": ("", ""),
        "user": ("biz-common", "user"),
        "userdomain": ("biz-common", "userdomain"),
        "usergroup": ("biz-common", "user"),
        # "userguide": ("", ""),
        "version": ("project-lib", "task"),
        # "webhook": ("", ""),
        "workflow": ("project-lib", "task"),
        "workorder": ("project-lib", "task"),
        # models
        # "accountnotice": ("", ""),
        # "action": ("", ""),
        # "app_platform": ("", ""),
        # "audit_log": ("", ""),
        # "auth": ("", ""),
        # "authconfig": ("", ""),
        # "authenticatorinfo": ("", ""),
        # "automation": ("", ""),
        # "blog.go": ("", ""),
        # "bot": ("", ""),
        # "captcha": ("", ""),
        # "channel": ("", ""),
        # "common": ("", ""),
        "condition": ("biz-common", "condition"),
        "dashboard": ("project-lib", "project"),
        # "db": ("", ""),
        # "department": ("", ""),
        # "es": ("", ""),
        "field_cal": ("project-lib", "task"),
        # "geolocation": ("", ""),
        # "i18n": ("", ""),
        # "imap.go": ("", ""),
        # "importerbase": ("", ""),
        # "ip_resolver": ("", ""),
        # "kilob": ("", ""),
        "layout_field": ("project-lib", "task"),
        # "mail.go": ("", ""),
        # "migrate_notice": ("", ""),
        "milestone": ("project-lib", "ppm"),
        "notification": ("biz-common", "notice"),
        # "observer": ("", ""),
        # "onesapp": ("", ""),
        # "pages": ("", ""),
        "ppmtask": ("project-lib", "ppm"),
        # "quickaction": ("", ""),
        # "request_code.go": ("", ""),
        # "reset_code.go": ("", ""),
        # "space": ("", ""),
        # "task_preference.go": ("", ""),
        # "team_scm": ("", ""),
        # "thirdparty": ("", ""),
        # "utils": ("", ""),
        # "whiteAppEmailRecord": ("", ""),
        "workordernotice": ("project-lib", "task"),
        # "activity": "ppm",
        # "commoncomment": "task",
        # "container": "project",
        # "dashboard": "project",
        # "deliverable": "ppm",
        # "field": "task",
        # "field_cal": "task",
        # "filter": "project",
        # "ganttchart": "ppm",
        # "issue_type_scope_field_constraint": "task",
        # "kanban": "project",
        # "layout": "task",
        # "layout_field": "task",
        # "milestone": "ppm",
        # "noticeconfig": "task",
        # "noticerules": "task",
        # "objectcount": "task",
        # "objectlink": "task",
        # "objectlinktype": "task",
        # "ppmtask": "ppm",
        # "product": "project",
        # "program": "project",
        # "publishVersion": "task",
        # "rank": "project",
        # "report": "project",
        # "status": "task",
        # "tabconfig": "task",
        # "taskrelation": "task",
        # "template": "task",
        # "workorder": "task",
        # "workordernotice": "task",

        # services/common
        # "app_platform": ("", ""),
        # "auth": ("", ""),
        # "automation": ("", ""),
        "batch": ("", ""),
        "component": ("project-lib", "project"),
        # "email": ("", ""),
        "errors": ("biz-common", "errors"),
        "gantt": ("project-lib", "ppm"),
        # "get.go": ("", ""),
        "issuetype": ("project-lib", "task"),
        "kmutex": ("biz-common", "mutex"),
        # "license_manager": ("", ""),
        # "liststore": ("", ""),
        "noticerule": ("biz-common", "notice"),
        # "notification.go": ("", ""),
        # "observer": ("", ""),
        "organization": ("biz-common", "user"),
        # "sample": ("", ""),
        # "sort.go": ("", ""),
        "sprint": ("project-lib", "project"),
        # "statdog": ("", ""),
        "task": ("project-lib", "task"),
        # "team.go": ("", ""),
        "template": ("project-lib", "task"),
        "template_defaultconfig": ("project-lib", "task"),
        # "thirdparty": ("", ""),
        # "utils": ("", ""),
    }
    move_and_replace_imports(main_directory, module_mapping)
