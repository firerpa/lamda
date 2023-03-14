## Out-of-the-box socks5 proxy service images

Here lamda provides two methods of installing socks5, to avoid problems please read the following rules first

> If you need to proxy the UDP protocol

Due to the nature of the socks5 udp proxy, this can make potholes as well as things more and more common, if you are sure you need to use UDP
One: your host system must be Linux and your firewall needs to be free of UDP ports `50000-55000
Two: your server network must not be NAT (FULL NAT is not an option, existing cloud servers are basically in NAT mode)

Why host Linux? Because on other systems docker may not be able to map such a large number of ports properly.
Secondly, the docker network mode on other systems will affect it.

If you don't know whether your server network is NAT or not, get the IP address of the default network interface by using a command such as ifconfig.
Then ping the address where you want to use the proxy. If the ping doesn't work, then your server is probably in NAT.

Of course, if the conditions are not met it doesn't mean that you can't use UDP, you can still set up gost yourself, the end of this article describes how to use gost to set up.

> If you don't need to use UDP, then everything is very simple

Just use the following command
```bash
docker run --it --rm -p 1080:1080 --name socks -e LOGIN=username -e PASSWORD=passwd rev1si0n/socks5
```

> you can specify the outgoing network card if you need to

If you need to be able to specify an outgoing network card, that is, if your server or computer has more than one interface to the internet, take a home computer, you have two networks connected via cable and WIFI respectively
Then your computer may have two network interfaces wlan0 , eth0
and you need to specify which one is the proxy outgoing network.

Your computer or server must be a Linux system, if you want to use eth0 to get out of the network, you can start it with the following command
```bash
docker run --it --rm --net host --name socks -e LOGIN=username -e PASSWORD=passwd -e DEV=eth0 rev1si0n/socks5
```

If you have met all the conditions for using UDP, use the following command

```bash
docker run -it --rm --net host --name socks -e LOGIN=username -e PASSWORD=passwd rev1si0n/socks5
```

## Using gost as a proxy

If you want to use UDP but can't meet the conditions for using UDP above, or can't use the specified outgoing interface, or don't want to install docker you can try gost.
Download the executable zip for your system from [github.com/ginuerzh/gost/releases/](https://github.com/ginuerzh/gost/releases).

```bash
gost -L=socks5://username:passwd@:1080
# Note that all UDP port firewalls on the system are turned off.
```

that works.


Finally, just connect with the following code in lamda

```python
profile = GproxyProfile()
profile.type = GproxyType.SOCKS5
#profile.udp_proxy = True or False
profile.host = "192.168.server IP"
profile.port = 1080
profile.login = "username"
profile.password = "passwd"
d.start_gproxy(profile)
```