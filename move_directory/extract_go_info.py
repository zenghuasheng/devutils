import fnmatch
import os
import re
import sys

import openpyxl as openpyxl


def find_package_function_calls(go_code, package_name):
    function_calls = []
    constant_references = []

    # 前面加一个空格，防止匹配到别的包
    pattern = r' {}\.\w+\(?'.format(package_name)
    matches = re.findall(pattern, go_code)

    for match in matches:
        match = match.strip()
        if re.search(r'\($', match):
            # 去掉最后一个字符
            match = match[:-1]
            function_calls.append(match)
        else:
            constant_references.append(match)

    # 去重
    function_calls = list(set(function_calls))
    constant_references = list(set(constant_references))
    return function_calls, constant_references


def to_qualified_name(path, alias, ref):
    return path + ref[len(alias):]


EXCLUDE_PATTERNS = [
    "github.com/bangwork/bang-api/app/models.*",
    "github.com/bangwork/bang-api/app/utils/log.*",
    "github.com/bangwork/ones-ai-api-common*",
    "github.com/bangwork/bang-api/app/utils/errors.*",
    "github.com/bangwork/bang-api/app/models/item.*",
    "github.com/bangwork/ones-context/*",
    "github.com/bangwork/bang-api/app/models/stamp.*",
    "github.com/bangwork/bang-api/app/utils/license.*",
    "github.com/bangwork/bang-api/app/utils.IsLenValid*",
    "github.com/bangwork/bang-api/app/models/common.*",
    "github.com/bangwork/bang-api/app/models/es.*",
    "github.com/bangwork/bang-api/app/models/utils.BuildSqlArgs",
    "github.com/bangwork/bang-api/app/models/utils.SqlPlaceholds",
    "github.com/bangwork/bang-api/app/models/db.*",
    "github.com/bangwork/bang-api/app/utils/env.*",
    "github.com/bangwork/thunder/graphql.*",
    "github.com/bangwork/bang-api/app/utils.UUID",
    "github.com/bangwork/bang-api/app/utils/timestamp.*",
    "github.com/bangwork/bang-api/app/utils/kafka.*",
    "github.com/bangwork/bang-api/app/utils.UniqueNoNullSlice",
    "github.com/bangwork/bang-api/app/utils.StringArrayToSet",
    "github.com/bangwork/bang-api/app/utils.StringSetToArray",
    "github.com/bangwork/bang-api/app/utils.DeepCopy",
    "github.com/bangwork/bang-api/app/utils/config.*",
    "github.com/bangwork/bang-api/app/utils.UniqueNoNullForArrays",
    "github.com/bangwork/bang-api/app/utils.IsEmptyOrLenValidUTF8",
    "github.com/bangwork/bang-api/app/utils.ConvertTostring",
    "github.com/bangwork/bang-api/app/utils/routine.GoSafe",
    "github.com/bangwork/bang-api/app/utils.HtmlStrip",
    "github.com/bangwork/bang-api/app/utils/unique.*",
    "github.com/bangwork/bang-api/app/utils.GetSha1Hash",
    "github.com/bangwork/bang-api/app/utils.UniqueNoNullForArrays",
    "github.com/bangwork/bang-api/app/utils.IsExistsDuplicateInSlice",
    "github.com/bangwork/bang-api/app/utils.StringArrayToSet",
    "github.com/bangwork/bang-api/app/utils.IsEmptyOrLenValidUTF8",
    "github.com/bangwork/bang-api/app/services/item/utils.*",
    "github.com/bangwork/bang-api/app/models/utils.TeamContext",
    "github.com/bangwork/bang-api/app/models/utils.OnesDecimal",
    "github.com/bangwork/bang-api/app/utils.StringArrayToString",
    "github.com/bangwork/bang-api/app/utils.SetKeyToArray",
    "github.com/bangwork/bang-api/app/utils.GetSep",
    "github.com/bangwork/bang-api/app/utils.GetColon",
    "github.com/bangwork/bang-api/app/utils.StringsToInterfaces",
    "github.com/bangwork/bang-api/app/utils.StringArrayIntersection",
    "github.com/bangwork/bang-api/app/utils.InterfacesToStrings",
    "github.com/bangwork/bang-api/app/utils.ToInterfaceArray",
    "github.com/bangwork/bang-api/app/utils.SnakeToLowerCamel",
    "github.com/bangwork/bang-api/app/utils/uuid.*",
    "github.com/bangwork/bang-api/app/services/item/common.*",
    "github.com/bangwork/bang-api/app/models/utils.ProjectContext",
    "github.com/bangwork/bang-api/app/models/utils.TestCasePlanContext",
    "github.com/bangwork/bang-api/app/models/utils.TranslationPinyin",
    "github.com/bangwork/bang-api/app/utils.CompareString",
    "github.com/bangwork/bang-api/app/utils.IsEmptyString",
    "github.com/bangwork/bang-api/app/utils.StringArrayDifference",
    "github.com/bangwork/bang-api/app/utils.CSVRecordEscape",
    "github.com/bangwork/bang-api/app/utils.CSVRecordsEscape",
    "github.com/bangwork/bang-api/app/utils/redislock.*",
    "github.com/bangwork/bang-api/app/utils.TruncateString",
    "github.com/bangwork/bang-api/app/utils.StringOrderArrayDifference",
    "github.com/bangwork/bang-api/app/utils/date.*",
    "github.com/bangwork/bang-api/app/utils.IsMissing",
    "github.com/bangwork/bang-api/app/utils/json.*",
    "github.com/bangwork/bang-api/app/models/utils.*",
    "github.com/bangwork/bang-api/app/utils.GenerateNewDescRich",

    # 多语言，权限的也过滤掉
    "github.com/bangwork/bang-api/app/models/custom_language.*",
    "github.com/bangwork/bang-api/app/utils/i18n/render.*",
    "github.com/bangwork/bang-api/app/services/permission.*",
    "github.com/bangwork/bang-api/app/utils/constraint.*",
    "github.com/bangwork/bang-api/app/services/custom_language.*",
    "github.com/bangwork/bang-api/app/utils/i18n.*",
    "github.com/bangwork/bang-api/app/services/permissionrule.*",

    "github.com/bangwork/bang-api/app/services/common.MustGetProject",
    "github.com/bangwork/bang-api/app/services/common.MustGetProjectIssueType",
    "github.com/bangwork/bang-api/app/services/common.MustGetProjectIssueTypeScope",
    "github.com/bangwork/bang-api/app/services/common.MustGetProjectIssueTypeScope",
    "github.com/bangwork/bang-api/app/services/common.MustGetSprint",
    "github.com/bangwork/bang-api/app/services/common.MustGetSprint",
    "github.com/bangwork/bang-api/app/services/common.MustGetSprint",
    "github.com/bangwork/bang-api/app/services/common.MustManageIssueTypeScope",
    "github.com/bangwork/bang-api/app/services/common/utils.BuildComponentCustomLanguage",
    "github.com/bangwork/bang-api/app/services/common/utils.ConstructComponentCustomLanguangeKey",
    "github.com/bangwork/bang-api/app/services/common/utils.ConstructComponentCustomLanguangeKey",
    "github.com/bangwork/bang-api/app/services/common/utils.ConstructComponentCustomLanguangeKey",

    # 获取数据库或 redis 连接的也去掉
    "github.com/bangwork/bang-api/app/models/setting.NewDBStore",

    "github.com/bangwork/bang-api/app/services/smsconfig.*",
    "github.com/bangwork/bang-api/app/services/common/email.*",
    "github.com/bangwork/bang-api/app/utils/rabbitmq.*",
    "github.com/bangwork/bang-api/app/utils/queue.*",
    "github.com/bangwork/bang-api/app/services/mail.*",
    "github.com/bangwork/bang-api/app/services/common/kmutex.*",
    "github.com/bangwork/bang-api/app/services/item.*",
    "github.com/bangwork/bang-api/app/services/common/errors.*",
    "github.com/bangwork/bang-api/app/core/utils/di.NewContainer",
    "github.com/bangwork/bang-api/app/services/common/utils.BuildPasswordHash",
    "github.com/bangwork/bang-api/app/services/common/utils.MapToArray",
    "github.com/bangwork/bang-api/app/utils.CoerceToString",
    "github.com/bangwork/bang-api/app/utils.CoerceToStringP",
    "github.com/bangwork/bang-api/app/utils.CompareStrings",
    "github.com/bangwork/bang-api/app/utils.ComputeAxisForExcel",
    "github.com/bangwork/bang-api/app/utils.ContainsString",
    "github.com/bangwork/bang-api/app/utils.CountCsvFileRecordsByFilter",
    "github.com/bangwork/bang-api/app/utils.EllipsizeString",
    "github.com/bangwork/bang-api/app/utils.ExtractHtmlElements",
    "github.com/bangwork/bang-api/app/utils.GetDayHourMinuteByDuration",
    "github.com/bangwork/bang-api/app/utils.GetMD5Hash",
    "github.com/bangwork/bang-api/app/utils.HasCharacter",
    "github.com/bangwork/bang-api/app/utils.HasIllegalAscii",
    "github.com/bangwork/bang-api/app/utils.InterfaceToString",
    "github.com/bangwork/bang-api/app/utils.InterfaceToStrings",
    "github.com/bangwork/bang-api/app/utils.IsEmptySlice",
    "github.com/bangwork/bang-api/app/utils.IsNil",
    "github.com/bangwork/bang-api/app/utils.ReverseStringMap",
    "github.com/bangwork/bang-api/app/utils.StringArrayContains",
    "github.com/bangwork/bang-api/app/utils.StringArrayUnion",
    "github.com/bangwork/bang-api/app/utils.StringPtr",
    "github.com/bangwork/bang-api/app/utils.StringStructSetToArray",
    "github.com/bangwork/bang-api/app/utils.TrimStringPointer",
    "github.com/bangwork/bang-api/app/utils.UniqueInt64Slice",
    "github.com/bangwork/bang-api/app/utils.UniqueIntSlice",
    "github.com/bangwork/bang-api/app/utils.UniqueNoNullSliceAndRemove",
    "github.com/bangwork/bang-api/app/utils.ValuePtr",
    "github.com/bangwork/bang-api/app/utils.NewCallbackList",
    "github.com/bangwork/bang-api/app/utils.RandomColor",
]

