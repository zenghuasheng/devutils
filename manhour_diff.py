import os

import pandas as pd

# 目录路径
manhour_dir = os.path.expanduser('~/task/修数据/')

# 读取 remaining_hour.csv 和 field_value_history.csv
remaining_hour_df = pd.read_csv(os.path.join(manhour_dir, 'remaining_hour.csv'), header=None)
field_value_history_df = pd.read_csv(os.path.join(manhour_dir, 'field_value_history.csv'), header=None)

# 给列命名，方便后续操作
remaining_hour_df.columns = ['id', 'col2', 'col3', 'value', 'timestamp']
field_value_history_df.columns = ['id', 'col2', 'history_value', 'timestamp']

# 将 field_value_history.csv 中的 id 和 history_value 提取出来
# 并将其合并到 remaining_hour.csv 中的 value 后
merged_df = pd.merge(remaining_hour_df,
                     field_value_history_df[['id', 'history_value']],
                     on='id',
                     how='left')

# 在第四列后面加上 field_value_history.csv 的第三列 history_value，直接附加而不相加
# 保留原始的列顺序并附加新列
final_df = merged_df[['id', 'col2', 'col3', 'value', 'history_value', 'timestamp']]

# 将结果保存到新的 CSV 文件
final_df.to_csv(os.path.join(manhour_dir, 'merged_remaining_hour.csv'), index=False, header=False)

print("合并完成，结果保存在 'merged_remaining_hour.csv' 文件中。")
