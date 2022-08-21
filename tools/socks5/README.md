## 开箱即用的 socks5 代理服务镜像

在这里 lamda 提供了两种 socks5 的安装方法，为了避免问题，请先阅读以下规则

> 如果你需要代理UDP协议

由于socks5 udp代理的特性，这会让坑以及事情越来越多，如果你确定需要使用UDP
你必须遵循这些规则，其一：你的宿主机系统必须为 Linux，且防火墙需要放开 `50000-55000` 的UDP端口
其二：你的服务器网络必不能为 NAT（FULL NAT 也不行，现有的云服务器基本都是 NAT 模式）

为什么宿主机要是 Linux，因为在其他系统上 docker 可能无法正常映射如此大段的端口，
其次，其他系统上 docker 网络模式会影响。

如果你不知道你的服务器网络是不是 NAT，请通过 ifconfig 等命令获取默认网络接口的IP地址，
随后在你想要使用代理的地方 ping 这个地址，如果PING不通，那么你的服务器可能在 NAT 里。

当然，如果有条件不符合并不代表就不能用UDP，你仍然可以自行搭建 gost，文末介绍如何使用 gost 搭建。

> 如果不需要使用 UDP，那么一切都很简单

使用如下命令即可
```bash
docker run -it --rm -p 1080:1080 --name socks -e LOGIN=username -e PASSWORD=passwd rev1si0n/socks5
```

> 如果你需要可以指定出网网卡

就是你的服务器或者电脑上有多个可以上网的接口，拿家用电脑来说，你通过网线和WIFI分别连接了两个网络
那么你的电脑可能就有两个网络接口 wlan0 , eth0
而你需要指定代理出网的那个网络。

你的电脑或者服务器必须为 Linux 系统，如果你想使用 eth0 出网，使用以下命令启动即可
```bash
docker run -it --rm --net host --name socks -e LOGIN=username -e PASSWORD=passwd -e DEV=eth0 rev1si0n/socks5
```

如果你已满足使用UDP的各项条件，使用如下命令即可

```bash
docker run -it --rm --net host --name socks -e LOGIN=username -e PASSWORD=passwd rev1si0n/socks5
```

## 使用 gost 来做代理

如果你想使用 UDP 但是无法满足上面使用UDP的条件，或者用不到指定出网接口，或者不想安装 docker 你可以尝试 gost。
从 [github.com/ginuerzh/gost/releases/](https://github.com/ginuerzh/gost/releases) 下载对应系统的可执行文件压缩包。

```bash
gost -L=socks5://username:passwd@:1080
# 注意关闭系统上的所有UDP端口防火墙。
```

即可。


最后，在 lamda 中使用如下代码连接即可

```python
profile = GproxyProfile()
profile.type        = GproxyType.SOCKS5
#profile.udp_proxy   = True 或者 False
profile.host        = "192.168.服务器IP"
profile.port        = 1080
profile.login       = "username"
profile.password    = "passwd"
d.start_gproxy(profile)
```