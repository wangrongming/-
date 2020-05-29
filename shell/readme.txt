1 ps -ef |grep chrom |awk '{print $2}'|xargs kill -9
2 软连接
    建立软链接: ln -s log2013.log link2013
    删除软链接: rm -rf  ./test_chk_ln  (删除软链接，但不删除实际数据)
    eg:

        rm -rf  /etc/localtime
        ln -s ../usr/share/zoneinfo/Asia/Shanghai /etc/localtime
    目标：
        localtime -> ../usr/share/zoneinfo/Asia/Shanghai
        localtime -> /usr/share/zoneinfo/Etc/UTC

        ln -s ../usr/share/zoneinfo/Etc/UTC /etc/localtime
3 yum检测某软件安装包来源
    yum  whatprovides  */lspci

4 修改桥接网络IP 为静态
    /etc/sysconfig/network-scripts/

    TYPE="Ethernet"
    PROXY_METHOD="none"
    BROWSER_ONLY="no"
    ############改动部分开始############
    #动态IP
    #BOOTPROTO="dhcp"

    #静态IP
    BOOTPROTO="static"
    IPADDR=192.168.1.121
    NETMASK=255.255.255.0
    GATEWAY=192.168.1.1
    DNS1=114.114.114.114
    ############改动部分结束############
    DEFROUTE="yes"
    IPV4_FAILURE_FATAL="no"
    IPV6INIT="yes"
    IPV6_AUTOCONF="yes"
    IPV6_DEFROUTE="yes"
    IPV6_FAILURE_FATAL="no"
    IPV6_ADDR_GEN_MODE="stable-privacy"
    NAME="enp0s3"
    UUID="73ab5a69-9070-4c5a-a0b9-c5a6250af943"
    DEVICE="enp0s3"
    ONBOOT="yes"

5 python3 demo.py >/dev/null 2>&1
  解释：标准输出和错误输出全部重定向到 /dev/null中

6 scp data_crawler_latest.tar root@10.0.1.1:/root
7