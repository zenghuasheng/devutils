#!/bin/bash
# 这里面写好 cd /tmp
cd /tmp || exit
# 下载调试工具
if [ -f debug_tool.tar.gz ]; then
    echo "debug_tool.tar.gz 已经存在, 如果想更新先删除原有的"
    exit 1
fi
curl -o /tmp/debug_tool.tar.gz http://112.74.98.121:8080/debug_tool.tar.gz
# 解压调试工具
tar -zxvf /tmp/debug_tool.tar.gz
# 替换容器
sh /tmp/debug_tool/replace_container.sh
# 提示用户到本地下载编译打包脚本，把调试的二进制传到 dev 机器上
echo "工具包已经下载到 /tmp/debug_tool 目录，请到本地下载编译打包脚本，把调试的二进制传到 dev 机器上"
echo "本地下载编译脚本命令: "
echo "curl -o build_compress.sh http://112.74.98.121:8080/build_compress.sh"