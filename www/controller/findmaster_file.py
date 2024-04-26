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

import qiniu

class CheckDemouserFileAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info": "error","about": "not login"})
            return
        user_id = self.current_user["id"]
        md5 = self.get_argument("md5",None)
        user = get_aim(user_id)
        if not user or not md5:
            self.finish({"info": "error","about": "no block or md5"})
            return
        files_md5 = user.get("files_md5",[])
        if md5 in files_md5:
            self.finish({"exists":True})
            return
        q = qiniu.Auth(settings["QiniuAccessKey"], settings["QiniuSecretKey"])
        uptoken = q.upload_token("tasterest-cdn")
        self.finish({
            "info":"ok",
            "token": uptoken,
            "exists": False
        })
class AddDemouserFileAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info": "error","about": "not login"})
            return
        user_id = self.current_user["id"]
        md5 = self.get_argument("md5",None)
        user = get_aim(user_id)
        if not user or not md5:
            self.finish({"info": "error","about": "no block or md5"})
            return
        files_md5 = user.get("files_md5",[])
        if md5 not in files_md5:
            self.finish({"info":"error","about":"already insert success","md5":md5})
            return
        files_md5.insert(0,md5)
        user["files_md5"]=files_md5
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"insert success","md5":md5})

# class SecretTokenAPIHandler(WebRequest):
#     def post(self):
#         url = self.get_argument("url",None)
#         expires_time = int(self.get_argument("expires_time","43200"))
#         if not url:
#             self.finish({"info":"error","about":"no url"})
#             return
#         q = qiniu.Auth(settings["QiniuAccessKey"], settings["QiniuSecretKey"])
#         reuslt_url = q.private_download_url(url,expires_time)
#         self.finish({"info":"ok","about":"private download url","url":reuslt_url})


