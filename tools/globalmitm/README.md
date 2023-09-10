用于分析需要使用国际代理才能访问的应用的流量，是一个整合的 docker 镜像，
因为 Windows/Mac 上的 docker 实现问题，此镜像对于 Windows/Mac，Linux 有着不同的使用方法，请分别看不同章节。
如果你使用的是 Mac M1，下列任何方式可能都不适用于你，请使用 x86 架构的 Windows 或者 linux。

你可能会说，为什么我不直接使用上游代理：由于某些原因影响DNS，你可能无法访问到真正的目标站点。

### 准备代理服务

此镜像同时支持普通模式（即 startmitm.py 的再次封装）以及国外APP模式，对于国外APP，你需要先准备下面任一类型代理。
目前**不支持需要登录的代理**。通常，你用的客户端软件（例如 clash 等）会在你的本机创建这样的代理端口（SOCKS5 或者 HTTP）。
但是有可能它只绑定到了 `127.0.0.1`，将其设置为绑定**任意接口**并获知它的绑定**端口**，随后获取你的**本机局域网地址**。

拼接代理为以下链接格式 `IP:端口`，并牢记其代理类型（SOCKS5/HTTP）。

```bash
# 这是一个示例 HTTP 代理地址
192.168.0.2:7890
# 这是一个示例 SOCKS5 代理地址
192.168.0.2:1080
# 是的，它们长得一样，请继续往下看
```

现在请选择性查看对应你当前系统的命令。

### Linux 系命令

> 国外APP模式

```bash
# 使用 HTTP 代理
docker run --rm -it --net host -e HTTP=192.168.0.2:7890 rev1si0n/mitm 192.168.x.x
# 使用 SOCKS5 代理
docker run --rm -it --net host -e SOCKS5=192.168.0.2:1080 rev1si0n/mitm 192.168.x.x
```

> 普通模式

```bash
docker run --rm -it --net host rev1si0n/mitm 192.168.x.x
```

现在使用浏览器打开 `http://127.0.0.1:1234` 或者 `http://本机IP:1234` 即可进行中间人。

### Mac (Intel)/Windows 系命令

对于此类系统，docker 并不支持原生 host 模式，程序也就无法获知宿主机的IP地址，
所以你需要提前准备本机**局域网IP**，即以下参数中的 LANIP，假设你的 LANIP 为 192.168.0.2

> 国外APP模式

```bash
# 使用 SOCKS5 代理
docker run -it --rm -p 8118:8118/udp -p 8118:8118/tcp -p 1234:1234 -e LANIP=192.168.0.2 -e SOCKS5=192.168.0.2:1080 rev1si0n/mitm 192.168.x.x
# 使用 HTTP 代理
docker run -it --rm -p 8118:8118/udp -p 8118:8118/tcp -p 1234:1234 -e LANIP=192.168.0.2 -e HTTP=192.168.0.2:7890 rev1si0n/mitm 192.168.x.x
```

> 普通模式

```bash
docker run -it --rm -p 8118:8118/tcp -p 1234:1234 -e LANIP=192.168.0.2 rev1si0n/mitm 192.168.x.x
```

现在使用浏览器打开 `http://127.0.0.1:1234` 或者 `http://本机IP:1234` 即可进行中间人。

### 如何构建镜像

```bash
# cd 到 tools 目录
docker build -t rev1si0n/mitm -f globalmitm/Dockerfile .
```

### DNS2SOCKS

https://sourceforge.net/projects/dns2socks
