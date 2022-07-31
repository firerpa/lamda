#!/usr/bin/env python3
#encoding=utf-8
import os
import sys
import time
import signal
import subprocess

from socket import *
from random import randint
from packaging.version import parse as ver
from mitmproxy.version import VERSION
from lamda.client import *


cleaning = False
def cleanup(*args, **kwargs):
    global cleaning
    if cleaning is True:
        return
    cleaning = True
    print (time.ctime(), "terminate server")
    proc.kill()
    print (time.ctime(), "uninstall certificate")
    d.uninstall_ca_certificate(ca)
    print (time.ctime(), "disable proxy")
    d.stop_gproxy()


def get_default_interface_ip_imp():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("114.114.114.114", 53))
    return s.getsockname()[0]


def get_default_interface_ip():
    default = get_default_interface_ip_imp()
    ip = os.environ.get("LANIP", default)
    return ip


pkgName = None
host = sys.argv[1]
if ":" in host:
    host, pkgName = host.split(":")
if "dns_server=true" in sys.argv and ver(VERSION)<ver("8.1.0"):
    print (time.ctime(), "dns_server needs mitmproxy>=8.1.0")
    sys.exit(1)
certfile = os.environ.get("CERTIFICATE", None)
d = Device(host, certificate=certfile)

is_usb = (host == "localhost")

# 如果设备地址是 localhost，那么将本机的 mitmproxy 端口
# 转发到设备的 8181 上，这样网络流量将经过 USB 而非本地局域网
# 使得设备可以和本机不在相同网络内
mitmport = int(os.environ.get("PROXYPORT",
                    randint(28080, 58080)))

reversecmd = []
reversecmd.append("adb")
reversecmd.append("reverse")
reversecmd.append("tcp:8181")
reversecmd.append("tcp:%s" % mitmport)

reverse = subprocess.Popen(reversecmd)

if is_usb and reverse.wait() != 0:
    print (time.ctime(), "adb reverse failed")
    sys.exit(1)

# 无论如何先将设备的服务端口转发到本机
os.popen("adb forward tcp:65000 tcp:65000")

# 如果设备是 localhost，那么代理和端口设置为 127.0.0.1:8181
# 因为本机上运行的 mitmproxy 已经被转发到设备的这个地址上
host = "127.0.0.1" if is_usb else get_default_interface_ip()
port = 8181 if is_usb else mitmport

# 拼接证书文件路径
HOME = os.path.expanduser("~")
ca = os.path.join(HOME, ".mitmproxy", "mitmproxy-ca-cert.pem")

print (time.ctime(), "install certificate: %s" % ca)
d.install_ca_certificate(ca)

print (time.ctime(), "set proxy: %s:%s" % (host, port))

# 初始化 proxy 配置
profile = GproxyProfile()
profile.type = GproxyType.HTTP_CONNECT
if "dns_server=true" in sys.argv:
    profile.nameserver = host
profile.drop_udp = True
# http 代理不支持 udp
#profile.udp_proxy = False
profile.host = host
profile.port = port

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
# 随机 web-port
servercmd.append("--web-port")
servercmd.append(str(randint(18080, 58080)))
# 关闭 rawtcp
servercmd.append("--no-rawtcp")
servercmd.append("--listen-port")
servercmd.append(str(mitmport))
# 追加额外传递的参数
servercmd.extend(sys.argv[2:])

print (time.ctime(), "mitmproxy: `%s`" % " ".join(servercmd))
proc = subprocess.Popen(servercmd, shell=False)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)
print (time.ctime(), "server pid %s" % proc.pid)
retcode = proc.wait()

# 确保 cleanup 被调用
os.kill(os.getpid(), signal.SIGTERM)
sys.exit (0)