PROJECT_COMMON_EXCLUDE_PATTERNS = [
    "github.com/bangwork/bang-api/app/models/component.*",
    "github.com/bangwork/bang-api/app/models/container.*",
    "github.com/bangwork/bang-api/app/models/dashboard.*",
    "github.com/bangwork/bang-api/app/models/filter.*",
    "github.com/bangwork/bang-api/app/models/project.*",
    "github.com/bangwork/bang-api/app/models/report.*",
    "github.com/bangwork/bang-api/app/models/role.*",
    "github.com/bangwork/bang-api/app/models/sprint.*",
    "github.com/bangwork/bang-api/app/services/amqp/project.*",
    "github.com/bangwork/bang-api/app/services/card.*",
    "github.com/bangwork/bang-api/app/services/card/carddelegates.*",
    "github.com/bangwork/bang-api/app/services/common/container.*",
    "github.com/bangwork/bang-api/app/services/common/field/cache.*",
    "github.com/bangwork/bang-api/app/services/common/filter.*",
    "github.com/bangwork/bang-api/app/services/common/sprint.*",
    "github.com/bangwork/bang-api/app/services/component.*",
    "github.com/bangwork/bang-api/app/services/component/helper.*",
    "github.com/bangwork/bang-api/app/services/container.*",
    "github.com/bangwork/bang-api/app/services/container/field.*",
    "github.com/bangwork/bang-api/app/services/filter.*",
    "github.com/bangwork/bang-api/app/services/project.*",
    "github.com/bangwork/bang-api/app/services/project/archive.*",
    "github.com/bangwork/bang-api/app/services/project/field.*",
    "github.com/bangwork/bang-api/app/services/project/status.*",
    "github.com/bangwork/bang-api/app/services/report.*",
    "github.com/bangwork/bang-api/app/services/report/project.*",
    "github.com/bangwork/bang-api/app/services/role.*",
    "github.com/bangwork/bang-api/app/utils.CheckTeamAllowCopyProject",
]

