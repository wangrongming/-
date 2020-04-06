# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2020/2/28 11:30
 @Auth : 明明
 @IDE  : PyCharm
 """
import json

from elasticsearch import Elasticsearch


class Handler:

    def __init__(self):
        pass

    @staticmethod
    def create_index():
        es = Elasticsearch(hosts=['127.0.0.1'], http_auth=('elastic', 'password'), port=9200)
        result = es.indices.create(index='news', ignore=400)
        print(result)

    @staticmethod
    def del_index():
        es = Elasticsearch(hosts=['127.0.0.1'], http_auth=('elastic', 'password'), port=9200)
        result = es.indices.delete(index='jd_sku_20200101001', ignore=[400, 404])
        print(result)

    @staticmethod
    def insert_data():
        es = Elasticsearch(hosts=['127.0.0.1'], http_auth=('elastic', 'password'), port=9200)
        es.indices.create(index='jd_sku_20200101001', ignore=[400])

        data = {
            "from_url": "https://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_&page=170&stock=0&sort=sort_rank_asc",
            "cat_id": "9987,653,655",
            "brand_id": "",
            "sku": "100001929007",
            "object_id": "5e535075581e0e4100b42a7a",
        }
        result = es.index(index='jd_sku_20200101001', body=data)
        print(result)

    @staticmethod
    def update_data():
        """
        更新 插入
        :return:
        """
        es = Elasticsearch(hosts=['127.0.0.1'], http_auth=('elastic', 'password'), port=9200)
        data = {
            'title': '5e535075581e0e4100b42a7a',
            'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
            'date': '2011-12-17'
        }
        result = es.index(index='news', doc_type='politics', body=data)
        print(result)

    @staticmethod
    def del_data():
        """
        更新 插入
        :return:
        """
        es = Elasticsearch(hosts=['127.0.0.1'], http_auth=('elastic', 'password'), port=9200)
        result = es.delete(index='news', doc_type='politics', id=1)
        print(result)

    @staticmethod
    def query_data():
        """
        查询 插入
        :return:
        """
        es = Elasticsearch(host='127.0.0.1', http_auth=('elastic', 'password'), port=9200)
        dsl = {
            'query': {
                'match_all': {}
            }
        }
        result = es.search(index='jd_sku_20200101001', body=dsl)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    handler = Handler()
    # handler.create_index()
    # handler.del_index()
    # handler.insert_data()
    # handler.update_data()
    handler.query_data()
