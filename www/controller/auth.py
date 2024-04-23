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
from nomagic.cache import get_user, get_users, update_user, get_doc, get_docs, update_doc, get_aim, get_aims, update_aim, get_entity, get_entities, update_entity
from nomagic.cache import BIG_CACHE
from setting import settings
from setting import conn

# from user_agents import parse as uaparse #早年KJ用来判断设备使用

from .base import WebRequest
from .base import WebSocket
# import pymail
# import qiniu

# import python_jwt as jwt, jwcrypto.jwk as jwk

# class LoginJsWithAppleAPIHandler(WebRequest):
#     @tornado.gen.coroutine
#     def post(self):
#         print(self.request.headers)
#         print(self.request.body)

#         request_list = self.request.body.decode('utf-8').split("&")
#         request_list_dict = {}
#         for item in request_list:
#             item_kv= item.split("=")
#             request_list_dict[item_kv[0]]=item_kv[1]
#         id_token = request_list_dict.get("id_token","")
#         # decoded_token = jwt.decode(id_token,verify=False)
#         print(self.request)
#         header, claims = jwt.process_jwt(id_token)  # 获取信息，但是不验证

#         self.finish({"info":"ok",
#             "about":"login js with apple",
#             "body":self.request.body.decode('utf-8'),
#             "id_token":id_token,
#             # "decoded_token":decoded_token
#             "header":header,
#             "claims":claims,

#             })

# class LoginMobileWithVcodeAPIHandler(WebRequest):
#     @tornado.gen.coroutine
#     def post(self):
#         if self.current_user:
#             user_id = self.current_user["id"]
#             self.finish({"info":"ok","about":"already login","user_id":user_id})
#             return
#         mobile = self.get_argument("mobile",None)
#         country = self.get_argument("country",None)
#         mobile_name = "+%s%s"%(country,mobile)
#         login = "mobile:+%s%s"%(country,mobile)
#         vcode = self.get_argument("vcode",None)
#         redirect = self.get_argument("redirect",None)
#         print("mobile",mobile)
#         print("vcode",vcode)
#         print("country",country)
#         if not (mobile and vcode and country):
#             self.finish({"info":"error","about":"Not enough info."})
#             return
#         time_now = int(time.time())
#         result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
#         if not result:
#             self.finish({"info":"error","about":"Not registered."})
#             return
#         user_id = result[0].get("entity_id",None)
#         user = get_aim(user_id)
#         old_vcode = user.get("vcode","")
#         old_vcode_finishtime = user.get("vcode_finishtime",0)
#         if time_now - old_vcode_finishtime > 0:
#             self.finish({"info":"error","about":"The verification code is expired."})
#             return
#         user["vcode_finishtime"] = time_now
#         user["update_timestamp"] = time.time()
#         if old_vcode != vcode:
#             update_aim(user_id,user)
#             self.finish({"info":"error","about":"Wrong verification code. Please click and get a new one."})
#             return
#         if not redirect:
#             redirect = "/"



#         is_update = False

#         need_keys = [
#             "tasterest_notes",
#             "tasterest_likes",
#             "tasterest_saves",
#             "tasterest_aroma",
#             "tasterest_taste",
#             "tasterest_questions",
#             "tasterest_update_log",

#             "system_chat",
#             "system_comments_collection_chat_id",
#             "system_likeds_and_collected_chat_id",
#             "system_new_followers_chat_id",

#         ]

#         for need_key in need_keys:
#             need_key_item = user.get(need_key,None)
#             if not need_key_item:
#                 group = {
#                     "owner":user_id,
#                     "editors":[user_id],
#                     "subtype":need_key,
#                     "owner_type":"user"
#                 }
#                 [group_id,group]=nomagic.group.create_chat(group)
#                 need_key_item = group_id
#                 user[need_key]=need_key_item
#                 is_update = True

#         if is_update:
#             user["updatetime"]=int(time.time())
#             update_aim(user_id,user)

#         self.set_secure_cookie("user", tornado.escape.json_encode({"id": user_id, "v":1}),expires=time.time()+63072000,domain=settings.get("cookie_domain"))
#         self.finish({"info":"ok","about":"redirect","redirect":redirect,"user_id":user_id})
# class LogoffMobileAskVcodeAPIHandler(WebRequest):
#     @tornado.gen.coroutine
#     def post(self):
#         if not self.current_user:
#             self.finish({"info":"error","about":"not login"})
#             return
#         user_id = self.current_user["id"]
#         user = get_aim(user_id)
#         time_now = int(time.time())
#         check_mobile = self.get_argument("mobile",None)
#         check_country = self.get_argument("country",None)

