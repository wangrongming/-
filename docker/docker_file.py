# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/10/28 16:40
 @Auth : 明明
 @IDE  : PyCharm
 """

# docker exec -it 8270f6009414 /bin/bash

# 0 dicker 安装
# 如果你的系统是Windows 10 64位，那么推荐使用Docker for Windows。 https://docs.docker.com/docker-for-windows/install/。
# linux：https://docs.docker.com/toolbox/toolbox_install_windows/。
# curl -sSL https://get.daocloud.io/docker | sh
# docker run hello-world 测试

# 1 制作镜像
# docker build -t imagename Dockerfilepath
# docker build -t kf .
# docker build -f Dockerfile-base -t kf .

# 2 运行镜像
# docker run -p 9011:9011 -d --name c_name imagename
# c_name为容器名  imagename为打包的镜像名 -p 9011:9011 映射端口号
# docker run -p 9011:9011 -d --name 8270f6009414 ccr.ccs.tencentyun.com/yunting-spider/yunting_spider:19120501


# sudo docker login --username=100010789672 ccr.ccs.tencentyun.com

#  问题总结
#  重启docker Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the d

# dns配置信息

# apiVersion: v1
# kind: Pod
# metadata:
#   namespace: default
#   name: dns-example
# spec:
#   containers:
#     - name: test
#       image: nginx
#   dnsPolicy: "None"
#   dnsConfig:
#     nameservers:
#       - 1.2.3.4
#     searches:
#       - ns1.svc.cluster-domain.example
#       - my.dns.search.suffix
#     options:
#       - name: ndots
#         value: "2"
#       - name: edns0
