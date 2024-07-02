from datetime import datetime, timedelta, timezone
import re
from collections import defaultdict

# 日志时间和实际时间差（8小时）
time_diff = timedelta(hours=8)

# 设置日期为2024-06-26，并设定时间段
date_str = "2024-06-26"
start_time_str = date_str + " 14:00:00"
end_time_str = date_str + " 16:00:00"

start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

# 匹配日志行的正则表达式
log_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" "(.*?)"')


def parse_log_line(line):
    # 解析日志行，并返回时间和请求路径
    match = log_pattern.match(line)
    if match:
        ip_address = match.group(1)
        log_time_str = match.group(2)
        request = match.group(3)
        return ip_address, log_time_str, request
    return None, None, None


def read_and_process_logs(log_file_path):
    # 打开日志文件
    with open(log_file_path, 'r') as log_file:
        # 初始化时间段的计数器
        current_time = start_time
        time_interval = timedelta(minutes=5)
        intervals = []

        while current_time <= end_time:
            intervals.append({
                "start_time": current_time,
                "end_time": current_time + time_interval,
                "requests": defaultdict(int)
            })
            current_time += time_interval

        # 逐行读取日志并处理
        for line in log_file:
            ip_address, log_time_str, request = parse_log_line(line.strip())
            if log_time_str and ip_address and request:
                log_time = datetime.strptime(log_time_str, "%d/%b/%Y:%H:%M:%S %z").astimezone(timezone.utc)
                log_time = log_time + time_diff  # 调整日志时间

                # 找到所属的时间段
                for interval in intervals:
                    if interval["start_time"] <= log_time <= interval["end_time"]:
                        interval["requests"][request] += 1
                        break

    return intervals


if __name__ == "__main__":
    log_file_path = "/Users/xhs/task/panic问题/云路/project-web.log"
    intervals = read_and_process_logs(log_file_path)

    # 输出每个时间段的调用情况
    # for interval in intervals:
    #     start_time_str = interval["start_time"].strftime("%H:%M:%S")
    #     end_time_str = interval["end_time"].strftime("%H:%M:%S")
    #     print(f"Time interval {start_time_str} - {end_time_str}:")
    #     for request, count in interval["requests"].items():
    #         print(f"{count} calls to {request}")
    #     print()
    # 统计每个请求在时间段内的出现次数
    request_counts = defaultdict(int)
    for interval in intervals:
        for request, count in interval["requests"].items():
            request_counts[request] += 1

    # 输出请求的调用次数
    for request, count in request_counts.items():
        if count > 3:
            print(f"{count} calls to {request}")
