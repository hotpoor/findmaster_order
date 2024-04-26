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
import nomagic.item
from nomagic.cache import get_user, get_users, update_user, get_doc, get_docs, update_doc, get_aim, get_aims, update_aim, get_entity, get_entities, update_entity

from .base import WebRequest
from tornado.escape import json_encode, json_decode
from .base_controller import BaseController

class DelRawMaterialsAPIHandler(WebRequest,BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        obj_id = self.get_argument("raw_materials_id", "")
        obj_item = self.get_item_by_id("raw_materials_id")
        if not obj_item:
            self.finish({"info": "error", "about": "RawMaterials does not exist"})
            return

        result= self.del_item_by_id(user, "raw_materials_list", obj_id)
        if result:
            self.finish({"info": "ok", "about": "del raw_materials success"})
        else :
            self.finish({"info": "error", "about": "raw_materials_id not in raw_materials_list already"})

class UpdateRawMaterialsAPIHandler(WebRequest,BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        obj_id = self.get_argument("raw_materials_id", "")
        obj_item = self.get_item_by_id("raw_materials_id")
        if not obj_item:
            self.finish({"info": "error", "about": "RawMaterials does not exist"})
            return

        base_data = self.get_argument("base_data", "")
        if not base_data:
            self.finish({"info": "error", "about": "base_data is empty"})
            return

        base_data_json = json_decode(base_data)
        for k, v in base_data_json.items():
            obj_item[k] = v

        update_aim(obj_id, obj_item)
        self.finish({"info": "ok", "about": "update raw_materials success"})

class CreateRawMaterialsAPIHandler(WebRequest,BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        user_id = self.get_argument("user_id", "")

        raw_materials_list = user.get("raw_materials_list",[])

        name = self.get_argument("name", "")
        sort = self.get_argument("sort", "")

        if not name:
            self.finish({"info":"error","about":"Name are required"})
            return

        if not sort:
            sort = 1

        raw_materials = {
            "owner": user_id,
            "name": name,
            "sort": sort,
        }
        [raw_materials_id,raw_materials]=nomagic.item.create_item(raw_materials, "raw_materials")
        raw_materials_list.insert(0,raw_materials_id)
        user["raw_materials_list"]=raw_materials_list
        user["updatetime"]=int(time.time())
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"create raw_materials success"})

class ListRawMaterialsAPIHandler(WebRequest,BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        items, obj_items, obj_json= self.get_list(user, "raw_materials_list")
        self.finish({
            "info": "ok",
            "about": "list success",
            "raw_materials_list": items,
            "raw_materials_items": obj_items,
            "raw_materials_json": obj_json,
        })

