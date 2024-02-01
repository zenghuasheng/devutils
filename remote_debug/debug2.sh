#!/bin/bash
set -e

case $1 in
        "wiki") bin="ones-wiki-api-core";name="wiki";;
        *) bin="ones-ai-api-core";name="project";;
esac

container_id=$(docker ps -q --filter "publish=80")

# 检查 `dlv` 进程是否存在
if pgrep -x "dlv" >/dev/null; then
  echo "Killing dlv process..."
  pkill -x dlv
else
  echo "dlv process not found."
fi

# 解压二进制
sh /tmp/debug_tool/uncompress.sh

docker cp /tmp/debug_tool/dlv $container_id:/tmp/dlv
md5_new=$(md5sum /tmp/$bin | xargs bash -c 'echo $0')
md5_old=$(docker exec -it $container_id md5sum /usr/local/ones-ai-$name-api/bin/$bin | xargs bash -c 'echo $0')
if [ "$md5_new" != "$md5_old" ]; then
        docker cp /tmp/$bin $container_id:/root/ones/
fi
docker exec $container_id bash -c "set -eux;
        chmod a+x /tmp/dlv;

        if [ -e /root/ones/$bin ]; then
                chmod a+x $bin;
                bakp=/usr/local/ones-ai-$name-api/bin/$bin.bak;
                i=0
                bak=\$bakp.\$i
                while [ -e \$bak ]
                do
                        i=\$((i+1))
                        bak=\$bakp.\$i
                done
                mv /usr/local/ones-ai-$name-api/bin/$bin \$bak;
                mv /root/ones/$bin /usr/local/ones-ai-$name-api/bin/$bin;
        fi
        supervisorctl stop ones-ai-$name-api;
        cd /usr/local/ones-ai-$name-api/ && exec gosu ones /tmp/dlv --listen=:10086 --headless=true --accept-multiclient --api-version=2 exec ./bin/$bin > nohup.out 2>&1 &
        "
# 在Goland IDE中配置远程调试，IP是
ip=$(curl -s ip.me)
echo "*****************************************************"
echo "请在 Goland 中配置远程调试，IP是 $ip，端口是 10086"
echo "*****************************************************"
