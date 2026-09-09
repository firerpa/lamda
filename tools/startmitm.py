#!/usr/bin/env python3
# Copyright 2025 rev1si0n (lamda.devel@gmail.com). All rights reserved.
#
# Distributed under MIT license.
# See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
#encoding=utf-8
import os
import re
import sys
import time
import uuid
import logging
import asyncio
import argparse
import subprocess
import threading

from socket import *
from random import randint
from multiprocessing import Process
from urllib.parse import urlparse
from functools import partial

from mitmproxy.certs import CertStore
from mitmproxy.tools.main import mitmweb as web
from mitmproxy.options import CONF_DIR, CONF_BASENAME, KEY_SIZE
from mitmproxy.version import VERSION

from packaging.version import parse as ver

from lamda import __version__
from lamda.client import *


serial = None
cleaning = False
def cleanup(*args, **kwargs):
    global cleaning
    if cleaning is True:
        return
    cleaning = True
    log ("uninstall certificate")
    d.uninstall_ca_certificate(ca)
    log ("disable proxy")
    d.stop_gproxy()
    os._exit (0)


def add_server(command, spec):
    spec and command.append("--mode")
    spec and command.append(spec)


def add_upstream(args, ext):
    u = urlparse(args.upstream)
    upstream = "upstream:{}://{}:{}".format(u.scheme,
                                            u.hostname,
                                            u.port)
    args.mode = upstream
    cred = "{}:{}".format(u.username, u.password)
    u.username and ext.append("--upstream-auth")
    u.username and ext.append(cred)


def log(*args):
    print (time.ctime(), *args)


def die(*args):
    print (time.ctime(), *args)
    sys.exit (1)


def adb(*args):
    command = ["adb"]
    if serial is not None:
        command.extend(["-s", serial])
    command.extend(args)
    log (" ".join(command))
    proc = subprocess.Popen(command)
    return proc


def adb_tcp(action, aport, bport):
    p = adb(action, "tcp:{}".format(aport),
                    "tcp:{}".format(bport))
    return p


def reverse(aport, bport):
    return adb_tcp("reverse", aport, bport)


def forward(aport, bport):
    return adb_tcp("forward", aport, bport)


def get_default_interface_ip_imp(target):
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(( target, lamda ))
    return s.getsockname()[0]


def get_default_interface_ip(target):
    default = get_default_interface_ip_imp(target)
    ip = os.environ.get("LANIP", default)
    return ip


print (r"           __                 __            .__  __            ")
print (r"   _______/  |______ ________/  |_    _____ |__|/  |_  _____   ")
print (r"  /  ___/\   __\__  \\_  __ \   __\  /     \|  \   __\/     \  ")
print (r"  \___ \  |  |  / __ \|  | \/|  |   |  Y Y  \  ||  | |  Y Y  \ ")
print (r" /____  > |__| (____  /__|   |__|   |__|_|  /__||__| |__|_|  / ")
print (r"      \/            \/                    \/               \/  ")
print (r"                 Android HTTP Traffic Capture                  ")
print (r"%60s" %                ("lamda#v%s BY firerpa" % (__version__)))


pkgName = None
argp = argparse.ArgumentParser()

login = "lamda"
psw = uuid.uuid4().hex[::3]
cert = os.environ.get("CERTIFICATE")
proxy = int(os.environ.get("PROXYPORT",
                    randint(28080, 58080)))
webport = randint(28080, 58080)
lamda = int(os.environ.get("PORT",
                    65000))

argp.add_argument("device", nargs=1)
mod = argp.add_mutually_exclusive_group(required=False)
mod.add_argument("-m", "--mode", default="socks5")
mod.add_argument("--upstream", type=str, default=None,
                  help="Upstream http proxy")
argp.add_argument("--proxy-dns", type=str, default=None,
                  help="Resolve dns(tcp) through proxy")
argp.add_argument("--device-side-out-interface", type=str, default="auto",
                  help="Specify the outgoing network interface on the device")
argp.add_argument("--serial", type=str, default=None,
                  help="Adb device serial")
args, extras = argp.parse_known_args()
serial = args.serial
host = args.device[0]

if ":" in host:
    host, pkgName = host.split(":")

server = get_default_interface_ip(host)
usb = server in ("127.0.0.1", "::1")

if cert:
    log ("ssl:", cert)
if args.upstream:
    add_upstream(args, extras)
if usb and forward(lamda, lamda).wait() != 0:
    die ("adb forward failed")
if usb and reverse(proxy, proxy).wait() != 0:
    die ("adb forward failed")

# Create instance
d = Device(host, port=lamda,
                 certificate=cert)
logger.setLevel(logging.WARN)

# Concat mitmproxy cert path
DIR = os.path.expanduser(CONF_DIR)
CertStore.from_store(DIR, CONF_BASENAME, KEY_SIZE)
ca = os.path.join(DIR, "mitmproxy-ca-cert.pem")

log ("install cacert: %s" % ca)
d.install_ca_certificate(ca)

# disable ipv6
# If the local device does not have a valid public IPv6 address but the mobile device does,
# it may cause the device to show "no network". so IPv6 is disabled here for the phone.
d.execute_script("echo 1 | tee /proc/sys/net/ipv6/conf/all/disable_ipv6")

# Initialize proxy profile
profile = GproxyProfile()
profile.type = GproxyType.SOCKS5
profile.bypass_local_subnet = True
profile.interface = args.device_side_out_interface

# SOCKS5 is not supported in upstream mode
# https://github.com/mitmproxy/mitmproxy/issues/2813
if args.upstream: profile.type = GproxyType.HTTP_CONNECT

if args.proxy_dns: profile.nameserver = args.proxy_dns
if args.proxy_dns: profile.dns_proxy = True
# Prevent DNS from being intercepted
if args.proxy_dns: extras.extend(["--ignore-host", args.proxy_dns])

profile.udp_proxy = True

profile.host = server
profile.port = proxy

profile.login = login
profile.password = psw
log ("set proxy: %s:%s@%s:%s/%s" % (
                            login, psw,
                            server, proxy,
                            pkgName or "all"))
if pkgName is not None:
    profile.application.set(d.application(pkgName))
d.start_gproxy(profile)

command = []
add_server(command, args.mode)
command.append("--ssl-insecure")
# Simple random auth
command.append("--proxyauth")
command.append("{}:{}".format(login, psw))
# Random web-port
command.append("--web-port")
command.append(str(webport))
command.append("--no-rawtcp")
command.append("--listen-port")
command.append(str(proxy))
# Append extra command line
command.extend(extras)

log (" ".join(command))

sys.exit = cleanup
log ("press CONTROL + C to stop")
proc = Process(target=web, name="mitmweb",
               args=(command,), daemon=True)
proc.run()
sys.exit(0)