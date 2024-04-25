import os

import tornado.web
import tornado.websocket
import tornado.locale
from nomagic.cache import get_aim, get_aims, update_aim
from tornado.escape import json_encode, json_decode
from .base import WebRequest

class BaseController(WebRequest):

    def get_list(self, obj_name):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        user_id = self.get_argument("user_id", "")
        user = get_aim(user_id)
        items = user.get(f"{obj_name}s", [])
        obj_items = get_aims(items)
        obj_json = {}
        for obj_item in obj_items:
            o_item = obj_item[0]
            obj_entity = obj_item[1]
            obj_json[o_item] = obj_entity
        self.finish({
            "info": "ok",
            "about": "list success",
            "list": items,
            "items": obj_items,
            "json": obj_json,
        })

    def del_obj(self, obj_name):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        obj_id_str=f"{obj_name}_id"
        obj_id = self.get_argument(obj_id_str, "")
        obj_item = get_aim(obj_id)
        if not obj_item:
            self.finish({"info": "error", "about": f"{obj_name} does not exist"})
            return

        obj_names=f"{obj_name}s"
        obj_items = user.get(obj_names, [])
        trashs = user.get("trashs", [])
        if obj_id in obj_items:
            obj_items.remove(obj_id)
            if obj_id not in trashs:
                trashs.insert(0, obj_id)
            user[obj_names] = obj_items
            user["trashs"] = trashs
            update_aim(obj_id, user)
            self.finish({"info": "ok", "about": f"del {obj_name} success"})
            return
        else:
            self.finish({"info": "error", "about": f"{obj_id_str} not in suppliers already"})

    def update_obj(self, obj_name):
        user = self.get_current_user_by_id()
        if not user:
            self.finish({"info": "error", "about": "User does not exist"})
            return

        obj_id_str = f"{obj_name}_id"
        obj_id = self.get_argument(obj_id_str, "")
        obj_item = get_aim(obj_id)
        if not obj_item:
            self.finish({"info": "error", "about": f"{obj_name} does not exist"})
            return

        base_data = self.get_argument("base_data", "")
        if not base_data:
            self.finish({"info": "error", "about": "base_data is empty"})
            return

        base_data_json = json_decode(base_data)
        for k, v in base_data_json.items():
            obj_item[k] = v

        update_aim(obj_id, obj_item)
        self.finish({"info": "ok", "about": f"update {obj_name} success"})

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