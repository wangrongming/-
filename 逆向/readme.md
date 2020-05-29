# 逆向步骤
`

`

# hook 步骤 
## https://mp.weixin.qq.com/s/bfurT1h32A1bLiBHa73oJA

`
1 安装 pip install frida-tools  &  frida-ps 
2 一台root权限手机(进入开发者模式+允许usb调试) 
3 手机上以Root权限运行一个叫frida-server 
    3.1 系统(windows)+CPU架构（x86,arm,arm64）
    3.2 command（启动frida）adb devices
        如果是模拟器再adb命令前需要运行（adb connect 127.0.0.1:62001）
        adb root
        adb push frida-server /data/local/tmp/ 
        adb shell "chmod 755 /data/local/tmp/frida-server"
        adb shell "/data/local/tmp/frida-server &"
        如果提示权限不足
        adb shell
        su 
        /data/local/tmp/frida-server &
    3.3 frida-ps -U   对usb链接设备进行操作     
4  除了JS代码部分，其他的其实只是个壳子，
   核心的Hook操作逻辑全在JS代码中，我们在使用时一般只改JS代码部分和指定包名的部分就可以了
`


`
常见问题:
    1 error:  frida.ServerNotRunningError: unable to connect to remote frida-server
      answer: adb forward tcp:27042 tcp:27042
              adb forward tcp:27043 tcp:27043
`

`
查找包名：
adb shell pm list packages -3
`