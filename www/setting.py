#!/bin/env python
#coding=utf-8
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

import logging
import uuid

settings = {
    "static_path": os.path.join(os.path.dirname(__file__),"static"),
    "cookie_secret": "hotpoorinchina",
    "cookie_domain": "",
    "QiniuAccessKey": "JBtRerctNpqEK3FgeZcLhRorC-SXkJKbY_esB4Wx",
    "QiniuSecretKey": "PAD3yzsVmqkQCqSV1YVvWM8lVZpJzvGedaOSWDcc",
    "debug": True,
    "wss_port":8100,
    "search_type":["title","desc","tags","doms","product_title","product_desc","sequence"],
    "search_no_str":" !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏.",
    "developers":[]
}

try:
    import torndb as database
    conn = database.Connection("127.0.0.1:3306", "test", "root", "@root2024")
    conn1 = database.Connection("127.0.0.1:3306", "test1", "root", "@root2024")
    conn2 = database.Connection("127.0.0.1:3306", "test2", "root", "@root2024")
    ring = [conn1, conn2]
except:
    pass
