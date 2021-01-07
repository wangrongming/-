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
    db.getCollection('huafen_club').find({"comment.content":{$regex:"手持，也就这样了"}})

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

-- 排序
db.getCollection('tmkf').find({"insert_timestamp":{"$gt":1572214458000, "$lt":1572290058000}}).sort({"timestamp":-1})

-- 分组查询
db.getCollection('huafen_club').aggregate([
   {$group:{_id:"$comment.content",total:{$sum:1}}}
])
db.getCollection('huafen_club').aggregate([
   {$group:{_id:"$sku",total:{$sum:1}}}
])

--字段存在
db.getCollection('huafen_club').find({ "quan_type": { $exists: true } })

--排序
sort([("level_1_id", 1), ("level_2_id", 1), ("level_3_id", 1)])

--分组统计
db.getCollection('jd_category_20200526').aggregate([
    {
        $group:{
            _id:"$cat_id",
            total:{$sum:1}d
        }
    }
])
-- 据合统计 mongo
db.getCollection('jd_category_20200526').aggregate(
  [
    {
        $group:{
            _id:"$cat_id",
            total:{$sum:1}
        }
    },{
        $group:{
            _id:"$_id.id",
            total:{$sum:1}
        }
    }
  ]
   ,{allowDiskUse:true}
)
-- 联表查询
db.orders.aggregate([
    {
      $lookup:
        {
          from: "inventory",
          localField: "item",
          foreignField: "sku",
          as: "inventory_docs"
        }
   },
   { $match:{"item":{"$eq":"abc"}}},
   { $project:{ "item":1, "inventory_docs":{"sku":1} } }
])

--快捷导出mongo数据
--/opt/mongodb-4.2.3/bin/mongodump -h 10.1.21.4 --port 28018 -d eqs_sales -o /mnt
--zip -r dump_20200602.zip eqs_sales/

--相同SPU 根据时间导出最新一条数据
GET eqs_tmall_goods_sales/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "terms": {
            "spu": [
              "596201072920"
            ]
          }
        }
      ]
    }
  },
  "track_total_hits": true,
  "size": 0,
  "aggs": {
    "aaa": {
      "terms": {
        "field": "spu"
      },
      "aggs": {
        "bbb": {
          "top_hits": {
            "size": 1,
            "sort": [
              {
                "created_at": {
                  "order": "desc"
                }
              }
            ]
          }
        }
      }
    }
  }
}



db.users.aggregate([
    {
        $match: {
            $and: [
                { UserName: { $eq: 'administrator' } },
                { 'Company.CompanyName': { $eq: 'test' } }
            ]
        }
    },
    {
        $lookup: {
            from: "companies",
            localField: "CompanyID",
            foreignField: "CompanyID",
            as: "Company"
        }
    },
])

-- 多字段组合去重查询
db.getCollection('biddings').aggregate([{
        '$group': {
            '_id': {
            'title': '$title',
            'currentDay': '$currentDay'
            },
            'uniqueIds': {
                '$addToSet': '$_id'
            },
            'count': {
                '$sum': 1
            }
        }
    },
    {
        '$match': {
            'count': {
                '$gt': 1
            }
        }
    }
], {
    allowDiskUse: true
})

-- 多字段统计根据某些字段去重后的个数
db.getCollection('jd_category_20200526').aggregate(
  [
    {
        $group:{
            '_id': {
            'title': '$title',
            'currentDay': '$currentDay'
            }
        }
    },{
        $group:{
            _id:"$_id.id",
            total:{$sum:1}
        }
    }
  ]
   ,{allowDiskUse:true}
)
--_id:"$cat_id",
-- total:{$sum:1}


db.getCollection('DETAIL_0616').aggregate(
  [
    {
        $group:{
            _id: {
            'keyword': '$keyword',
            'product_id': '$product_id'
            },
            total:{$sum:1}
        }
    }
  ]
   ,{allowDiskUse:true}
)

--  $match 指定条件查询  $group分组查询，
db.getCollection('DETAIL_0616').aggregate(
  [
    {
        $match: {
            $and: [
                {
                    category_id: { $in: [
                        "50012358",
                        "124440001",
                        "124406005",
                        "50019128",
                        "50014089"
                    ] }
                },
                {shop_name : /官方旗舰店/}
            ]
        }
    },{
        $group:{
            _id:"$category_id",
            total:{$sum:1}
        }
    }
  ]
   ,{allowDiskUse:true}
)


db.getCollection('tmall_detail_once').aggregate(
  [
    {
        $group:{
            _id:"$shop_name",
            total:{$sum:1}
        }
    }
  ]
   ,{allowDiskUse:true}
)

-- 列出列表页名称
db.getCollectionNames()
-- 创建collection
db.createCollection('ai_taobao_keyword_list')

-- 修改店铺名称