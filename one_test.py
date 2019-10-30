import random


def one_test():
    old_cookie = {'l': 'dBIMbwrmqGmTlXf9KOCNdZaF1u7OSIRAguWbLcYMi_5BC1L6Wp7OkZl7gep6VfXftlTBqFNLRKy9-etUikJXJfIpXUJ6CxDc.', 'cookieCheck': '45139', 'uc1': 'cookie14=UoTbnKo97ZokZw%3D%3D', 'isg': 'BAkJYuyzsApgNUz-rOWJoYHlGDxpV_qM4_973at-hfAv8ikE86YNWPegMB9hqpXA', 'cna': '3jU3Fq3o/U4CAT2NQL+R8Ub+', '_tb_token_': '7db37317b3ebe', 'v': '0', 'cookie2': '1a4a9a7d347baacf80bde8b217ee69d7', 't': 'ca794abe039717bcaef5eff36822504c'}

    COOKIE = ''
    for i in old_cookie:
        COOKIE += i + '=' + old_cookie[i] + ';'
    print(COOKIE)


if __name__ == '__main__':
    one_test()

# l=dB_Z0bh4qkSTfrjoBOCanurza77OSIRYYuPzaNbMi_5aq6T6pL7OkZliaF96Vfj1gFYBqFNLRKJ9-etUZnrCIAutZrPGrgsbHFZ_UBMKUxf..;cna=3jU3Fq3o/U4CAT2NQL+R8Ub+;v=0;skt=f0a5c43956572653;sn=oppo%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E7%BE%8A%E7%BE%8A;_tb_token_=5577bf7b3056e;unb=2200784750096;cookie2=1d4d67f6ecccaa7bc7e56bab8f975011;isg=BGpqwUyXw5epRE95Y0MLDSa1u9kG2ukxZOo4GPQjFr1IJwrh3Gs-RbDVsxqezGbN;uc1=cookie14=UoTbnKo97ZZw%2Bw%3D%3D&lng=zh_CN;x=901409638;csg=05c7e161;t=ca794abe039717bcaef5eff36822504c;
# l=-etUikJXJfIpXUJ6CxDc.;cookieCheck=45139;uc1=cookie14=UoTbnKo97ZokZw%3D%3D;isg=BAkJYuyzsApgNUz-rOWJoYHlGDxpV_qM4_973at-hfAv8ikE86YNWPegMB9hqpXA;cna=3jU3Fq3o/U4CAT2NQL+R8Ub+;_tb_token_=7db37317b3ebe;v=0;cookie2=1a4a9a7d347baacf80bde8b217ee69d7;t=ca794abe039717bcaef5eff36822504c;dBIMbwrmqGmTlXf9KOCNdZaF1u7OSIRAguWbLcYMi_5BC1L6Wp7OkZl7gep6VfXftlTBqFNLRKy9