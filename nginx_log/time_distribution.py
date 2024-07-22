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


# 检查是否提供了日志文件路径、接口路径和时间粒度
if len(sys.argv) < 3:
    print("错误：请提供nginx日志文件路径、接口路径和时间粒度（可选，默认为hour）作为命令行参数")
    sys.exit(1)

LOG_FILE = sys.argv[1]  # nginx日志文件路径
api_path = sys.argv[2]  # 接口路径
granularity = sys.argv[3] if len(sys.argv) > 3 else "hour"  # 时间粒度，默认为hour

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

pre_replacements = [
    (r'/api/project/team/[A-Za-z0-9]*', ''),
    (r'/api/project/organization/[A-Za-z0-9]*', ''),
]

pattern_replacements = [
    (r'/task/[A-Za-z0-9]*/info', '/task/{uuid}/info'),
]


def parse_route_path(api_path, url):
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


# 过滤特定接口的日志条目并统计请求数量
time_counts = defaultdict(int)
for match in matches:
    time_str = match[0]
    method = match[1]
    url = match[2]
    route_path = parse_route_path(api_path, url)  # 将 URL 转换为不带参数的路由 path
    if api_path == route_path:
        log_time = datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S')
        rounded_time_str = log_time.strftime(time_format)
        rounded_time = datetime.strptime(rounded_time_str, time_format)
        time_counts[rounded_time] += 1

# 按时间排序
sorted_times = sorted(time_counts.items())

# 分离时间和计数
times, counts = zip(*sorted_times) if sorted_times else ([], [])

# 文本方式的柱状图
if counts:
    max_count = max(counts)
    scale_factor = 50 / max_count  # 控制柱状图的宽度

    print(f"时间线分布图（每{granularity}请求数量，过滤接口：{api_path}）：\n")
    for time, count in sorted_times:
        bar = '*' * int(count * scale_factor)
        print(f"{time}: {bar} ({count})")
else:
    print(f"未找到匹配接口 {api_path} 的请求")
