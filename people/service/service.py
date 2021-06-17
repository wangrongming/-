# !/usr/bin python3
# -*- coding: utf-8 -*-
"""
 @file:service.py
 @time:2021/06/16/16:36
 @detail:
 """
import re

from absl.app import FLAGS
from pymongo import MongoClient


def connect_mongo(mongo_uri):
    user_pass_clean = re.findall("//(.*):(.*)@", mongo_uri)
    if len(user_pass_clean):
        username = user_pass_clean[0][0]
        password = user_pass_clean[0][1]
        final_mongo_url = "mongodb://" + re.sub(f"mongodb://(.*):(.*)@", "", mongo_uri)
        mongo_uri_clean = MongoClient(final_mongo_url)
        mongo_uri_clean.admin.authenticate(username, password)
    else:
        mongo_uri_clean = MongoClient(FLAGS.mongo_uri_clean)
    return mongo_uri_clean


mongo = connect_mongo(FLAGS.mongo)
people_db = mongo.get_database("people")
keyword_col = people_db.get_collection("keyword")
list_col = people_db.get_collection("list")
content_col = people_db.get_collection("content")
position_col = people_db.get_collection("position")
