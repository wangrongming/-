#!/bin/sh
echo tm_chat_spider is not running, start it
ps -ef |grep chrom |awk '{print $2}'|xargs kill -9
cd /root/kf/TMALL/
nohup python3 -u /root/kf/TMALL/tm_chat_spider.py --start_time $(date -d "yesterday" +%Y-%m-%d) --end_time $(date -d "yesterday" +%Y-%m-%d) > tm_chat_spider_log.log 2>&1 &