#         country = user.get("mobile_country",None)
#         mobile = user.get("mobile",None)

#         if "+%s%s"%(check_country,check_mobile) != "+%s%s"%(country,mobile):
#             self.finish({"info":"error","about":"not login mobile info"})
#             return
#         if not country or not mobile:
#             self.finish({"info":"error","about":"error mobile info"})
#             return
#         mobile_name = "+%s%s"%(country,mobile)
#         vcode = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
#         vcode = "%s"%(random.randint(100000, 999999))
#         user["vcode"] = vcode
#         user["vcode_finishtime"] = time_now+60*5
#         user["update_timestamp"] = time.time()
#         update_aim(user_id,user)
#         mobile_send = mobile

#         if country not in ["86"]:
#             # 国际短信
#             mobile_send = mobile_name
#             q = qiniu.QiniuMacAuth(settings["QiniuAccessKey"], settings["QiniuSecretKey"])
#             sms = qiniu.Sms(q)
#             template_id = '1727625091799330816'
#             mobiles = [mobile_send]
#             parameters = {"code":vcode}
#             req, info = sms.sendMessageOversea(template_id, mobiles, parameters)
#             print(req,info)
#             info_json = json_decode(info.text_body)
#             print(info_json)
#             if info_json.get("error",None):
#                 self.finish({"info":"error","about":info_json.get("message","unkown error"),"info_json":json_encode(info_json)})
#                 return
#         else:
#             # 国内短信
#             mobile_send = mobile_send
#             q = qiniu.QiniuMacAuth(settings["QiniuAccessKey"], settings["QiniuSecretKey"])
#             sms = qiniu.Sms(q)
#             template_id = '1727624309821685760'
#             mobiles = [mobile_send]
#             parameters = {"code":vcode}
#             req, info = sms.sendMessage(template_id, mobiles, parameters)
#             print(req,info)
#             info_json = json_decode(info.text_body)
#             print(info_json)
#             if info_json.get("error",None):
#                 self.finish({"info":"error","about":info_json.get("message","unkown error"),"info_json":json_encode(info_json)})
#                 return
#         self.finish({"info":"ok","about":"Verification code is sent to the mobile.","info_json":json_encode(info_json)})

# class LoginMobileAskVcodeAPIHandler(WebRequest):
#     @tornado.gen.coroutine
#     def post(self):
#         mobile = self.get_argument("mobile","")
#         country = self.get_argument("country","")
#         mobile_name = "+%s%s"%(country,mobile)
#         time_now = int(time.time())
#         if mobile_name == "+":
#             self.finish({"info":"error","about":"error mobile"})
#             return
#         login = "mobile:+%s%s"%(country,mobile)
#         result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
#         is_new_user = False
#         if not result:
#             is_new_user = True
#             user = {}
#             password_str = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
#             password_str = "%s"%(random.randint(100000, 999999))
#             user["password"] = password_str
#             user["name"] = mobile_name
#             user["name"] = ""
#             user["mobile"]=mobile
#             user["mobile_country"]=country
#             user["mobile_login"]=login
#             vcode = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
#             vcode = "%s"%(random.randint(100000, 999999))
#             user["vcode"] = vcode
#             user["vcode_finishtime"] = time_now+60*5
#             user["update_timestamp"] = time.time()
#             [new_id, result] = nomagic.auth.create_user(user)
#             user_name = new_id
#             conn.execute("INSERT INTO index_login (login, entity_id,app) VALUES(%s, %s, %s)", login, new_id,"")

#             mobile_send = mobile
#             if country not in ["86"]:
#                 # 国际短信
#                 mobile_send = mobile_name
#                 q = qiniu.QiniuMacAuth(settings["QiniuAccessKey"], settings["QiniuSecretKey"])
#                 sms = qiniu.Sms(q)
#                 template_id = '1727625091799330816'
#                 mobiles = [mobile_send]
#                 parameters = {"code":vcode}
#                 req, info = sms.sendMessageOversea(template_id, mobiles, parameters)
#                 print(req,info)
#                 info_json = json_decode(info.text_body)
#                 print(info_json)
#                 if info_json.get("error",None):
#                     self.finish({"info":"error","about":info_json.get("message","unkown error"),"info_json":json_encode(info_json)})
#                     return
#             else:
#                 # 国内短信
#                 mobile_send = mobile_send
#                 q = qiniu.QiniuMacAuth(settings["QiniuAccessKey"], settings["QiniuSecretKey"])
#                 sms = qiniu.Sms(q)
#                 template_id = '1727624309821685760'
#                 mobiles = [mobile_send]
#                 parameters = {"code":vcode}
#                 req, info = sms.sendMessage(template_id, mobiles, parameters)
#                 print(req,info)
#                 info_json = json_decode(info.text_body)
#                 print(info_json)
#                 if info_json.get("error",None):
#                     self.finish({"info":"error","about":info_json.get("message","unkown error"),"info_json":json_encode(info_json)})
#                     return

