import sys

import frida


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


#  Java.use   确定hook类
#  MainActivity.onClick.implementation，意思就是Hook前面获取到的类中的onClick方法
jscode = """
Java.perform(function () {
  // Function to hook is defined here
  var MainActivity = Java.use('com.example.seccon2015.rock_paper_scissors.MainActivity');

  // Whenever button is clicked
  var onClick = MainActivity.onClick;
  onClick.implementation = function (v) {
    // Show a message to know that the function got called
    send('onClick');

    // Call the original onClick handler
    onClick.call(this, v);

    // Set our values after running the original onClick handler
    this.m.value = 0;
    this.n.value = 1;
    // this.cnt.value = 999;

    // Log to the console that it's done, and we should have the flag!
    console.log('Done:' + JSON.stringify(this.cnt));
  };
});
"""

js_str = ""
with open("ctf.js", "r", encoding="utf-8") as f:
    for line in f:
        js_str = js_str + line
# jscode = js_str

# process = frida.get_usb_device().attach('com.example.seccon2015.rock_paper_scissors')
# process = frida.get_remote_device().attach('com.example.seccon2015.rock_paper_scissors')  # 参数为包名 # TODO
# process = frida.get_remote_device().attach('com.tmall.wireless')  # 参数为包名 # TODO
process = frida.get_remote_device().attach('com.example.seccon2015.rock_paper_scissors')
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running CTF')
script.load()
sys.stdin.read()
