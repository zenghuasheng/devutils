#!/usr/bin/env python3

import sys
import re
from collections import defaultdict

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
        r'/items/graphql\?t=config-in-plan-case-detail-[A-Za-z0-9]*',
        '/items/graphql?t=config-in-plan-case-detail-{uuid}'),
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
        r'/res/attachment/[A-Za-z0-9]*\?op=imageMogr2%2Fauto-orient',
        '/res/attachment/{uuid}?op=imageMogr2%2Fauto-orient'),
    (r'/dingding\?signature=.*', '/dingding?signature={signature}'),
    (r'/dashboard/[A-Za-z0-9]*/card/[A-Za-z0-9]*/update', '/dashboard/{uuid}/card/{uuid}/update'),
    (r'/repo/[A-Za-z0-9]*/scm_webhook', '/repo/{uuid}/scm_webhook'),
    (r'/project/[A-Za-z0-9]*/sprint/[A-Za-z0-9]*/sprint_field/[A-Za-z0-9]*/update',
     '/project/{uuid}/sprint/{uuid}/sprint_field/{uuid}/update'),
    (r'/automation/rule/[A-Za-z0-9]*/update', '/automation/rule/{uuid}/update'),
]


def parse_route_path(api_path, url):
    pre_replacements = [
        (r'/api/project/team/[A-Za-z0-9]*', ''),
        (r'/api/project/organization/[A-Za-z0-9]*', ''),
    ]
    pattern = None
    for p, replacement in pattern_replacements:
        if api_path == replacement:
            pattern = p
            break
    if pattern:
        for p, replacement in pre_replacements:
            url = re.sub(p, replacement, url)
        url = re.sub(pattern, api_path, url)
    return url


# 检查是否提供了日志文件路径和接口路径
if len(sys.argv) < 3:
    print("错误：请提供nginx日志文件路径和接口路径作为命令行参数")
    sys.exit(1)

LOG_FILE = sys.argv[1]  # nginx日志文件路径
api_path = sys.argv[2]  # 接口路径

# 读取日志文件
with open(LOG_FILE, 'r') as file:
    log_data = file.read()

# 使用正则表达式提取时间戳、URL和User-Agent
log_pattern = re.compile(
    r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) [^\]]*\] "(GET|POST|HEAD|OPTIONS) ([^\s\"]+) HTTP/1\.1" \d+ \d+ ".*?" "([^"]+)"'
)
matches = log_pattern.findall(log_data)

if not matches:
    print("未能匹配任何日志条目")
    sys.exit(1)

# 过滤特定接口的日志条目并统计 User-Agent 分布
user_agent_counts = defaultdict(int)
for match in matches:
    time_str = match[0]
    method = match[1]
    url = match[2]
    user_agent = match[3]
    route_path = parse_route_path(api_path, url)  # 将 URL 转换为不带参数的路由 path
    if api_path == route_path:
        user_agent_counts[user_agent] += 1

# 按 User-Agent 分布进行统计
if user_agent_counts:
    max_count = max(user_agent_counts.values())
    scale_factor = 50 / max_count  # 控制柱状图的宽度

    print(f"User-Agent 分布（过滤接口：{api_path}）：\n")
    for user_agent, count in user_agent_counts.items():
        bar = '*' * int(count * scale_factor)
        truncated_user_agent = (user_agent[:10] + '...') if len(user_agent) > 10 else user_agent
        print(f"{truncated_user_agent}: {bar} ({count}) - {user_agent}")
else:
    print(f"未找到匹配接口 {api_path} 的请求")
