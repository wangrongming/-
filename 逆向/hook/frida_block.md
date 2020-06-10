安装参考文件：
    https://mp.weixin.qq.com/s?__biz=Mzg5NzIyMzkzNw==&mid=2247483722&idx=1&sn=fd044018190081c4a47b12ae9fb5d088&chksm=c0745d24f703d43276b5b00707859d14bf6e9bd2872be8f9a3ab7c95419dbad0223d6ab24163&mpshare=1&scene=1&srcid=&sharer_sharetime=1572932600902&sharer_shareid=0235552c1b11bbd74539a5422f295683&key=8a70e2627455295cb0ece5fecdda14b696ef392dd1ccc2e8cde46a4db6eb28377bc535e6d83f0676130b4dd9c5f3058bd1fbe7c1d59338e2ce87c1a9fbf36fd551a61b26b8757012b643d23248c302e6&ascene=1&uin=MjE1Nzc3MTgwMw%3D%3D&devicetype=Windows+10&version=62070158&lang=zh_CN&pass_ticket=0FCcdVutTE0C2n60hCdakso0LDyJQNbz0bhERXEBo9xfI8UnFa1Lf7KCSFd3LN9N

1 安装基础包
    pip install frida-tools

2 一台已经Root了的Android手 Android版本选择在6.0 (手机需要安装的配置)
    1> 需要判断自己手机输入哪一种CPU架构 Device Info HW的
        https://www.coolapk.com/apk/ru.andr7e.deviceinfohw
    2> 下载 frida-server
        https://github.com/frida/frida/releases
    3> adb 命令下载 （Android Debug Bridge 安卓调试桥）
        https://adb.clockworkmod.com/ 暂时无法访问
        https://blog.csdn.net/u010783226/article/details/102912350 下载安装使用
    4> 连接夜神模拟器
        打开开发者模式：连续点击版本号 7次
        adb devices
        adb connect 127.0.0.1:62001

3
    adb root
    adb push frida-server /data/local/tmp/
    adb shell "chmod 755 /data/local/tmp/frida-server"
    adb shell "/data/local/tmp/frida-server &"

到此为止：环境配置完毕
=====================================================================================================================

https://frida.re/docs/examples/android/ 抓包实例


常见问题:
    error:  frida.ServerNotRunningError: unable to connect to remote frida-server
    answer: adb forward tcp:27042 tcp:27042

查看数据线连接设备
    frida-ps -U  

权限不足
    如果你的手机和我的一样，直接这么运行会提示权限不足的话，
    可以先进入adb shell，在执行su命令获取Root权限后（手机端可能会弹出Root授权提示），
    再运行/data/local/tmp/frida-server &启动frida-server。

除了JS代码部分，其他的其实只是个壳子，核心的Hook操作逻辑全在JS代码中，我们在使用时一般只改JS代码部分和指定包名的部分就可以了