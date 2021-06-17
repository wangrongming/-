###实际部署时运行步骤：
    1 数据库： 
        a> mongo中新建 text 数据库，
        b> text 数据库中，新建 keyword 集合，里面存入需要采集关键词
        c> text 数据库中，新建 list 集合，并设置唯一索引：db.getCollection("list").ensureIndex({new_id:1},{unique:true}); 
    2  安装依赖
        pip install -r requirements.txt
    3 运行代码：
        python3 run.py --mongo=mongodb://root:Bqi7io41KUIx@192.168.21.22:27017 --start_time='20210615 00:00:00' --interval=3600 --max_page=100 --worker=10

###动态配置参数说明：
    --mongo=mongodb://root:Bqi7io41KUIx@192.168.21.22:27017
    --start_time=20210615 采集新闻最早发布时间
    --end_time==20210615(默认 end_time=start_time+interval)  采集新闻最晚发布时间
    --interval=14400   轮询采集时间范围(秒),默认14400（4小时）
    --max_page=100    默认最大采集页数：100
    --worker=1   默认工作线程：1 (依据服务器配置 调整 1-30，越多运行采集越快)
    --plat=list|detail|comment|reply   启动时采集内容：可单个或多个  单个配置示例：--plat=list
    
###数据格式：以"中考认数"为关键词
	`1 发现不同新闻的采集链接为：http://search.people.cn/s?keyword=%E6%89%8B%E6%9C%BA&st=0&_=1623750355144
	2 采集其中具体某新闻的链接为：http://finance.people.com.cn/n1/2021/0419/c1004-32081225.html
	3 采集后数据如下：`
	
    新闻内容表：
    {
        "news_id":"n1/2021/0419/c1004-32081225",
        "news_source":"强国论坛",  # 新闻来源：人民网-人民日报，强国论坛
        "news_url":"http://finance.people.com.cn/n1/2021/0419/c1004-32081225.html",  # 来源url
        "news_type":"",  # 类别（社会，科技）
        "title":"手机“公摊面积”该谁买单", # bia
        "publish_time":1618791278000, # 新闻发布时间
        "author":"殷呈悦",  # 发布者
        "view_count":"",  # 浏览量
        "tags_count":"", # 点赞量
        "comment_count":"",  # 评论量
        "content":"明明买的是128G的手机，为何显示只有112G的内存？日前，相声演员岳云鹏" 
        "insert_timestamp":1618791278000 # 数据插入时间
    }
        
    新闻评论表：
    {
        "title":"",
        "news_url":"",
        "news_id":"",
        "comment_id":"",
        "comment":{  # 评论
                "comment_author":"",	
                "comment_time":"",	
                "comment_content":"",	
            },
        "insert_timestamp":1618791278000 # 数据插入时间
    }
        
    新闻评论回复表:
    {
        "title":"",
        "news_url":"",
        "news_id":"",
        "comment_id":"",
        "reply_id":"",
        "reply":{  # 评论
                "reply_author":"",	
                "reply_time":"",	
                "reply_content":"",	
            },
        "insert_timestamp":1618791278000 # 数据插入时间
    }
    部分字段,在人民网中无对应字段，存储空字符串

