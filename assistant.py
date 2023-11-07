
a_str = '''
github.com/bangwork/bang-api/app/services/container.RunExecutor
github.com/bangwork/bang-api/app/services/role.AddDefaultRoleConfigsAndMembers
github.com/bangwork/bang-api/app/models/dashboard.AddCards
github.com/bangwork/bang-api/app/models/dashboard.ListCardsInObjects
github.com/bangwork/bang-api/app/models/report.AddBatchProjectReport
github.com/bangwork/bang-api/app/models/report.AddBatchReportCategory
github.com/bangwork/bang-api/app/models/report.ListProjectReports
github.com/bangwork/bang-api/app/models/report.ListReportCategory
github.com/bangwork/bang-api/app/models/sprint.ListSprintsByProject
github.com/bangwork/bang-api/app/models/sprint.BatchAddSprint
github.com/bangwork/bang-api/app/services/common/filter.ReplaceConditionVarFuncUUID
github.com/bangwork/bang-api/app/services/common/filter.Traverse
github.com/bangwork/bang-api/app/services/common/filter.FixConditionByProjectSprint
github.com/bangwork/bang-api/app/services/common/sprint.GetSprintMode
github.com/bangwork/bang-api/app/services/common/sprint.SetSprintMode
github.com/bangwork/bang-api/app/services/container.NewBaseCreator
github.com/bangwork/bang-api/app/services/report/project.AddDefaultIssueTypeReports
github.com/bangwork/bang-api/app/services/report/project.AddDefaultProjectReport
github.com/bangwork/bang-api/app/models/filter.AddProjectFilter
github.com/bangwork/bang-api/app/models/sprint.BatchAddSprint
github.com/bangwork/bang-api/app/services/common/sprint.GetSprintMode
github.com/bangwork/bang-api/app/services/common/sprint.SetSprintMode
github.com/bangwork/bang-api/app/services/container.RunExecutor
github.com/bangwork/bang-api/app/services/common/field/cache.LockTeamProjectFields
github.com/bangwork/bang-api/app/models/sprint.BatchAddSprint
github.com/bangwork/bang-api/app/models/sprint.NewSprint
github.com/bangwork/bang-api/app/models/sprint.Period
github.com/bangwork/bang-api/app/models/filter.ListProjectFiltersByUserUUID
github.com/bangwork/bang-api/app/models/sprint.ListSprintsByProject
github.com/bangwork/bang-api/app/models/sprint.ListSprintsByProject
github.com/bangwork/bang-api/app/services/common/container.RegisterMeta
github.com/bangwork/bang-api/app/services/common/container.RegisterFieldGetter
github.com/bangwork/bang-api/app/services/container.RunExecutor
github.com/bangwork/bang-api/app/services/common/sprint.DeleteSprintMode
github.com/bangwork/bang-api/app/services/container.NewBaseDeleter
github.com/bangwork/bang-api/app/models/sprint.Period
github.com/bangwork/bang-api/app/models/sprint.NewSprint
github.com/bangwork/bang-api/app/services/common/sprint.SetSprintMode
github.com/bangwork/bang-api/app/services/container.NewBaseCreator
github.com/bangwork/bang-api/app/services/project/field.BuildDefaultSprintFields
github.com/bangwork/bang-api/app/services/project/field.ForkEntryStatusField
github.com/bangwork/bang-api/app/services/project/status.BuildDefaultSprintStatus
github.com/bangwork/bang-api/app/services/report/project.AddDefaultProjectReportAndAdded
github.com/bangwork/bang-api/app/models/dashboard.AddCards
github.com/bangwork/bang-api/app/services/amqp/project.PublishAddActivityChartMessage
github.com/bangwork/bang-api/app/services/common/filter.FixFilterConditionByProjectSprint
github.com/bangwork/bang-api/app/services/common/filter.ReplaceConditionVarFuncUUID
github.com/bangwork/bang-api/app/services/common/filter.FixConditionByProjectSprint
github.com/bangwork/bang-api/app/services/common/sprint.GetSprintMode
github.com/bangwork/bang-api/app/services/common/sprint.SetSprintMode
github.com/bangwork/bang-api/app/services/report/project.AddDefaultIssueTypeReports
github.com/bangwork/bang-api/app/services/report/project.AddDefaultProjectReport
github.com/bangwork/bang-api/app/models/sprint.GetSprintCountByStatusUUID
github.com/bangwork/bang-api/app/models/project.MapProjectFieldByFieldUUIDs
github.com/bangwork/bang-api/app/models/role.MapMemberNamesByProjectUUIDs
github.com/bangwork/bang-api/app/services/common/filter.NewPlainParser
github.com/bangwork/bang-api/app/models/component.GetFilterInUserFilterView
github.com/bangwork/bang-api/app/models/component.GetView
github.com/bangwork/bang-api/app/models/component.GetComponentByUUID
github.com/bangwork/bang-api/app/services/common/filter.ToExpression
github.com/bangwork/bang-api/app/services/common/filter.GetTaskImportantField
github.com/bangwork/bang-api/app/services/common/filter.ToSorts
github.com/bangwork/bang-api/app/services/common/filter.GetFieldValueShowView
github.com/bangwork/bang-api/app/models/component.GetFilterInUserFilterView
github.com/bangwork/bang-api/app/services/common/container.NewViewTaskContextMaker
github.com/bangwork/bang-api/app/models/project.BatchAddOrUpdateSprintFieldValue
github.com/bangwork/bang-api/app/models/project.GetFieldValueByType
github.com/bangwork/bang-api/app/services/project/archive.CheckUnknownArchiveProjectPermission
github.com/bangwork/bang-api/app/models/project.AddOrUpdateFieldValue
github.com/bangwork/bang-api/app/models/project.GetSprintFieldByUUID
github.com/bangwork/bang-api/app/models/project.GetSprintFieldValue
github.com/bangwork/bang-api/app/models/project.MapSprintStatusesByUUIDs
github.com/bangwork/bang-api/app/models/project.MapSprintStatusValuesByCategorys
github.com/bangwork/bang-api/app/models/project.FieldTypeName
github.com/bangwork/bang-api/app/models/project.GetSprintPipelineSetting
github.com/bangwork/bang-api/app/services/project.ListPipelineBindingPipelineRuns
github.com/bangwork/bang-api/app/services/project.GetPipelineBindingRuleOrDefault
github.com/bangwork/bang-api/app/models/project.AddOrUpdateFieldValue
github.com/bangwork/bang-api/app/services/project/archive.CheckUnknownArchiveProjectPermission
github.com/bangwork/bang-api/app/models/project.GetProject
github.com/bangwork/bang-api/app/services/report.BuiltInReportUUID
github.com/bangwork/bang-api/app/services/report.BuildReportData
github.com/bangwork/bang-api/app/services/report/project.BuildBuiltInReport
github.com/bangwork/bang-api/app/models/project.ListSprintFeilds
github.com/bangwork/bang-api/app/models/project.FieldTypeName
github.com/bangwork/bang-api/app/models/project.GetSprintStatusByCategory
github.com/bangwork/bang-api/app/models/project.MapProjectNameByUUIDs
github.com/bangwork/bang-api/app/models/project.ListSprintFeilds
github.com/bangwork/bang-api/app/models/project.MapSprintTodoStatusValuesBySprintUUIDs
github.com/bangwork/bang-api/app/models/project.MapSprintStatusesByProjectUUIDs
github.com/bangwork/bang-api/app/models/project.MapSprintStatusValuesBySprintUUIDs
github.com/bangwork/bang-api/app/models/project.MapSprintFeildsByProjectUUIDs
github.com/bangwork/bang-api/app/models/project.MapSprintFieldValuesBySprintUUIDs
github.com/bangwork/bang-api/app/models/project.CategoryName
github.com/bangwork/bang-api/app/models/project.IsExistsProject
github.com/bangwork/bang-api/app/models/project.AddSprintStatus
github.com/bangwork/bang-api/app/models/project.ListSprintStatusesByCategory
github.com/bangwork/bang-api/app/models/project.GetSprintStatusByCategory
github.com/bangwork/bang-api/app/models/project.GetStatusNameByCategory
github.com/bangwork/bang-api/app/models/project.InsertOrUpdateSprintStatusValue
github.com/bangwork/bang-api/app/services/project/archive.CheckUnknownArchiveProjectPermission
github.com/bangwork/bang-api/app/models/component.GetComponentByTemplateUUID
github.com/bangwork/bang-api/app/models/component.GetComponentByUUID
github.com/bangwork/bang-api/app/models/project.MapSprintStatusValuesByCategorys
github.com/bangwork/bang-api/app/services/project/archive.CheckUnknownArchiveProjectPermission
github.com/bangwork/bang-api/app/services/report.BuiltInReportUUID
github.com/bangwork/bang-api/app/services/report.BuildReportData
github.com/bangwork/bang-api/app/services/report/project.BuildBuiltInReport
github.com/bangwork/bang-api/app/models/container.IsProjectContainer
github.com/bangwork/bang-api/app/models/dashboard.AddCards
github.com/bangwork/bang-api/app/models/project.GetProjectType
github.com/bangwork/bang-api/app/models/project.GetProject
github.com/bangwork/bang-api/app/models/report.MapNameProjectReportUUID
github.com/bangwork/bang-api/app/services/project/archive.CheckUnknownArchiveProjectPermission
github.com/bangwork/bang-api/app/models/sprint.ListNormalSprintsInProject
github.com/bangwork/bang-api/app/services/project/archive.CheckUnknownArchiveProjectPermission
github.com/bangwork/bang-api/app/services/project/archive.CheckUnknownArchiveProjectPermission
github.com/bangwork/bang-api/app/models/filter.NoneConditionExpr
github.com/bangwork/bang-api/app/services/common/container.UserDomainVarLabel
github.com/bangwork/bang-api/app/models/container.IsProjectContainer
github.com/bangwork/bang-api/app/models/filter.IsTeamFixedFilterUUID
github.com/bangwork/bang-api/app/models/project.MapProjectFieldByContextAndFieldUUIDs
github.com/bangwork/bang-api/app/models/project.ListProjectsByUUIDs
github.com/bangwork/bang-api/app/services/amqp/project.PublishAddActivityChartMessage
github.com/bangwork/bang-api/app/services/common/container.ComponentContext
github.com/bangwork/bang-api/app/models/container.IsProjectContainer
github.com/bangwork/bang-api/app/services/card/carddelegates.BuildCardDelegate
github.com/bangwork/bang-api/app/models/project.MapProjectsByUUIDs
github.com/bangwork/bang-api/app/models/project.ListProjectUUIDsByTeamUUID
github.com/bangwork/bang-api/app/models/sprint.MapSprintByUUIDs
github.com/bangwork/bang-api/app/services/filter.ListTasksForManhourReport
github.com/bangwork/bang-api/app/models/sprint.MapSprintsByTeamUUID
github.com/bangwork/bang-api/app/services/filter.ListTasks
github.com/bangwork/bang-api/app/models/component.UpdateComponentName
github.com/bangwork/bang-api/app/models/component.UpdateComponentDesc
github.com/bangwork/bang-api/app/services/component.AddComponentsToProjectInTeam
github.com/bangwork/bang-api/app/models/project.DeleteProjectField
github.com/bangwork/bang-api/app/models/role.DeleteRoleConfigsByProject
github.com/bangwork/bang-api/app/models/role.DeleteRoleMembersByProject
github.com/bangwork/bang-api/app/services/common/container.GetFieldGetter
github.com/bangwork/bang-api/app/models/role.ListRoleMemberByProjectUUIDs
github.com/bangwork/bang-api/app/models/role.AllRolesInTeam
github.com/bangwork/bang-api/app/services/container/field.NewBatchFieldFetcher
github.com/bangwork/bang-api/app/services/card.CheckCardPermissionRead
github.com/bangwork/bang-api/app/models/filter.NoneConditionExpr
'''

