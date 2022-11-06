#!/usr/bin/env python3
#encoding=utf-8
import os
import sys
import time
import signal
import subprocess
import uuid

from socket import *
from random import randint
from packaging.version import parse as ver
from mitmproxy.version import VERSION
from lamda import __version__
from lamda.client import *


cleaning = False
def cleanup(*args, **kwargs):
    global cleaning
    if cleaning is True:
        return
    cleaning = True
    log ("terminate server")
    proc.kill()
    log ("uninstall certificate")
    d.uninstall_ca_certificate(ca)
    log ("disable proxy")
    d.stop_gproxy()


def initialize_mitmproxy():
    proc = subprocess.Popen("mitmdump")
    log ("first run mitmproxy, "\
                         "will take a few seconds")
    time.sleep(10)
    proc.terminate()


def log(*args):
    print (time.ctime(), *args)


def adb(*args):
    command = ["adb"]
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
print (r"%60s" %                            ("lamda#v%s" % (__version__)))


pkgName = None
argv = sys.argv
host = argv[1]
if ":" in host:
    host, pkgName = host.split(":")
if "dns_server=true" in argv and ver(VERSION)<ver("8.1.0"):
    log ("dns mitm needs mitmproxy>=8.1.0")
    sys.exit (1)

login = "mitm"
passwd = uuid.uuid4().hex[::4]
cert = os.environ.get("CERTIFICATE")
proxy = int(os.environ.get("PROXYPORT",
                    randint(28080, 58080)))
lamda = int(os.environ.get("LAMDAPORT",
                    65000))

server = get_default_interface_ip(host)
usb = server in ("127.0.0.1", "::1")

if cert:
    log ("ssl:", cert)
if usb and "dns_server=true" in argv:
    log ("dns mitm not available with usb")
if usb and (forward(lamda, lamda).wait() != 0 or \
            reverse(proxy, proxy).wait() != 0):
    log ("forward failed")
    sys.exit (1)

# 创建设备实例
d = Device(host, port=lamda,
                 certificate=cert)

# 拼接证书文件路径
HOME = os.path.expanduser("~")
ca = os.path.join(HOME, ".mitmproxy",
                        "mitmproxy-ca-cert.pem")

if not os.path.isfile(ca):
    initialize_mitmproxy()
log ("install cacert: %s" % ca)
d.install_ca_certificate(ca)

# 初始化 proxy 配置
profile = GproxyProfile()
profile.type = GproxyType.HTTP_CONNECT
if not usb and "dns_server=true" in argv:
    profile.nameserver = server
profile.drop_udp = True

profile.host = server
profile.port = proxy

profile.login = login
profile.password = passwd
log ("set proxy: %s:%s@%s:%s/%s" % (
                            login, passwd,
                            server, proxy,
                            pkgName or "all"))
if pkgName is not None:
    profile.application.set(d.application(pkgName))
d.start_gproxy(profile)

servercmd = []
servercmd.append("mitmweb")
# 默认监听的是 127.0.0.1，改为全局
servercmd.append("--set")
servercmd.append("dns_listen_host=0.0.0.0")
servercmd.append("--set")
servercmd.append("dns_listen_port=53")
servercmd.append("--ssl-insecure")
# 代理认证，防止误绑定到公网被扫描
servercmd.append("--proxyauth")
servercmd.append("{}:{}".format(login, passwd))
# 随机 web-port
servercmd.append("--web-port")
servercmd.append(str(randint(18080, 58080)))
# 关闭 rawtcp
servercmd.append("--no-rawtcp")
servercmd.append("--listen-port")
servercmd.append(str(proxy))
# 追加额外传递的参数
servercmd.extend(argv[2:])

log (" ".join(servercmd))
proc = subprocess.Popen(servercmd, shell=False)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

log ("press CONTROL + C to stop")
log ("server pid %s" % proc.pid)
retcode = proc.wait()

# 确保 cleanup 被调用
os.kill(os.getpid(), signal.SIGTERM)
sys.exit (0)