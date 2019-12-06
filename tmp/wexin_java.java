OkHttpClient client = new OkHttpClient();

Request request = new Request.Builder()
  .url("https://mp.weixin.qq.com/s?src=11&timestamp=1575250202&ver=2009&signature=piur2vknSD9-I4M2UA76Ep-OHpuHah6ngSBiLN8Y4jjL%2AwI3YlQXIZcs5ggdUT6DGLnReDXMBhpVQ1p2RwYDDRoToYRgCHaJw2SXMxa6E-M=&new=1")
  .get()
  .addHeader("authority", "mp.weixin.qq.com")
  .addHeader("cache-control", "max-age=0,no-cache")
  .addHeader("upgrade-insecure-requests", "1")
  .addHeader("user-agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36")
  .addHeader("sec-fetch-mode", "navigate")
  .addHeader("sec-fetch-user", "?1")
  .addHeader("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3")
  .addHeader("sec-fetch-site", "cross-site")
  .addHeader("accept-encoding", "gzip, deflate, br")
  .addHeader("accept-language", "zh-CN,zh;q=0.9")
  .addHeader("cookie", "pgv_pvi=1434090496; pgv_pvid=3882778600; rewardsn=; wxtokenkey=777")
  .addHeader("Host", "mp.weixin.qq.com")
  .addHeader("Connection", "keep-alive")
  .build();

Response response = client.newCall(request).execute();