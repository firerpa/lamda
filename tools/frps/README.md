FRPS 服务 docker，省得你自己搭建，一条命令就可以跑起来

注意此类端口转发程序只建议在 Linux 类系统上使用，如果你的 docker 宿主机不是 Linux 类，请不要使用。

> 开始前请先放通防火墙 6009/tcp，如果需要从外网登录 frps 的后台，你还需要放通 6119/tcp。

执行命令
```bash
docker run -it --rm --net host -e TOKEN=mypasswod -e BIND=127.0.0.1 -e PORTS=1000-5000 rev1si0n/frps
# TOKEN 为密码，同样为 frps 后台的登录密码
# BIND 为绑定接口 默认为 127.0.0.1，请不要设为 0.0.0.0 除非你知道自己在做什么
# PORTS 为允许绑定端口的范围 默认为 3000-5000
```

注意，启动后会在终端输出一些配置及连接信息，找到 `----- LAMDA  CONFIG -----` 段
复制其中 `fwd.xxxxx=xxxx` 的行，并将其写入到设备上的 `/data/usr/properties.local` 文件中，
你可以修改其中的 `rport` 字段为你想要的端口，这个端口值必须在启动时指定的 `PORTS` 范围中，默认 0 则为随机分配。
重启设备并启动 lamda，lamda 将会自动将自身端口转发到服务器上。


你还可以通过 127.0.0.1:6119 访问 frps 的后台页面（如果放通了防火墙 6119，你也可以通过 http://服务器IP:6119 访问）
后台登录用户名为 `lamda`，登录密码为你启动时提供的 TOKEN。
