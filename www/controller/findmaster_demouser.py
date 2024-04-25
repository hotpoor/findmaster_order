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
from nomagic.cache import get_user, get_users, update_user, get_doc, get_docs, update_doc, get_aim, get_aims, update_aim, get_entity, get_entities, update_entity
from nomagic.cache import BIG_CACHE
from setting import settings
from setting import conn

# from user_agents import parse as uaparse #早年KJ用来判断设备使用

from .base import WebRequest
from .base import WebSocket

from .data import DataWebSocket

class CreateUserAPIHandler(WebRequest):
    def post(self):
        time_now = time.time()
        login = self.get_argument("login","%s"%time_now)
        name = self.get_argument("name","demo user")
        password = self.get_argument("password","123456")

        result = conn.query("SELECT * FROM index_login WHERE login=%s",login)
        if result:
            self.finish({"info":"error","about":"login already in, change another one"})
            return

        user = {
            "name":name,
            "password":password,
        }
        [user_id, user] = nomagic.auth.create_user(user)
        conn.execute("INSERT INTO index_login (login, entity_id,app) VALUES(%s, %s, %s)", login, user_id,"demouser")
        self.finish({
            "info":"ok",
            "about":"success",
            "user_id":user_id,
            "user":user
            })
class LoginAPIHandler(WebRequest):
    def post(self):
        if self.current_user:
            self.finish({"info":"error","about":"already login"})
            return
        login = self.get_argument("login","")
        password = self.get_argument("password","")
        result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
        if not result:
            self.finish({"info":"error","about":"not registered"})
            return
        user_id = result[0].get("entity_id",None)
        user = get_aim(user_id)
        hash_pwd = hashlib.sha1((password + user["salt"]).encode("utf8")).hexdigest()
        if user["password"] != hash_pwd:
            self.finish({"info":"error","about":"Wrong password or login."})
            return
        self.set_secure_cookie("user", tornado.escape.json_encode({"id": user_id, "v":1}),expires=time.time()+63072000,domain=settings.get("cookie_domain"))
        self.finish({"info":"ok","about":"login success"})
class LogoutAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"already not login"})
            return
        self.clear_cookie("user")
        self.finish({"info":"ok","about":"logout success"})
class DataAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"already not login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        self.finish({
            "info":"ok",
            "about":"success",
            "user_id":user_id,
            "user":user
            })
