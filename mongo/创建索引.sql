-- 1 mongo嵌套查询
db.getCollection('jdkf').createIndex({"insert_timestamp": -1})
db.col.createIndex({"title":1,"description":1})

db.col.createIndex({"title":1,"description":-1})
db.col.ensureIndex({"sid": 1}, {unique: true});


db.getCollection('tmkf').createIndex({"insert_timestamp":1})
db.getCollection('tmkf').createIndex({"sid":1})
db.getCollection('tmkf').createIndex({"source_id":1,"cid":1})
db.getCollection('jdkf').createIndex({"spu_sku":1})
db.getCollection('jdkf').createIndex({"waiter":1})

--建立索引
db.getCollection('ai_taobao_promotion').createIndex({"itemId":1,"couponActivityId":1})
db.getCollection('ai_taobao_promotion').createIndex({"itemId":1})
mongo_goods_list = "ai_taobao_goods_list"
mongo_keywords_list = "ai_taobao_keyword_list"
mongo_promotion = "ai_taobao_promotion"


