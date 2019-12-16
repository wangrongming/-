#!/bin/sh
ps -ef |grep chrom |awk '{print $2}'|xargs kill -9
cd /root/kf/JD
nohup python3 -u /root/kf/JD/jd_chat_spider.py --start_time $(date -d "yesterday" +%Y-%m-%d) --end_time $(date -d "yesterday" +%Y-%m-%d) > jd_chat_spider.log 2>&1 &