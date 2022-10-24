## 开箱即用的 OpenVPN 服务镜像

此镜像仅确保了基本功能无误，如果你自己有能力配置，建议自行搭建或者可以参考这个镜像的实现方法来完成。使用前，你需要有 Linux 以及 Docker 相关基础。此镜像在 Debian 9 上测试通过。

> 这里讲述的是如何在 Debian 9 上使用，通常情况下，这可以适用于其他系统例如 Ubuntu 以及 CentOS。该服务默认端口为 1190/UDP，请确保已在防火墙允许该规则。


如果你的服务器是全新创建的，你可能需要先安装 Docker，使用如下命令安装 Docker
```bash
apt update; apt upgrade -y; apt install -y curl
curl https://get.docker.com | sh
# 在测试环境下，安装 docker 出现了失败的问题，报错为
#E: Unable to locate package docker-compose-plugin
#E: Unable to locate package docker-scan-plugin
# 此时执行如下命令即可
apt-get install -y --no-install-recommends docker-ce docker-ce-cli containerd.io
```

## 准备工作

你还需要在服务器上做出如下修改，执行命令

```bash
echo net.ipv4.ip_forward=1 >>/etc/sysctl.conf
sysctl -p
```

如果你的服务器上**安装了 `ufw`**，还需在 `/etc/ufw/before.rules` 的前几行写入如下内容

> 这里的 eth0 和网段根据你的实际服务器接口和配置做修改，注意是加在 *filter 之前（如果有的话）

```bash
*nat
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -s 172.27.27.0/24 -o eth0 -j MASQUERADE
COMMIT
```

然后修改 `/etc/default/ufw`
```bash
DEFAULT_FORWARD_POLICY="ACCEPT"
```

随后执行命令
```bash
ufw reload
```

如果你的服务器上**没有安装 `ufw`**
请确保 iptables 的 FORWARD 默认为 ACCEPT，你可以执行如下命令

> 注意服务器重启后你可能需要重新应用此规则，建议安装 ufw

```bash
iptables -P FORWARD ACCEPT
```

## 初始化配置

现在，创建一个目录用来保存服务的配置

```bash
mkdir -p ~/lamda-openvpn-server
```

紧接着，开始 OpenVPN 服务的初始化操作

```bash
docker run -it --rm --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn ovpn-server-new
```

等待命令结束，现在，你可以在 `~/lamda-openvpn-server` 目录下看到服务的配置
配置文件为 `config.ovpn`


你可以使用编辑器打开此文件，建议只修改下面几个字段

```ini
# VPN 的网段以及掩码
server 172.27.27.0 255.255.255.0
# VPN 服务端口
port 1190

# 或者如果你需要服务器上某个网络接口可以被VPN客户端访问
# 你也可以增加一条路由，但是注意此时你也只能访问到当前主机在此网段的IP
# 如果需要客户端对此网段的完全访问，你还需进行额外设置
push "route 192.168.68.0 255.255.255.0"

# 修改 114 为你需要的 DNS 服务器
push "dhcp-option DNS 114.114.114.114"
```

## 创建客户端连接凭证

编辑完毕，现在开始创建一个客户端，`myname` 可以改为其他你想要的，但是不可重复

```bash
docker run -it --rm --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn ovpn-client-new myname
```

创建完成后，使用如下命令来获取此客户端的登录凭证

```bash
# 注意：配置中的 IP 是自动获取的当前公网IP，如果不对还需自行修改
#
# 生成 ovpn 配置，并重定向保存到文件 myname.ovpn，这个文件可以用于 OpenVPN-Connect 等 APP
docker run -it --rm --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn ovpn-client-profile ovpn myname >myname.ovpn
# 生成 lamda 使用的 OpenVPNProfile，可以直接在 lamda 中使用
# 其中包含一段 properties.local 注释部分，你可以将其中的 openvpn.* 配置
# 复制到 /data/local/tmp/properties.local 中以实现自动连接 VPN
docker run -it --rm --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn ovpn-client-profile lamda myname
```

## 撤销客户端凭证

如果需要撤销某个客户端凭证请执行以下命令，撤销后可能需重新启动 OpenVPN 服务

```bash
docker run -it --rm --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn ovpn-client-revoke myname
```

## 启动 OpenVPN 服务

现在，启动 OpenVPN 服务

> 在前台运行，可以直接看到客户端连接日志，用于排查错误
```bash
docker run -it --rm --name openvpn-server --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn run
```

> 在后台运行，确认无误后建议使用此方法启动
```bash
docker run -d --rm --name openvpn-server --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn run
```

如果没错的话，各个功能都是刚刚好，你可以开始使用了。

## 其他参考

基础文档：[https://openvpn.net/community-resources/reference-manual-for-openvpn-2-4/](https://openvpn.net/community-resources/reference-manual-for-openvpn-2-4/)

路由设置：[https://community.openvpn.net/openvpn/wiki/BridgingAndRouting](https://community.openvpn.net/openvpn/wiki/BridgingAndRouting)
