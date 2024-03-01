#!/bin/bash

# 解压
tar -xzvf /tmp/api.tar.gz -C /tmp/

# 备份 ones-ai-api-core
docker exec -it $(docker ps -q --filter "publish=80") /bin/bash -c 'cp /usr/local/ones-ai-project-api/bin/ones-ai-api-core /usr/local/ones-ai-project-api/bin/ones-ai-api-core.bak' &&

# 将新的 ones-ai-api-core 复制到容器
docker cp /tmp/ones-ai-api-core $(docker ps -q --filter "publish=80"):/usr/local/ones-ai-project-api/bin/ones-ai-api-core &&

# 赋予可执行权限
docker exec -it $(docker ps -q --filter "publish=80") /bin/bash -c 'chmod +x /usr/local/ones-ai-project-api/bin/ones-ai-api-core' &&

# 重启应用
docker exec -it $(docker ps -q --filter "publish=80") /bin/bash -c 'supervisorctl restart ones-ai-project-api' &&

# 备份 ones-project-api
docker exec -it $(docker ps -q --filter "publish=80") /bin/bash -c 'cp /usr/local/ones-project-api/bin/ones-project-api /usr/local/ones-project-api/bin/ones-project-api.bak' &&
# 将新的 ones-project-api 复制到容器
docker cp /tmp/ones-project-api $(docker ps -q --filter "publish=80"):/usr/local/ones-project-api/bin/ones-project-api &&
# 赋予可执行权限
docker exec -it $(docker ps -q --filter "publish=80") /bin/bash -c 'chmod +x /usr/local/ones-project-api/bin/ones-project-api' &&
# 重启应用
docker exec -it $(docker ps -q --filter "publish=80") /bin/bash -c 'supervisorctl restart ones-project-api'
