#!/usr/bin/env python3

import sys
import re


def parse_log_file(log_file_path):
    with open(log_file_path, 'r') as file:
        log_data = file.read()
    return log_data


def extract_requests(log_data):
    # 匹配日志中的整个字符串
    log_pattern = re.compile(
        r'\[IRIS\] (\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) \d{2}/\d{2} - \d{2}:\d{2}:\d{2} \d{3} (\S+) ([\d.]+) (POST|GET|HEAD|OPTIONS) ([^\s]+)'
    )
    matches = log_pattern.findall(log_data)
    return matches


def convert_time_to_ms(time_str):
    # 匹配 ms、µs 和 s 格式，包括带小数点和不带小数点的情况
    ms_pattern = r'(\d+(\.\d+)?)ms'
    us_pattern = r'(\d+(\.\d+)?)µs'
    s_pattern = r'(\d+(\.\d+)?)s'

    match = re.match(ms_pattern, time_str)
    if match:
        total_ms = float(match.group(1))
    else:
        match = re.match(us_pattern, time_str)
        if match:
            total_ms = float(match.group(1)) / 1000
        else:
            match = re.match(s_pattern, time_str)
            if match:
                total_ms = float(match.group(1)) * 1000
            else:
                raise ValueError(f"无法解析时间字符串：{time_str}")

    return total_ms


def parse_requests(matches):
    requests = []
    for match in matches:
        log_time = match[0]
        time_str = match[1]
        client_ip = match[2]
        method = match[3]
        url = match[4]

        # 转换为毫秒
        request_time = convert_time_to_ms(time_str)

        requests.append({
            'log_time': log_time,
            'request_time': request_time,
            'client_ip': client_ip,
            'method': method,
            'url': url
        })
    return requests


def sort_requests_by_time(requests):
    return sorted(requests, key=lambda x: x['request_time'], reverse=True)


def print_top_requests(requests, top_n=50):
    print(f"Top {top_n} 耗时请求（按请求耗时倒序排列）：\n")
    for i, request in enumerate(requests[:top_n], start=1):
        print(
            f"{i}. Request Time: {request['request_time']}ms, Log Time: {request['log_time']}, Method: {request['method']}, URL: {request['url']}, Client IP: {request['client_ip']}")


# 检查是否提供了日志文件路径
if len(sys.argv) < 2:
    print("错误：请提供日志文件路径作为命令行参数")
    sys.exit(1)

LOG_FILE = sys.argv[1]  # 日志文件路径

top_n = 10
if len(sys.argv) > 2:
    top_n = int(sys.argv[2])

log_data = parse_log_file(LOG_FILE)
matches = extract_requests(log_data)

if not matches:
    print("未能匹配任何日志条目")
    sys.exit(1)

requests = parse_requests(matches)
sorted_requests = sort_requests_by_time(requests)
print_top_requests(sorted_requests, top_n)
