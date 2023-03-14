An integrated docker image for analysing the traffic of applications that need to be accessed using an international proxy (You are in a regulated network).
Due to docker implementation issues on Windows/Mac, this image is used differently for Windows/Mac and Linux, please see separate sections.
If you are using a Mac M1, any of the following may not work for you, please use Windows or linux on an x86 architecture.

You may say, why don't I just use an upstream proxy: for some reason affecting DNS, you may not be able to access the real target site.

### Preparing the proxy service

This image supports both normal mode (i.e. startmitm.py wrapped again) and foreign APP mode, for which you will need to prepare either of the following types of proxies first.
Currently **proxies that require a login are not supported**. Usually the client software you use (e.g. clash etc.) will create such a proxy port on your local machine (SOCKS5 or HTTP).
But it may only be bound to `127.0.0.1`, set it to bind to **any interface** and get its binding **port**, then get your **local LAN address**.

Splice the proxy into the following link format ``IP:port`` and keep in mind its proxy type (SOCKS5/HTTP).

```bash
# This is an example HTTP proxy address
192.168.0.2:7890
# This is an example SOCKS5 proxy address
192.168.0.2:1080
# Yes, they look the same, so read on
```

Now selectively look at the commands that correspond to your current system.

### Linux system commands

> foreign app mode

```bash
# Use the HTTP proxy
docker run --rm -it --net host -e HTTP=192.168.0.2:7890 rev1si0n/mitm 192.168.x.x
# Use the SOCKS5 proxy
docker run --rm -it --net host -e SOCKS5=192.168.0.2:1080 rev1si0n/mitm 192.168.x.x
```

> normal mode

```bash
docker run --rm -it --net host rev1si0n/mitm 192.168.x.x
```

Now use your browser to open ``http://127.0.0.1:1234`` or ``http://本机IP:1234`` for man-in-the-middle.

### Mac (Intel)/Windows system commands

For such systems, docker does not support native host mode, and the program will not know the IP address of the host.
So you need to prepare the local **LAN IP** in advance, i.e. the LANIP in the following parameters, assuming your LANIP is 192.168.0.2

> Foreign APP mode

```bash
# Use the SOCKS5 proxy
docker run -it --rm -p 53:53/udp -p 8118:8118 -p 1234:1234 -e LANIP=192.168.0.2 -e SOCKS5=192.168.0.2:1080 rev1si0n/mitm 192.168.x.x
# Use HTTP proxy
docker run -it --rm -p 53:53/udp -p 8118:8118 -p 1234:1234 -e LANIP=192.168.0.2 -e HTTP=192.168.0.2:7890 rev1si0n/mitm 192.168.x.x
```

> normal mode

```bash
docker run -it --rm -p 8118:8118 -p 1234:1234 -e LANIP=192.168.0.2 rev1si0n/mitm 192.168.x.x
```

Now use your browser to open `http://127.0.0.1:1234` or `http://MY_IP:1234` for the intermediary.

### How to build the image

```bash
### cd to the tools directory
docker build -t rev1si0n/mitm -f globalmitm/Dockerfile .
```

### DNS2SOCKS

https://sourceforge.net/projects/dns2socks