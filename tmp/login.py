import json
import re
from multiprocessing import dummy


def res(i):
    import requests

    url = "https://rate.taobao.com/detailCommon.htm?auctionNumId=597825722598&userNumId=&ua=123" \
          "%23FjKDbn1HqVKb56bxlDnv8ldEzQXHO1A9926XYQledl%2FHzaHKDWQbdSE%2Fs%2BZj0YqkHA7Xz1ncAT5Kg9SLAg%2BO1ZOm" \
          "%2BUnSsQSUO8zgQaP2ZgfZYk08E7V6VqJk3IKkhnJHqCXZ2zvxknp1ImIOg3TiK9QUMGsakJgMnEszoQZnkKd79JM8MOJmwm" \
          "%2FUZRP4bKOg1tDdF%2Fs4s%2BJHpNZbDNAE30lEWRHODHYJnkHixvipMZ6wtc4We28Nqc7EXo8nUyhr8tnLf%2BFzTmViYi2iEF1vdj" \
          "%2FY46FFAyrMqsBVBRA%2BB4Mc75cdodA4%2BewtmboT2xI4ee%2Fqs9bmKK1Y08va5hxcIPFy2HLjqkZA02rKA8cV" \
          "%2FBSproOPPTk1CQ7esZBGo57irC7VWKvNv%2BUR8fmsBd6b3%2BYc2OMzpX0ftMrTQMMHzm2UfCINeTkeSGSQ7l1f0NHzE" \
          "%2BrFImGLXnXwuoi52rpSUsFHxuJq0Ds15BW6Oxl2Ri0Rqj4VWOEDEUhYZaAs8%2Bz2iG706Whii" \
          "%2FWPKS19FgPgb2ArPD3FTWmXuN6E0G17qZgjMccOarHH9TfamMXwCR9wAbjnq29O8g6XNWlXgPSwnLW%2BJlNnaKLKNIGM98H" \
          "%2FIZ1vW9BLX9EBL2WQ5JiNgO0%3D&callback=json_tbc_rate_summary "

    payload = {}
    headers = {
        'Sec-Fetch-Mode': 'no-cors',
        'Referer': 'https://item.taobao.com/item.htm?spm=a230r.1.14.20.70e06fbej8Es0n&id=613038769411&ns=1&abbucket=5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        # 'Cookie': 't=015de0d4e5b7c01d426ff81efdbbe317; cookie2=155b69699074d002cce1c0452c49b70a; v=0; _tb_token_=e08b561e4360e'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    text = re.sub("\n|\s|\t", "", response.text)
    res = re.findall("json_tbc_rate_summary\((.*)\)", text)
    res_json = json.loads(res[0])
    print(i, res_json)


if __name__ == '__main__':
    pool = dummy.Pool(1)
    pool.map(res, [i for i in range(1, 2)])
    pool.close()
    pool.join()
