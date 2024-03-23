#!/usr/bin/env python3
# Copyright 2024 rev1si0n (lamda.devel@gmail.com). All rights reserved.
#
# Distributed under MIT license.
# See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
#encoding=utf-8
import os
import re
import sys
import time
import logging
import subprocess
import argparse
import uuid
import asyncio
import threading
import dns.message
import dns.query
import httpx

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


def is_doh(server):
    u = urlparse(server)
    return u.scheme in ("http", "https")


def fmt_rdns(dns, lport):
    return "reverse:dns://{}@{}".format(dns, lport)


class DOHProxiedProtocol(asyncio.Protocol):
    def __init__(self, loop, server, proxy):
        self.server = server
        log ("using DOH: {}".format(server))
        self.client = httpx.Client(proxies=proxy)
        self.loop = loop
    def datagram_received(self, pkt, addr):
        self.loop.create_task(self.handle(pkt, addr))
    def connection_made(self, transport):
        self.transport = transport
    async def handle(self, pkt, addr):
        res = await self.loop.run_in_executor(None,
                               self.dns_query, pkt)
        self.transport.sendto(res, addr)
    def dns_query(self, pkt):
        res = dns.message.from_wire(pkt)
        res = dns.query.https(res, self.server,
                           session=self.client)
        return res.to_wire()
    @classmethod
    def start(cls, *args, **kwargs):
        dns = threading.Thread(target=cls._start,
                            args=args, kwargs=kwargs)
        dns.daemon = True
        dns.start()
    @classmethod
    def _start(cls, bind, port, upstream, proxy=None):
        loop = asyncio.new_event_loop()
        factory = partial(cls, loop, upstream, proxy)
        coro = loop.create_datagram_endpoint(factory,
                            local_addr=(bind, port))
        loop.run_until_complete(coro)
        loop.run_forever()


def setup_dns_upstream(args):
    port = randint(28080, 58080)
    dns = "{}:{}".format("127.0.0.1", port)
    DOHProxiedProtocol.start(
                             "127.0.0.1",
                             port,
                             args.dns,
                             args.upstream)
    args.dns = fmt_rdns(dns, proxy)


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
print (r"%60s" %                ("lamda#v%s BY rev1si0n" % (__version__)))


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
mod.add_argument("-m", "--mode", default="regular")
mod.add_argument("--upstream", type=str, default=None)
argp.add_argument("--serial", type=str, default=None)
argp.add_argument("--dns", type=str, default=None)
args, extras = argp.parse_known_args()
serial = args.serial
host = args.device[0]

if ":" in host:
    host, pkgName = host.split(":")
if args.dns and ver(VERSION) < ver("9.0.0"):
    log ("dns mitm needs mitmproxy>=9.0.0")
    sys.exit (1)

server = get_default_interface_ip(host)
usb = server in ("127.0.0.1", "::1")

if cert:
    log ("ssl:", cert)
if args.upstream:
    add_upstream(args, extras)
if usb and args.dns:
    die ("dns mitm not available in USB mode")
if usb and args.upstream:
    log ("dns will not sent via upstream in USB mode")
if args.upstream and not args.dns:
    die ("dns must be set in upstream mode")
if args.upstream and args.dns and not is_doh(args.dns):
    die ("dns must be DOH in upstream mode")
if usb and forward(lamda, lamda).wait() != 0:
    die ("adb forward failed")
if usb and reverse(proxy, proxy).wait() != 0:
    die ("adb forward failed")
if not args.upstream and args.dns and not is_doh(args.dns):
    args.dns = fmt_rdns(args.dns, proxy)
if args.dns and is_doh(args.dns):
    setup_dns_upstream(args)


# 创建设备实例
d = Device(host, port=lamda,
                 certificate=cert)
logger.setLevel(logging.WARN)

# 拼接证书文件路径
DIR = os.path.expanduser(CONF_DIR)
CertStore.from_store(DIR, CONF_BASENAME, KEY_SIZE)
ca = os.path.join(DIR, "mitmproxy-ca-cert.pem")

log ("install cacert: %s" % ca)
d.install_ca_certificate(ca)

# 初始化 proxy 配置
profile = GproxyProfile()
profile.type = GproxyType.HTTP_CONNECT
profile.nameserver = "1.1.1.1"
if not usb and (args.upstream or args.dns):
    profile.nameserver = "{}:{}".format(server, proxy)
profile.drop_udp = True

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
# 设置 MITMPROXY 代理模式
add_server(command, args.mode)
add_server(command, args.dns)
command.append("--ssl-insecure")
# 代理认证，防止误绑定到公网被扫描
command.append("--proxyauth")
command.append("{}:{}".format(login, psw))
# 随机 web-port
command.append("--web-port")
command.append(str(webport))
command.append("--no-rawtcp")
command.append("--listen-port")
command.append(str(proxy))
# 追加额外传递的参数
command.extend(extras)

log (" ".join(command))

sys.exit = cleanup
log ("press CONTROL + C to stop")
proc = Process(target=web, name="mitmweb",
               args=(command,), daemon=True)
proc.run()
sys.exit(0)