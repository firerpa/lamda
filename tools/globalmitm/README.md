用于分析需要使用代理才能访问的应用的流量，是一个整合的 docker 镜像，需要支持 UDP 协议的 ss 服务，请自行获取该服务。
因为 Windows/Mac 上的 docker 实现问题，此镜像对于 Windows/Mac，Linux 有着不同的使用方法，请分别看不同章节。
如果你使用的是 Mac M1，下列任何方式可能都不适用于你，请使用 x86 架构的 Windows 或者 linux。

此镜像同时支持普通模式（即 startmitm.py 的再次封装）以及国外APP模式，对于国外APP，
你必须使用纯 ss 协议的服务端，建议使用 libev 版本，这里不会教你如何搭建。现在下文的命令都是假设你使用了如下命令启动 server，且防火墙已经正确允许 9090 端口的 udp/tcp 流量。

```bash
ss-server -m aes-256-gcm -k password -p 9090 -s 0.0.0.0 -u --reuse-port -v
```

拼接代理为以下链接格式

```bash
ss://aes-256-gcm:password@IP地址:9090
```

现在请选择性查看对应你当前系统的命令。

### Linux 系命令

> 国外APP模式

```bash
docker run --rm -it --net host -e SS=ss://aes-256-gcm:password@IP地址:9090 rev1si0n/mitm 192.168.x.x
```

如果显示 `Cannot resolve DNS through...`，请确保你的 SS 启用了 `-u` 选项。

> 普通模式

```bash
docker run --rm -it --net host rev1si0n/mitm 192.168.x.x
```

现在使用浏览器打开 `http://本机局域网IP:1234` 即可。

### Mac (Intel)/Windows 系命令

对于此类系统，docker 并不支持原生 host 模式，程序也就无法获知宿主机的IP地址，
所以你需要提前准备本机**局域网IP**，即以下参数中的 LANIP，假设你的 LANIP 为 192.168.0.2

> 国外APP模式

```bash
docker run -it --rm -p 53:53/udp -p 8118:8118 -p 1234:1234 -e LANIP=192.168.50.9 -e SS=ss://aes-256-gcm:password@IP地址:9090 rev1si0n/mitm 192.168.x.x
```

> 普通模式

```bash
docker run -it --rm -p 8118:8118 -p 1234:1234 -e LANIP=192.168.0.2 rev1si0n/mitm 192.168.x.x
```

现在使用浏览器打开 `http://本机局域网IP:1234` 即可。