#             self.finish({"info":"ok","about":"Verification code is sent to the mobile.","info_json":json_encode(info_json),"is_new_user":is_new_user})
#             return

#         user_id = result[0].get("entity_id")
#         user = get_aim(user_id)
#         vcode = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
#         vcode = "%s"%(random.randint(100000, 999999))
#         user["vcode"] = vcode
#         user["vcode_finishtime"] = time_now+60*5
#         user["update_timestamp"] = time.time()
#         user_name = user.get("nickname",user_id)
#         update_aim(user_id,user)
#         mobile_send = mobile
#         if country not in ["86"]:
#             # 国际短信
#             mobile_send = mobile_name
#             q = qiniu.QiniuMacAuth(settings["QiniuAccessKey"], settings["QiniuSecretKey"])
#             sms = qiniu.Sms(q)
#             template_id = '1727625091799330816'
#             mobiles = [mobile_send]
#             parameters = {"code":vcode}
#             req, info = sms.sendMessageOversea(template_id, mobiles, parameters)
#             print(req,info)
#             info_json = json_decode(info.text_body)
#             print(info_json)
#             if info_json.get("error",None):
#                 self.finish({"info":"error","about":info_json.get("message","unkown error"),"info_json":json_encode(info_json)})
#                 return
#         else:
#             # 国内短信
#             mobile_send = mobile_send
#             q = qiniu.QiniuMacAuth(settings["QiniuAccessKey"], settings["QiniuSecretKey"])
#             sms = qiniu.Sms(q)
#             template_id = '1727624309821685760'
#             mobiles = [mobile_send]
#             parameters = {"code":vcode}
#             req, info = sms.sendMessage(template_id, mobiles, parameters)
#             print(req,info)
#             info_json = json_decode(info.text_body)
#             print(info_json)
#             if info_json.get("error",None):
#                 self.finish({"info":"error","about":info_json.get("message","unkown error"),"info_json":json_encode(info_json)})
#                 return
#         self.finish({"info":"ok","about":"Verification code is sent to the mobile.","info_json":json_encode(info_json)})

# class LogoffEmailAskVcodeAPIHandler(WebRequest):
#     @tornado.gen.coroutine
#     def post(self):
#         if not self.current_user:
#             self.finish({"info":"error","about":"not login"})
#             return
#         time_now = int(time.time())
#         user_id = self.current_user["id"]
#         user = get_aim(user_id)
#         email = user.get("email",None)
#         check_email = self.get_argument("email","")
#         if check_email != email:
#             self.finish({"info":"error","about":"not user email"})
#             return
#         if not email:
#             self.finish({"info":"error","about":"user without email"})
#             return
#         vcode = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
#         vcode = "%s"%(random.randint(100000, 999999))
#         user["vcode"] = vcode
#         user["vcode_finishtime"] = time_now+60*5
#         user["update_timestamp"] = time.time()
#         user_name = user.get("nickname",user_id)
#         user_name = "Digitaste, Account Deletion Verification Code"
#         email_subject = "Your verification code - Account Deletion"
#         update_aim(user_id,user)
#         self.finish({"info":"ok","about":"Verification code is sent to the email."})
#         pymail.send_email_vcode("noreply@digitaste.ai", email, email_subject, "digitaste123!",vcode,"https://tasterest.xialiwei.com",user_name)
# class LoginEmailAskVcodeAPIHandler(WebRequest):
#     @tornado.gen.coroutine
#     def post(self):
#         email = self.get_argument("email","")
#         login = email
#         email_subject = "Your verification code - Login"
#         time_now = int(time.time())
#         if not pymail.check_email(email):
#             self.finish({"info":"error","about":"Wrong email address."})
#             return
#         result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
#         is_new_user = False
#         if not result:
#             is_new_user = True
#             user = {}
#             password_str = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
#             password_str = "%s"%(random.randint(100000, 999999))
#             user["password"] = password_str
#             user["name"] = login.split("@")[0]
#             user["name"] = ""
#             user["email"]=email
#             vcode = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
#             vcode = "%s"%(random.randint(100000, 999999))
#             user["vcode"] = vcode
#             user["vcode_finishtime"] = time_now+60*5
#             user["update_timestamp"] = time.time()
#             [new_id, result] = nomagic.auth.create_user(user)
#             user_name = "Welcome to Digitaste"
#             conn.execute("INSERT INTO index_login (login, entity_id,app) VALUES(%s, %s, %s)", login, new_id,"")
#             self.finish({"info":"ok","about":"Verification code is sent to the email."})
#             pymail.send_email_vcode("noreply@digitaste.ai", email, email_subject, "digitaste123!",vcode,"https://tasterest.xialiwei.com",user_name)
#             return
#         user_id = result[0].get("entity_id")
#         user = get_aim(user_id)
#         vcode = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
#         vcode = "%s"%(random.randint(100000, 999999))
#         user["vcode"] = vcode
#         user["vcode_finishtime"] = time_now+60*5
#         user["update_timestamp"] = time.time()
#         user_name = user.get("nickname",user_id)
#         user_name = "Welcome to Digitaste"
#         update_aim(user_id,user)
#         self.finish({"info":"ok","about":"Verification code is sent to the email.","is_new_user":is_new_user})
#         pymail.send_email_vcode("noreply@digitaste.ai", email, email_subject, "digitaste123!",vcode,"https://tasterest.xialiwei.com",user_name)
        
