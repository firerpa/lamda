# Copyright 2025 rev1si0n (lamda.devel@gmail.com). All rights reserved.
#encoding=utf-8
from lamda.client import *
import time

d = Device("localhost")

app = d.application("com.taobao.taobao")
app.start()

while True:
    goodsid = input("Please input a taobao goods id (item_id) (eg. 123456): ")
    if goodsid.isdigit():
        intent["package"] = "com.taobao.taobao"
        intent["action"] = "android.intent.action.VIEW"
        intent["component"] = "com.taobao.taobao/com.taobao.android.detail.alittdetail.TTDetailActivity"
        intent["data"] = f"http://internal.tt.detail.taobao.com/detail/index.html?id={goodsid}"
        d.start_activity(**intent)
        time.sleep(2)