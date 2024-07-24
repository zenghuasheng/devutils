#!/usr/bin/env python3

import sys
import re
from collections import defaultdict


def parse_log_file(log_file_path):
    with open(log_file_path, 'r') as file:
        log_data = file.read()
    return log_data


def extract_requests(log_data):
    # 正则表达式匹配日志中的时间戳、URL、User-Agent 和请求耗时
    log_pattern = re.compile(
        r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) [^\]]*\] "(GET|POST|HEAD|OPTIONS) ([^\s\"]+) HTTP/1\.1" \d+ \d+ ".*?" "([^"]+)" "([^"]+)" "([^"]+)"'
    )
    matches = log_pattern.findall(log_data)
    return matches


def parse_requests(matches):
    requests = []
    for match in matches:
        time_str = match[0]
        method = match[1]
        url = match[2]
        user_agent = match[3]
        client_ip = match[4]
        request_time = float(match[5])
        requests.append({
            'time': time_str,
            'method': method,
            'url': url,
            'user_agent': user_agent,
            'client_ip': client_ip,
            'request_time': request_time
        })
    return requests


def sort_requests_by_time(requests):
    return sorted(requests, key=lambda x: x['request_time'], reverse=True)


def print_top_requests(requests, top_n=50):
    print(f"Top {top_n} 耗时请求（按请求耗时倒序排列）：\n")
    for i, request in enumerate(requests[:top_n], start=1):
        print(
            f"{i}. Request Time: {request['request_time']}s, Time: {request['time']}, Method: {request['method']}, URL: {request['url']}, User-Agent: {request['user_agent']}, "
            f"Client IP: {request['client_ip']}")


# 检查是否提供了日志文件路径
if len(sys.argv) < 2:
    print("错误：请提供nginx日志文件路径作为命令行参数")
    sys.exit(1)

LOG_FILE = sys.argv[1]  # nginx日志文件路径

log_data = parse_log_file(LOG_FILE)
matches = extract_requests(log_data)

if not matches:
    print("未能匹配任何日志条目")
    sys.exit(1)

requests = parse_requests(matches)
sorted_requests = sort_requests_by_time(requests)
print_top_requests(sorted_requests)
