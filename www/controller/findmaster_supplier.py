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

class DelSupplierAPIHandler(WebRequest):
    def post(self):
        super().del_obj("supplier")

class UpdateSupplierAPIHandler(WebRequest):
    def post(self):
        super().update_obj("supplier")

class CreateSupplierAPIHandler(WebRequest):
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

class ListSupplierAPIHandler(WebRequest):
    def post(self):
        super().get_list("supplier")
class ListTestSupplierAPIHandler(WebRequest):
    def post(self):
        self.get_list("supplier")