# class LoginEmailWithVcodeAPIHandler(WebRequest):
#     @tornado.gen.coroutine
#     def post(self):
#         if self.current_user:
#             user_id = self.current_user["id"]
#             self.finish({"info":"ok","about":"already login","user_id":user_id})
#             return
#         email = self.get_argument("email",None)
#         login = email
#         vcode = self.get_argument("vcode",None)
#         redirect = self.get_argument("redirect",None)
#         if not (email and vcode):
#             self.finish({"info":"error","about":"Not enough info."})
#             return
#         if not pymail.check_email(email):
#             self.finish({"info":"error","about":"Wrong email address."})
#             return
#         time_now = int(time.time())
#         result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
#         if not result:
#             self.finish({"info":"error","about":"Not registered."})
#             return
#         user_id = result[0].get("entity_id",None)
#         user = get_aim(user_id)

#         old_vcode = user.get("vcode","")
#         old_vcode_finishtime = user.get("vcode_finishtime",0)
#         if time_now - old_vcode_finishtime > 0:
#             self.finish({"info":"error","about":"The verification code is expired."})
#             return
#         user["vcode_finishtime"] = time_now
#         user["update_timestamp"] = time.time()
#         if old_vcode != vcode:
#             update_aim(user_id,user)
#             self.finish({"info":"error","about":"Wrong verification code. Please click and get a new one."})
#             return
#         if not redirect:
#             redirect = "/"


#         is_update = False

#         need_keys = [
#             "tasterest_notes",
#             "tasterest_likes",
#             "tasterest_saves",
#             "tasterest_aroma",
#             "tasterest_taste",
#             "tasterest_questions",
#             "tasterest_update_log",

#             "system_chat",
#             "system_comments_collection_chat_id",
#             "system_likeds_and_collected_chat_id",
#             "system_new_followers_chat_id",

#         ]

#         for need_key in need_keys:
#             need_key_item = user.get(need_key,None)
#             if not need_key_item:
#                 group = {
#                     "owner":user_id,
#                     "editors":[user_id],
#                     "subtype":need_key,
#                     "owner_type":"user"
#                 }
#                 [group_id,group]=nomagic.group.create_chat(group)
#                 need_key_item = group_id
#                 user[need_key]=need_key_item
#                 is_update = True

#         if is_update:
#             user["updatetime"]=int(time.time())
#             update_aim(user_id,user)
#         self.set_secure_cookie("user", tornado.escape.json_encode({"id": user_id, "v":1}),expires=time.time()+63072000,domain=settings.get("cookie_domain"))
#         self.finish({"info":"ok","about":"redirect","redirect":redirect,"user_id":user_id})

