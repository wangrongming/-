-- 1 mongo嵌套查询

-- 1 mongo嵌套查询
db.storage.find({
    'items.category': {
        $eq: 'food'
    }
})

-- 2 返回一个结果
db.getCollection('jdkf').find(
    {
    'element.chatLogMessageList.content': {
            $eq: '许愿今天发货🙏'
        }
    },
    {
        'items.$': 1
    }
)

-- 3 返回多查询结果
db.storage.aggregate( {
    $project: {
        "items": {
            $filter: {
                input: "$items",
                as: "item",
                cond: {
                    $eq: [ '$$item.category', 'food' ]
                }
            }
        }
    }
} )
--4 模糊查询
db.getCollection('WT_SpareManage').find({"useDate":{"$regex":"2019-02"}})

--5 大于小于等于
db.getCollection('jdkf').find({"insert_timestamp": {"$gt": 1571781600000}}).count()
$gt:大于
$lt:小于
$gte:大于或等于
$lte:小于或等于
$eq

db.getCollection('jdkf').find({"insert_timestamp":{"$gt":1571781600000, "$lt":1571868000000}, "username" : "云听李云杨自营"}).count()
db.getCollection('jdkf').find({"insert_timestamp":{"$gt":1571781600000, "$lt":1571868000000}, "username" : "云听李云杨"}).count()
db.getCollection('tmkf').find({"insert_timestamp":{"$gt":1572214458000, "$lt":1572290058000}}).count()