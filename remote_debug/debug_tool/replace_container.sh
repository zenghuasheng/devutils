# build mkdebug from https://github.com/BangWork/ones-tools/blob/master/dev_standalone/mkdebugc/main.go
# 检查容器是否已经是调试模式
docker rm ones_dup
cid=$(docker ps -q --filter "publish=80")
docker stop $cid
chmod +x /tmp/debug_tool/mkdebugc
/tmp/debug_tool/mkdebugc -cid $cid