# class GetVcodeAPIHandler(WebRequest):
#     @tornado.gen.coroutine
#     def post(self):
#         email = self.get_argument("email","")
#         login = email
#         email_subject = "Your verification code - Reset Password"
#         time_now = int(time.time())
#         if not pymail.check_email(email):
#             self.finish({"info":"error","about":"Wrong email address."})
#             return
#         result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
#         if not result:
#             self.finish({"info":"error","about":"Not registered."})
#             return
#         user_id = result[0].get("entity_id")
#         user = get_aim(user_id)
#         vcode = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
#         vcode = "%s"%(random.randint(100000, 999999))
#         user["vcode"] = vcode
#         user["vcode_finishtime"] = time_now+60*5
#         user["update_timestamp"] = time.time()
#         user_name = user.get("nickname",user_id)
#         update_aim(user_id,user)
#         pymail.send_email_vcode("noreply@digitaste.ai", email, email_subject, "digitaste123!",vcode,"https://tasterest.xialiwei.com",user_name)
#         self.finish({"info":"ok","about":"Verification code is sent to the email."})
# class ResetPasswordAPIHandler(WebRequest):
#     def post(self):
#         email = self.get_argument("email",None)
#         login = email
#         vcode = self.get_argument("vcode",None)
#         password0 = self.get_argument("password0",None)
#         password1 = self.get_argument("password1",None)
#         if not (email and vcode and password0 and password1):
#             self.finish({"info":"error","about":"Not enough info."})
#             return
#         time_now = int(time.time())
#         if not pymail.check_email(email):
#             self.finish({"info":"error","about":"Wrong email address."})
#             return
#         result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
#         if not result:
#             self.finish({"info":"error","about":"Not registered."})
#             return
#         user_id = result[0].get("entity_id")
#         user = get_aim(user_id)
#         old_vcode = user.get("vcode","")
#         old_vcode_finishtime = user.get("vcode_finishtime",0)
#         if time_now - old_vcode_finishtime > 0:
#             self.finish({"info":"error","about":"The verification code is expired."})
#             return
#         user["vcode_finishtime"] = time_now
#         user["update_timestamp"] = time.time()
#         if old_vcode != vcode:
#             update_aim(user_id,user)
#             self.finish({"info":"error","about":"Wrong verification code. Please click and get a new one."})
#             return
#         if password0 != password1:
#             update_aim(user_id,user)
#             self.finish({"info":"error","about":"Different passwords. Please change and get a new verification code."})
#             return
#         hash_pwd = hashlib.sha1((password0 + user["salt"]).encode("utf8")).hexdigest()
#         user["password"] = hash_pwd
#         update_aim(user_id,user)
#         self.finish({"info":"ok","about":"Reset Password Success."})

# class ResetPasswordHandler(WebRequest):
#     def get(self):
#         self.time_now = int(time.time())
#         self.version = settings["version"]
#         self.render("../template/auth/reset_password.html")
# class LogoutAPIHandler(WebRequest):
#     def get(self):
#         redirect_url = self.get_argument("next", "/")
#         self.clear_cookie("user")
#         # self.redirect(redirect_url)
#         self.finish({"info":"ok","about":"logout success","action":"redirect","redirect":redirect_url})
# class LogoutHandler(WebRequest):
#     def get(self):
#         redirect_url = self.get_argument("next", "/")
#         self.clear_cookie("user")
#         self.redirect(redirect_url)
# class LogoffAPIHandler(WebRequest):
#     def get(self):
#         if not self.current_user:
#             self.finish({"info":"ok","about":"no login"})
#             return
#         user_id = self.current_user["id"]
#         time_now = int(time.time())
#         user = get_aim(user_id)
#         logoff = user.get("logoff",False)
#         user["logoff"]=True
#         user["updatetime"]=time_now
#         user["name"]="已注销·Reset"
#         user["headimgurl"]="https://tasterest.xialiwei.com/static/img/headimgurl.png"
#         update_aim(user_id,user)
#         result = conn.query("SELECT * FROM index_login WHERE entity_id=%s",user_id)
#         if result:
#             login = result[0]["login"]
#             if len(login.split("_@@_"))==3:
#                 self.finish({"info":"error","about":"already logoff login"})
#                 return
#             new_login = "old_@@_%s_@@_%s"%(time_now,login)
#             conn.execute("UPDATE index_login SET login = %s WHERE entity_id=%s AND login=%s",new_login,user_id,login)
#         self.clear_cookie("user")
#         self.finish({"info":"ok","about":"logoff success"})
# class LogoffWithVcodeCheckAPIHandler(WebRequest):
#     def post(self):
#         if not self.current_user:
#             self.finish({"info":"error","about":"not login"})
#             return
#         user_id = self.current_user["id"]
#         vcode = self.get_argument("vcode",None)
#         time_now = int(time.time())
#         user = get_aim(user_id)
#         old_vcode = user.get("vcode","")
#         old_vcode_finishtime = user.get("vcode_finishtime",0)
#         if time_now - old_vcode_finishtime > 0:
#             self.finish({"info":"error","about":"The verification code is expired."})
#             return
#         user["vcode_finishtime"] = time_now
#         user["update_timestamp"] = time.time()
#         if old_vcode != vcode:
#             self.finish({"info":"error","about":"Wrong verification code. Please click and get a new one."})
#             return
#         update_aim(user_id,user)
#         self.finish({"info":"ok","about":"success, you could continue logoff"})
# class LoginAPIHandler(WebRequest):
#     def post(self):
#         if self.current_user:
#             self.finish({"info":"ok","about":"already login"})
#             return
#         email = self.get_argument("email",None)
#         password = self.get_argument("password",None)
#         token = self.get_argument("token",None)
#         redirect = self.get_argument("redirect",None)

