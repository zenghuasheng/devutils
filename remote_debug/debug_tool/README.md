### 1. 打环境时 init_extra_parameters 填上 --expose_ports_string=3306:3306,10086:10086

### 2. 到 dev 机器上命令下载调试工具

```bash
curl -o install.sh http://112.74.98.121:8080/debug_tool/install.sh && chmod +x install.sh && ./install.sh
```