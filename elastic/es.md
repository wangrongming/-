# 基础说明
`https://cuiqingcai.com/6214.html`  
`node:  节点 `  
`cluster:  一组节点 `  
`index:  索引 小写（db）`  
`document  文档(json):`   
`Fields  字段(json):`   


# python 对接 elasticsearch
`用法链接：https://elasticsearch-py.readthedocs.io/en/master/`  

###创建index：
`from elasticsearch import Elasticsearch`  
`es = Elasticsearch()`  
`result = es.indices.create(index='news', ignore=400)`  
`print(result)`  

# 基础查询语句用法
{
    "query": {
        "match_all": {}
    }
}

{
    "query": {
        "match": {
            "tweet": "elasticsearch"
        }
    }
}


一条复合语句可以将多条语句 — 叶子语句和其它复合语句 — 合并成一个单一的查询语句
{
    "bool": {
        "must": { "match":   { "email": "business opportunity" }},
        "should": [
            { "match":       { "starred": true }},
            { "bool": {
                "must":      { "match": { "folder": "inbox" }},
                "must_not":  { "match": { "spam": true }}
            }}
        ],
        "minimum_should_match": 1
    }
}


