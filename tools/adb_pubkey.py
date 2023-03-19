#!/usr/bin/env python3
#encoding=utf-8
import os
import argparse

from os.path import isfile
from lamda.client import *

certfile = os.environ.get("CERTIFICATE", None)
port = int(os.environ.get("PORT", 65000))

android_path = os.path.join("~", ".android")
abs_android_path = os.path.expanduser(android_path)
f = "adbkey.pub"

argp = argparse.ArgumentParser()

argp.add_argument("action", nargs=1)
argp.add_argument("device", nargs=1)

args = argp.parse_args()

d = Device(args.device[0], port=port,
                certificate=certfile)
cmd = args.action[0]

os.chdir(abs_android_path)

# try generate pubkey
pubkey = os.popen("adb pubkey adbkey").read()
open("adbkey.lamda", "w").write(pubkey)

f = ("adbkey.lamda", f)[isfile(f)]

call = getattr(d, "%s_adb_pubkey" % cmd)
exit(not call(f))