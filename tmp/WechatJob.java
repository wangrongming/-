package com.yuntingai.proxy.job;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.yuntingai.proxy.net.HttpUtils;
import lombok.extern.slf4j.Slf4j;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.protocol.HttpClientContext;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;

import java.io.Closeable;
import java.net.Authenticator;
import java.net.InetSocketAddress;
import java.net.PasswordAuthentication;

/**
 * @author: kaze
 * @date: 2019-04-23
 */
@Slf4j
public class WechatJob {


    private static Proxy getProxy() {

        JSONObject ip = getIp();
        while (!ip.containsKey("trueIp")) {
            ip = getIp();
            System.out.println("========================" + ip);
        }
        System.out.println(ip);
        Proxy proxy = new Proxy();
        proxy.proxyName = ip.getString("userName");
        proxy.proxyPwd = ip.getString("passWord");
        proxy.proxyHost = ip.getString("host");
        proxy.proxyPort = ip.getInteger("port");
        return proxy;

    }

    private static JSONObject getIp() {
        String result = HttpUtils.get("http://proxy.yuntingai.com/proxy/getProxy/90", null);
        JSONObject json = JSON.parseObject(result);
        return json;
    }

    private static class Proxy {

        private String proxyHost;
        private int proxyPort;
        private String proxyName;
        private String proxyPwd;

    }

    private static void close(Closeable closeable) {
        try {
            closeable.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static String wechat() {
        String url = "https://mp.weixin.qq.com/s?src=11&timestamp=1575250202&ver=2009&signature=piur2vknSD9-I4M2UA76Ep-OHpuHah6ngSBiLN8Y4jjL*wI3YlQXIZcs5ggdUT6DGLnReDXMBhpVQ1p2RwYDDRoToYRgCHaJw2SXMxa6E-M=&new=1";
        Proxy proxy = getProxy();
        //用户名和密码验证
        Authenticator.setDefault(new Authenticator() {
            @Override
            protected PasswordAuthentication getPasswordAuthentication() {
                PasswordAuthentication p = new PasswordAuthentication(proxy.proxyName, proxy.proxyPwd.toCharArray());
                return p;
            }
        });
        CloseableHttpClient httpClient = HttpClientBuilder.create().build();
        try {
            InetSocketAddress socksAddr = new InetSocketAddress(proxy.proxyHost, proxy.proxyPort);
            HttpClientContext context = HttpClientContext.create();
            context.setAttribute("socks.address", socksAddr);
            HttpGet httpGet = new HttpGet(url);
            //设置超时时间
            RequestConfig requestConfig = RequestConfig.custom()
                    .setRedirectsEnabled(true)
                    .setConnectTimeout(5000).setConnectionRequestTimeout(1000)
                    .setSocketTimeout(5000).build();
            httpGet.setConfig(requestConfig);
            httpGet.setHeader("authority", "mp.weixin.qq.com");
            httpGet.setHeader("cache-control", "max-age=0,no-cache");
            httpGet.setHeader("upgrade-insecure-requests", "1");
            httpGet.setHeader("user-agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36");
            httpGet.setHeader("sec-fetch-mode", "navigate");
            httpGet.setHeader("sec-fetch-user", "1");
            httpGet.setHeader("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3");
            httpGet.setHeader("sec-fetch-site", "cross-site");
            httpGet.setHeader("accept-encoding", "gzip, deflate, br");
            httpGet.setHeader("accept-language", "zh-CN,zh;q=0.9");
            httpGet.setHeader("accept-encoding", "gzip, deflate, br");
            httpGet.setHeader("cookie", "pgv_pvi=1434090496; pgv_pvid=3882778600; rewardsn=; wxtokenkey=777");
            httpGet.setHeader("Host", "mp.weixin.qq.com");
            httpGet.setHeader("Connection", "keep-alive");
            CloseableHttpResponse response = httpClient.execute(httpGet, context);
            try {
                return EntityUtils.toString(response.getEntity());
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                response.close();
            }
        } catch (Exception e) {
            log.error("请求错误", e);
        } finally {
            close(httpClient);
        }
        return "";
    }

}