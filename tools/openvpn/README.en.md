## Out-of-the-box OpenVPN service image

This image only ensures that the basic functionality is correct. If you are able to configure it yourself, it is recommended that you build it yourself or you can refer to the implementation of this image to do so. You will need to have a basic knowledge of Linux and Docker before using it. This image has been tested on Debian 9.

> The default port for this service is 1190/UDP, so make sure you have allowed this rule in your firewall.


If your server is newly created, you may need to install Docker first, using the following command to install Docker
```bash
apt update; apt upgrade -y; apt install -y curl
curl https://get.docker.com | sh
# In the test environment, the installation of docker failed with the following error
#E: Unable to locate package docker-compose-plugin
#E: Unable to locate package docker-scan-plugin
#E: Unable to locate package docker-scan-plugin
apt-get install -y --no-install-recommends docker-ce docker-ce-cli containerd.io
```

## Preparation

You will also need to make the following changes on the server by executing the command

```bash
echo net.ipv4.ip_forward=1 >>/etc/sysctl.conf
sysctl -p
```

If you have `ufw`** installed on your server, you also need to write the following in the first few lines of `/etc/ufw/before.rules`

> where eth0 and the network segment are modified according to your actual server interface and configuration, note that they are added before *filter (if any)

```bash
*nat
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -s 172.27.27.0/24 -o eth0 -j MASQUERADE
COMMIT
```

Then modify `/etc/default/ufw`
```bash
DEFAULT_FORWARD_POLICY="ACCEPT"
```

Then execute the command
```bash
ufw reload
```

If `ufw is not installed on your server**
Make sure that iptables' FORWARD defaults to ACCEPT, you can execute the following command

> Note that you may need to reapply this rule after a server reboot, it is recommended that you install ufw

```bash
iptables -P FORWARD ACCEPT
```

## Initialising the configuration

Now, create a directory to store the service's configuration

```bash
mkdir -p ~/lamda-openvpn-server
```

Immediately afterwards, start the initialization of the OpenVPN service

```bash
docker run -it --rm --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn ovpn-server-new
```

Wait for the command to finish and you can now see the configuration of the service in the `~/lamda-openvpn-server` directory
The configuration file is `config.ovpn`


You can open this file with an editor and it is recommended to change only the following fields

```ini
# VPN network segment and mask
server 172.27.27.0 255.255.255.0
# VPN service port
port 1190

# or if you need a network interface on the server to be accessible by the VPN client
# You can also add a route, but note that you will only be able to access the IP of the current host in this segment
# If you need full client access to this network segment, you will need to make additional settings
push "route 192.168.68.0 255.255.255.0"

# Change 114 to the DNS server you need
push "dhcp-option DNS 114.114.114.114"
```

## Create client connection credentials

Now that you've finished editing, start creating a client, `myname` can be changed to whatever you want, but don't duplicate it

```bash
docker run --it --rm --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn ovpn-client-new myname
```

Once created, use the following command to get the login credentials for this client

```bash
# Note: The IP in the configuration is the current public IP that is automatically obtained, if it is not correct you will need to change it yourself
#
# Generate the ovpn configuration and redirect it to the file myname.ovpn, which can be used for APPs such as OpenVPN-Connect
docker run -it --rm --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn ovpn-client-profile ovpn myname >myname. ovpn
# Generate the OpenVPNProfile used by lamda, which can be used directly in lamda
# It contains a properties.local comment section where you can configure openvpn.*
# Copy it to /data/local/tmp/properties.local for automatic VPN connection
docker run -it --rm --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn ovpn-client-profile lamda myname
```

## Revoke client credentials

If you need to revoke a client credential please execute the following command, you may need to restart the OpenVPN service after revocation

```bash
docker run -it --rm --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn ovpn-client-revoke myname
```

## Start the OpenVPN service

Now, start the OpenVPN service

> Run in the foreground to see client connection logs directly for troubleshooting errors
```bash
docker run --it --rm --name openvpn-server --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn run
```

> Run in the background, it is recommended to start with this method after confirming
```bash
docker run -d --rm --name openvpn-server --privileged --net host -v ~/lamda-openvpn-server:/etc/openvpn rev1si0n/openvpn run
```

If that's correct, the individual functions are just right and you're ready to go.

## Other references

Basic documentation: [https://openvpn.net/community-resources/reference-manual-for-openvpn-2-4/](https://openvpn.net/community-resources/reference -manual-for-openvpn-2-4/)

Routing setup: [https://community.openvpn.net/openvpn/wiki/BridgingAndRouting](https://community.openvpn.net/openvpn/wiki/BridgingAndRouting )