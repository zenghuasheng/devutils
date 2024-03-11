#!/bin/bash

function copy_config() {
  container_id=$1

  # 拷贝配置文件到本地
  docker cp "$container_id":/usr/local/ones-ai-project-api/conf/config.json .
  docker cp "$container_id":/usr/local/ones-ai-project-api/conf/config.json ./config.json.bak
}

function update_elasticsearch_config() {
  container_id=$1
  ip=$2

  # 检查配置文件中是否已存在 network.host: 0.0.0.0
  if docker exec "$container_id" grep -q "network.host: 0.0.0.0" /usr/share/elasticsearch/config/elasticsearch.yml; then
    echo "network.host: 0.0.0.0 already exists in the configuration file."
  else
    # 追加 network.host: 0.0.0.0 到配置文件
    docker exec -it "$container_id" bash -c 'echo "network.host: 0.0.0.0" >> /usr/share/elasticsearch/config/elasticsearch.yml'
    echo "Added network.host: 0.0.0.0 to the configuration file."
  fi

  # 重启 Elasticsearch
  docker exec -it "$container_id" supervisorctl restart elasticsearch
  sed -i 's/"es_host":"127.0.0.1"/"es_host":"'$ip'"/' config.json
}

function update_mysql_config() {
  # 获取 Elasticsearch 容器的 ID
  container_id=$1
  ip=$2

  # mysql
  docker exec -it "$container_id" mysql -uroot -pdFdfX8mBhI0G990 -e "GRANT ALL PRIVILEGES ON *.* TO 'onesdev'@'%' IDENTIFIED BY 'mt8rIJ25wsFYr0' WITH GRANT OPTION; FLUSH PRIVILEGES;"
  # 打印连接信息
  echo "mysql -h$ip -P3306 -uonesdev -pmt8rIJ25wsFYr0"
#  sed -i 's/"db_spec":"onesdev:mt8rIJ25wsFYr0@tcp(localhost:3306)\/project?parseTime=true\&loc=Asia%2FShanghai\&charset=utf8mb4"/"db_spec":"onesdev:mt8rIJ25wsFYr0@tcp('$ip':3306)\/project?parseTime=true\&loc=Asia%2FShanghai\&charset=utf8mb4"/' config.json
  #   "wiki_db_spec":"onesdev:mt8rIJ25wsFYr0@tcp(localhost:3306)/wiki?parseTime=true&loc=Asia%2FShanghai&charset=utf8mb4",
#  sed -i 's/"wiki_db_spec":"onesdev:mt8rIJ25wsFYr0@tcp(localhost:3306)\/wiki?parseTime=true\&loc=Asia%2FShanghai\&charset=utf8mb4"/"wiki_db_spec":"onesdev:mt8rIJ25wsFYr0@tcp('$ip':3306)\/wiki?parseTime=true\&loc=Asia%2FShanghai\&charset=utf8mb4"/' config.json
}

function update_log_file() {
  # 检查是否存在 config.json 文件
  if [ ! -f "config.json" ]; then
    echo "config.json 文件不存在"
    exit 1
  fi

  # 替换配置文件中的 log_file 行
  sed -i 's/"log_file":"\/data\/log\/ones-ai-project-api\/ones-ai-project-api.log"/"log_file":".\/ones-ai-project-api.log"/' config.json
  sed -i 's/"local_file_root":"\/data\/ones\/files"/"local_file_root":"\/var\/tmp\/ones-files"/' config.json
  sed -i 's/"plugin_log_file_directory":"\/data\/plugin\/pluginlog"/"plugin_log_file_directory":"\/var\/tmp\/pluginlog"/' config.json
  sed -i 's/"unoconv_exec":"\/usr\/local\/bin\/unoconv"/"unoconv_exec":""/' config.json
  sed -i 's/"enable_plugin": true/"enable_plugin": false/' config.json
  # 	"internal_wiki_api_base_url":"http://47.106.185.102:9002",
}

function replace_cert_path() {
  cert_path=$1
  sed -i 's#"constraint_cert_path": "/data/ones/files/constraint_cert"#"constraint_cert_path": "'$cert_path'"#' config.json
}

function print_config() {
  #    cat config.json
  cp config.json /tmp/config.json
}

function update_clickhouse() {
  container_id=$1
  ip=$2
  # 运行命令在容器内执行配置文件的修改和服务重启
  docker exec -it "$container_id" bash -c '
      # 替换配置文件中的注释行
      sed -i "s/<!-- <listen_host>::<\/listen_host> -->/<listen_host>0.0.0.0<\/listen_host>/" /etc/clickhouse-server/config.xml

      # 停止 ClickHouse 服务
      supervisorctl stop clickhouse

      # 杀死 ClickHouse 进程
      ps -ef | grep clickhouse-server | grep -v watchd | grep -v grep | awk "{print \$2}" | xargs kill -9

      # 重新启动 ClickHouse 服务
      supervisorctl restart clickhouse
  '
  sed -i 's/"clickhouse_addrs": \["localhost:8122"\]/"clickhouse_addrs": \["'$ip:8122'"\]/' config.json
}

function update_kafka() {
  container_id=$1
  ip=$2

  docker exec -it "$container_id" bash -c '
        # 修改 Kafka 配置文件
        sed -i "s/^listeners=PLAINTEXT:\/\/0.0.0.0:9092/# listeners=PLAINTEXT:\/\/0.0.0.0:9092/" /usr/share/kafka/config/server.properties
        sed -i "s/^advertised.listeners=PLAINTEXT:\/\/localhost:9092/# advertised.listeners=PLAINTEXT:\/\/localhost:9092/" /usr/share/kafka/config/server.properties
        echo -e "\nlisteners=INTERNAL:\/\/:9092,EXTERNAL:\/\/:9093" >> /usr/share/kafka/config/server.properties
        echo -e "advertised.listeners=INTERNAL:\/\/:9092,EXTERNAL:\/\/:9093" >> /usr/share/kafka/config/server.properties
        echo -e "listener.security.protocol.map=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT" >> /usr/share/kafka/config/server.properties
        echo -e "inter.broker.listener.name=INTERNAL" >> /usr/share/kafka/config/server.properties
    '

  # 重启 Kafka
  docker exec -it "$container_id" supervisorctl stop kafka
  docker exec -it "$container_id" ps -ef | grep kafka | grep -v grep | awk '{print $2}' | xargs kill -9
  docker exec -it "$container_id" supervisorctl restart kafka
  sed -i 's/"kafka_brokers": \["localhost:9092"\]/"kafka_brokers": \["'$ip':9092"\]/' config.json
}

function update_configs() {
#  cert_path=$1
#  if [[ -z $cert_path ]]; then
#    cert_path="/Users/xhs/Downloads/新版密钥/constraint_cert_new"
#  fi
#
#  echo "证书路径: $cert_path"

  container_id=$(docker ps -q --filter "publish=80")
  ip=$(curl -s ip.me)
#  copy_config "$container_id"
#  update_elasticsearch_config "$container_id" "$ip"
  update_mysql_config "$container_id" "$ip"
#  update_clickhouse "$container_id" "$ip"
#  update_kafka "$container_id" "$ip"
#  update_log_file
#  replace_cert_path "$1"
#  print_config
  # 停止 ones-ai-project-api
#  docker exec -it  "$container_id" /bin/bash -c 'supervisorctl stop ones-ai-project-api'
}

update_configs

