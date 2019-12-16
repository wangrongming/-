# coding:utf-8
import platform

redis_dis_customer = "tmkf:customer"

if 'Win' in platform.system():
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    txt_path = '../data_text'
    headless = False
    cookie = "uc1=cookie14=UoTbnKo0%2FtYBPA%3D%3D;_uab_collina=157183380790835007078158;_tb_token_=355759803d3b7;t=9abe4d87790859801a0b54ffa592b033;log=lty=Ug%3D%3D;cookieCheck=68809;cookie2=10731c5f2d907785df6c774000a1e25d;cna=3jU3Fq3o/U4CAT2NQL+R8Ub+;v=0;isg=BNDQj_IkueLoZ2XnPUEBO_DXoR7iMdrWUshSJsqhnCv-BXCvcqmEcya32YxAzmy7;l=dB_Z0bh4qkSTf8RBBOCanurza77OSIRYYuPzaNbMi_5NN6T671QOkZ9hZF96VjXft9LBqFNLRKJ9-etuZd4lVVSpXUJ1hDc.;"
else:
    REDIS_HOST = '10.1.4.81'
    REDIS_PORT = 6379

    # 内网mongodb—redis库
    MONGO_HOST = '10.1.6.173'
    MONGO_PORT = 28018
    txt_path = '/root/kf/data_text'
    headless = True
    cookie = "_tb_token_=e713145ee1b7d;t=9abe4d87790859801a0b54ffa592b033;everywhere_service_strategy=cco_busi:ads_crmwx_wanxiang_guard_crowd:20191007@1;x=901409638;cookie2=18cb668b8f322a044b8188bec836c393;unb=2200784750096;csg=ce78dbb8;sn=oppo%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E7%BE%8A%E7%BE%8A;skt=fd64b30417e8b3f0;cna=3jU3Fq3o/U4CAT2NQL+R8Ub+;v=0;uc1=cookie14=UoTbnKoyaMk6vw%3D%3D&lng=zh_CN;isg=BFRUA__S9bUg42H6PdoXUDIyJZIGBRaiPmRWGu414F9i2fQjFr1IJwrZ3ZBkOrDv;l=dBgAhIwnqkUdqGqzBOCanurza77OSIRYYuPzaNbMi_5wq6T6DMQOkZ8OxF96VjXfGbTBqFNLRKJ9-etuNII9r7utZrPiSDc.;"
