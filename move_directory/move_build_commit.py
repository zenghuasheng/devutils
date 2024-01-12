import argparse
import sys

import openpyxl

from move_go_file import move_dir


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Script to move go directory.")
    parser.add_argument("file_path", help="file path", type=str)
    parser.add_argument("--main-dir", help="directory path of bang-api", required=False,
                        default='/Users/xhs/go/src/github.com/bangwork/bang-api-gomod')
    parser.add_argument("--go-path", help="go path", required=False, default='/Users/xhs/go1.17/go1.20.1/bin/go')
    args = parser.parse_args()

    return args


def read_excel(file_path):
    module_list = []

    # 打开 Excel 文件
    workbook = openpyxl.load_workbook(file_path)

    # 选择第一个工作表
    sheet = workbook.active

    # 跳过第一行
    for row in sheet.iter_rows(min_row=2, values_only=True):
        module_list.append(tuple(row))

    # 关闭 Excel 文件
    workbook.close()

    return module_list


if __name__ == '__main__':
    # 从命令行参数中获取文件路径
    args = parse_command_line_args()
    module_list = read_excel(sys.argv[1])
    source_target_list = []
    for item in module_list:
        # 判断是否有 None
        if None in item:
            print(f'映射不完整: {item}')
            continue
        source_target_list.append({
            "source": item[0],
            # 要去掉 app
            "target": item[1] + "/" + item[2] + "/" + item[0].replace("app/", "")
        })
    for item in source_target_list:
        move_dir(args.main_dir, args.go_path, item["source"], item["target"])