MODULE_EXTRA_EXCLUDE_MAP = {
    "app/services/filter": PROJECT_COMMON_EXCLUDE_PATTERNS + ["github.com/bangwork/bang-api/app/models/filter.*"],
    "app/services/sprint": PROJECT_COMMON_EXCLUDE_PATTERNS + [
        "github.com/bangwork/bang-api/app/models/sprint.*",
        # "github.com/bangwork/bang-api/app/models/pipeline.*",
        # "github.com/bangwork/bang-api/app/services/pipeline.*",
        "github.com/bangwork/bang-api/app/services/common/sprint.*",
        "github.com/bangwork/bang-api/app/models/version.*",
    ],
    "app/services/component": PROJECT_COMMON_EXCLUDE_PATTERNS + [
        "github.com/bangwork/bang-api/app/models/component.*",
        "github.com/bangwork/bang-api/app/services/component/object.*",
        "github.com/bangwork/bang-api/app/services/component/todo.*",
        "github.com/bangwork/bang-api/app/services/common/component.*",
        "github.com/bangwork/bang-api/app/services/component/base.*",
    ],
    "app/services/rank": PROJECT_COMMON_EXCLUDE_PATTERNS + [
        "github.com/bangwork/bang-api/app/models/rank.*"
    ],
    "app/services/dashboard": PROJECT_COMMON_EXCLUDE_PATTERNS + [
        "github.com/bangwork/bang-api/app/models/dashboard.*"
    ],
    "app/services/report": PROJECT_COMMON_EXCLUDE_PATTERNS + [
        "github.com/bangwork/bang-api/app/models/report.*",
        "github.com/bangwork/bang-api/app/models/report/generators.*",
        "github.com/bangwork/bang-api/app/services/report.*",
    ],
    "app/services/project": PROJECT_COMMON_EXCLUDE_PATTERNS + [
        "github.com/bangwork/bang-api/app/models/project.*",
        "github.com/bangwork/bang-api/app/services/amqp/project.*",
        "github.com/bangwork/bang-api/app/services/project.*",
    ],
    # role
    "app/services/role": PROJECT_COMMON_EXCLUDE_PATTERNS + [
        "github.com/bangwork/bang-api/app/models/role.*",
    ],

    "app/services/activity": [
        "github.com/bangwork/bang-api/app/models/activity.*",
    ],
    "app/services/batch": [
        "github.com/bangwork/bang-api/app/models/batch.*",
    ],
    "app/services/commoncomment": [
        "github.com/bangwork/bang-api/app/models/commoncomment.*",
    ],
    "app/services/container": [
        "github.com/bangwork/bang-api/app/models/container.*",
    ],
    "app/services/field": [
        "github.com/bangwork/bang-api/app/models/field.*",
    ],
    "app/services/ganttchart": [
        "github.com/bangwork/bang-api/app/models/ganttchart.*",
    ],
    "app/services/import_rule": [
        "github.com/bangwork/bang-api/app/models/import_rule.*",
    ],
    "app/services/importer": [
        "github.com/bangwork/bang-api/app/models/importer.*",
    ],
    "app/services/issuetype": [
        "github.com/bangwork/bang-api/app/models/issuetype.*",
    ],
    "app/services/kanban": [
        "github.com/bangwork/bang-api/app/models/kanban.*",
    ],
    "app/services/layout": [
        "github.com/bangwork/bang-api/app/models/layout.*",
    ],
    "app/services/objectlink": [
        "github.com/bangwork/bang-api/app/models/objectlink.*",
    ],
    "app/services/objectlinktype": [
        "github.com/bangwork/bang-api/app/models/objectlinktype.*",
    ],
    "app/services/product": [
        "github.com/bangwork/bang-api/app/models/product.*",
    ],
    "app/services/program": [
        "github.com/bangwork/bang-api/app/models/program.*",
    ],
    "app/services/publishVersion": [
        "github.com/bangwork/bang-api/app/models/publishVersion.*",
    ],
    "app/services/related": [
        "github.com/bangwork/bang-api/app/models/related.*",
    ],
    "app/services/status": [
        "github.com/bangwork/bang-api/app/models/status.*",
    ],
    "app/services/tabconfig": [
        "github.com/bangwork/bang-api/app/models/tabconfig.*",
    ],
    "app/services/task": [
        "github.com/bangwork/bang-api/app/models/task.*",
    ],
    "app/services/version": [
        "github.com/bangwork/bang-api/app/models/version.*",
    ],
    "app/services/workflow": [
        "github.com/bangwork/bang-api/app/models/workflow.*",
    ],
    "app/services/workorder": [
        "github.com/bangwork/bang-api/app/models/workorder.*",
    ],
}

