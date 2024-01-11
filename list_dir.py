import os

if __name__ == '__main__':
    main_directory = '/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/app'
    base = os.path.basename(main_directory)
    dirs = []
    for dirpath, dirnames, filenames in os.walk(main_directory):
        dirs.append(dirpath)
    # 替换掉 /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/
    relative_dirs = []
    for item in dirs:
        if item == main_directory:
            continue
        relative_dirs.append(item.replace(os.path.dirname(main_directory) + '/', ''))
    # 按 / 分割，取 len = 2 的
    for item in relative_dirs:
        if len(item.split('/')) != 4:
            continue
        if os.path.dirname(item) != 'app/services/common':
            continue
        # app/services/common
        print(f'        "{item}": ("", ""),')
