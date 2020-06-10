//Java.perform(function () {
//  // Function to hook is defined here
//  var MainActivity = Java.use('com.example.seccon2015.rock_paper_scissors.MainActivity'); // TODO 配置类名
//
//  // Whenever button is clicked
//  var onClick = MainActivity.getUnifiedSign;  // 找到软件入口 # TODO
//  onClick.implementation = function (v) {
//    // Show a message to know that the function got called
//    send('getUnifiedSign');
//
//    // Call the original onClick handler
//    onClick.call(this, v);
//
//    // Set our values after running the original onClick handler
//    this.m.value = 0;
//    this.n.value = 1;
////    this.cnt.value = 999;
//
//    // Log to the console that it's done, and we should have the flag!
//    console.log('Done:' + JSON.stringify(this.cnt));
//  };
//});

Java.perform(function () {
  // Function to hook is defined here
  var MainActivity = Java.use('mtopsdk.security.InnerSignImpl'); // TODO 配置类名

  // Whenever button is clicked
  var onClick = MainActivity.getUnifiedSign;  // 找到软件入口 # TODO
  onClick.implementation = function (params, ext,appKey,authCode, useWua) {
    // Show a message to know that the function got called
    send('getUnifiedSign');

    // Call the original onClick handler
    onClick.call(this, params, ext,appKey,authCode, useWua);

    // Set our values after running the original onClick handler


    // Log to the console that it's done, and we should have the flag!
    var input = {
        "appkey":appKey
    }
    console.log("***************")
//    for(var attr in this.mUnifiedSign.getSecurityFactors){
//        console.log(this.mUnifiedSign.getSecurityFactors(input)))
//    }
    console.log(this.mUnifiedSign.getSecurityFactors)
    console.log("***************")

    console.log(this.mUnifiedSign);
  };
});

// 由于sdk使用spdy协议，导致无法抓包 通过hook 将是否使用spdy返回false
//setTimeout(function () {
//     console.log('start——*-*-*-*-*-');
//    Java.perform(function () {
//        var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
//        SwitchConfig.isGlobalSpdySwitchOpen.overload().implementation = function () {
//            var ret = this.isGlobalSpdySwitchOpen.apply(this, arguments);
//            console.log("开启抓包" + ret);
//            return false;
//        }
//    });
//});
