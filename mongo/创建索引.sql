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