# 值数组的第一个元素是模块，第二个元素是子模块
FUNCTION_CALL_MODULE_SUBMODULE_PATTERN_MAP = {
    "github.com/bangwork/bang-api/app/utils/i18n.*": ["i18n", ""],
    "github.com/bangwork/bang-api/app/models/notice/webhook_setting.*": ["notice", "webhook_setting"],
    "github.com/bangwork/bang-api/app/models/deliverable.*": ["ppmtask", "deliverable"],
    "github.com/bangwork/bang-api/app/models/testcase.*": ["testcase", ""],
    "github.com/bangwork/bang-api/app/models/devops.*": ["devops", ""],
    "github.com/bangwork/bang-api/app/models/task.*": ["task", ""],
    "github.com/bangwork/bang-api/app/utils/app_platform.*": ["app_platform", ""],
    "github.com/bangwork/bang-api/app/services/amqp/gantt.*": ["ppmtask", "gantt"],
    "github.com/bangwork/bang-api/app/models/template.*": ["template", ""],
    "github.com/bangwork/bang-api/app/services/card/carddelegates.*": ["project", "carddelegates"],
    "github.com/bangwork/bang-api/app/services/report/project.*": ["project", "report"],
    "github.com/bangwork/bang-api/app/models/sprint.*": ["project", "sprint"],
    "github.com/bangwork/bang-api/app/services/custom_language.*": ["i18n", ""],
    "github.com/bangwork/bang-api/app/services/plugin-platform/abilities/implement/project_custom_component.*": [
        "plugin", ""],
    "github.com/bangwork/bang-api/app/services/layout/issuetype.*": ["task", "issuetype"],
    "github.com/bangwork/bang-api/app/services/plugin-platform/abilities/implement/item_handler.*": ["plugin",
                                                                                                     ""],
    "github.com/bangwork/bang-api/app/models/notice/webhook_filter.*": ["notice", "webhook_filter"],
    "github.com/bangwork/bang-api/app/models/manhour.*": ["manhour", ""],
    "github.com/bangwork/bang-api/app/models/plugin.*": ["plugin", ""],
    "github.com/bangwork/bang-api/app/services/common/status.*": ["task", "status"],
    "github.com/bangwork/bang-api/app/models/project.*": ["project", ""],
    "github.com/bangwork/bang-api/app/services/task.*": ["task", ""],
    "github.com/bangwork/bang-api/app/models/tabconfig.*": ["task", "tabconfig"],
    "github.com/bangwork/bang-api/app/services/container.*": ["project", "container"],
    "github.com/bangwork/bang-api/app/models/team.*": ["team", ""],
    "github.com/bangwork/bang-api/app/services/project/field.*": ["project", "project_field"],
    "github.com/bangwork/bang-api/app/models/custom_language.*": ["i18n", ""],
    "github.com/bangwork/bang-api/app/models/field.*": ["task", "field"],
    "github.com/bangwork/bang-api/app/models/component.*": ["project", "component"],
    "github.com/bangwork/bang-api/app/models/message.*": ["message", ""],
    "github.com/bangwork/bang-api/app/services/common/container.*": ["project", "container"],
    "github.com/bangwork/bang-api/app/models/userguide.*": ["userguide", ""],
    "github.com/bangwork/bang-api/app/models/objectlink.*": ["task", "objectlink"],
    "github.com/bangwork/bang-api/app/models/objectlinktype.*": ["task", "objectlinktype"],
    "github.com/bangwork/bang-api/app/models/auth.*": ["auth", ""],
    "github.com/bangwork/bang-api/app/models/layout_field.*": ["task", "layout_field"],
    "github.com/bangwork/bang-api/app/services/issuetype.*": ["task", "issuetype"],
    "github.com/bangwork/bang-api/app/services/noticeconfig.*": ["notice", ""],
    "github.com/bangwork/bang-api/app/models/role.*": ["project", "role"],
    "github.com/bangwork/bang-api/app/services/common/workorder.*": ["task", "workorder"],
    "github.com/bangwork/bang-api/app/services/filter.*": ["project", "filter"],
    "github.com/bangwork/bang-api/app/models/report.*": ["project", "report"],
    "github.com/bangwork/bang-api/app/services/role.*": ["project", "role"],
    "github.com/bangwork/bang-api/app/models/setting.*": ["setting", ""],
    "github.com/bangwork/bang-api/app/models/noticerules.*": ["notice", ""],
    "github.com/bangwork/bang-api/app/services/lua.*": ["lua", ""],
    "github.com/bangwork/bang-api/app/services/common/stamp.*": ["stamp", ""],
    "github.com/bangwork/bang-api/app/models/workflow.*": ["task", "workflow"],
    "github.com/bangwork/bang-api/app/services/container/field.*": ["project", ""],
    "github.com/bangwork/bang-api/app/services/common/field/cache.*": ["project", ""],
    "github.com/bangwork/bang-api/app/services/objectlinktype.*": ["task", "objectlinktype"],
    "github.com/bangwork/bang-api/app/models/container.*": ["project", "container"],
    "github.com/bangwork/bang-api/app/models/bot.*": ["user", "bot"],
    "github.com/bangwork/bang-api/app/services/message.*": ["message", ""],
    "github.com/bangwork/bang-api/app/services/permission.*": ["permission", ""],
    "github.com/bangwork/bang-api/app/models/kanban.*": ["kanban", ""],
    "github.com/bangwork/bang-api/app/models/user.*": ["user", ""],
    "github.com/bangwork/bang-api/app/services/component.*": ["project", "component"],
    "github.com/bangwork/bang-api/app/services/push.*": ["push", ""],
    "github.com/bangwork/bang-api/app/models/product.*": ["product", ""],
    "github.com/bangwork/bang-api/app/services/environment.*": ["environment", ""],
    "github.com/bangwork/bang-api/app/models/noticeconfig.*": ["notice", ""],
    "github.com/bangwork/bang-api/app/services/project.*": ["project", ""],
    "github.com/bangwork/bang-api/app/services/userdomain.*": ["user", "userdomain"],
    "github.com/bangwork/bang-api/app/services/workflow.*": ["task", "workflow"],
    "github.com/bangwork/bang-api/app/models/taskrelation.*": ["task", "taskrelation"],
    "github.com/bangwork/bang-api/app/models/dashboard.*": ["project", "dashboard"],
    "github.com/bangwork/bang-api/app/services/card.*": ["project", "card"],
    "github.com/bangwork/bang-api/app/models/ganttchart.*": ["ppmtask", "ganttchart"],
    "github.com/bangwork/bang-api/app/services/common/userdomain.*": ["user", "userdomain"],
    "github.com/bangwork/bang-api/app/utils/constraint.*": ["constraint", ""],
    "github.com/bangwork/bang-api/app/models/milestone.*": ["ppmtask", "milestone"],
    "github.com/bangwork/bang-api/app/services/permissionrule.*": ["permission", ""],
    "github.com/bangwork/bang-api/app/services/manhour*": ["manhour", ""],
    "github.com/bangwork/bang-api/app/models/issue_type_scope_field_constraint.*": ["task",
                                                                                    "issue_type_scope_field_constraint"],
    "github.com/bangwork/bang-api/app/services/common/filter.*": ["project", "filter"],
    "github.com/bangwork/bang-api/app/models/importer.*": ["importer", ""],
    "github.com/bangwork/bang-api/app/models/program.*": ["program", ""],
    "github.com/bangwork/bang-api/app/services/common/app_platform.*": ["app_platform", ""],
    "github.com/bangwork/bang-api/app/models/layout.*": ["task", "layout"],
    "github.com/bangwork/bang-api/app/services/objectlink.*": ["task", "objectlink"],
    "github.com/bangwork/bang-api/app/core/task.*": ["task", ""],
    "github.com/bangwork/bang-api/app/services/common/sprint.*": ["project", "sprint"],
    "github.com/bangwork/bang-api/app/services/common/issuetype.*": ["task", "issuetype"],
    "github.com/bangwork/bang-api/app/services/common/field.*": ["task", "field"],
    "github.com/bangwork/bang-api/app/services/common/template.*": ["task", "template"],
    "github.com/bangwork/bang-api/app/models/activity.*": ["ppmtask", ""],
    "github.com/bangwork/bang-api/app/services/report.*": ["project", "report"],
    "github.com/bangwork/bang-api/app/services/amqp/project.*": ["project", ""],
    "github.com/bangwork/bang-api/app/services/issuetype/trigger.*": ["task", "trigger"],
    "github.com/bangwork/bang-api/app/utils/wikiutils.*": ["wiki", ""],
    "github.com/bangwork/bang-api/app/models/ppmtask.*": ["ppmtask", ""],
    "github.com/bangwork/bang-api/app/models/status.*": ["task", "status"],
    "github.com/bangwork/bang-api/app/models/resource.*": ["resource", ""],
    "github.com/bangwork/bang-api/app/services/project/status.*": ["project", "sprint"],
    "github.com/bangwork/bang-api/app/models/filter.*": ["project", "filter"],
    "github.com/bangwork/bang-api/app/services/eventbus.*": ["eventbus", ""],
    "github.com/bangwork/bang-api/app/models/issuetype.*": ["task", "issuetype"],
    "github.com/bangwork/bang-api/scripts/issuetype/model/issuetype.*": ["task", "issuetype"],

    "github.com/bangwork/bang-api/app/services/common/container.MustCheckContainer": ["permission", ""],
    "github.com/bangwork/bang-api/app/services/common/container.MustCheckOne": ["permission", ""],
    "github.com/bangwork/bang-api/app/services/common.MustGetSprint": ["permission", ""],
    "github.com/bangwork/bang-api/app/services/project/archive.CheckUnknownArchiveProjectPermission": ["project", ""],
    "github.com/bangwork/bang-api/app/services/devops/webhook.AddCommitStats": ["devops", ""],
    "github.com/bangwork/bang-api/app/core/task/types.GetFinalRelations": ["task", ""],
    "github.com/bangwork/bang-api/app/models/report/generators/cache.ClearSprintCacheBySprintUUID": ["report", ""],
    "github.com/bangwork/bang-api/app/utils/i18n/render.ReplacePlaceholder": ["i18n", ""],
    "github.com/bangwork/bang-api/app/models/space.IsExistSpaceUUID": ["wiki", ""],
    "github.com/bangwork/bang-api/app/services/common/utils.ConstructComponentCustomLanguangeKey": ["i18n",
                                                                                                    ""],
    "github.com/bangwork/bang-api/app/services/common/container.MustCheckComponent": ["permission", ""],
    "github.com/bangwork/bang-api/app/services/common.MustGetProjectIssueType": ["permission", ""],
    "github.com/bangwork/bang-api/app/services/common/utils.BuildComponentCustomLanguage": ["i18n", ""],
    "github.com/bangwork/bang-api/app/services/common/utils.MapProjectTaskStatusCategory": ["task", ""],
    "github.com/bangwork/bang-api/app/services/common/utils.MapSprintTaskStatusCategory": ["task", ""],
    "github.com/bangwork/bang-api/app/services/common.MustGetProject": ["permission", ""],
    "github.com/bangwork/bang-api/app/services/common.MustManageIssueTypeScope": ["permission", ""],
    "github.com/bangwork/bang-api/app/services/common.MustGetProjectIssueTypeScope": ["permission", ""],
    "github.com/bangwork/bang-api/app/utils.ListSamplePages": ["wiki", ""],
    "github.com/bangwork/bang-api/app/services/layout/redis.UpdateLayoutRelatedScopeStamp": ["layout", ""],
    "github.com/bangwork/bang-api/app/services/task/common.BuildTasksCommonSystemFieldValues": ["task", ""],
    "github.com/bangwork/bang-api/app/services/component/helper.DeleteUserViewByFilter": ["component", ""],
    "github.com/bangwork/bang-api/app/services/component/helper.UpdateUserViewByFilter": ["component", ""],
    "github.com/bangwork/bang-api/app/services/component/helper.AddUserViewByFilter": ["component", ""],

    "github.com/bangwork/bang-api/app/core/task/types.*": ["task", ""],
    "github.com/bangwork/bang-api/app/core/sprint.*": ["project", "sprint"],
    "github.com/bangwork/bang-api/app/services/publishVersion/common.*": ["publish_version", ""],
    "github.com/bangwork/bang-api/app/utils/identity.*": ["identity", "identity"],
    "github.com/bangwork/bang-api/app/utils/numbers.*": ["numbers", "numbers"],
    "github.com/bangwork/bang-api/app/services/importer/constants.*": ["importer", ""],
    "github.com/bangwork/bang-api/app/services/tabconfig.*": ["task", "tabconfig"],
    "github.com/bangwork/bang-api/app/services/layout/redis.*": ["task", "layout"],
    "github.com/bangwork/bang-api/app/services/layout/block.*": ["task", "layout"],
    "github.com/bangwork/bang-api/app/services/testcase.*": ["testcase", ""],
    "github.com/bangwork/bang-api/app/services/automation/types.*": ["automation", ""],
    "github.com/bangwork/bang-api/app/utils/file.*": ["resource", ""],
    "github.com/bangwork/bang-api/app/models/pipeline.*": ["pipeline", ""],
    "github.com/bangwork/bang-api/app/services/common/gantt.*": ["ppmtask", "gantt"],
    "github.com/bangwork/bang-api/app/services/setting.*": ["setting", ""],
    "github.com/bangwork/bang-api/app/services/layout/draft.*": ["task", "layout"],
    "github.com/bangwork/bang-api/app/services/importer.*": ["importer", ""],
    "github.com/bangwork/bang-api/app/core/task/event.*": ["task", ""],
    "github.com/bangwork/bang-api/app/models/performance.*": ["performance", ""],
    "github.com/bangwork/bang-api/app/utils/flow.*": ["flow", "flow"],
    "github.com/bangwork/bang-api/app/models/migrate_notice.*": ["notice", ""],
    "github.com/bangwork/bang-api/app/utils/oldtimetransfer.*": ["oldtimetransfer", ""],
    "github.com/bangwork/bang-api/app/controllers_refactor/task/types.*": ["task", ""],
    "github.com/bangwork/bang-api/app/services/sprint.*": ["project", "sprint"],
    "github.com/bangwork/bang-api/app/services/issuetype/field_constraint.*": ["task", "issuetype"],
    "github.com/bangwork/bang-api/app/models/issuetype/trigger.*": ["task", "issuetype"],
    "github.com/bangwork/bang-api/app/services/pipeline.*": ["pipeline", ""],
    "github.com/bangwork/bang-api/app/models/organization.*": ["organization", ""],
    "github.com/bangwork/bang-api/app/services/encryption.*": ["encryption", ""],
    "github.com/bangwork/bang-api/app/services/plugin-platform/abilities/implement/user_list_filter.*": ["plugin", ""],
    "github.com/bangwork/bang-api/app/core/objectlink/types.*": ["task", "objectlink"],
    "github.com/bangwork/bang-api/app/services/ganttchart.*": ["ppmtask", "ganttchart"],
    "github.com/bangwork/bang-api/app/core/collector.*": ["collector", ""],
    "github.com/bangwork/bang-api/app/models/region.*": ["region", ""],
    "github.com/bangwork/bang-api/app/services/workflow/executors.*": ["task", "workflow"],
    "github.com/bangwork/bang-api/app/core/task/internal/repo.*": ["task", ""],
    "github.com/bangwork/bang-api/app/services/common/thirdparty.*": ["thirdparty", ""],
    "github.com/bangwork/bang-api/app/utils/metric/hubspot.*": ["hubspot", ""],
    "github.com/bangwork/bang-api/app/models/issuetype/common.*": ["task", "issuetype"],
    "github.com/bangwork/bang-api/app/services/user.*": ["user", ""],
    "github.com/bangwork/bang-api/app/services/issuetype/calibrator.*": ["task", "issuetype"],
    "github.com/bangwork/bang-api/app/models/notice.*": ["notice", ""],
    "github.com/bangwork/bang-api/app/services/card/carddelegates/performance.*": ["performance", ""],
    "github.com/bangwork/bang-api/app/core/issuetype.*": ["task", "issuetype"],
    "github.com/bangwork/bang-api/app/core/task/internal/domain.*": ["task", ""],
    "github.com/bangwork/bang-api/app/models/batch.*": ["batch", ""],
    "github.com/bangwork/bang-api/app/services/task/common.*": ["task", ""],
    "github.com/bangwork/bang-api/app/services/layout/transform.*": ["task", "layout"],
    "github.com/bangwork/bang-api/app/services/card/quickquery.*": ["project", "card"],
    "github.com/bangwork/bang-api/app/services/common.*": ["common", ""],
    "github.com/bangwork/bang-api/app/services/importer/importer_web.*": ["importer", ""],
    "github.com/bangwork/bang-api/app/services/common/automation.*": ["automation", ""],
    "github.com/bangwork/bang-api/app/services/common/observer.*": ["observer", ""],
    "github.com/bangwork/bang-api/app/services/common/template_defaultconfig.*": ["task", "template"],
    "github.com/bangwork/bang-api/app/utils/user.*": ["user", ""],
    "github.com/bangwork/bang-api/app/services/open-platform-services/field/group_field_platform.*": ["plugin", ""],
    "github.com/bangwork/bang-api/app/services/notify.*": ["notify", ""],
    "github.com/bangwork/bang-api/app/services/issuetype/interceptor.*": ["task", "issuetype"],
    "github.com/bangwork/bang-api/app/services/importer/sync/helper.*": ["importer", ""],
    "github.com/bangwork/bang-api/app/services/importer/sync.*": ["importer", ""],
    "github.com/bangwork/bang-api/app/services/layout/dynamic.*": ["task", "layout"],
    "github.com/bangwork/bang-api/app/services/webhook/webhook_filter.*": ["webhook", ""],
    "github.com/bangwork/bang-api/app/services/importer/importer_web/cache.*": ["importer", ""],
    "github.com/bangwork/bang-api/app/services/workflow/handlers.*": ["task", "workflow"],
    "github.com/bangwork/bang-api/app/core/task/internal/domain/relation.*": ["task", ""],
    "github.com/bangwork/bang-api/app/services/plugin-platform/abilities.*": ["plugin", ""],
    "github.com/bangwork/bang-api/app/core/task/internal/domain/relation/driver.*": ["task", ""],
    "github.com/bangwork/bang-api/app/services/organization.*": ["organization", ""],
    "github.com/bangwork/bang-api/app/core/task/utils.*": ["task", ""],
    "github.com/bangwork/bang-api/app/utils.*": ["utils", ""],
    "github.com/bangwork/bang-api/app/services/importer/resolve/plugin/plugin_type/validate.*": ["importer", ""],

    "github.com/bangwork/bang-api/app/core/scope.*": ["task", "issuetype"],
    "github.com/bangwork/bang-api/app/core/task/internal/domain/property.*": ["task", ""],
    "github.com/bangwork/bang-api/app/services/plugin-platform/abilities/implement/third_import.*": ["plugin", ""],
    "github.com/bangwork/bang-api/app/openapi/utils/errors.*": ["openapi", ""],
    "github.com/bangwork/bang-api/app/services/issuetype/batch.*": ["batch", ""],
    "github.com/bangwork/bang-api/app/models/condition.*": ["project", "filter"],
    "github.com/bangwork/bang-api/app/services/resource.*": ["resource", ""],
    "github.com/bangwork/bang-api/app/services/eventbus/user.*": ["eventbus", ""],
    "github.com/bangwork/bang-api/app/services/importer/resolve.*": ["importer", ""],
    "github.com/bangwork/bang-api/app/services/plugin-platform/abilities/implement/http.*": ["plugin", ""],
    "github.com/bangwork/bang-api/app/services/project/archive.*": ["project", ""],
    "github.com/bangwork/bang-api/app/services/batch/import_update.*": ["batch", ""],
    "github.com/bangwork/bang-api/app/services/plugin-platform/abilities/implement/custom_card.*": ["plugin", ""],
    "github.com/bangwork/bang-api/app/services/sso.v2/common/base.*": ["user", ""],
    "github.com/bangwork/bang-api/app/utils/metric/segment.*": ["metric", ""],
    "github.com/bangwork/bang-api/app/models/observer.*": ["task", "observer"],
    "github.com/bangwork/bang-api/app/core/task/internal/domain/property/driver.*": ["task", ""],
    "github.com/bangwork/bang-api/app/services/common/task.*": ["task", ""],
    "github.com/bangwork/bang-api/app/services/layout/schema.*": ["task", "layout"],
    "github.com/bangwork/bang-api/app/models/action.*": ["task", "action"],
    "github.com/bangwork/bang-api/app/services/batch.*": ["batch", ""],
    "github.com/bangwork/bang-api/app/services/task/executor.*": ["task", ""],
    "github.com/bangwork/bang-api/app/models/objectcount.*": ["objectcount", ""],
    "github.com/bangwork/bang-api/app/services/config.*": ["config", ""],
    "github.com/bangwork/bang-api/app/core/scope/inside/domain.*": ["task", "scope"],
    "github.com/bangwork/bang-api/app/core/project.*": ["project", ""],
    "github.com/bangwork/bang-api/app/models/config.*": ["config", ""],
    "github.com/bangwork/bang-api/app/models/version.*": ["publish_version", ""],
    "github.com/bangwork/bang-api/app/services/queue.*": ["queue", ""],
    "github.com/bangwork/bang-api/app/services/sso.v2/common/manager.*": ["user", "sso"],
    "github.com/bangwork/bang-api/app/services_refactor/task.*": ["task", ""],
    "github.com/bangwork/bang-api/app/models/report/generators.*": ["project", "report"],
    "github.com/bangwork/bang-api/app/services/commonmessage.*": ["message", ""],
    "github.com/bangwork/bang-api/app/models/import_rule.*": ["importer", ""],
    "github.com/bangwork/bang-api/app/services/status.*": ["task", "status"],
    "github.com/bangwork/bang-api/app/models/publishVersion.*": ["publish_version", ""],
    "github.com/bangwork/bang-api/app/utils/audit_log.*": ["audit_log", ""],
    "github.com/bangwork/bang-api/app/controllers_refactor/task/plugin.*": ["plugin", ""],
    "github.com/bangwork/bang-api/app/services/scope_field.*": ["task", "scope"],
    "github.com/bangwork/bang-api/app/services/common/objectlink.*": ["task", "objectlink"],
    "github.com/bangwork/bang-api/app/services/automation/trigger/task.*": ["automation", ""],
    "github.com/bangwork/bang-api/app/services/task/helper.*": ["task", ""],
    "github.com/bangwork/bang-api/app/utils/performanceutils.*": ["performance", ""],
    "github.com/bangwork/bang-api/app/services/layout.*": ["task", "layout"],
    "github.com/bangwork/bang-api/app/services/common/objectlinktype.*": ["task", "objectlink"],
    "github.com/bangwork/bang-api/app/utils/format.*": ["utils", ""],
    "github.com/bangwork/bang-api/app/services/plugin-platform/abilities/implement/task_event_handler.*": ["plugin",
                                                                                                           ""],
    "github.com/bangwork/bang-api/app/services/common/statdog.*": ["statdog", ""],
    "github.com/bangwork/bang-api/app/services/field.*": ["task", "field"],
    "github.com/bangwork/bang-api/app/utils/mime.*": ["resource", "mime"],
    "github.com/bangwork/bang-api/app/services/sso.v2/common/message.*": ["user", "sso"],
    "github.com/bangwork/bang-api/app/services/item/delegates/utils.*": ["item", ""],
    "github.com/bangwork/bang-api/app/models/usergroup.*": ["user", "usergroup"],
    "github.com/bangwork/bang-api/app/services/common/utils.*": ["utils", ""],
    "github.com/bangwork/bang-api/app/core/user.*": ["user", ""],
    "github.com/bangwork/bang-api/app/services/team.*": ["team", ""],
    "github.com/bangwork/bang-api/app/services/eventbus/types.*": ["eventbus", ""],
    "github.com/bangwork/bang-api/app/services/related.*": ["task", "objectlink"],
    "github.com/bangwork/bang-api/app/core/utils/di.*": ["utils", "di"],
    "github.com/bangwork/bang-api/app/models/permission.*": ["permission", ""],
    "github.com/bangwork/bang-api/app/services/import_rule.*": ["importer", ""],
    "github.com/bangwork/bang-api/app/services/open-platform-services/field/script_field.*": ["plugin", ""],
    "github.com/bangwork/bang-api/app/models/commoncomment.*": ["task", "comment"],
    "github.com/bangwork/bang-api/app/services/manhour/generator.*": ["manhour", ""],
    "github.com/bangwork/bang-api/app/models/commonmessage.*": ["message", ""],

    "github.com/bangwork/bang-api/app/services/common/utils.NewValueFixer": ["task", "field"],
    "github.com/bangwork/bang-api/app/services/common/utils.UpdateUserPassword": ["user", ""],

    "github.com/bangwork/bang-api/app/utils.ToExcelColumn": ["importer", ""],
    "github.com/bangwork/bang-api/app/utils.ReadLineByCSVFileOffsetByFilter": ["importer", ""],
    "github.com/bangwork/bang-api/app/utils.ReadLineByFileOffset": ["importer", ""],
    "github.com/bangwork/bang-api/app/utils.ReadLinesByCSVFileOffsetByFilter": ["importer", ""],
    "github.com/bangwork/bang-api/app/utils.ReadNextLineByOffset": ["importer", ""],
    "github.com/bangwork/bang-api/app/utils/format.ConvertXLSXToCSV": ["importer", ""],
    "github.com/bangwork/bang-api/app/utils/format.ConvertXLSXToCSVNewFile": ["importer", ""],

    "github.com/bangwork/bang-api/app/utils.CheckStrongPasswordFormat": ["user", ""],
}


