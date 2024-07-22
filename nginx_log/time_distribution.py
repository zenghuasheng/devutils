#!/usr/bin/env python3

import sys
import re
from collections import Counter, defaultdict
from datetime import datetime
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 检查是否提供了日志文件路径
if len(sys.argv) < 2:
    print("错误：请提供nginx日志文件路径作为命令行参数")
    sys.exit(1)

LOG_FILE = sys.argv[1]  # nginx日志文件路径

# 读取日志文件
with open(LOG_FILE, 'r') as file:
    log_data = file.read()

# 使用正则表达式提取时间戳和URL
log_pattern = re.compile(r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) .*?"(GET|POST|HEAD|OPTIONS) ([^\s\"]+)')
matches = log_pattern.findall(log_data)

if not matches:
    print("未能匹配任何日志条目")
    sys.exit(1)

# 将时间戳转换为datetime对象，并统计每秒的请求数量
time_counts = defaultdict(int)
for match in matches:
    time_str = match[0]
    log_time = datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S')
    time_counts[log_time] += 1

# 按时间排序
sorted_times = sorted(time_counts.items())

# 分离时间和计数
times, counts = zip(*sorted_times)

# 绘制时间线分布图
plt.figure(figsize=(10, 6))
plt.plot(times, counts, marker='o')
plt.xlabel('Time')
plt.ylabel('Number of Requests')
plt.title('Number of Requests per Second')
plt.gcf().autofmt_xdate()
plt.savefig('output.png')
# plt.show()  # 不再需要
