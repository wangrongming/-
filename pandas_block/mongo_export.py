# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2020/3/11 22:20
 @IDE  : PyCharm
 """
import pandas as pd
from pymongo import MongoClient


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id and '_id' in df:
        del df['_id']

    print(df)
    return df


if __name__ == '__main__':
    df = read_mongo('eqs', 'tmall_comment_20200311002', {}, '192.168.0.93')
    df.to_excel('tmall_comment.xls', index=False)
