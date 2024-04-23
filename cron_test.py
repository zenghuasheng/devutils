import sys
import time

if __name__ == '__main__':
    # 把命令行的输入写入到文件中，追加写
    # with open('cron_test.txt', 'w') as f:
    #     # 先获取输入
    #     input_str = sys.argv[1]
    #     # 追加写
    #     f.write(input_str)
    with open('/Users/xhs/go_workspace/aidemo/cron_test.txt', 'a') as f:
        # 先获取输入
        input_str = sys.argv[1]
        # 写一下时间
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        f.write(' ')
        f.write(input_str)
        f.write('\n')
