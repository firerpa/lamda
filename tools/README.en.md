These tools normally only work on linux/mac systems and are a package of common personal functions, not specifically designed to be Windows compatible but that doesn't mean lamda doesn't support them. If you are using Windows, scripts ending in `.sh` should not work properly.

## Pre-requisites

Before you start, make sure that you have started the lamda server on your device.

**Note**: Some of the command documentation may be updated from time to time, so to avoid versioning issues, make sure you have the latest version of lamda and its Python libraries and dependencies installed on your device before continuing. Some functions require adb, so please ensure that you have the latest version of adb installed.

```bash
# If you don't have it installed, please do your own search for how to install it, this is only basic advice
# Windows
https://developer.android.com/studio/releases/platform-tools
# Mac
brew install android-platform-tools
# brew cask install android-platform-tools
# Debian/Ubuntu
apt install adb
```

Clone the code locally

```bash
git clone https://github.com/rev1si0n/lamda.git
# If you don't know how to use git or don't have it installed, download this file locally and unpack it
# https://github.com/rev1si0n/lamda/archive/refs/heads/master.zip
```

Go to the tools directory and install the required dependencies
```bash
# Switch to the tools/ directory and execute
pip3 install -r requirements.txt
```

If you have enabled communication encryption (certificate) on the server side, you will need to set the environment variable ``CERTIFICATE`` before you can use it
```bash
# For linux / Mac
export CERTIFICATE=/path/to/lamda.pem
# For Windows (paths must not contain spaces)
set CERTIFICATE=C:\Users\path\to\lamda.pem
```

If you have changed lamda's default port 65000, you will also need to set the environment variable before using it

```bash
# For linux / Mac
export PORT=8123
# For Windows (path must not contain spaces)
set PORT=8123
```

192.168.1.2 is the example IP, please get the actual IP address of the device yourself.

## cert.sh

Used to generate a certificate for transmission encryption
```bash
bash cert.sh
```

If you need to generate a certificate for a specific CN
```bash
bash cert.sh device1.example.com
```

The lamda.pem or device1.example.com.pem in the current directory will be the required certificate.
After the certificate has been applied on the server side, the client must also use the certificate for remote calls and ssh connections.
Once the certificate is applied, any operations performed through the client library will be encrypted and ssh will no longer use the default secret key.
The web control page will also require a login (you can find this login password in the last line of the certificate).

If the operating system is not convenient for using this tool, a default SSL certificate is already available for you in the current directory

```bash
test.pem # The certificate used to encrypt client-server communication
```

## cert.py

Used to generate a certificate for transport encryption, equivalent to ``cert.sh`` except that this script can also be run on Windows and is used in the same way as cert.sh.

> Note: you may need to install the pyOpenSSL dependencies manually `pip install pyOpenSSL`


## id_rsa

The default ssh private key used by lamda's built-in ssh, which is the same as the hard-coded private key in `ssh.sh`, `scp.sh`.

## startmitm.py

Start the man-in-the-middle, this will fully automate the global man-in-the-middle on the device and you will be able to intercept http/s traffic for your application, including of course DNS requests (globally).
It is possible to apply and withdraw the man-in-the-middle automatically, and the device and network will be restored to its original state when you exit the script.

> Tip: Sometimes it is annoying to have all this stuff on Windows.
> So specifically for Windows there is **startmitm.exe**, a **Windows command line program** that can be downloaded and placed in the system PATH or current directory and executed from the command line.
> It has the same arguments as startmitm.py. You can do this without installing Python and any associated environment, but you will only be able to do basic man-in-the-middle operations. You can find it in every release. If not, you can look at older releases.
> For Linux/Mac users, if you want to generate/use this standalone executable, package it yourself using the `pyinstaller startmitm.spec` command
> (requires pyinstaller to be installed).

> If you need to intermediate the IAPP, go to **globalmitm**

First make sure that the current computer is on the same network segment as the device, 192.168.1.2 for the mobile device with lamda running.
Secondly, make sure you have verified on the command line that mitmproxy has been installed successfully (type `mitmdump` on the command line to verify this).

Of course, you can also easily mitm if the computer is not on the same network segment as the device or if it is a remote device, please read on.

> Note: mitmweb is not suitable for long periods of multiple requests, the intercepted requests are stored in memory. So your memory will be eaten up if you use it for a long time (you can free it up from time to time by clicking on File->Clear All in the top left corner of the mitmweb interface).
> For long man-in-the-middle operations, please use mitmdump instead, please find out how to use it yourself.

