import os.path
import subprocess

if __name__ == '__main__':
    # files = [
    #     "app/controllers/admin/stamp.go",
    #     "app/controllers/license.go",
    #     "app/controllers/menu.v2.go",
    #     "app/controllers/organization.go",
    #     "app/controllers/plugin.go",
    #     "app/controllers/resource.go",
    #     "app/controllers/task/task.go",
    #     "app/controllers/task_batch.go",
    #     "app/controllers/test_case.go",
    #     "app/controllers/testcase/apid.go",
    #     "app/controllers/testcase/testcase_library.go",
    #     "app/controllers/testcase/testcase_plan.go",
    #     "app/controllers/workflow.go",
    #     "app/core/task/internal/domain/relation/publish_version.go",
    #     "app/core/task/transit.go",
    #     "app/core/task/update.go",
    #     "app/core/utils/di/container.go",
    #     "app/core/utils/di/di.go",
    #     "app/models/audit_log/constants.go",
    #     "app/models/batch/batch_task.go",
    #     "app/models/batch/types.go",
    #     "app/models/deliverable/deliverable.go",
    #     "app/models/field/field_value.go",
    #     "app/models/i18n/audit_log.go",
    #     "app/models/milestone/milestone.go",
    #     "app/models/pages/page.go",
    #     "app/models/resource/resource.go",
    #     "app/models/testcase/plan.go",
    #     "app/models/testcase/testcase_report_template_item.go",
    #     "app/models/utils/constant.go",
    #     "app/models/utils/entity.go",
    #     "app/router/router.go",
    #     "app/services/amqp/init.go",
    #     "app/services/audit_log/i18n.go",
    #     "app/services/audit_log/v2.go",
    #     "app/services/auth/join_team_action/action_share_wiki_page.go",
    #     "app/services/batch/attachments/batch_download.go",
    #     "app/services/batch/batch_task.go",
    #     "app/services/batch/download_batch_task.go",
    #     "app/services/batch/interrupt_task.go",
    #     "app/services/batch/utils.go",
    #     "app/services/card/carddelegates/announcement.go",
    #     "app/services/common/container/permission.go",
    #     "app/services/common/email/config.go",
    #     "app/services/component/wikipage/related_wiki_pages.go",
    #     "app/services/cron/dkron.go",
    #     "app/services/cron/email.go",
    #     "app/services/dashboard/types.go",
    #     "app/services/item/delegates/activity/activity.go",
    #     "app/services/item/delegates/activity/activity_chart_config.go",
    #     "app/services/item/delegates/deliverable.go",
    #     "app/services/item/delegates/schedule/total_manhour_resolver.go",
    #     "app/services/item/delegates/task.go",
    #     "app/services/item/delegates/testcase/case.go",
    #     "app/services/layout/block/tab.go",
    #     "app/services/layout/draft/shaper.go",
    #     "app/services/license/grant.go",
    #     "app/services/license/grant_manager.go",
    #     "app/services/license/license.go",
    #     "app/services/menu.v2/manager.go",
    #     "app/services/menu.v2/validate/custom.go",
    #     "app/services/menu.v2/validate/schema.go",
    #     "app/services/message/refactor/common_event.go",
    #     "app/services/message/refactor/task_created_event.go",
    #     "app/services/message/refactor/utils.go",
    #     "app/services/message/system.go",
    #     "app/services/plugin-platform/ability-framework/sdk.go",
    #     "app/services/plugin_info/plugin_info.go",
    #     "app/services/report/project/export.go",
    #     "app/services/resource/batch_download.go",
    #     "app/services/resource/s3_proxy_download.go",
    #     "app/services/resource/upload.go",
    #     "app/services/task/bind_testcase_plan.go",
    #     "app/services/task/bind_wiki_page.go",
    #     "app/services/task/wiki_page_executor.go",
    #     "app/services/team/department.go",
    #     "app/services/testcase/fieldconfig/copy_field_config.go",
    #     "app/services/testcase/plan/add_plan_report_template.go",
    #     "app/services/testcase/plan/export_plan_report.go",
    #     "app/services/testcase/plan/update_plan_report.go",
    #     "app/services/testcase/plan/update_plan_report_template.go",
    #     "app/services/testcase/type.go",
    #     "app/services/user/types.go",
    #     "app/services/user/user.go",
    #     "app/services/usergroup/group.go",
    #     "app/services/userguide/user_guide.go",
    #     "app/utils/errors/code.go",
    #     "app/utils/wikiutils/types.go",
    #     "app/utils/wikiutils/utils.go",
    #     "app/utils/wikiutils/wiki_api.go",
    #     "docs/project_docs.go",
    #     "docs/project_swagger.yaml",
    #     "go.mod",
    #     "go.sum",
    #     "locales/i18n.json",
    #     "migration/upgrade.yaml",
    #     "template/component/sprint/v2.json",
    #     "template/pandoc/custom-reference.docx",
    #     "tests/backlog/sprint_estimated_test.go",
    # ]
    files_path_map = [
        ("app/controllers/task_batch.go", "project-api/task/controllers/task_batch.go"),
        ("app/controllers/workflow.go", "project-api/task/controllers/workflow.go"),
        ("app/core/task/internal/domain/relation/publish_version.go",
         "project-api/task/core/task/internal/domain/relation/publish_version.go"),
        ("app/core/task/transit.go", "project-api/task/core/task/transit.go"),
        ("app/core/task/update.go", "project-api/task/core/task/update.go"),
        ("app/core/utils/di/container.go", "project-api/task/core/utils/di/container.go"),
        ("app/core/utils/di/di.go", "project-api/task/core/utils/di/di.go"),
        ("app/models/audit_log/constants.go", "biz-common/audit_log/models/audit_log/constants.go"),
        ("app/models/batch/batch_task.go", "biz-common/batch/models/batch/batch_task.go"),
        ("app/models/batch/types.go", "biz-common/batch/models/batch/types.go"),
        ("app/models/deliverable/deliverable.go", "project-api/ppm/models/deliverable/deliverable.go"),
        ("app/models/field/field_value.go", "project-api/task/models/field/field_value.go"),
        ("app/models/i18n/audit_log.go", "biz-common/i18n/models/i18n/audit_log.go"),
        ("app/models/milestone/milestone.go", "project-api/ppm/models/milestone/milestone.go"),
        ("app/models/pages/page.go", "project-api/project/models/pages/page.go"),
        ("app/models/resource/resource.go", "biz-common/resource/models/resource/resource.go"),
        ("app/models/utils/constant.go", "biz-common/models/utils/constant.go"),
        ("app/models/utils/entity.go", "biz-common/models/utils/entity.go"),
        ("app/services/batch/attachments/batch_download.go",
         "biz-common/batch/services/batch/attachments/batch_download.go"),
        ("app/services/card/carddelegates/announcement.go",
         "project-api/project/services/card/carddelegates/announcement.go"),
        ("app/services/common/container/permission.go", "project-api/project/services/common/container/permission.go"),
        ("app/services/component/wikipage/related_wiki_pages.go",
         "project-api/project/services/component/wikipage/related_wiki_pages.go"),
        ("app/services/dashboard/types.go", "project-api/project/services/dashboard/types.go"),
        ("app/services/layout/block/tab.go", "project-api/task/services/layout/block/tab.go"),
        ("app/services/layout/draft/shaper.go", "project-api/task/services/layout/draft/shaper.go"),
        ("app/services/message/refactor/common_event.go", "project-api/task/services/message/refactor/common_event.go"),
        ("app/services/message/refactor/task_created_event.go",
         "project-api/task/services/message/refactor/task_created_event.go"),
        ("app/services/message/refactor/utils.go", "project-api/task/services/message/refactor/utils.go"),
        ("app/services/plugin_info/plugin_info.go", ""),
        ("app/services/report/project/export.go", "project-api/project/services/report/project/export.go"),
        ("app/services/task/bind_wiki_page.go", "project-api/task/services/task/bind_wiki_page.go"),
        # 看起来这个文件被删掉了
        # ("app/services/task/wiki_page_executor.go", ""),
        ("app/utils/errors/code.go", "biz-common/errors/utils/errors/code.go"),
        ("app/utils/wikiutils/types.go", "biz-common/utils/wikiutils/types.go"),
        ("app/utils/wikiutils/utils.go", "biz-common/utils/wikiutils/utils.go"),
        ("app/utils/wikiutils/wiki_api.go", "biz-common/utils/wikiutils/wiki_api.go"),
        ("docs/project_swagger.yaml", ""),
        ("go.mod", ""),
        ("go.sum", ""),
        ("locales/i18n.json", ""),
        ("migration/upgrade.yaml", ""),
        ("template/component/sprint/v2.json", ""),
        ("template/pandoc/custom-reference.docx", ""),
    ]

    # docs/project_swagger.yaml
    # go.mod
    # go.sum
    # locales/i18n.json
    # migration/upgrade.yaml
    # template/component/sprint/v2.json
    # template/pandoc/custom-reference.docx

    new_project_path = '/Users/xhs/go/src/github.com/bangwork/bang-api-gomod'
    old_project_path = '/Users/xhs/go/src/github.com/bangwork/bang-api'
    have_not_deal_files = []
    for ft in files_path_map:
        f = ft[0]
        # 不是 go 文件，跳过
        if not f.endswith('.go'):
            have_not_deal_files.append(f)
            continue
        # 拼上新项目目录，看文件是否存在
        new_file = os.path.join(new_project_path, ft[1])
        if os.path.exists(new_file):
            # 文件存在，从旧项目目录拷贝到新项目目录
            old_file = os.path.join(old_project_path, f)
            # cp
            cp_cmd = f'cp {old_file} {new_file}'
            # 执行
            # move_result = subprocess.run(move_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            res = subprocess.run(cp_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode != 0:
                print(f'Error: {res.stderr.decode("utf-8")}')
        else:
            have_not_deal_files.append(f)
    for f in have_not_deal_files:
        print(f)
