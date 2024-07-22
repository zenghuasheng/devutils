#!/usr/bin/env python3

import sys
import re
from collections import defaultdict
from datetime import datetime, timedelta


def parse_time_granularity(granularity):
    if granularity == "second":
        return "%d/%b/%Y:%H:%M:%S"
    elif granularity == "minute":
        return "%d/%b/%Y:%H:%M"
    elif granularity == "hour":
        return "%d/%b/%Y:%H"
    else:
        print("错误：不支持的时间粒度。请使用 'second'、'minute' 或 'hour'。")
        sys.exit(1)


# 检查是否提供了日志文件路径和时间粒度
granularity = "hour"
if len(sys.argv) < 3:
    print("可设置时间粒度（second、minute、hour）, 默认使用了 hour")
else:
    granularity = sys.argv[2]  # 时间粒度
LOG_FILE = sys.argv[1]  # nginx日志文件路径

# 解析时间粒度格式
time_format = parse_time_granularity(granularity)

# 读取日志文件
with open(LOG_FILE, 'r') as file:
    log_data = file.read()

# 使用正则表达式提取时间戳和URL
log_pattern = re.compile(r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) .*?"(GET|POST|HEAD|OPTIONS) ([^\s\"]+)')
matches = log_pattern.findall(log_data)

if not matches:
    print("未能匹配任何日志条目")
    sys.exit(1)

# 将时间戳转换为datetime对象，并根据粒度统计请求数量
time_counts = defaultdict(int)
for match in matches:
    time_str = match[0]
    log_time = datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S')
    rounded_time_str = log_time.strftime(time_format)
    rounded_time = datetime.strptime(rounded_time_str, time_format)
    time_counts[rounded_time] += 1

# 按时间排序
sorted_times = sorted(time_counts.items())

# 分离时间和计数
times, counts = zip(*sorted_times)

# 文本方式的柱状图
max_count = max(counts)
scale_factor = 50 / max_count  # 控制柱状图的宽度

print(f"时间线分布图（每{granularity}请求数量）：\n")
for time, count in sorted_times:
    bar = '*' * int(count * scale_factor)
    print(f"{time}: {bar} ({count})")