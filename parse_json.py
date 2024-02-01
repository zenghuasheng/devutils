import json

if __name__ == '__main__':
    # 读取 json 文件
    with open('/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/tmp/2.json', 'r') as file:
        data = json.load(file)
        # {
        #   "component": {
        #     "components": [
        #       {
        #         "uuid": "qaxHTLnB",
        #         "template_uuid": "com00014",
        #         "container_type": 1,
        #         "container_uuid": "TqqdgyUbsCq32n8y",
        #         "project_uuid": "TqqdgyUbsCq32n8y",
        #         "parent_uuid": "",
        #         "name": "项目计划",
        #         "name_pinyin": "xiang4mu4ji4hua4",
        #         "desc": "“项目计划”组件包含计划和里程碑，支持通过 WBS 拆解计划，支持对比项目计划的历史版本。",
        #         "type": 2,
        #         "objects": [],
        #         "create_time": 1663151116,
        #         "views": [],
        #         "url_setting": {
        #           "url": ""
        #         }
        #       },
        # 提取里面的 uuid, name，也存为 json 文件
        new_data = []
        for item in data['component']['components']:
            new_data.append({'template_uuid': item['template_uuid'], 'uuid': item['uuid']})
        with open('component_uuids.json', 'w') as file2:
            json.dump(new_data, file2, indent=2, ensure_ascii=False)