# 例如：app/services/project/field
def get_module_submodule_from_function_call(function_call):
    # 倒序遍历
    sorted_pattern = sorted(FUNCTION_CALL_MODULE_SUBMODULE_PATTERN_MAP.items(), key=lambda x: x[0], reverse=True)
    for pattern in sorted_pattern:
        if fnmatch.fnmatch(function_call, pattern[0]):
            return pattern[1][0], pattern[1][1]
    return "", ""


DIRECTORY_PATH_MODULE_SUBMODULE_PATTERN_MAP = {
    "app/services/project/field*": ["project", "project_field"],
    "app/services/project*": ["project", ""],
    "app/services/filter*": ["project", "filter"],
    "app/services/role*": ["project", "role"],
    "app/services/sprint*": ["project", "sprint"],
    "app/services/component*": ["project", "component"],
    "app/services/dashboard*": ["project", "dashboard"],
    "app/services/report*": ["project", "report"],
    "app/services/rank*": ["project", "sprint"],
    "app/services/container*": ["project", "container"],
    "app/services/common/sprint*": ["project", "sprint"],
    "app/services/common/component*": ["project", "component"],
    "app/services/common/container*": ["project", "container"],
    "app/services/common/filter*": ["project", "filter"],

    "app/core/objectlink*": ["objectlink", ""],
    "app/core/product*": ["product", ""],
    "app/core/publish_version*": ["publish_version", ""],
    "app/core/scope*": ["task", "issuetype"],
    "app/core/task*": ["task", ""],
    "app/core/workflow*": ["task", "workflow"],
    "app/services/activity*": ["ppmtask", ""],
    "app/services/agent*": ["agent", ""],
    # TODO 批量的要继续细分
    "app/services/batch*": ["batch", ""],
    "app/services/batch/add_fields*": ["task", "field"],
    "app/services/batch/import_update*": ["importer", ""],
    "app/services/batch_refactor*": ["batch", ""],
    "app/services/card*": ["project", "card"],
    "app/services/common/activity*": ["ppmtask", ""],
    "app/services/common/field*": ["task", "field"],
    "app/services/common/gantt*": ["ppmtask", "gantt"],
    "app/services/common/issuetype*": ["task", "issuetype"],
    "app/services/common/objectlink*": ["task", "objectlink"],
    "app/services/common/report*": ["project", "report"],
    "app/services/common/status*": ["task", "status"],
    "app/services/common/task*": ["task", ""],
    "app/services/common/template*": ["template", ""],
    "app/services/common/workorder*": ["task", "workorder"],
    "app/services/desk*": ["task", "desk"],
    "app/services/field*": ["task", "field"],
    "app/services/ganttchart*": ["ppmtask", "ganttchart"],
    "app/services/importer*": ["importer", ""],
    "app/services/issuetype*": ["task", "issuetype"],
    "app/services/kanban*": ["project", "kanban"],
    "app/services/layout*": ["task", "layout"],
    "app/services/objectlink*": ["task", "objectlink"],
    "app/services/ones_task*": ["task", ""],
    "app/services/product*": ["product", ""],
    "app/services/program*": ["program", ""],
    "app/services/publishVersion*": ["task", "publish_version"],
    "app/services/scope_field*": ["task", "field"],
    "app/services/status*": ["task", "status"],
    "app/services/tabconfig*": ["task", "tabconfig"],
    "app/services/task*": ["task", ""],
    "app/services/version*": ["task", "publish_version"],
    "app/services/workflow*": ["task", "workflow"],
    "app/services/workorder*": ["task", "workorder"],
    "app/services_refactor/product*": ["product", ""],
    "app/services_refactor/task*": ["task", ""],
    "app/services_refactor/workflow_refactor/handlers*": ["task", "workflow"],
}


