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
            total:{$sum:1}
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


db.getCollection('DETAIL_0616').aggregate(
  [
    {
        $match: {
            $and: [
                { category_id: { $in: [
    "50012358",
    "124440001",
    "124406005",
    "50019128",
    "50002664",
    "50008905",
    "121404017",
    "124438001",
    "50012781",
    "50012776",
    "50023591",
    "50010394",
    "50003509",
    "50010616",
    "50025883",
    "50006217",
    "50011167",
    "50022728",
    "1629",
    "50001748",
    "124688002",
    "50005867",
    "50010524",
    "121434004",
    "50011720",
    "50019131",
    "162702",
    "50000852",
    "50011130",
    "50025884",
    "50011127",
    "50015983",
    "124394003",
    "121406004",
    "50014800",
    "50012355",
    "50012372",
    "50012369",
    "121402003",
    "50023573",
    "121450004",
    "121454009",
    "50158002",
    "50012773",
    "50012774",
    "50023594",
    "50012772",
    "50014788",
    "50015396",
    "124200008",
    "50000697",
    "162201",
    "50000671",
    "50010850",
    "162205",
    "50008901",
    "50011277",
    "162104",
    "50008899",
    "50013194",
    "50010159",
    "50008900",
    "121412004",
    "50008898",
    "50000436",
    "50008897",
    "1623",
    "50010167",
    "50000557",
    "50007068",
    "50010539",
    "50013196",
    "3035",
    "50013228",
    "50008904",
    "50022566",
    "50023108",
    "162103",
    "50023107",
    "50011739",
    "50014785",
    "50011718",
    "50013238",
    "50011704",
    "50014798",
    "50013618",
    "50011123",
    "121416004",
    "50011129",
    "50010158",
    "50015984",
    "50010402",
    "50013189",
    "50010520",
    "121466005",
    "121408006",
    "50010527",
    "121484044",
    "50010548",
    "50011153",
    "50010540",
    "121452038",
    "50010160",
    "50006584",
    "121424009",
    "50014799",
    "50012310",
    "50011159",
    "50014803",
    "50010537",
    "50011161",
    "121404005",
    "121366007",
    "50011165",
    "50013933",
    "121472003",
    "50006993",
    "50010531",
    "121462005",
    "50010518",
    "50013932",
    "50014787",
    "50015978",
    "50010519",
    "121404006",
    "50024769",
    "124436002",
    "121394006",
    "121404004",
    "50016450",
    "124422002",
    "124408002",
    "50014786",
    "121382013",
    "121364004",
    "50017082",
    "50012424",
    "50006994",
    "50140003",
    "121484002",
    "50012360",
    "50012325",
    "50013204",
    "50013825",
    "125074041",
    "50006995",
    "50022890",
    "50022892",
    "125024039",
    "50008903",
    "162703",
    "121410016",
    "50014791",
    "50011717",
    "125114030",
    "50011411",
    "125088030",
    "121396007",
    "121462057",
    "50014677",
    "121506001",
    "50023161",
    "124208011",
    "50023096",
    "50023113",
    "162403",
    "50019520",
    "123216004",
    "124230010",
    "162401",
    "50014801",
    "50016143",
    "121416022",
    "50010530",
    "50023111",
    "50011412",
    "50011726",
    "121412007",
    "50006996",
    "162404",
    "121366006",
    "50146004",
    "121450006",
    "124242004",
    "124436001",
    "162116",
    "50005065",
    "124732001",
    "50014512",
    "201232409",
    "124394004",
    "121470015",
    "50012771",
    "124396002",
    "121392024",
    "50019543",
    "121474019",
    "50012777",
    "50012785",
    "121406022",
    "50026651",
    "50008885",
    "121482018",
    "50003510",
    "50014802",
    "50012365",
    "50019541",
    "50008884",
    "50012357",
    "50019549",
    "50019136",
    "50012778",
    "50025885",
    "124426002",
    "124410005",
    "121480022",
    "50008886",
    "50012378",
    "124208012",
    "50012766",
    "50019547",
    "121370019",
    "162402",
    "124402002",
    "124172011",
    "121414024",
    "124216004",
    "50012359",
    "50014089"
] } },
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