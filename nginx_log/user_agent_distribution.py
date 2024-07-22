#!/usr/bin/env python3

import sys
import re
from collections import defaultdict


def parse_route_path(api_path, url):
    pre_replacements = [
        (r'/api/project/team/[A-Za-z0-9]*', ''),
        (r'/api/project/organization/[A-Za-z0-9]*', ''),
    ]
    pattern_replacements = [
        (r'/task/[A-Za-z0-9]*/info', '/task/{uuid}/info'),
    ]

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


# 检查是否提供了日志文件路径和接口路径
if len(sys.argv) < 3:
    print("错误：请提供nginx日志文件路径和接口路径作为命令行参数")
    sys.exit(1)

LOG_FILE = sys.argv[1]  # nginx日志文件路径
api_path = sys.argv[2]  # 接口路径

# 读取日志文件
with open(LOG_FILE, 'r') as file:
    log_data = file.read()

# 使用正则表达式提取时间戳、URL和User-Agent
log_pattern = re.compile(
    r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) [^\]]*\] "(GET|POST|HEAD|OPTIONS) ([^\s\"]+) HTTP/1\.1" \d+ \d+ ".*?" "([^"]+)"'
)
matches = log_pattern.findall(log_data)

if not matches:
    print("未能匹配任何日志条目")
    sys.exit(1)

# 过滤特定接口的日志条目并统计 User-Agent 分布
user_agent_counts = defaultdict(int)
for match in matches:
    time_str = match[0]
    method = match[1]
    url = match[2]
    user_agent = match[3]
    route_path = parse_route_path(api_path, url)  # 将 URL 转换为不带参数的路由 path
    if api_path == route_path:
        user_agent_counts[user_agent] += 1

# 按 User-Agent 分布进行统计
if user_agent_counts:
    print(f"User-Agent 分布（过滤接口：{api_path}）：\n")
    for user_agent, count in user_agent_counts.items():
        print(f"{user_agent}: {count}")
else:
    print(f"未找到匹配接口 {api_path} 的请求")
