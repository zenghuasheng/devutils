import json
import yaml
import os


def convert_json_to_yaml(json_file):
    # 读取 JSON 文件内容
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    # 构建输出的 YAML 文件名
    yaml_file = os.path.splitext(json_file)[0] + ".yaml"

    # 写入 YAML 文件内容
    with open(yaml_file, 'w') as f:
        yaml.dump(json_data, f, default_flow_style=False)

    print(f"Conversion completed. YAML file saved as {yaml_file}")


if __name__ == "__main__":
    json_file = "/Users/xhs/task/项目模板/entry.json"  # 你的 JSON 文件名
    convert_json_to_yaml(json_file)