#         login = email
#         result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
#         if not result:
#             self.finish({"info":"error","about":"Not registered","redirect":"/#register_dom"})
#             return
#         user_id = result[0].get("entity_id",None)
#         user = get_aim(user_id)
        
#         logoff = user.get("logoff",False)
#         if logoff:
#             user["logoff"]=False
#             user["updatetime"]=int(time.time())
#             update_aim(user_id,user)
#         hash_pwd = hashlib.sha1((password + user["salt"]).encode("utf8")).hexdigest()
#         if user["password"] != hash_pwd:
#             self.finish({"info":"error","about":"Wrong password or login.","redirect":"/#login_dom"})
#             return
#         if not redirect:
#             redirect = "/"
#         self.set_secure_cookie("user", tornado.escape.json_encode({"id": user_id, "v":1}),expires=time.time()+63072000,domain=settings.get("cookie_domain"))
#         self.finish({"info":"ok","about":"redirect","redirect":redirect,"user_id":user_id})
# class RegisterAPIHandler(WebRequest):
#     @tornado.gen.coroutine
#     def post(self):
#         if self.current_user:
#             self.finish({"info":"ok","about":"already login"})
#             return
#         email = self.get_argument("email","")
#         login = email
#         email_subject = "Your verification code - Login"
#         time_now = int(time.time())
#         if not pymail.check_email(email):
#             self.finish({"info":"error","about":"Wrong email address."})
#             return
#         result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
#         if result:
#             self.finish({"info":"error","about":"Already registered."})
#             return
#         user = {}
#         password_str = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
#         password_str = "%s"%(random.randint(100000, 999999))
#         user["password"] = password_str
#         user["name"] = login.split("@")[0]
#         user["name"] = ""
#         user["email"]=email
#         [new_id, result] = nomagic.auth.create_user(user)
#         conn.execute("INSERT INTO index_login (login, entity_id,app) VALUES(%s, %s, %s)", login, new_id,"")
#         pymail.send_email("noreply@digitaste.ai", email, email_subject, "digitaste123!",password_str,"https://tasterest.xialiwei.com",user["name"])
#         self.finish({"info":"ok","about":"Password is sent to the email, and go to login."})
# class GetLoginAPIHandler(WebRequest):
#     @tornado.gen.coroutine
#     def get(self):
#         if not self.current_user:
#             self.finish({"info":"error","about":"not login"})
#             return
#         user_id = self.current_user["id"]
#         result = conn.query("SELECT * FROM index_login WHERE entity_id = %s ORDER BY id ASC",user_id)
#         if not result:
#             self.finish({"info":"error","about":"no login"})
#             return
#         login = result[0].get("login",None)
#         self.finish({"info":"ok","about":"get login info success","login":login})
# class IsLoginAPIHandler(WebRequest):
#     @tornado.gen.coroutine
#     def get(self):
#         if not self.current_user:
#             self.finish({"info":"error","about":"not login"})
#             return
#         user_id = self.current_user["id"]
#         result = conn.query("SELECT * FROM index_login WHERE entity_id = %s ORDER BY id ASC",user_id)
#         if not result:
#             self.finish({"info":"error","about":"no login"})
#             return
#         login = result[0].get("login",None)
#         self.finish({"info":"ok","about":"get login info success","login":login,"user_id":user_id})