def get_module_submodule_from_directory_path(directory_path):
    directory_path = parse_directory_path(directory_path)
    # 先对 DIRECTORY_PATH_MODULE_SUBMODULE_PATTERN_MAP 按照 key 倒序排序，存到数组里
    sorted_pattern = sorted(DIRECTORY_PATH_MODULE_SUBMODULE_PATTERN_MAP.items(), key=lambda x: x[0], reverse=True)
    for pattern in sorted_pattern:
        if fnmatch.fnmatch(directory_path, pattern[0]):
            return pattern[1][0], pattern[1][1]
    return "", ""


# module 名字 map
# 要再加一层子模块的名字映射
MODULE_NAME_MAP = {
    "action": "后置动作",
    "audit_log": "审计日志",
    "automation": "自动化",
    "config": "配置中心",
    "encryption": "加密",
    "organization": "组织",
    "performance": "效能管理",
    "pipeline": "流水线",
    "comment": "工作项动态",
    "desk": "工单",
    "batch": "进度管理器",
    "publish_version": "发布版本",
    "carddelegates": "卡片",
    "card": "卡片",
    "environment": "环境",
    "container": "容器",
    "workorder": "工单",
    "app_platform": "应用平台",
    "auth": "授权",
    "bot": "机器人",
    "cache": "缓存",
    "constraint": "证书",
    "dashboard": "仪表盘",
    "devops": "DevOps",
    "field": "工作项属性",
    "filter": "筛选过滤器",
    "gantt": "甘特图",
    "importer": "导入",
    "issuetype": "工作项类型",
    "layout": "工作项视图",
    "layout_field": "工作项视图",
    "lua": "Lua脚本",
    "manhour": "工时",
    "message": "message消息",
    "notice": "通知",
    "objectlink": "关联工作项",
    "objectlinktype": "关联工作项",
    "permission": "权限",
    "plugin": "插件",
    "program": "项目集",
    "project": "项目",
    "push": "推送",
    "redis": "Redis",
    "resource": "附件",
    "setting": "设置",
    "sprint": "迭代",
    "stamp": "stamp缓存",
    "status": "工作项状态",
    "tabconfig": "工作项视图",
    "task": "工作项",
    "taskrelation": "工作项",
    "team": "团队",
    "template": "模板",
    "testcase": "测试用例",
    "user": "用户",
    "userdomain": "用户域",
    "userguide": "用户指南",
    "wiki": "Wiki",
    "workflow": "工作项工作流",
    "ganttchart": "甘特图",
    "ppmtask": "项目计划",
    "i18n": "多语言",
    "role": "角色",
    "deliverable": "交付物",
    "issue_type_scope_field_constraint": "工作项类型",
    "milestone": "里程碑",
    "product": "产品管理",
    "report": "报表",
    "trigger": "工作项类型",
    "webhook": "Webhook",
    "webhook_filter": "Webhook",
    "webhook_setting": "Webhook",
    "tunnel": "Webhook",
    "kanban": "看板",
    "eventbus": "事件总线",
    "component": "组件",
    "project_field": "项目属性",
}


