import argparse

from move_go_file import move_dir


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Script to move go directory.")
    parser.add_argument("--main-dir", help="directory path of bang-api", required=False,
                        default='/Users/xhs/go/src/github.com/bangwork/bang-api-gomod')
    parser.add_argument("--go-path", help="go path", required=False, default='/Users/xhs/go1.17/go1.20.1/bin/go')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    # TODO 改成读表格
    module_list = [
        ("app/services/sprint", "project-api", "project"),
    ]
    source_target_list = []
    for item in module_list:
        source_target_list.append({
            "source": item[0],
            # 要去掉 app
            "target": item[1] + "/" + item[2] + "/" + item[0].replace("app/", "")
        })
    args = parse_command_line_args()
    for item in source_target_list:
        move_dir(args.main_dir, args.go_path, item["source"], item["target"])
