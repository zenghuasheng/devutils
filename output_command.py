if __name__ == '__main__':
    # main_dir = '/Users/xhs/go/src/github.com/bangwork/ones-api-biz-common/biz-common'
    main_dir = '/Users/xhs/go/src/github.com/bangwork/ones-project-api'
    source = 'project-api'
    target = 'project-api'
    replace_commands = [
        f"find {main_dir} -type f -name '*.go' -exec sed -i '' 's|\"github\.com/bangwork/bang-api/{source}\"|\"github\.com/bangwork/ones-project-api/{target}\"|g' {{}} +",
        f"find {main_dir} -type f -name '*.go' -exec sed -i '' 's|\"github\.com/bangwork/bang-api/{source}/|\"github\.com/bangwork/ones-project-api/{target}/|g' {{}} +",
    ]
    for replace_command in replace_commands:
        print(replace_command)
