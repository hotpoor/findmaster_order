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
import nomagic.item
from nomagic.cache import get_user, get_users, update_user, get_doc, get_docs, update_doc, get_aim, get_aims, update_aim, get_entity, get_entities, update_entity
from nomagic.cache import BIG_CACHE
from setting import settings
from setting import conn

# from user_agents import parse as uaparse #早年KJ用来判断设备使用

from .base import WebRequest
from .base_controller import BaseController
from .base import WebSocket

from .data import DataWebSocket


class DelProductAPIHandler(WebRequest,BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        obj_id = self.get_argument("product_id", "")
        obj_item = self.get_item_by_id("product_id")
        if not obj_item:
            self.finish({"info": "error", "about": "product does not exist"})
            return

        result = self.del_item_by_id(user, "products", obj_id)
        if result:
            self.finish({"info": "ok", "about": "del product success"})
        else:
            self.finish({"info": "error", "about": "product_id not in products already"})

class UpdateProductAPIHandler(WebRequest,BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        obj_id = self.get_argument("product_id", "")
        obj_item = self.get_item_by_id("product_id")
        if not obj_item:
            self.finish({"info": "error", "about": "product does not exist"})
            return

        base_data = self.get_argument("base_data", "")
        if not base_data:
            self.finish({"info": "error", "about": "base_data is empty"})
            return

        base_data_json = json_decode(base_data)
        for k, v in base_data_json.items():
            obj_item[k] = v

        update_aim(obj_id, obj_item)
        self.finish({"info": "ok", "about": "update product success"})

class CreateProductAPIHandler(WebRequest,BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        user_id = self.get_argument("user_id", "")
        products = user.get("products",[])

        name = self.get_argument("name", "")  # 商品标题
        code = self.get_argument("code", "")  # 产品编码
        description = self.get_argument("description", "")  # 商品描述
        images = self.get_argument("images", "")  # 商品轮播图
        details = self.get_argument("details", "")  # 商品详情（长图文）
        price = self.get_argument("price", "")  # 商品价格
        category_id = self.get_argument("category_id", "")  # 产品类别
        supplier_id = self.get_argument("supplier_id", "")  # 生产商
        vintage = self.get_argument("vintage", "")  # 年份
        specification_id = self.get_argument("specification_id", "")  # 规格
        raw_materials_id = self.get_argument("raw_materials_id", "")  # 原材料
        packing_id = self.get_argument("packing_id", "")  # 包装
        tasting_id = self.get_argument("tasting_id", "") # 口味参数
        stock = self.get_argument("stock", "")  # 库存数量
        status = self.get_argument("status", "")  # 上架状态

        if not (name and code and description and images and details and price and category_id and supplier_id and vintage and specification_id and raw_materials_id and packing_id):
            self.finish({"info": "error", "about": "name and code and description and images and details and price and category_id and supplier_id and vintage and specification_id and raw_materials_id and packing_id are required"})
            return

        # 检查类别是否存在
        category_item = self.get_item_by_id("category_id")
        if not category_item:
            self.finish({"info": "error", "about": "Category does not exist"})
        # 检查供应商是否存在
        supplier_item = self.get_item_by_id("supplier_id")
        if not supplier_item:
            self.finish({"error": "error", "about": "Supplier does not exist"})
        # 检查规格是否存在
        specification_item = self.get_item_by_id("specification_id")
        if not specification_item:
            self.finish({"error": "error", "about": "Specification does not exist"})
        # 检查原材料是否存在
        raw_metrials_item = self.get_item_by_id("raw_materials_id")
        if not raw_metrials_item:
            self.finish({"error": "error", "about": "Raw metrials does not exist"})
        # 检查包装是否存在
        packing_item = self.get_item_by_id("packing_id")
        if not packing_item:
            self.finish({"error": "error", "about": "Packing does not exist"})
        # 检查口味是否存在
        tasting_item = self.get_item_by_id("tasting_id")
        if tasting_id and not tasting_item:
            self.finish({"info": "error", "about": "Tasting does not exist"})

        product = {
            "owner":user_id,
            "name":name,
            "code":code,
            "description": description,
            "images": images,
            "details": details,
            "price": price,
            "category_id": category_id,
            "supplier_id": supplier_id,
            "specification_id": specification_id,
            "raw_materials_id": raw_materials_id,
            "packing_id": packing_id,
            "tasting_id": tasting_id,
            "stock":stock,
            "status":status
        }

        [product_id,product]=nomagic.item.create_item(product,"product")
        products.insert(0,product_id)
        user["products"]=products
        user["updatetime"]=int(time.time())
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"create product success"})

class ListProductAPIHandler(WebRequest,BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        items, obj_items, obj_json = self.get_list(user, "products")
        self.finish({
            "info": "ok",
            "about": "list success",
            "product_list": items,
            "product_items": obj_items,
            "product_json": obj_json,
        })