Execute
```bash
# Note that the device IP must be first in the argument
python3 -u startmitm.py 192.168.1.2
```
That's all.

If you want to analyse with a LAN buddy

```bash
python3 -u startmitm.py 192.168.1.2 --web-port 7890 --web-host 0.0.0.0
# Then, have your little one open http://你的IP地址:7890 in their browser and voila!
```

If you need to intercept application-specific traffic rather than global
```bash
# where com.some.package is the application ID
python3 -u startmitm.py 192.168.1.2:com.some.package
```
That will work.


If you want to use a specific DNS, or in some cases you may have DNS resolution errors/unresolvable (which may occur on some native systems), you can do this

```bash
# Use mainland China DNS
python3 -u startmitm.py 192.168.1.2 --nameserver 114.114.114.114
```

If additional arguments need to be passed to mitmproxy, such as -s, then execute

> For information on how to write the `http_flow_hook.py` script, please refer to [docs.mitmproxy.org/stable/addons-examples](https://docs.mitmproxy.org/stable/addons-examples/) and [ mitmproxy/examples/contrib](https://github.com/mitmproxy/mitmproxy/tree/9.0.0/examples/contrib)

```bash
# So you can modify the request or response in real time by writing http_flow_hook.py
python3 -u startmitm.py 192.168.1.2 -s http_flow_hook.py
```
That's all.

The phone is not on the same network as the current computer, but you can physically touch the device, you can still do man-in-the-middle, but **you need to make sure the current device is connected to the **computer** via USB or ``adb connect`` and is ADB authorized.

```bash
# localhost means using an adb device
# Only one adb device is currently connected
python3 -u startmitm.py localhost
# The computer is connected to multiple adb devices, you need to specify adb serial
# This serial can be found in the output of the command adb devices
python3 -u startmitm.py localhost --serial bfde362
```
This will work.

The phone is not under the same network as the current computer and does not have physical access to the device, but as long as you have access to the lamda port you can also do man-in-the-middle.
**This is usually the case** when you have forwarded lamda to a remote server using the built-in frp service, or when you have forwarded lamda's port 65000 somewhere on your own in some way (e.g. SSH, router port forwarding, etc. - **be aware of security issues**), in which case you and lamda
**Only this port** is available for direct communication, the other ports are not accessible to each other. In this case, the phone cannot access any of the local ports, and the local phone can only access the lamda port of the phone (or the phone has a public IP, but the local phone is on a non-interoperable intranet), so that you need to go through the following. (Note that OpenVPN network interworking is not a case of this)

In this case, it needs to be done in a slightly more cumbersome combination, and here's how to do it.

First, install your own adb public key onto the device using `adb_pubkey.py` or by calling the interface yourself (search for it in this document).

Now execute the following command

```bash
adb kill-server
# If you are using the built-in frp or using ssh forwarding yourself
# where x.x.x.x is usually 127.0.0.1, please change this to suit the facts
# and 65000 here is not fixed, change it according to your actual destination forwarding port
adb connect x.x.x.x:65000
```

Finally, do the same as above via USB
```bash
# localhost means the adb device is being used
# Only one adb device is currently connected
python3 -u startmitm.py localhost
# The computer is connected to multiple adb devices, you need to specify the adb serial
python3 -u startmitm.py localhost --serial x.x.x.x:65000
```

and that will do it.

Note: You may need to end the app completely and reopen it before the traffic data will be displayed.

Press `CONTROL` + `C` once to exit the script.

### Forwarding to upstream agents

startmitm itself will also start mitmproxy as a proxy service, by default traffic is sent from the local NIC by mitmproxy, if you need traffic to go through an upstream proxy instead of the local machine, you can specify an upstream proxy using the following, **only** **HTTP** is supported as an upstream proxy.

> DNS traffic will not go through the upstream proxy

```bash
python3 -u startmitm.py 192.168.1.2 --mode upstream:http://example.com:8080
# Omitting the http:// start is fine
python3 -u startmitm.py 192.168.1.2 --mode upstream:example.com:8080
```

If the upstream proxy requires login authentication

```bash
python3 -u startmitm.py 192.168.1.2 --mode upstream:example.com:8080 --upstream-auth USER:PASSWORD
```

These options are compatible with mitmproxy.

### DNS man-in-the-middle (DNS+HTTP/S)

Intercepting DNS requests requires that mitmproxy version >= 9.0.0 (and Python >= 3.9) and that the script is run as **administrator** or **root**.
Some systems may have their own DNS service, so make sure that no other service is using port 53 before using this feature.

This option is different from `-nameserver` above, the `-dns` option refers to the dns intermediary

> DNS broker, default upstream DNS server is 1.1.1.1
```bash
python3 -u startmitm.py 192.168.1.2 --dns
```

> Specify the upstream DNS as 114.114.114.114 (if in mainland China, we recommend using the following command to specify DNS)

```bash
python3 -u startmitm.py 192.168.1.2 --dns 114.114.114.114
```

> If the upstream DNS uses a non-standard port (e.g. 5353)

```bash
python3 -u startmitm.py 192.168.1.2 --dns 192.168.0.100:5353
```

There are some changes to the method name definitions in the hook script, `response()` for normal http requests, and `dns_response()` for intercepting DNS.

```python
def response(flow):
    print (flow, type(flow))

def dns_response(flow):
    print (flow, type(flow))
```

See the documentation for mitmproxy for details.

## adb_pubkey.py

A script to install the local adb pubkey to lamda, otherwise the adb connection will show unauthorized.

```bash
## install adb pubkey
python3 -u adb_pubkey.py install 192.168.1.2
# Uninstall adb pubkey
python3 -u adb_pubkey.py uninstall 192.168.1.2
```

After installation, execute
```bash
adb kill-server
adb connect 192.168.1.2:65000
adb -s 192.168.1.2:65000 shell
```
to connect to the lamda adb.

## ssh.sh

Connect to the shell terminal on the phone.

Execute
```bash
bash ssh.sh 192.168.1.2
```

and you're done.

## scp.sh

Use ``scp`` to copy the files on the device locally.

Copy the `/sdcard/DCIM` directory of 192.168.1.2 to the current directory

```bash
bash scp.sh 192.168.1.2:/sdcard/DCIM .
```

Copy the local directory/file `test/` to `/sdcard/` on device 192.168.1.2

```bash
bash scp.sh test/ 192.168.1.2:/sdcard
```

## discover.py

List all devices online in the **local network** (some devices may not be listed in some network situations, please try several times)

```bash
python3 discover.py
```

## fridarpc.py

A simple wrapper for the fridarpc function.

This function requires you to be proficient in writing frida scripts. Please refer to the test-fridarpc.js file for the script used in the example, and note in particular that the return value of the function defined by rpc.exports in the frida script can only be string/list/json or any js that can be serialised by json. Assume that the device IP is 192.168.0.2.

> Execute the following command to inject RPC into com.android.settings (watch for errors)

```bash
python3 fridarpc.py -f test-fridarpc.js -a com.android.settings -d 192.168.0.2
```

Now that you have the interface out, you can simply request `http://192.168.0.2:65000/fridarpc/myRpcName/getMyString?args=["A", "B"]` to get the results of the methods within the script, and the link can be opened with a browser. GET, and the parameter list can also use multiple parameters at the same time.

Note that the arguments are provided in **double quotes** and we recommend using json.dumps(["A", "B"])

> call with requests

```python
import json
import requests
url = "http://192.168.0.2:65000/fridarpc/myRpcName/getMyString"
data = requests.post(url, data={"args": json.dumps(["A", "B"])}).json()
print (data["result"])

#* Status code 200 Everything is fine
#* Status code 410 Script needs to be re-injected or script is not injected (automatic re-injection is not currently supported)
#* Status code 500 Script or parameter exception
#* Status code 400 Parameter error
```

The format of the response result is fixed and can be opened in a browser for viewing.

## emu-install.sh

Server-side installation script for mainstream emulators only, requires device to be WIFI adb enabled, needs to be downloaded in advance
The corresponding architecture server-side installation package to the current running directory.

```bash
bash emu-install 192.168.1.2
```

## statistics.sh

If you are unable to run LAMDA properly, you can use this script to generate an issue report by rebooting the device and ensuring that LAMDA has exited, pushing ``statistics.sh`` to /data/local/tmp using adb, and then executing it as root.

```bash
# launch.sh is the path to the script that starts LAMDA
sh /data/local/tmp/statistics.sh /data/local/tmp/arm64-v8a/bin/launch.sh
# After execution, the file /sdcard/statistics.txt will be generated, just report this file
```

## magisk

lamda's magisk module architecture

## Various service scripts (Docker)

> All images are for x86 platforms, you may have to make your own modifications and regenerate them for use on ARM processor Linux/Mac.

### openvpn

Out-of-the-box OpenVPN service

### globalmitm

Used to analyse traffic from foreign apps that require a proxy to connect

### frps

Out-of-the-box frp port forwarding

### socks5

Out-of-the-box socks5 proxy service