# 分行，去掉空行，每行按 . 分割，把最后一个元素替换为 *，输出

a_list = a_str.split('\n')
a_list = [i for i in a_list if i != '']
a_list = [i.split('.') for i in a_list]
a_list = [i[:-1] + ['*'] for i in a_list]
a_list = ['.'.join(i) for i in a_list]
# 打印
a_list = list(set(a_list))
# for i in a_list:
#     print(f"\"{i}\",")

a_array = [
    "github.com/bangwork/bang-api/app/services/component/helper.*",
    "github.com/bangwork/bang-api/app/models/project.*",
    "github.com/bangwork/bang-api/app/models/role.*",
    "github.com/bangwork/bang-api/app/models/component.*",
    "github.com/bangwork/bang-api/app/models/sprint.*",
    "github.com/bangwork/bang-api/app/services/container.*",
    "github.com/bangwork/bang-api/app/services/role.*",
    "github.com/bangwork/bang-api/app/services/filter.*",
    "github.com/bangwork/bang-api/app/services/common/sprint.*",
    "github.com/bangwork/bang-api/app/models/filter.*",
    "github.com/bangwork/bang-api/app/services/card.*",
    "github.com/bangwork/bang-api/app/services/project/field.*",
    "github.com/bangwork/bang-api/app/models/role.*",
    "github.com/bangwork/bang-api/app/services/project/archive.*",
    "github.com/bangwork/bang-api/app/services/report.*",
    "github.com/bangwork/bang-api/app/services/report/project.*",
    "github.com/bangwork/bang-api/app/models/component.*",
    "github.com/bangwork/bang-api/app/models/report.*",
    "github.com/bangwork/bang-api/app/services/card/carddelegates.*",
    "github.com/bangwork/bang-api/app/services/component.*",
    "github.com/bangwork/bang-api/app/services/project/status.*",
    "github.com/bangwork/bang-api/app/models/project.*",
    "github.com/bangwork/bang-api/app/services/container.*",
    "github.com/bangwork/bang-api/app/services/common/field/cache.*",
    "github.com/bangwork/bang-api/app/models/dashboard.*",
    "github.com/bangwork/bang-api/app/services/common/container.*",
    "github.com/bangwork/bang-api/app/services/role.*",
    "github.com/bangwork/bang-api/app/services/container/field.*",
    "github.com/bangwork/bang-api/app/services/amqp/project.*",
    "github.com/bangwork/bang-api/app/models/container.*",
    "github.com/bangwork/bang-api/app/models/sprint.*",
    "github.com/bangwork/bang-api/app/services/common/filter.*",
    "github.com/bangwork/bang-api/app/services/project.*",
    "github.com/bangwork/bang-api/app/utils.CheckTeamAllowCopyProject",
]

a_array = list(set(a_array))
# 排序
a_array.sort()
for i in a_array:
    print(f"\"{i}\",")
