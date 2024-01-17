import time

if __name__ == '__main__':
    # 当前时间戳写入 now.txt
    with open('now.txt', 'w') as file:
        file.write(str(time.time()))
    pass
