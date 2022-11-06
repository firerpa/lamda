#!/usr/bin/env python3
#encoding=utf-8
import os
import sys
import shutil
from lamda.client import *

cmd, host = sys.argv[1:]

certfile = os.environ.get("CERTIFICATE", None)
port = int(os.environ.get("LAMDAPORT", 65000))

d = Device(host, port=port, certificate=certfile)

shutil.which("adb") or exit("no adb")

os.popen("adb start-server").read()

android_path = os.path.join("~", ".android")
abs_android_path = os.path.expanduser(android_path)

os.chdir(abs_android_path)

pubkey = os.popen("adb pubkey adbkey").read()
open("adbkey.pub", "w").write(pubkey)

func = getattr(d, "%s_adb_pubkey" % cmd)
r = func("adbkey.pub")
print ("OK: %s" % r)