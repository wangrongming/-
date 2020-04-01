elk:elasticsrarch logstash kibana beats=> elasticStack
1 访问 es 可视化界面 http://192.168.110.140:5601/app/kibana


#安装
1 useradd elsearch
2 新建目录 itcast/es 修改为 elsearch用户目录
    chown elsearch:elsearch itcast/ -R
3 解压安装文件
4 config 配置文件修改:
    conf/elasticsearch.yml
        network.host: 192.168.0.1
    jvm.options:
        -Xms128m
        -Xmx128m
    vim /etc/sysctl.conf # 一个进程在VMA(虚拟内存区域) 创建内存映射最大数量
        cm.max_map_count=655360
5 sysctl -p #使配置生效


# 启动
1 cd bin ./elasticsearch ./elasticsecrch -d #前端 后端启动

# error
    问题1 ：
        max file descriptors [4096] for elasticsearch is too low
    解决1：
        vim /etc/srcurity/limits.conf
        * soft nofile 65536
        * hard nofile 131072
        * soft nproc 2048
        * hard nproc 4096

    问题2 ：
        max number of threads [1024] for user [elsearch] is too low,increase to as least [4096]
    解决2：
        vim /etc/srcurity/limits.d/90-nproc.conf
        * soft nproc 2048
        * hard nproc 4096

    问题3：
        system call filters failed to intall
    解决3：
        vim config/elaticsearch.yml
            bootstrap.system_call_filter:false

