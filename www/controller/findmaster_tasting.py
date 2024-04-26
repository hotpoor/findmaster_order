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

class DelTastingAPIHandler(WebRequest,BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        obj_id = self.get_argument("tasting_id", "")
        obj_item = self.get_item_by_id("tasting_id")
        if not obj_item:
            self.finish({"info": "error", "about": "Tasting does not exist"})
            return

        result= self.del_item_by_id(user, "tastings", obj_id)
        if result:
            self.finish({"info": "ok", "about": "del tasting success"})
        else :
            self.finish({"info": "error", "about": "tasting_id not in tastings already"})

class UpdateTastingAPIHandler(WebRequest,BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        obj_id = self.get_argument("tasting_id", "")
        obj_item = self.get_item_by_id("tasting_id")
        if not obj_item:
            self.finish({"info": "error", "about": "Tasting does not exist"})
            return

        base_data = self.get_argument("base_data", "")
        if not base_data:
            self.finish({"info": "error", "about": "base_data is empty"})
            return

        base_data_json = json_decode(base_data)
        for k, v in base_data_json.items():
            obj_item[k] = v

        update_aim(obj_id, obj_item)
        self.finish({"info": "ok", "about": "update tasting success"})

class CreateTastingAPIHandler(WebRequest,BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        user_id = self.get_argument("user_id", "")

        tastings = user.get("tastings",[])

        name = self.get_argument("name", "")
        sort = self.get_argument("sort", "")

        if not name:
            self.finish({"info":"error","about":"Name are required"})
            return

        if not sort:
            sort = 1

        tasting = {
            "owner": user_id,
            "name": name,
            "sort": sort,
        }
        [tasting_id,tasting]=nomagic.item.create_item(tasting, "tasting")
        tastings.insert(0,tasting_id)
        user["tastings"]=tastings
        user["updatetime"]=int(time.time())
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"create tasting success"})

class ListTastingAPIHandler(WebRequest,BaseController):
    def post(self):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        items, obj_items, obj_json= self.get_list(user, "tastings")
        self.finish({
            "info": "ok",
            "about": "list success",
            "tasting_list": items,
            "tasting_items": obj_items,
            "tasting_json": obj_json,
        })