def filter_references(refs, exclude_patterns):
    return [ref for ref in refs if not any(fnmatch.fnmatch(ref, pattern) for pattern in exclude_patterns)]


def extract_go_info(file_path, exclude_patterns):
    with open(file_path, 'r') as file:
        go_code = file.read()

    # 提取包名称
    package_match = re.search(r'package\s+([\w\d_]+)', go_code)
    package_name = package_match.group(1) if package_match else "N/A"

    # 提取引用的包
    imported_packages = []
    import_match = re.findall(r'import\s+\((.*?)\)', go_code, re.DOTALL)
    if import_match:
        import_block = import_match[0]
        pattern = r'(([a-zA-Z0-9]+\s+)?"[^"]+")'
        import_lines = re.findall(pattern, import_block)
        for match in import_lines:
            if not match:
                continue
            package = match[0]
            # 'jsonUtils "github.com/bangwork/bang-api/app/utils/json"'
            # 先按空格分割，如果不包含空格，说明没有别名
            packages = package.split(" ")
            if len(packages) == 2:
                alias = packages[0]
                package = packages[1]
            else:
                alias = None
                package = packages[0]
            package = package.strip('"')
            # 包含 bangwork 才是我们需要的包
            if "bangwork" in package:
                # if not alias:
                # alias = package.split("/")[-1].replace('"', '')
                imported_packages.append({
                    "package": package,
                    "alias": alias
                })
    # 如果 imported_packages 不为空，排序
    if imported_packages:
        imported_packages = sorted(imported_packages, key=lambda x: x["package"])
    for package_info in imported_packages:
        if package_info["alias"]:
            search_name = f"{package_info['alias']}"
        else:
            search_name = package_info['package'].split("/")[-1].replace('"', '')
        function_calls, constant_references = find_package_function_calls(go_code, search_name)
        package_path = package_info["package"]
        package_info["function_calls"] = filter_references(
            (to_qualified_name(package_path, search_name, v) for v in function_calls), exclude_patterns)
        # 取出函数的原型
        function_declaration = []
        for i, function_call in enumerate(package_info["function_calls"]):
            function_declaration.append(get_function_declaration(function_call))
        package_info["function_declaration"] = function_declaration

        package_info["constant_references"] = filter_references(
            (to_qualified_name(package_path, search_name, v) for v in
             constant_references), exclude_patterns)
    return package_name, imported_packages




