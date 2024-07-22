import sys
from collections import defaultdict
import re

# 检查是否提供了日志文件路径和阈值参数
if len(sys.argv) < 2:
    print("错误：请提供日志文件路径作为第一个命令行参数")
    sys.exit(1)

logfile = sys.argv[1]  # 日志文件路径

# 检查是否提供了阈值参数
if len(sys.argv) >= 3:
    threshold = float(sys.argv[2])
else:
    threshold = None  # 如果没有输入阈值参数，则将其设置为None，表示不进行阈值过滤

# 创建字典用于存储URL的请求量和总请求时间
url_counts = defaultdict(int)
url_times = defaultdict(list)

# 读取日志文件并统计URL的请求量和请求时间
with open(logfile, "r") as file:
    log_data = file.read()

pre_replacements = [
    (r'/api/project/team/[A-Za-z0-9]*', ''),
    (r'/api/project/organization/[A-Za-z0-9]*', ''),
]

for pattern, replacement in pre_replacements:
    log_data = re.sub(pattern, replacement, log_data)

# 使用str_replace逻辑进行URL替换
pattern_replacements = [
    (r'/card/[A-Za-z0-9]*/data', '/card/{uuid}/data'),
    (r'/items/graphql\?t=graphql_project_list_[A-Za-z0-9]*', '/items/graphql?t=graphql_project_list_{uuid}'),
    (r'/task/[A-Za-z0-9]*/new_transit', '/task/{uuid}/new_transit'),
    (r'/task/[A-Za-z0-9]*/messages.*', '/task/{uuid}/messages'),
    (r'/tasks/info\?ids=[A-Za-z0-9]*', '/tasks/info?ids'),
    (r'/projects/info\?ids=[A-Za-z0-9]*', '/projects/info?ids'),
    (r'/bff/task/[A-Za-z0-9]*/check_view', '/bff/task/{uuid}/check_view'),
    (r'/task/[A-Za-z0-9]*/notice_rules', '/task/{uuid}/notice_rules'),
    (r'/items/graphql\?t=userManhoursInfo-[-A-Za-z0-9:]*', '/items/graphql?t=userManhoursInfo-{params}'),
    (r'/items/graphql\?t=groupedManhours-[-A-Za-z0-9:]*', '/items/graphql?t=groupedManhours-{uuid}'),
    (r'/items/graphql\?t=sprint_select_[-A-Za-z0-9:]*', '/items/graphql?t=sprint_select_{uuid}'),
    (r'/items/graphql\?t=issueTypeScope-1-[-A-Za-z0-9:]*', '/items/graphql?t=issueTypeScope-1-{uuid}'),
    (r'/project/[A-Za-z0-9]*/stamps/data\?t=component', '/project/{uuid}/stamps/data?t=component'),
    (r'/items/graphql\?t=FETCH_DASHBOARD_[A-Za-z0-9]*_project_dashboard_DATA',
     '/items/graphql?t=FETCH_DASHBOARD_{uuid}_project_dashboard_DATA'),
    (r'/container_component/[A-Za-z0-9]*/user_views/detail', '/container_component/{uuid}/user_views/detail'),
    (r'/project/[A-Za-z0-9]*/stamps/data\?t=transition,task_status_config',
     '/project/{uuid}/stamps/data?t=transition,task_status_config'),
    (r'/task/[A-Za-z0-9]*/send_message', '/task/{uuid}/send_message'),
    (r'/layout/[A-Za-z0-9]*/draft', '/layout/{uuid}/draft'),
    (r'/layout/[A-Za-z0-9]*/copy', '/layout/{uuid}/copy'),
    (r'/project/[A-Za-z0-9]*/browse', '/project/{uuid}/browse'),
    (r'/project/[A-Za-z0-9]*/reports/peek', '/project/{uuid}/reports/peek'),
    (r'/project/[A-Za-z0-9]*/stamps/data\?t=sprint', '/project/{uuid}/stamps/data?t=sprint'),
    (r'/search\?.*', '/search?{params}'),
    (r'/task/[A-Za-z0-9]*/delete', '/task/{uuid}/delete'),
    (r'/task/[A-Za-z0-9]*/copy', '/task/{uuid}/copy'),
    (r'/task/[A-Za-z0-9]*/watchers/delete', '/task/{uuid}/watchers/delete'),
    (r'/project/[A-Za-z0-9]*/stamps/data\?t=task_status_config', '/project/{uuid}/stamps/data?t=task_status_config'),
    (r'/project/[A-Za-z0-9]*/stamps/data\?t=task_status_config,field_config',
     '/project/{uuid}/stamps/data?t=task_status_config,field_config'),
    (r'/project/[A-Za-z0-9]*/stamps/data\?t=role_config', '/project/{uuid}/stamps/data?t=role_config'),
    (r'/project/[A-Za-z0-9]*/role/[A-Za-z0-9]*/members/update', '/project/{uuid}/role/{uuid}/members/update'),
    (r'/items/graphql\?t=project_select_component_for_selected_project_.*',
     '/items/graphql?t=project_select_component_for_selected_project_{uuid}'),
    (r'/items/graphql\?t=FETCH_DASHBOARD_[A-Za-z0-9]*_dashboard_DATA',
     '/items/graphql?t=FETCH_DASHBOARD_{uuid}_dashboard_DATA'),
    (r'/project/[A-Za-z0-9]*/stamps/data\?t=project', '/project/{uuid}/stamps/data?t=project'),
    (r'/version/[A-Za-z0-9]*/delete', '/version/{uuid}/delete'),
    (r'/items/graphql\?t=member-list-count-[A-Za-z0-9]*', '/items/graphql?t=member-list-count-{uuid}'),
    (r'/items/graphql\?t=userManhours-.*', '/items/graphql?t=userManhours-{params}'),
    (r'/task/[A-Za-z0-9]*/related_tasks', '/task/{uuid}/related_tasks'),
    (r'/project/[A-Za-z0-9]*/recordable_manhour', '/project/{uuid}/recordable_manhour'),
    (r'/items/graphql\?t=grouped-reports-[A-Za-z0-9]*', '/items/graphql?t=grouped-reports-{uuid}'),
    (r'/items/graphql\?t=manhours_aggregated_detail_task_tree-.*',
     '/items/graphql?t=manhours_aggregated_detail_task_tree-{uuid}'),
    (r'/task/[A-Za-z0-9]*/message/[A-Za-z0-9]*/update_discussion', '/task/{uuid}/message/{uuid}/update_discussion'),
    (r'/item/project-[A-Za-z0-9]*/update', '/item/project-{uuid}/update'),
    (r'/task/[A-Za-z0-9]*/watchers/add', '/task/{uuid}/watchers/add'),
    (r'/items/graphql\?t=manhours_aggregated_detail_task_tree-.*',
     '/items/graphql?t=manhours_aggregated_detail_task_tree-{uuid}'),
    (r'/task/[A-Za-z0-9]*/batch_related_tasks', '/task/{uuid}/batch_related_tasks'),
    (r'/items/graphql\?t=graphql_sprint_list_.*', '/items/graphql?t=graphql_sprint_list_{uuid}'),
    (r'/items/graphql\?t=agile-kanban-parent-data_.*', '/items/graphql?t=agile-kanban-parent-data_{uuid}'),
    (r'/project/[A-Za-z0-9]*/sprint/[A-Za-z0-9]*/sprint_statuses/update',
     '/project/{uuid}/sprint/{uuid}/sprint_statuses/update'),
    (r'/project/[A-Za-z0-9]*/sprint/[A-Za-z0-9]*/work_hours_report', '/project/{uuid}/sprint/{uuid}/work_hours_report'),
    (r'/project/[A-Za-z0-9]*/activities/[A-Za-z0-9]*/external_activities',
     '/project/{uuid}/activities/{uuid}/external_activities'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/layout/update', '/project/{uuid}/issue_type/{uuid}/layout/update'),
    (r'/project/[A-Za-z0-9]*/sprint/[A-Za-z0-9]*/task_stats/refresh',
     '/project/{uuid}/sprint/{uuid}/task_stats/refresh'),
    (r'/task/[A-Za-z0-9]*/message/[A-Za-z0-9]*/delete', '/task/{uuid}/message/{uuid}/delete'),
    (r'/items/graphql\?t=agile-kanban-sub-data_.*', '/items/graphql?t=agile-kanban-sub-data_{uuid}'),
    (r'/project/[A-Za-z0-9]*/sprint/[A-Za-z0-9]*/task_stats/refresh',
     '/project/{uuid}/sprint/{uuid}/task_stats/refresh'),
    (r'/project/[A-Za-z0-9]*/stamps/data\?t=field_config', '/project/{uuid}/stamps/data?t=field_config'),
    (r'/items/graphql\?t=paged-member-list-data-key-.*', '/items/graphql?t=paged-member-list-data-key-{uuid}'),
    (r'/items/graphql\?t=sprint-related-ppm-.*', '/items/graphql?t=sprint-related-ppm-{uuid}'),
    (r'/items/graphql\?t=department-descendant-.*', '/items/graphql?t=department-descendant-{uuid}'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/transition/[A-Za-z0-9]*/update',
     '/project/{uuid}/issue_type/{uuid}/transition/{uuid}/update'),
    (r'/item/product_module-[A-Za-z0-9]*/update', '/item/product_module-{uuid}/update'),
    (r'/project/[A-Za-z0-9]*/pin', '/project/{uuid}/pin'),
    (r'/project/[A-Za-z0-9]*/components/add', '/project/{uuid}/components/add'),
    (r'/project/[A-Za-z0-9]*/unpin', '/project/{uuid}/unpin'),
    (r'/items/graphql\?t=SPRINT_[A-Za-z0-9]*_DATA', '/items/graphql?t=SPRINT_{uuid}_DATA'),
    (r'/project/[A-Za-z0-9]*/stamps/data\?t=issue_type_config', '/project/{uuid}/stamps/data?t=issue_type_config'),
    (r'/project/[A-Za-z0-9]*/project_plan/export', '/project/{uuid}/project_plan/export'),
    (r'/items/graphql\?t=SPRINT_[A-Za-z0-9]*_DATA', '/items/graphql?t=SPRINT_{uuid}_DATA'),
    (r'/project/[A-Za-z0-9]*/stamps/data\?t=transition', '/project/{uuid}/stamps/data?t=transition'),
    (r'/items/graphql\?t=issue-type-scope-name-info-.*', '/items/graphql?t=issue-type-scope-name-info-{uuid}'),
    (r'/items/graphql\?t=issueTypeLayouts-issue_type_layout-.*',
     '/items/graphql?t=issueTypeLayouts-issue_type_layout-{uuid}'),
    (r'/items/graphql\?t=report-data__workspace_manhour-.*', '/items/graphql?t=report-data__workspace_manhour-{uuid}'),
    (r'/layout/[A-Za-z0-9]*/batch_apply', '/layout/{uuid}/batch_apply'),
    (r'/users/search\?.*', '/users/search?{params}'),
    (r'/items/graphql\?t=userManhoursTimeSeriesAggregateInfo-.*',
     '/items/graphql?t=userManhoursTimeSeriesAggregateInfo-{uuid}'),
    (r'/items/graphql\?t=userManhoursTimeSeries-[A-Za-z0-9]*-actual_hours',
     '/items/graphql?t=userManhoursTimeSeries-{uuid}-actual_hours'),
    (r'/items/graphql\?t=userManhoursTimeSeries-[A-Za-z0-9]*-estimated_hours',
     '/items/graphql?t=userManhoursTimeSeries-{uuid}-estimated_hours'),
    (r'/task/[A-Za-z0-9]*/bind_wiki_page', '/task/{uuid}/bind_wiki_page'),
    (
    r'/items/graphql\?t=config-in-plan-case-detail-[A-Za-z0-9]*', '/items/graphql?t=config-in-plan-case-detail-{uuid}'),
    (r'/items/graphql\?t=plancase-detail-[A-Za-z0-9]*', '/items/graphql?t=plancase-detail-{uuid}'),
    (r'/task/[A-Za-z0-9]*/bind_testcase_plan', '/task/{uuid}/bind_testcase_plan'),
    (r'/testcase/plan/[A-Za-z0-9]*/cases/add', '/testcase/plan/{uuid}/cases/add'),
    (r'/items/graphql\?t=view-setting-layout-[A-Za-z0-9]*', '/items/graphql?t=view-setting-layout-{uuid}'),
    (r'/dashboard/B5NNKtjn/update', '/dashboard/{uuid}/update'),
    (r'/layout/[A-Za-z0-9]*/rename', '/layout/{uuid}/rename'),
    (r'/items/graphql\?t=plan-testcase-list-[A-Za-z0-9]*-allLib-all',
     '/items/graphql?t=plan-testcase-list-{uuid}-allLib-all'),
    (r'/items/graphql\?t=view-setting-layout-[A-Za-z0-9]*', '/items/graphql?t=view-setting-layout-{uuid}'),
    (r'/container_component/[A-Za-z0-9]*/view/[A-Za-z0-9]*/update', '/container_component/{uuid}/view/{uuid}/update'),
    (r'/issue_type/[A-Za-z0-9]*/transition/[A-Za-z0-9]*/delete', '/issue_type/{uuid}/transition/{uuid}/delete'),
    (r'/items/graphql\?t=report-data__manhour_calendar-[A-Za-z0-9]*',
     '/items/graphql?t=report-data__manhour_calendar-{uuid}'),
    (r'/items/graphql\?t=taskManhoursInfo-.*', '/items/graphql?t=taskManhoursInfo-{uuid}'),
    (r'/items/graphql\?t=FETCH_DASHBOARD_[A-Za-z0-9]*_new_performance_dashboard_DATA',
     '/items/graphql?t=FETCH_DASHBOARD_{uuid}_new_performance_dashboard_DATA'),
    (r'/user_filter_view/[A-Za-z0-9]*/delete', '/user_filter_view/{uuid}/delete'),
    (r'/items/graphql\?t=task-attachments-.*', '/items/graphql?t=task-attachments-{uuid}'),
    (r'/items/graphql\?t=paged-department-select-member-list-data-key-.*',
     '/items/graphql?t=paged-department-select-member-list-data-key-{uuid}'),
    (r'/permission_rule/[A-Za-z0-9]*/delete', '/permission_rule/{uuid}/delete'),
    (r'/items/graphql\?t=config-in-plan-case-detail-.*', '/items/graphql?t=config-in-plan-case-detail-{uuid}'),
    (r'/project/[A-Za-z0-9]*/role/[A-Za-z0-9]*/members/add', '/project/{uuid}/role/{uuid}/members/add'),
    (r'/items/graphql\?t=team-setting-user-group-member-list-.*',
     '/items/graphql?t=team-setting-user-group-member-list-{uuid}'),
    (r'/user/[A-Za-z0-9]*/check_user_guide', '/user/{uuid}/check_user_guide'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/notice_config/[A-Za-z0-9]*/update_methods',
     '/project/{uuid}/issue_type/{uuid}/notice_config/{uuid}/update_methods'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/field/[A-Za-z0-9]*/update',
     '/project/{uuid}/issue_type/{uuid}/field/{uuid}/update'),
    (r'/field/[A-Za-z0-9]*/update', '/field/{uuid}/update'),
    (r'/api/project/file/attachment/[-A-Za-z0-9_]*\?yifangyun_preview/v2/ext=.*',
     '/api/project/file/attachment/{uuid}?yifangyun_preview/v2/ext={params}'),
    (r'/api/project/file/attachment/[-A-Za-z0-9_]*\?e=.*', '/api/project/file/attachment/{uuid}?e={params}'),
    (r'/api/project/organization/[A-Za-z0-9]*/wechat\?.*', '/api/project/organization/{uuid}/wechat?{signature}'),
    (r'/api/project/file/attachment/[-A-Za-z0-9_]*\?imageMogr2/.*',
     '/api/project/file/attachment/{uuid}?imageMogr2/{params}'),
    (r'/api/project/file/avatar/[A-Za-z0-9]*', '/api/project/file/avatar/{uuid}'),
    (r'/project/filters/download_export_task\?key=[A-Za-z0-9]*', '/project/filters/download_export_task?key={uuid}'),
    (r'/testcase/library/[A-Za-z0-9]*/export', '/testcase/library/{uuid}/export'),
    (r'/testcase/library/[A-Za-z0-9]*/upload', '/testcase/library/{uuid}/upload'),
    (r'/testcase/library/[A-Za-z0-9]*/import', '/testcase/library/{uuid}/import'),
    (r'/items/graphql\?t=plan-testcase-list-.*', '/items/graphql?t=plan-testcase-list-{params}'),
    (r'/project/[A-Za-z0-9]*/issue_types/add', '/project/{uuid}/issue_types/add'),
    (r'/issue_type/[A-Za-z0-9]*/delete', '/issue_type/{uuid}/delete'),
    (r'statusForward\?rule_uuid=[A-Za-z0-9]*', 'statusForward?rule_uuid={uuid}'),
    (r'/testcase/plan/[A-Za-z0-9]*/export', '/testcase/plan/{uuid}/export'),
    (r'/project/[A-Za-z0-9]*/delete', '/project/{uuid}/delete'),
    (r'/testcase/case/[A-Za-z0-9]*/attachments', '/testcase/case/{uuid}/attachments'),
    (r'/items/graphql\?t=library-fields-[A-Za-z0-9]*', '/items/graphql?t=library-fields-{uuid}'),
    (r'/items/graphql\?t=library-module-list-[A-Za-z0-9]*', '/items/graphql?t=library-module-list-{uuid}'),
    (r'/items/graphql\?t=newst-fields-in-plancase-detail-[A-Za-z0-9]*',
     '/items/graphql?t=newst-fields-in-plancase-detail-{uuid}'),
    (r'/testcase/library/[A-Za-z0-9]*/cases/update', '/testcase/library/{uuid}/cases/update'),
    (r'/testcase/plan/[A-Za-z0-9]*/cases/update', '/testcase/plan/{uuid}/cases/update'),
    (r'/items/graphql\?t=cache-fields-in-plancase-detail-[A-Za-z0-9]*',
     '/items/graphql?t=cache-fields-in-plancase-detail-{uuid}'),
    (r'/wechat\?msg_signature=.*', '/wechat?msg_signature={signature}'),
    (r'/task/[A-Za-z0-9]*/batch_set_publish_version', '/task/{uuid}/batch_set_publish_version'),
    (r'/task/[A-Za-z0-9]*/create_demand', '/task/{uuid}/create_demand'),
    (r'/items/graphql\?t=product-[A-Za-z0-9]*-for-graphql', '/items/graphql?t=product-{uuid}-for-graphql'),
    (r'/project/[A-Za-z0-9]*/sprint/[A-Za-z0-9]*/delete', '/project/{uuid}/sprint/{uuid}/delete'),
    (r'/testcase/library/[A-Za-z0-9]*/cases/delete', '/testcase/library/{uuid}/cases/delete'),
    (r'/testcase/library/[A-Za-z0-9]*/modules/add', '/testcase/library/{uuid}/modules/add'),
    (r'/project/[A-Za-z0-9]*/sprint/[A-Za-z0-9]*/end', '/project/{uuid}/sprint/{uuid}/end'),
    (r'/project/[A-Za-z0-9]*/sprint/[A-Za-z0-9]*/start', '/project/{uuid}/sprint/{uuid}/start'),
    (r'/issue_type/[A-Za-z0-9]*/layout/update', '/issue_type/{uuid}/layout/update'),
    (r'/issue_type/[A-Za-z0-9]*/task_status/[A-Za-z0-9]*/delete', '/issue_type/{uuid}/task_status/{uuid}/delete'),
    (r'/issue_type/[A-Za-z0-9]*/task_status_configs/position', '/issue_type/{uuid}/task_status_configs/position'),
    (r'/project/[A-Za-z0-9]*/components/sort', '/project/{uuid}/components/sort'),
    (r'/items/graphql\?t=planning-task-data-.*', '/items/graphql?t=planning-task-data-{uuid}'),
    (r'/items/graphql\?t=total-manhours-task-data-.*', '/items/graphql?t=total-manhours-task-data-{uuid}'),
    (r'/project/[A-Za-z0-9]*/components/update', '/project/{uuid}/components/update'),
    (r'/task/[A-Za-z0-9]*/assess_manhour/update', '/task/{uuid}/assess_manhour/update'),
    (r'/user_filter_view/[A-Za-z0-9]*/update', '/user_filter_view/{uuid}/update'),
    (r'/dashboard/[A-Za-z0-9]*/delete', '/dashboard/{uuid}/delete'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/transitions/add',
     '/project/{uuid}/issue_type/{uuid}/transitions/add'),
    (r'/dashboard/[A-Za-z0-9]*/cards/add', '/dashboard/{uuid}/cards/add'),
    (r'/project/[A-Za-z0-9]*/reports/export', '/project/{uuid}/reports/export'),
    (r'/usergroup/[A-Za-z0-9]*/add_user', '/usergroup/{uuid}/add_user'),
    (r'/project/[A-Za-z0-9]*/sprints/add', '/project/{uuid}/sprints/add'),
    (r'/project/[A-Za-z0-9]*/stamps/data', '/project/{uuid}/stamps/data'),
    (r'/task/[A-Za-z0-9]*/unbind_wiki_page', '/task/{uuid}/unbind_wiki_page'),
    (r'/project/[A-Za-z0-9]*/tasks/form_import', '/project/{uuid}/tasks/form_import'),
    (r'/project/[A-Za-z0-9]*/tasks/form_upload', '/project/{uuid}/tasks/form_upload'),
    (r'/project/[A-Za-z0-9]*/tasks/form_download', '/project/{uuid}/tasks/form_download'),
    (r'/project/[A-Za-z0-9]*/component/[A-Za-z0-9]*/related_wiki_pages/update',
     '/project/{uuid}/component/{uuid}/related_wiki_pages/update'),
    (r'/items/graphql\?t=planning-task-data-.*', '/items/graphql?t=planning-task-data-{uuid}'),
    (r'/testcase/plan/[A-Za-z0-9]*/update', '/testcase/plan/{uuid}/update'),
    (r'/testcase/library/[A-Za-z0-9]*/modules/update', '/testcase/library/{uuid}/modules/update'),
    (r'/testcase/library/[A-Za-z0-9]*/cases/move', '/testcase/library/{uuid}/cases/move'),
    (r'/container_component/[A-Za-z0-9]*/user_views/config/update',
     '/container_component/{uuid}/user_views/config/update'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/field_configs', '/project/{uuid}/issue_type/{uuid}/field_configs'),
    (r'/testcase/library/[A-Za-z0-9]*/cases/copy', '/testcase/library/{uuid}/cases/copy'),
    (r'/item/product_component_view-[A-Za-z0-9]*/update', '/item/product_component_view-{uuid}/update'),
    (r'/res/attachment/update/[A-Za-z0-9]*', '/res/attachment/update/{uuid}'),
    (r'/container_component/[A-Za-z0-9]*/user_view/[A-Za-z0-9]*/update',
     '/container_component/{uuid}/user_view/{uuid}/update'),
    (r'/items/graphql\?t=quick-filter-content_.*', '/items/graphql?t=quick-filter-content_{uuid}'),
    (r'/project/[A-Za-z0-9]*/roles/add', '/project/{uuid}/roles/add'),
    (r'/container_component/[A-Za-z0-9]*/user_views/add', '/container_component/{uuid}/user_views/add'),
    (r'/items/graphql\?t=commit-data-key-.*', '/items/graphql?t=commit-data-key-{uuid}'),
    (r'/project/[A-Za-z0-9]*/components/delete/[A-Za-z0-9]*', '/project/{uuid}/components/delete/{uuid}'),
    (r'/dashboard/[A-Za-z0-9]*/cards/layout', '/dashboard/{uuid}/cards/layout'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/fields/position',
     '/project/{uuid}/issue_type/{uuid}/fields/position'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/field/[A-Za-z0-9]*/delete',
     '/project/{uuid}/issue_type/{uuid}/field/{uuid}/delete'),
    (r'/user/[A-Za-z0-9]*/update_user_guide', '/user/{uuid}/update_user_guide'),
    (r'/items/graphql\?t=PPM_RELATED_[A-Za-z0-9]*_DATA', '/items/graphql?t=PPM_RELATED_{uuid}_DATA'),
    (r'/project/[A-Za-z0-9]*/activity_chart/[A-Za-z0-9]*/auto_shedule',
     '/project/{uuid}/activity_chart/{uuid}/auto_shedule'),
    (r'/items/graphql\?t=file-[A-Za-z0-9]*', '/items/graphql?t=file-{uuid}'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/notice_rule/[A-Za-z0-9]*/update',
     '/project/{uuid}/issue_type/{uuid}/notice_rule/{uuid}/update'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/task_status/[A-Za-z0-9]*/delete',
     '/project/{uuid}/issue_type/{uuid}/task_status/{uuid}/delete'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/task_status/[A-Za-z0-9]*/update',
     '/project/{uuid}/issue_type/{uuid}/task_status/{uuid}/update'),
    (r'/items/graphql\?t=item-detail_[A-Za-z0-9]*', '/items/graphql?t=item-detail_{uuid}'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/layout/copy', '/project/{uuid}/issue_type/{uuid}/layout/copy'),
    (r'/project/[A-Za-z0-9]*/issue_type/[A-Za-z0-9]*/notice_config/[A-Za-z0-9]*/add_subscription',
     '/project/{uuid}/issue_type/{uuid}/notice_config/{uuid}/add_subscription'),
    (r'/task/[A-Za-z0-9]*/info', '/task/{uuid}/info'),
    (r'/transition_async_status\?token=[A-Za-z0-9]*', '/transition_async_status?token={token}'),
    (
    r'/res/attachment/[A-Za-z0-9]*\?op=imageMogr2%2Fauto-orient', '/res/attachment/{uuid}?op=imageMogr2%2Fauto-orient'),
    (r'/dingding\?signature=.*', '/dingding?signature={signature}'),
    (r'/dashboard/[A-Za-z0-9]*/card/[A-Za-z0-9]*/update', '/dashboard/{uuid}/card/{uuid}/update'),
    (r'/repo/[A-Za-z0-9]*/scm_webhook', '/repo/{uuid}/scm_webhook'),
    (r'/project/[A-Za-z0-9]*/sprint/[A-Za-z0-9]*/sprint_field/[A-Za-z0-9]*/update',
     '/project/{uuid}/sprint/{uuid}/sprint_field/{uuid}/update'),
    (r'/automation/rule/[A-Za-z0-9]*/update', '/automation/rule/{uuid}/update'),
]
for pattern, replacement in pattern_replacements:
    log_data = re.sub(pattern, replacement, log_data)

for url in log_data.split('\n'):
    fields = url.strip().split()
    if not fields:
        continue
    try:
        request_time = float(fields[-1].strip("\""))  # 去除引号并转换为浮点数
    except ValueError:
        continue

    request = fields[6].strip("\"")
    url_counts[request] += 1
    url_times[request].append(request_time)

# 计算每个URL的P90请求时间阈值
url_p90_thresholds = {url: sorted(times)[int(len(times) * 0.9)] for url, times in url_times.items()}

# 根据请求数量降序排序URL
sorted_urls = sorted(url_counts.items(), key=lambda x: x[1], reverse=True)

# 输出URL数量排行
print("URL数量排行：")
for url, count in sorted_urls:
    p90_threshold = url_p90_thresholds.get(url, 0.0)
    if threshold is None or p90_threshold >= threshold:
        # print(f"URL: {url}，请求数量: {count}，P90: {p90_threshold}")
        print(f"{count} : {url} , P90: {p90_threshold}")
