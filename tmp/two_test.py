import requests

url = "https://club.huawei.com/forum.html"

headers = {
    'Connection': "keep-alive",
    'Cache-Control': "max-age=0",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    'Sec-Fetch-Mode': "navigate",
    'Sec-Fetch-User': "?1",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Sec-Fetch-Site': "same-origin",
    'Referer': "https://club.huawei.com/forum-2901-1.html",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cookie': "_gscu_1109330234=7430576802t4co81; "
              "HWWAFSESID=9150e8eb867d772b3d; "
              "HWWAFSESTIME=1574310085294; "
              "a3ps_2132_saltkey=2S96%2FrCMLj%2BfEWoZrzFO%2FDyixy0RsJlKoTZFxioFpFOPPxj4Y9Wwyyt%2B5nYGVdmV6Hpfg4fhKTaFhfytCUYxqA74z4f%2FSlRv5KkPrbAPMoYG16Vxc7VRsCIufnCrHFoCYXV0aGtleQ%3D%3D; a3ps_2132_lastvisit=1574306487; "
              "a3ps_2132_st_p=0%7C1574310087%7C32f6699b3e713c6bfe251bef347ddeff25154f8f240e33659ce98fa4870aae81; "
              "a3ps_2132_visitedfid=4329; a3ps_2132_viewid=tid_21951424; "
              "Hm_lvt_ac495a6d816d7387c803953f3a2637d0=1574310090; _"
              "pk_cvar.cn.club.vmall.com.7f49=%7B%2210%22%3A%5B%22uid%22%2C%220%22%5D%7D; _"
              "pk_ses.cn.club.vmall.com.7f49=*; _gscbrs_1109330234=1; udmp_cm_sign_1109330234=1; a3ps_2132_acceptCookieTip=2; _dmpa_ref=%5B%22%22%2C%22%22%2C1574310350%2C%22https%3A%2F%2Fclub.huawei.com%2Fforum.html%22%5D; _dmpa_ses=d6fb1081c6d4e1a1dee4bb1b6b886bfd62204260; a3ps_2132_lastact=1574310350%09forum.php%09; a3ps_2132_currentHwLoginUrl=http%3A%2F%2Fclub.huawei.com%2Fcn%2Fforum.html; _pk_id.cn.club.vmall.com.7f49=2ea190a51680c310.1574310090.1.1574310350.1574310090.; _gscs_1109330234=74310090iyvwa411|pv:2; Hm_lpvt_ac495a6d816d7387c803953f3a2637d0=1574310350; _dmpa_ses_time=1574312150584; _dmpa_id=112259eb8ce90c741d4dee14779151574310350670.1574310351.0.1574310351..",
    'cache-control': "no-cache",
}

response = requests.request("GET", url, headers=headers)

print(response.text)