def get_function_declaration(function_call):
    # github.com/bangwork/bang-api/app/models/manhour.ListManhoursByTaskUUIDs
    # 把 app/models/manhour 路径提取出来
    # 把 ListManhoursByTaskUUIDs 提取出来
    function_call_parts = function_call.split("bang-api")
    path_name = function_call_parts[-1]
    path_name_parts = path_name.split(".")
    bang_api_root = "/Users/xhs/go/src/github.com/bangwork/bang-api-gomod"
    package_path = bang_api_root + path_name_parts[0]
    function_name = path_name_parts[1]
    # 遍历，从文件里找到 ListManhoursByTaskUUIDs 的声明
    for root, dirs, files in os.walk(package_path):
        for file in files:
            if file.endswith(".go"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    go_code = file.read()
                    function_prototype = extract_function_prototype(go_code, function_name)
                    if function_prototype:
                        return function_prototype
    return ""


def extract_function_prototype(source_code, function_name):
    # 构建匹配函数原型的正则表达式
    pattern = re.compile(fr'\bfunc\b\s+{function_name}\s*\(.*?\)*{{', re.DOTALL)

    # 使用正则表达式匹配函数原型
    match = pattern.search(source_code)

    if match:
        # 返回匹配到的函数原型
        # print(match.group(0))
        return match.group(0)
    else:
        return ""


def write_data_to_excel(data, column_widths, excel_filename):
    wb = openpyxl.Workbook()
    ws = wb.active

    for row in data:
        ws.append(row)

    for i, width in enumerate(column_widths, 1):
        column_letter = openpyxl.utils.get_column_letter(i)
        ws.column_dimensions[column_letter].width = width

    wb.save(excel_filename)


def parse_directory_path(path):
    # /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/app/services/filter
    # app/services/filter
    # 按 / 分割，倒着找到第一个包含 app 的，然后取后面的
    parts = path.split("/")
    for i in range(len(parts) - 1, -1, -1):
        if "app" in parts[i]:
            return "/".join(parts[i:])


def process_directory(directory_path, exclude_patterns):
    data = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".go"):
                file_path = os.path.join(root, file)
                package_name, imported_packages = extract_go_info(file_path, exclude_patterns)
                # 排除 imported_packages 里没有 function_calls 的元素
                imported_packages = [x for x in imported_packages if x["function_calls"]]
                if imported_packages:
                    for i, package_info in enumerate(imported_packages):
                        prefix = package_info['package']
                        for j, function_call in enumerate(package_info["function_calls"]):
                            # 第一行才需要 Directory 和 File
                            module, submodule = get_module_submodule_from_function_call(function_call)
                            this_module, this_submodule = get_module_submodule_from_directory_path(root)
                            # if FUNCTION_CALL_MODULE_MAP.get(function_call):
                            #     module = FUNCTION_CALL_MODULE_MAP.get(function_call)
                            # else:
                            #     module = function_call.split(".")[1].split("/")[-1]
                            # this_module = MODULE_NAME_MAP.get(root.split("/")[-1], root.split("/")[-1])
                            module = MODULE_NAME_MAP.get(module, module)
                            submodule = MODULE_NAME_MAP.get(submodule, submodule)
                            this_module = MODULE_NAME_MAP.get(this_module, this_module)
                            this_submodule = MODULE_NAME_MAP.get(this_submodule, this_submodule)
                            function_declaration = package_info["function_declaration"][j]
                            data.append(
                                [root, file_path, function_call, this_module, this_submodule, module, submodule,
                                 function_declaration])

    return data


# 调用示例，多个目录路径用逗号分隔
# python extract_go_info.py /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/app/services/project,/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/app/services/filter
if __name__ == "__main__":
    all_data = []
    all_data.append(["Directory", "File", "Reference", "ThisModule", "ThisSubmodule", "Module", "Submodule", "FunctionDeclaration"])
    dependency_data = []
    if len(sys.argv) != 2:
        print("Usage: python extract_go_info.py <directory_path>")
        sys.exit(1)
    directory_paths = sys.argv[1].split(",")
    exclude_patterns = EXCLUDE_PATTERNS
    for directory_path in directory_paths:
        directory_path = directory_path.strip()
        for name in MODULE_EXTRA_EXCLUDE_MAP:
            if name in directory_path:
                exclude_patterns = EXCLUDE_PATTERNS + MODULE_EXTRA_EXCLUDE_MAP[name]
                break
        data = process_directory(directory_path, exclude_patterns)
        dependency_data.extend(data)

    # 目录路径后面两级作为文件名
    column_widths = [25, 40, 80, 15, 15, 15, 15, 80]
    output_name = "dependency"
    if len(directory_paths) == 1:
        # 取最后两级作为文件名
        if len(directory_paths[0].split("/")) > 2:
            output_name = directory_paths[0].split("/")[-2] + "_" + directory_paths[0].split("/")[-1]
        else:
            output_name = directory_paths[0].split("/")[-1]
    # 按 Module 列排序，倒序
    # dependency_data = sorted(dependency_data, key=lambda x: x[5], reverse=True)
    # 按 FunctionDeclaration 列排序
    # dependency_data = sorted(dependency_data, key=lambda x: x[7])
    # 按 Reference 列排序
    dependency_data = sorted(dependency_data, key=lambda x: x[2])
    all_data.extend(dependency_data)
    write_data_to_excel(all_data, column_widths, f"{output_name}.xlsx")
