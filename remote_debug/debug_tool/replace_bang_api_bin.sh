#!/bin/bash

# 解压
sh /tmp/debug_tool/uncompress.sh

# 备份 ones-ai-api-core
docker exec -it $(docker ps -q --filter "publish=80") /bin/bash -c 'cp /usr/local/ones-ai-project-api/bin/ones-ai-api-core /usr/local/ones-ai-project-api/bin/ones-ai-api-core.bak' &&

# 将新的 ones-ai-api-core 复制到容器
docker cp /tmp/ones-ai-api-core $(docker ps -q --filter "publish=80"):/usr/local/ones-ai-project-api/bin/ones-ai-api-core &&

# 赋予可执行权限
docker exec -it $(docker ps -q --filter "publish=80") /bin/bash -c 'chmod +x /usr/local/ones-ai-project-api/bin/ones-ai-api-core' &&

# 重启应用
docker exec -it $(docker ps -q --filter "publish=80") /bin/bash -c 'supervisorctl restart ones-ai-project-api'

