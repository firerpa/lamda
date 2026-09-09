#!/usr/bin/env python3
#encoding=utf-8
import os
import sys
import time
import argparse
import subprocess

from shlex import split as s
from lamda.client import *

certfile = os.environ.get("CERTIFICATE", None)
port = int(os.environ.get("PORT", 65000))

argp = argparse.ArgumentParser()
argp.add_argument("-d", type=str, required=True)
argp.add_argument("-a", type=str, required=True)
args = argp.parse_args()

certfile = os.environ.get("CERTIFICATE", None)
d = Device(args.d, certificate=certfile)

app = d.application(args.a)
d.start_activity(**app.query_launch_activity(), debug=True)
print (time.ctime(), "{} is started as debuggable mode".format(args.a))
print (time.ctime(), "Waitting for 'Waitting For Debugger' popup")
if not d(textContains="Waiting").wait_for_exists(25*1000):
    print (time.ctime(), "No debugger prompt detected, please ensure "\
                "you already run 'setdebuggable' in firerpa terminal." )
    exit (1)

pName = app.info().processName
processes = d.enumerate_running_processes()
p = list(filter(lambda p: p.processName == pName,
                                    processes))[0]
print (time.ctime(), "Found pid: {}".format(p.pid))
# Build forward cmd
print (time.ctime(), "Forwarding jwdp pid")
cmd = s("adb forward tcp:8700 jdwp:%s" % p.pid)
forward = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                shell=False)
forward.wait()

print (time.ctime(), "--------------------------------")
print (time.ctime(), "Now please use your IDA to attach this target")
print (time.ctime(), "name: {} pid: {}".format(pName, p.pid))
print (time.ctime(), "and wait for IDA 'Downloading symbols' to finish")
print (time.ctime(), "when all is finished, press ENTER to continue")
print (time.ctime(), "--------------------------------")

_ = input()

cmd = s("jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port=8700")
debug = subprocess.Popen(cmd, stdin=sys.stdin,
                              stdout=sys.stdout,
                              stderr=sys.stderr,
                              bufsize=0,
                              shell=False)
debug.wait()