import os

import tornado.web
import tornado.websocket
import tornado.locale
from nomagic.cache import get_aim, get_aims, update_aim
from tornado.escape import json_encode, json_decode
from .base import WebRequest

class BaseController(WebRequest):

    def get_list(self, user, obj_names):

        items = user.get(obj_names, [])
        obj_items = get_aims(items)
        obj_json = {}
        for obj_item in obj_items:
            o_item = obj_item[0]
            obj_entity = obj_item[1]
            obj_json[o_item] = obj_entity
        return items, obj_items, obj_json

    def get_current_user_by_id(self):
        user_id = self.get_argument("user_id", "")
        return get_aim(user_id)

    def get_item_by_id(self, object_id):
        obj_id = self.get_argument(object_id, "")
        return get_aim(obj_id)

    def del_item_by_id(self, user, obj_name, obj_id):
        obj_items = user.get(obj_name, [])
        trashs = user.get("trashs", [])
        if obj_id in obj_items:
            obj_items.remove(obj_id)
            if obj_id not in trashs:
                trashs.insert(0, obj_id)
            user[obj_name] = obj_items
            user["trashs"] = trashs
            update_aim(obj_id, user)
            return True
        return False

class BaseControllerV1(object):

    def get_list(self, user, obj_names):

        items = user.get(obj_names, [])
        obj_items = get_aims(items)
        obj_json = {}
        for obj_item in obj_items:
            o_item = obj_item[0]
            obj_entity = obj_item[1]
            obj_json[o_item] = obj_entity
        return items, obj_items, obj_json

    def get_current_user_by_id(self):
        user_id = self.get_argument("user_id", "")
        return get_aim(user_id)

    def get_item_by_id(self, object_id):
        obj_id = self.get_argument(object_id, "")
        return get_aim(obj_id)

    def del_item_by_id(self, user, obj_name, obj_id):
        obj_items = user.get(obj_name, [])
        trashs = user.get("trashs", [])
        if obj_id in obj_items:
            obj_items.remove(obj_id)
            if obj_id not in trashs:
                trashs.insert(0, obj_id)
            user[obj_name] = obj_items
            user["trashs"] = trashs
            update_aim(obj_id, user)
            return True
        return False