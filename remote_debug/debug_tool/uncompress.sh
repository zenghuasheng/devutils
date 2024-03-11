#!/bin/bash

# 检查是否存在 /tmp/ones-ai-api-core.tar.gz 文件
if [ -f "/tmp/ones-ai-api-core.tar.gz" ]; then
    echo "/tmp/ones-ai-api-core.tar.gz exists."
        # 解压文件
        tar -xzvf /tmp/ones-ai-api-core.tar.gz -C /tmp/

        # 检查解压是否成功
        if [ $? -eq 0 ]; then
            echo "Extraction successful."

            # 复原 ones-ai-api-core
            cp /tmp/bin/ones-ai-api-core /tmp/ones-ai-api-core

            # 检查复原是否成功
            if [ $? -eq 0 ]; then
                echo "Restoration of ones-ai-api-core successful."
                md5sum /tmp/ones-ai-api-core
            else
                echo "Restoration of ones-ai-api-core failed."
            fi
        else
            echo "Extraction failed."
        fi
else
    echo "/tmp/ones-ai-api-core.tar.gz does not exist."
fi