#!/usr/bin/env python
# -*- coding: utf8 -*-

import time
import datetime
import pickle
import uuid
import binascii

import zlib
#import gzip
import hashlib
import json
import random
import string

# import __init__ as nomagic
import nomagic

from setting import conn

def create_item(item, name):
    time_now = int(time.time())
    item["type"] = name
    item["owner"] = item.get("owner", "")
    item["datetime"] = datetime.datetime.now().isoformat()
    item["createtime"] = time_now
    item["updatetime"] = time_now

    new_id = nomagic._new_key()
    while True:
        new_order = nomagic._get_entity_by_id(new_id)
        if not new_order:
            break
        else:
            new_id = nomagic._new_key()
    rowcount = nomagic._node(new_id).execute_rowcount("INSERT INTO entities (id, body) VALUES(%s, %s)", new_id, nomagic._pack(item))
    assert rowcount
    return (new_id, item)

def update_order(order_id, data):
    rowcount = nomagic._node(order_id).execute_rowcount("UPDATE entities SET body = %s WHERE id = %s", nomagic._pack(data), nomagic._key(order_id))
    assert rowcount

