import os
import pprint

# 获取当前用户的根目录
user_home = os.path.expanduser("~")

# 定义保存文件的路径
env_info_path = os.path.join(user_home, "env_infos.json")

# 如果文件不存在，创建一个新的
# if not os.path.exists(env_info_path):
#     open(env_info_path, 'w').close()

# 原始代码
env_infos = {'key1': 'value1', 'key2': 'value2'}  # 请替换成实际的 env_infos
pp = pprint.PrettyPrinter(indent=4)

# 保存到文件
with open(env_info_path, 'w') as f:
    f.write(pp.pformat(env_infos))