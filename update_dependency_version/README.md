# 更新依赖版本

背景：目前仓库做了拆分，但是拆分后在 bang-api 还是把 ones-project-api 当做依赖引入，为了保证ones-project-api的版本一致，需要频繁
更新 ones-project-api 的版本，但是手动更新比较麻烦，所以写了一个脚本来自动更新依赖的版本。

# repos.yaml 配置说明

- repositories: 仓库列表
- path: 本地仓库路径
- dependencies: 依赖列表
    - name: 依赖仓库名称

注意顺序，先写最底层的仓库，然后依次往上写

```yaml
repositories:
  ones-api-biz-common:
    path: /Users/xhs/go/src/github.com/bangwork/ones-api-biz-common
  ones-project-api:
    path: /Users/xhs/go/src/github.com/bangwork/ones-project-api
    dependencies:
      - name: ones-api-biz-common
  bang-api:
    path: /Users/xhs/go/src/github.com/bangwork/bang-api-gomod
    dependencies:
      - name: ones-project-api
```

# 使用方法

```shell
python /Users/xhs/go_workspace/aidemo/update_dependency_version/update_repos.py H1042 "commit message"
```

其中 H1042 是分支名，commit message 是提交信息