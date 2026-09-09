# Copyright 2025 rev1si0n (lamda.devel@gmail.com). All rights reserved.
#encoding=utf-8
from lamda.client import *
import time

"""
This is a simple demo for performing keyword searches on Taobao.
"""

d = Device("localhost")

app = d.application("com.taobao.taobao")

if not app.is_installed():
    print ("taobao app is not installed")
    exit (1)

if app.info().versionName != "10.48.0":
    print ("please intall taaobao 10.48.0")
    exit (1)

# ensure the app is stopped
app.stop()
time.sleep(1.5)

app.start()
time.sleep(10) # wait for app fully started

if not d(description="我的淘宝").exists():
    print ("is taobao home page?")
    exit (1)

# click to activate input
d(description="搜索栏").click()

# wait for search input activated
d(resourceId="com.taobao.taobao:id/searchbtn").wait_for_exists(15*1000)

# input search keyword: 苹果手机
d(resourceId="com.taobao.taobao:id/searchEdit").set_text("苹果手机")

# click "Search"
d(resourceId="com.taobao.taobao:id/searchbtn").click()

# wait for goods showsup
d(description="筛选").wait_for_exists(15*1000)

# do a simple swipe
d().swipe()

# ...