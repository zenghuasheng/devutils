#!/bin/bash

# 获取正在运行的容器的 ID
CONTAINER_ID=$(docker ps -q --filter "publish=80")

# 检查是否存在正在运行的容器
if [ -z "$CONTAINER_ID" ]; then
  echo "Error: No running container found with port 80 published."
  exit 1
fi

# 进入容器并执行 mysqldump
docker exec -it "$CONTAINER_ID" bash -c 'mysqldump -uonesdev -pmt8rIJ25wsFYr0 project > /root/ones/project.sql'

# 将备份文件从容器复制到本地
docker cp "$CONTAINER_ID":/root/ones/project.sql /tmp/project.sql

echo "Backup completed successfully. Backup file saved to /tmp/project.sql"
