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