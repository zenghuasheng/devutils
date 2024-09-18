import csv


# 读取 remaining_manhour.txt 文件并忽略最后一行
def read_remaining_manhour(file_path):
    remaining_manhour = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()[3:-1]  # 忽略前两行表头，并且忽略最后一行
        for line in lines:
            if line.strip():  # 忽略空行
                parts = line.split('|')
                task_uuid = parts[1].strip()
                user_uuid = parts[2].strip()
                team_uuid = parts[3].strip()
                hours = int(parts[4].strip())
                manual_deviation = int(parts[5].strip())
                create_time = int(parts[6].strip())
                status = int(parts[7].strip())
                remaining_manhour.append({
                    'task_uuid': task_uuid,
                    'user_uuid': user_uuid,
                    'team_uuid': team_uuid,
                    'hours': hours,
                    'manual_deviation': manual_deviation,
                    'create_time': create_time,
                    'status': status
                })
    return remaining_manhour


# 读取 field_value_history.txt 文件
def read_field_value_history(file_path):
    field_value_history = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()[3:-1]  # 忽略前两行表头，并且忽略最后一行
        for line in lines:
            if line.strip():  # 忽略空行
                parts = line.split('|')
                task_uuid = parts[1].strip()
                # 考虑为 NULL 的情况
                if parts[2].strip() == 'NULL':
                    field_value_hours = None
                else:
                    field_value_hours = int(parts[2].strip())
                field_value_history[task_uuid] = field_value_hours
    return field_value_history


# 合并数据并生成 CSV 文件
def merge_data_and_generate_csv(remaining_manhour, field_value_history, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['task_uuid', 'user_uuid', 'team_uuid', 'hours', 'manual_deviation', 'create_time', 'status',
                      'field_value_hours']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for task in remaining_manhour:
            task_uuid = task['task_uuid']
            # 获取 field_value_hours，若不存在则为 None
            task['field_value_hours'] = field_value_history.get(task_uuid, None)
            writer.writerow(task)


# 主函数
def main():
    remaining_manhour_file = 'remaining_manhour.txt'
    field_value_history_file = 'field_value_history.txt'
    output_file = 'merged_data.csv'

    remaining_manhour = read_remaining_manhour(remaining_manhour_file)
    field_value_history = read_field_value_history(field_value_history_file)

    merge_data_and_generate_csv(remaining_manhour, field_value_history, output_file)
    print(f'Merged CSV file generated: {output_file}')


if __name__ == '__main__':
    main()
