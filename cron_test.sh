#!/bin/bash

PYTHON_PATH=/opt/local/bin/python
SCRIPT_PATH=/Users/xhs/go_workspace/aidemo/cron_test.py
ARGUMENT=54
ERROR_LOG=/Users/xhs/go_workspace/aidemo/cron_test.txt

# 检查 Python 文件是否存在
if [ -x "$PYTHON_PATH" ]; then
    # 如果 Python 文件存在，则执行命令
    echo "exist" >> "$ERROR_LOG"
    "$PYTHON_PATH" "$SCRIPT_PATH" "$ARGUMENT"
else
    # 如果 Python 文件不存在，则将错误信息追加写入文件
    echo "Error: $PYTHON_PATH not found" >> "$ERROR_LOG"
fi
