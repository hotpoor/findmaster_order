#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import os.path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')

import time
import nomagic
import nomagic.auth
import nomagic.block
import nomagic.supplier
from nomagic.cache import get_user, get_users, update_user, get_doc, get_docs, update_doc, get_aim, get_aims, update_aim, get_entity, get_entities, update_entity

from .base import WebRequest
from tornado.escape import json_encode, json_decode
from .base_controller import BaseController
from .base_controller import BaseControllerV1

class DelSupplierAPIHandler(BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        obj_id = self.get_argument("supplier_id", "")
        obj_item = self.get_item_by_id("supplier_id")
        if not obj_item:
            self.finish({"info": "error", "about": "Supplier does not exist"})
            return

        result= self.del_item_by_id(user, "suppliers", obj_id)
        if result:
            self.finish({"info": "ok", "about": "del supplier success"})
        else :
            self.finish({"info": "error", "about": "supplier_id not in suppliers already"})

class UpdateSupplierAPIHandler(BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        obj_id = self.get_argument("supplier_id", "")
        obj_item = self.get_item_by_id("supplier_id")
        if not obj_item:
            self.finish({"info": "error", "about": "Supplier does not exist"})
            return

        base_data = self.get_argument("base_data", "")
        if not base_data:
            self.finish({"info": "error", "about": "base_data is empty"})
            return

        base_data_json = json_decode(base_data)
        for k, v in base_data_json.items():
            obj_item[k] = v

        update_aim(obj_id, obj_item)
        self.finish({"info": "ok", "about": "update supplier success"})

class CreateSupplierAPIHandler(BaseController):
    def post(self):
        user = super().get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        user_id = self.get_argument("user_id", "")

        suppliers = user.get("suppliers",[])

        country = self.get_argument("country", "")
        region = self.get_argument("region", "")
        subregion = self.get_argument("subregion", "")
        region_grade = self.get_argument("region_grade", "")

        if not (country and region and subregion and region_grade):
            self.finish({"info":"error","about":"Country and region and subregion and region grade are required"})
            return

        supplier = {
            "owner":user_id,
            "country":country,
            "region":region,
            "subregion":subregion,
            "region_grade":region_grade
        }
        [supplier_id,supplier]=nomagic.supplier.create_supplier(supplier)
        suppliers.insert(0,supplier_id)
        user["suppliers"]=suppliers
        user["updatetime"]=int(time.time())
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"create supplier success"})

class ListSupplierAPIHandler(BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        items, obj_items, obj_json= self.get_list(user, "suppliers")
        self.finish({
            "info": "ok",
            "about": "list success",
            "supplier_list": items,
            "supplier_items": obj_items,
            "supplier_json": obj_json,
        })

class ListTestSupplierAPIHandler(WebRequest,BaseControllerV1):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return
        items, obj_items, obj_json= self.get_list(user, "suppliers")
        self.finish({
            "info": "ok",
            "about": "list success",
            "supplier_list": items,
            "supplier_items": obj_items,
            "supplier_json": obj_json,
        })
class ListTest2SupplierAPIHandler(WebRequest):
    def post(self):
        user_id = self.get_argument("user_id")
        user = get_aim(user_id)
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return
        suppliers = user.get("suppliers",[])
        suppliers_items = get_aims(suppliers)
        suppliers_json = {}
        for suppliers_item in suppliers_items:
            supplier_id = suppliers_item[0]
            supplier_entity = suppliers_item[1]
            suppliers_json[supplier_id]=supplier_entity
        self.finish({
            "info":"ok",
            "about":"list success",
            "supplier_list":suppliers,
            "supplier_items":suppliers_items,
            "supplier_json":suppliers_json
            })


