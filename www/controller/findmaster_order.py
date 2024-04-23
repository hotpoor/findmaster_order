#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import os.path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')

import re
import uuid
import time
import random
import string
import hashlib
import urllib
import urllib.parse
import copy
from functools import partial
import logging
import datetime

import markdown
import tornado
import tornado.web
import tornado.escape
import tornado.websocket
import tornado.httpclient
import tornado.gen
from tornado.escape import json_encode, json_decode

import nomagic
import nomagic.auth
import nomagic.block
import nomagic.order
from nomagic.cache import get_user, get_users, update_user, get_doc, get_docs, update_doc, get_aim, get_aims, update_aim, get_entity, get_entities, update_entity
from nomagic.cache import BIG_CACHE
from setting import settings
from setting import conn

# from user_agents import parse as uaparse #早年KJ用来判断设备使用

from .base import WebRequest
from .base import WebSocket

from .data import DataWebSocket

class JsonDataAPIHandler(WebRequest):
    def get(self):
        block_id = self.get_argument("block_id",None)
        block = get_aim(block_id)
        self.finish({
            "info":"ok",
            "about":"success",
            "block_id":block_id,
            "block":block
            })
class DelOrderAPIHandler(WebRequest):
    def post(self):
        user_id = self.get_argument("user_id","")
        order_id = self.get_argument("order_id","")
        user = get_aim(user_id)
        orders = user.get("orders",[])
        trashs = user.get("trashs",[])
        if order_id in orders:
            orders.remove(order_id)
            if order_id not in trashs:
                trashs.insert(0,order_id)
            user["orders"]=orders
            user["trashs"]=trashs
            update_aim(user_id,user)
            self.finish({"info":"ok","about":"del order success"})
            return
        else:
            self.finish({"info":"error","about":"order_id not in orders already"})
class UpdateOrderAPIHandler(WebRequest):
    def post(self):
        user_id = self.get_argument("user_id","")
        order_id = self.get_argument("order_id","")
        key = self.get_argument("key","")
        value = self.get_argument("value","")
        order = get_aim(order_id)
        old_value = order.get(key,"")
        if old_value == value:
            self.finish({"info":"error","about":"same value"})
            return
        order[key]=value
        update_aim(order_id,order)
        self.finish({"info":"ok","about":"update key value success"})
class CreateOrderAPIHandler(WebRequest):
    def post(self):
        user_id = self.get_argument("user_id","")
        user = get_aim(user_id)
        orders = user.get("orders",[])
        base_data = self.get_argument("base_data","{}")
        base_data_json = json_decode(base_data)
        order = {
            "owner":user_id
        }
        for k,v in base_data_json.items():
            order[k]=v
        [order_id,order]=nomagic.order.create_order(order)
        orders.insert(0,order_id)
        user["orders"]=orders
        user["updatetime"]=int(time.time())
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"create order success"})

class ListOrderAPIHandler(WebRequest):
    def post(self):
        user_id = self.get_argument("user_id","")
        user = get_aim(user_id)
        orders = user.get("orders",[])
        orders_items = get_aims(orders)
        orders_json = {}
        for orders_item in orders_items:
            order_id = orders_item[0]
            order_entity = orders_item[1]
            orders_json[order_id]=order_entity
        self.finish({
            "info":"ok",
            "about":"list success",
            "orders":orders,
            "orders_items":orders_items,
            "orders_json":orders_json,
            })
