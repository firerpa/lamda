<p align="center">
<img src="image/logo.svg" alt="LAMDA" width="256">
</p>

<p align="center">Android reverse engineering & automation framework</p>

**English README is translated by deepl, we not guarantee it's the original meaning of the author, all readme is named README.en.md, if you still confused, please reach me at [t.me/lamda_dev](https://t.me/lamda_dev) or by mail/gitter.**

LAMDA is a helper framework for reverse and automation, designed to reduce the time and trivialities of security analysis and application testers by replacing a lot of manual work with programmatic interfaces, it is not a single feature framework. To give you an idea of its usefulness: do you install all kinds of proxies, plug-ins or point-and-click setups on your mobile phone to do your job? Do you have to operate your phone from a remote location that is thousands of miles away? Do you have the need to program your phone to control it? Are you still buying expensive **IP switching**, **remote ADB debugging**, **RPA automation** or even **logcat logging** services from some cloud phone vendors that you have to pay for? If so, then yes, all these problems can be solved with just one LAMDA. And, LAMDA is even more focused on **distribution** - in fact, you can manage devices scattered around the world in various network environments on a single public network server. Of course, LAMDA can do much more than that.

* Zero dependency, just **root** is all you need
* Stable production environment tested with over 500 devices under pressure
* Easy root certificate setup via interface, with http/socks5 proxy for man-in-the-middle
* Expose internal Java interface via frida as http api
* near-commercial-grade software quality and stability, full ARM/X86 architecture
* High security, support for interface and login authentication
* Turns your device into a http web proxy
* Partially compatible with uiautomator2
* Device status/resource consumption readout
* System configuration/property readout modification
* UI layout review
* WIFI ADB with built-in root privileges for wireless connect
* Support for custom startup configuration
* Support for emulators and real phones, cloud phones/headless development boards, redroid (ARM only)
* Support for Android 6.0 (M, API 23) - 13 (T, API 33)
* Support for WSA (Windows Subsystem for Android ™️)
* Support for UDP protocol proxies (socks5 UDP mode)
* Support for OpenVPN and coexistence with http proxy
* Support for Magisk autostart service
* Encapsulates a lot of common interfaces, only Python is required
* Completely networked, no physical USB cable/USB hub, etc.
* Large file uploads and downloads
* Significantly reduces the threshold and time cost of mundane tasks
* Get/replay the most recent Activity on the system
* Send any application Activity
* ssh login to device terminals
* Connect to any device anywhere with LAMDA running
* Run shell commands front and back, grant revocation of application privileges, etc.
* Built-in http/socks5 proxy, can set proxy for global/specific applications
* Built-in frida 15.x, IDA 7.5 server and other tools
* Built-in crontab task service
* Built-in Python 3.9 and some common modules
* Built-in OpenVPN for global/non-global VPN
* WIFI remote desktop (web)
* WEB-side file upload and download
* UI automation with interfaces to automate operations

## One-click man-in-the-middle traffic analysis

With support for regular and international APP traffic analysis, DNS traffic analysis, and thanks to the [mitmproxy flow hook](https://docs.mitmproxy.org/stable/api/events.html), you have maximum control over any request, mitmproxy is feature rich enough to export `curl` commands or `HTTPie` commands for specific requests via its `Export` option. It is rich enough that you can export request-specific `curl` commands or `HTTPie` commands via its `Export` option, and the combination of analysis replay, interception modification, and functionality is a good substitute for any commercial/non-commercial software you have used. If you're still not sure what mitmproxy is and what it can do, be sure to look up the documentation first, as LAMDA will be using mitmproxy to present you with application requests.

This is done via `globalmitm`, `startmitm.py` in the tools/ directory, see the README in the same directory for how to use it.

![Man-in-the-middle traffic analysis motion graphic demo](image/mitm.gif)

## Drag and Drop Uploads

Drag and drop uploads can be done directly from the remote desktop, with support for uploading entire directories up to a single 256MB file, which will always be uploaded to the `/data/local/tmp` directory.

![Drag and Drop Upload Demo](image/upload.gif)

## Remote Desktop Connection

The interface can be operated at any time using your browser even when your phone is not with you, and with Python and related frida tools built in, it is your alternative online shell.

![Remote desktop motion demo](image/lamda.gif)

## Automation through code

Directly through code point and click, it can replace most manual operations.

![automation motion demo](image/automation.gif)

## Interface layout review

You can instantly review the interface layout of your Android app for writing automation code from your remote desktop, by pressing `CTRL + I` from your remote desktop to enter the mode.
Press `CTRL + R` to refresh the layout and `CTRL + I` again to exit.

![Interface layout view](image/inspect.gif)

## Device Directory Index

You can browse the files on your device in your browser and you can also click on the file name to download the desired file.

![directory indexing animation](image/listing.gif)

If you wish to continue, please ensure that you have a rooted Android device with more than 2GB of RAM and more than 1GB of free storage or an Android emulator (the latest version of **Nightmare**, **Thunderbolt** emulator, or AVD [Android Studio Virtual Device] is recommended). **Not fully supported** by NetEase Mumu, **Not supported** by Tencent Handy Assistant, Blue Stack and Android internal virtualization such as VMOS). For real devices, we recommend devices running closest to the native system such as Google Series, One Plus, Android development boards, etc., or devices with only lightly modified systems. If you are using an OPPO/VIVO/Huawei/Xiaomi device and it does not run properly after trying, we recommend using an emulator instead.

For **Cloud Mobile**, AliCloud/Huawei Cloud Mobile is supported, X Finger, X MultiCloud, X Electric, X Cloud Rabbit, X Zixing, X MaCloud and any other brands are not supported.

<br>

# Index

- [Index](#index)
- [Disclaimer and Terms](#disclaimer-and-terms)
- [Preamble](#preamble)
- [Install LAMDA](#install-lamda)
  - [Precautions](#precautions)
    - [Basic requirements](#basic-requirements)
    - [System settings](#system-settings)
    - [Network settings](#network-settings)
    - [Other settings](#other-settings)
  - [Installing the client](#installing-the-client)
  - [Installing the server](#installing-the-server)
    - [Installation via Magisk](#installation-via-magisk)
    - [Manual installation](#manual-installation)
      - [Method 1](#method-1)
      - [Method 2](#method-2)
  - [Start the server](#start-the-server)
  - [Shutdown server](#shutdown-server)
  - [Uninstalling server](#uninstalling-server)
- [Using LAMDA](#using-lamda)
  - [Remote Desktop](#remote-desktop)
  - [File Uploads](#file-uploads)
  - [File downloads](#file-downloads)
  - [Mobile Proxy](#mobile-proxy)
  - [Connecting devices](#connecting-devices)
  - [Let's start with a warm up](#lets-start-with-a-warm-up)
  - [Setting up a system proxy](#setting-up-a-system-proxy)
  - [Installing the man-in-the-middle certificate](#installing-the-man-in-the-middle-certificate)
  - [Setting up OpenVPN](#setting-up-openvpn)
  - [Connecting to the built-in FRIDA](#connecting-to-the-built-in-frida)
  - [Exposing Java interfaces using FRIDA](#exposing-java-interfaces-using-frida)
  - [Using the built-in timed tasks](#using-the-built-in-timed-tasks)
  - [Make LAMDA connectable from any location](#make-lamda-connectable-from-any-location)
  - [Read and write system properties](#read-and-write-system-properties)
  - [Read and write system settings](#read-and-write-system-settings)
  - [Get device running status](#get-device-running-status)
  - [Execute commands on the device](#execute-commands-on-the-device)
  - [Make system debuggable](#make-system-debuggable)
  - [Start IDA Debugging Service](#start-ida-debugging-service)
  - [Wireless connection built-in WIFI ADB](#wireless-connection-built-in-wifi-adb)
  - [File manipulation](#file-manipulation)
  - [Shutdown and restart](#shutdown-and-restart)
  - [Application Operations](#application-operations)
  - [WIFI operation](#wifi-operation)
  - [Basic UI Operations](#basic-ui-operations)
  - [Advanced UI Operations](#advanced-ui-operations)
  - [Interface Lock](#interface-lock)
  - [Using the internal terminal](#using-the-internal-terminal)
- [Tools and tutorials](#tools-and-tutorials)
  - [One-click middleman](#one-click-middleman)
  - [International proxies for man-in-the-middle](#international-proxies-for-man-in-the-middle)
  - [Installing the ADB public key](#installing-the-adb-public-key)
  - [OpenVPN service](#openvpn-service)
  - [SOCKS5 service](#socks5-service)
  - [Port Forwarding Service](#port-forwarding-service)
  - [Injecting Frida RPC scripts](#injecting-frida-rpc-scripts)
  - [Generate encrypted connection certificate](#generate-encrypted-connection-certificate)
  - [List intranet devices](#list-intranet-devices)

# Disclaimer and Terms

In order to download and use the software LAMDA developed by rev1si0n (account github.com/rev1si0n) ("I"), you should read and comply with the User Agreement ("this Agreement") ("Agreement"). You must read and fully understand the terms and conditions, especially those that exclude or limit liability, and choose to accept or not accept them; unless you have read and accepted all of the terms and conditions of this Agreement, you are not authorized to download, install or use the Software and related services. By downloading, installing, using, obtaining an account, logging in, etc., you are deemed to have read and agreed to be bound by the above agreement; if you wish to access the Service, you (hereinafter referred to as "User") shall agree to all of the terms of this agreement and complete the application process as indicated on the page. You can find [DISCLAIMER.TXT](DISCLAIMER.TXT) in the same directory as this document, or here [DISCLAIMER.TXT](DISCLAIMER.TXT). As it is not fully open source, in addition to the above terms:** You are authorised to reverse-analyse LAMDA itself for the purpose of malicious code**.

Please confirm that you have read and accepted all of the terms of this Agreement, otherwise you are not authorized to download, install or use the Software and related services.

# Preamble

LAMDA is free software (freeware) developed by individuals, currently only the client and the protocol are open source, but I promise that it has nothing against you or superfluous, if you still have concerns, you can **leave now** or choose to **pay** for psychological comfort. Please respect each other and use it in accordance with the terms of use. Collaborative exchanges can be [click here to send an email](mailto:ihaven0emmail@gmail.com).

Why is it partially open source? Because LAMDA is both black and white and can easily be used by unscrupulous people to put the author at risk, so please respect the terms of use. It is recommended that you work with the code in the documentation and samples on a Linux or Mac system. Some of the functions require the use of tools in the `tools/` directory, please refer to [tools/README.en.md](tools/README.en.md).

**Special Note**: **Do not run on your own device, and when there is a possibility of using it on a public or untrusted network, make sure that you specify the PEM certificate at startup**

> Side effects after use

You may write `lambda` in your Python code as lamda, this is normal.

> Feedback and suggestions

Because Android is widely used by various devices, it is not possible to guarantee 100% compatibility, and there may be various unknown situations such as running exceptions. The exceptions that occur include: restarting for no reason, app crashing frequently, touch failing or moving around for no reason, etc., frozen screen, etc. If you encounter this frequently, it is recommended to stop using it.
Click here [Report a problem/suggestion](https://github.com/rev1si0n/lamda/issues/new), please describe in detail and include information such as model system.

Community discussion: [t.me/lamda_dev](https://t.me/lamda_dev) | [gitter.im/lamda-dev](https://gitter.im/lamda-dev/community)

> Support the author

If you need to purchase a server, you can choose to purchase cloud services through the **promotional link** below.

<a href="https://lamda.run/referral/aliyun"><img src="image/logo-aliyun.png" alt="阿里云" height="40"></a>
<a href="https://lamda.run/referral/tencent"><img src="image/logo-tencent.svg" alt="腾讯云" height="40"></a>

<br>

# Install LAMDA

> There is a client side and a server side. The client side is mainly Python related libraries and interfaces, and the server side is the service that runs on the device/phone.

## Precautions

### Basic requirements

LAMDA ideally runs in an environment where you are freshly rooted (e.g. a new emulator, a ROM with its own permissions, Magisk just rooted), and before launching **make sure** that.

```
* Magisk Hide must be turned off
* frida-server must be turned off
* It is recommended to disable the Xposed/Magisk plugin
* Reboot the device after confirming
```

and will not enable any of the above entries marked as `must` after startup.

### System settings

> Check time zone time

Open System Settings, find Date & Time, check if the time is automatically set to **China Standard Time** or your location's time zone, check if the time is correct or within an acceptable margin of error, if not turn off **Use network-provided time zone** and **Network time** and manually set the time zone and time to your current location's time zone and time.

> Turn off accessibility

Open System Settings, find Accessibility (in System or More Settings) and turn off or uninstall all applications that use accessibility (e.g. talkback, autojs, etc.).

### Network settings

For real machines, you just need to make sure that your computer is on the same network as your phone.
For emulators, the emulator created by default does not normally interoperate with your local network. If you are using android x86 (VMWare-based Android virtual machine)
If you are using an android x86 (VMWare based Android virtual machine), please try setting the network mode to bridge in the virtual machine settings. For emulators such as Thunderbolt and Nightmare, you will need to follow the instructions in their settings to install the driver and enable bridge mode and then restart the emulator.
For Android Studio Virtual Device, there are no settings. If you need to connect to AVD, please execute `adb forward tcp:65000 tcp:65000` first.
and use `localhost` (do not use 127.0.0.1) to connect.

### Other settings

> WSA (Windows Subsystem Android)

If you are using WSA (Windows Subsystem Android), make sure that the WSA version is not lower than 2210.40000 and that you are rooted, then open WSA Settings -> Subsystem Resources -> select Continuous and turn off Advanced Networking. Then restart the WSA subsystem.

> AVD (Android Studio Virtual Device)

If you are using AVD (Android Studio Virtual Device), first extend the default storage size as follows.

```bash
# Pixel_5_API_29 is the virtual machine ID, which can be listed using the command emulator -list-avds
# -partition-size Some of the newly created AVDs may only have a hundred megabytes of available storage space, change it to 2G here
emulator -avd Pixel_5_API_29 -partition-size 2048 -no-snapshot-load
# Use this command every time you start the virtual machine afterwards
#
# You may encounter a situation where the emulator command is not found.
# See this documentation for the location of this command https://developer.android.com/studio/run/emulator-commandline?hl=zh-cn and add it to the PATH variable
#
# If you are unable to complete the above command, manually click on Virtual Device Manager in Android Studio, create a new virtual machine, then find the corresponding virtual machine and click on the Edit button (a pen symbol) at the back.
# Click on Show Advanced Settings, find Storage -> Internal Storage and set it to at least 2GB.
```

> Redroid (android in docker)

Note that currently **only ARM (aarch64) based hosts** are supported for Redroid, which you can check with the command `uname -m`.

If you are using Redroid (android in docker), take the officially recommended `Ubuntu 20.04` as an example, first install the relevant modules for linux-modules-extra, (note that the following method may not be suitable for other Linux distributions, and if you are not familiar with Linux, we do not recommend that you continue with the following actions ).

```bash
apt install linux-modules-extra-`uname -r`
```

Edit the file `/etc/modules`, copy the following names and insert them at the bottom of the file and restart the current host.

```bash
# redroid modules
mac80211_hwsim

binder_linux
ashmem_linux
```

**or** every time the host reboots (note that if you don't use the above method then you have to do it every time you reboot)

```bash
modprobe mac80211_hwsim
modprobe binder_linux devices="binder,hwbinder,vndbinder"
modprobe ashmem_linux
```

Finally use the following command to start, `redroid_gpu_mode` Please modify it as appropriate (note that this is different from the official command written).

```bash
docker run -itd --rm --privileged --pull always -v /lib/modules:/lib/modules:ro -v ~/redroid:/data -p 127.0.0.1:5555:5555 -p 127.0.0.1:65001:65000 redroid/redroid:12.0.0-latest androidboot.redroid_gpu_mode=guest
```

> The container 65000 is mapped here to the local 65001 because some of the tools need to be temporarily bound to port 65000.

Subsequently, you can access LAMDA on the host through `http://127.0.0.1:65001`.

## Installing the client

Please use Python versions 3.6 - 3.10, Python 3.9 is recommended if possible

```bash
pip3 install -U lamda
## That's it.
#
# If you need to use the built-in frida, be sure to install it using the following method
# You may need extranet access to install frida, otherwise you may be stuck for a long time (~10 minutes) until the installation fails
# Even if you have installed frida before, you should re-run the following command
pip3 install -U --force-reinstall 'lamda[full]'
# Please note that after completing the installation you will need to update any third party libraries that rely on frida using pip at the same time
# any third party libraries such as frida-tools objection etc. (if installed)
# Otherwise you may get undetectable exceptions in later use
```

After installation, run the command `python3 -m lamda.client` to check that it is installed correctly. If you get an error like the following

```python
* AttributeError 'NoneType' object has no..
* TypeError: Couldn't build proto file..
```

This may be due to a conflict with another package installed that depends on protobuf. Please try the following command

```bash
pip3 install -U --force-reinstall lamda
```

If you still have problems, create virtualenv to use it.


## Installing the server

**LAMDA installed by default does not have any authentication enabled, so others can access any content on your device, listen to your device or even access your network for further control. Please pay particular attention to the `Enabling interface authentication` section and be sure to use it on a network that you can `trust`.**

Before installing, please select the appropriate architecture. You can get the current system architecture by using the adb shell command `getprop ro.product.cpu.abi`.
Normally, for current generation phones, you can just choose the `arm64-v8a` version, while for emulators such as Thunderbolt, you would choose either the 32 or 64 bit version of the Android system when creating a new emulator.
The 32-bit emulator system corresponds to `x86` and the 64-bit corresponds to `x86_64`. Normally, the Thunderbolt emulator creates an `x86` based Android 7.0 system by default.

LAMDA supports active reporting of device status, you can write an interface or use grafana to log device status, which includes information about the system, network, memory, CPU, disk, etc.

```bash
# If you are not sure what this feature is please do not perform it and take care to replace the following link
echo "stat-report.url=http://example.com/report" >>/data/local/tmp/properties.local
```

This will cause LAMDA to **POST** device status information (JSON) to this link **every minute** after startup, which will not be listed here due to the number of fields.

LAMDA is updated regularly from github, the default channel update frequency is approximately 1-2 months, for stable the update frequency is 3-6 months, it is recommended to manually download the latest version from github release and update it manually on a regular basis. If this frequency affects your usage, run the following command to create an update configuration before starting LAMDA for the first time.

```bash
# Enter the adb shell and execute
echo "upgrade.channel=stable" >>/data/local/tmp/properties.local
```

Before we start, it is important to introduce the `properties.local` file above.
properties.local is the LAMDA startup configuration file, usually stored on top of the device, which contains strings of type `a=b`.
By writing this file you can implement automatic connections to OpenVPN, proxies, port forwarding etc. when LAMDA starts.
LAMDA will look for this file and load it from `/data/usr`, `/data/local/tmp`, `${CFGDIR:-/data/local}` at boot time.
You can place your properties.local configuration file in any one of these three locations.

In addition to `properties.local`, there is also a parameter `-properties.remote` that loads the configuration from a remote location, which allows LAMDA to download the configuration from an HTTP server at startup, see the section on starting LAMDA further on.

How to write the configuration is described in the individual functions.

> possible errors with launch.sh and how to resolve them

```bash
# If llllaamDaa started is displayed, the service is in daemon mode and you can exit the terminal

already running (already running, please do not start it more than once)
invalid TZ area (time zone is not set, set the time zone in the system time settings)
not run as root (not running as root)
unsupported sdk (running on an unsupported Android system)
abi not match   (wrong tar.gz package used)
```

### Installation via Magisk

If your device uses Magisk, then you can install it in the easiest way possible and LAMDA can **boot up**. Make sure that Magisk version >= 20.4 and only supports installation in the **Magisk App**. For example, you want all LAMDAs flashed with this magisk module to have the interface authentication enabled, or you want them all to boot with the Magisk App**.
Or if you want them all to automatically connect to the proxy on boot, you can simply write properties.local or generate a PEM certificate and rename it to `lamda.pem` (see tools/ for instructions on how to use the tool).
Then open `lamda-magisk-module.zip` using **compression software** and drag it (`lamda.pem` or `properties.local`) into the `common` folder for automatic configuration at startup!

Now, download `lamda-magisk-module.zip` from the [lamda/releases](https://github.com/rev1si0n/lamda/releases) page and push it to `/sdcard`, open the Magisk App, click on Modules-> Install from local, select lamda-magisk-module.zip and wait for a while.

After a successful flash, please reboot the device. After rebooting, LAMDA should start itself on boot. However, to avoid possible crash problems, lamda will start after 30 seconds instead of immediately and you will have enough time to disable the LAMDA module (please wait 2 minutes after booting before connecting to use LAMDA). Once the installation is complete, you don't need to read the next paragraph on manual installation, just skip it.

### Manual installation

The difference between the two methods is that some older devices may not be able to decompress the tar.gz suffix with the system's `tar` command, so `*-install.sh` is provided as a supplement, with a built-in busybox to decompress it. The device architecture obtained by getprop is known to be `arm64-v8a`, now connect the device to the current computer and make sure that the ADB is authorised and that you can switch root properly.

#### Method 1

From the `release` page [lamda/releases](https://github.com/rev1si0n/lamda/releases)
Download `arm64-v8a.tar.gz-install.sh`.

```bash
# /data/local/tmp is the standard service installation path, but not mandatory
# You can put it in any folder with read/write access other than /sdcard
adb push arm64-v8a.tar.gz-install.sh /data/local/tmp
# Enter the adb shell
adb shell
# Type su to make sure you are root
su
# Switch to the directory
cd /data/local/tmp
# Execute the install script and start it (this will unpack and start the service)
sh arm64-v8a.tar.gz-install.sh
# Remove the installer
rm arm64-v8a.tar.gz-install.sh
```

#### Method 2

From the `release` page [lamda/releases](https://github.com/rev1si0n/lamda/releases)
Download `arm64-v8a.tar.gz`.

```bash
# /data/local/tmp is the standard service installation path, but not mandatory
# You can put it in any folder with read/write access other than /sdcard
adb push arm64-v8a.tar.gz /data/local/tmp
```

When finished, go to the `adb shell` and unpack the files.

```bash
# You should now be in the adb shell
cd /data/local/tmp
# Unpack the server file
# Note that the included tar command may not support the z option, so you may need to use busybox tar to unpack
# If your system does not come with the busybox command, download a version for the appropriate architecture from https://busybox.net/downloads/binaries/1.20.0
tar -xzf arm64-v8a.tar.gz
# Remove the installation package
rm arm64-v8a.tar.gz
```

## Start the server

For method 1 installations, the service is started after installation, so you don't need to run the following command after installation** using this method, but it's fine to do it again as described below.
For either of the above installation methods, you will only ever need to do this on the first install, but the process of **starting the service** will need to be done every time the device reboots or after you manually shut down LAMDA, as LAMDA will not run itself.

Go to the adb shell and switch to `su` root and execute.

```bash
# You should now be inside the adb shell, switching to the directory
cd /data/local/tmp
#
# Start the server
# Note that the arm64-v8a directory is named differently depending on the platform
# If you are using the x86 version, then the directory name is x86/ and you will need to change the command accordingly
sh arm64-v8a/bin/launch.sh
#
# If you want to enable encrypted transfers
# Use cert.sh/py in tools/ to generate the PEM certificate first
# Push it to the device e.g. /data/local/tmp/lamda.pem
# and set its owner and permissions to root and 600 (chown root:root lamda.pem; chmod 600 lamda.pem)
# and start it with the following command, lamda.pem must be an absolute path
sh arm64-v8a/bin/launch.sh --certificate=/data/local/tmp/lamda.pem
# This will encrypt any traffic generated through the LAMDA client
# but not the webui remote desktop traffic
# This will encrypt any traffic generated by the LAMDA client # but not webui remote desktop traffic.
# Load properties.local from a remote location
# Sometimes you may wish to load the startup configuration from a link, in which case you can upload properties.local to the server
# When LAMDA downloads this configuration, it will provide some information about the current device such as, unique device ID, device model, current version, etc.
# You can also write your own web service to distribute different startup configurations based on these device parameters
# It is recommended to use HTTPS links for added security, please ensure the device time is correct.
# Then start LAMDA as follows
sh arm64-v8a/bin/launch.sh --properties.remote=http://example.com/config/properties.local
# For static file services with Basic Auth enabled, the same username password is supported
sh arm64-v8a/bin/launch.sh --properties.remote=http://user:password@example.com/config/properties.local
# Hint: LAMDA will retry the request if it times out or returns a 50x status code.
# If it still fails 5 times in a row, LAMDA will abandon the attempt and continue to launch.
# You can of course customize the number of retries.
# Of course, it is possible to customise the number of retries but note that if the server continues to be unresponsive, LAMDA will also be stuck here forever
# When to set the retry count: the device may not have a network connection when it is first booted, if you want to start LAMDA at this point you can increase the value
sh arm64-v8a/bin/launch.sh --properties.remote=http://example.com/config/properties.local --properties.tries=30
# The number of seconds per round n of the retry mechanism will increase as the number of retries increases. So please set this value carefully.
#
# If you need LAMDA to listen to a specific port instead of 65000
# If you change it, make sure that all intranet devices are started on the same port
# Otherwise functions such as device discovery will not work properly
sh arm64-v8a/bin/launch.sh --port=8123
# Do not bind to a port below 1024
```
Wait for the exit, then close the terminal, and the service start is complete.

**Note**: There is a chance that the remote desktop will keep loading when starting up for the first time. When this happens, please first try to reboot the device and restart lamda.
If you experience a black screen/restart lag on the device several times during startup or use and other similar situations, it is recommended to stop using it.

## Shutdown server

LAMDA is designed to run in the background 24/7 and it is not recommended to start and shut down frequently, if you do need to do so please make sure you shut down in one of the two ways below. To shut down the service using the interface please refer to the `Shutdown and Restart` section below, or you can use the following command as it may not be convenient to use the interface.

```bash
kill -SIGUSR2 $(cat /data/usr/lamda.pid)
```

It may take up to ten seconds for the LAMDA service to exit completely, please do not execute this command more than once in a row.

## Uninstalling server

LAMDA is very disciplined about its data planning and will never place random files on your system.
You can completely uninstall lamda with a few commands, before doing so, please follow the ``Shutdown LAMDA service`` above and wait at least 30 seconds to ensure that the service exits properly.

```bash
# Delete LAMDA related directories
rm -rf /data/local/tmp/arm64-v8a /data/usr
# Reboot the device
reboot
```

# Using LAMDA

Port `65000` on the device is the standard public port for this service and may need to be remembered, but in most cases you will not need to explicitly provide this port number.
You can also use the tools/ directory to list all devices and IPs on your network.
The following will always **assume** that the IP of the device is `192.168.0.2`.

## Remote Desktop

The remote desktop feature is designed for Chrome 95+ only, it does not support multiple access and is not guaranteed to be compatible with all browsers.

Open the link `http://192.168.0.2:65000` in your browser to access the web remote desktop, where you can operate the device and execute commands through the root emulation terminal of the interface. If you specify the PEM certificate `--certificate` when starting the server, the remote desktop will require you to enter a password in order to continue accessing it, which you can find in the last line of the PEM certificate as a fixed 32-bit password.

You can also customise the video frame rate (fps), resolution scaling (res) and image quality of the remote desktop. Also, H.264 soft encoding is supported (less traffic and smoother in some cases, only with the latest Chrome browser).
All you need to do is compose the above parameters into the following link `http://192.168.0.2:65000/?fps=25&quality=20&res=0.5&h264`, this link means that the remote desktop is displayed at 25fps with image quality of 20, scaled to 0.5 times the original resolution, and H264 support is enabled. These are the defaults, except for h264 which is not enabled by default. Please note, however, that adjusting the above parameters will not necessarily produce positive results, so please adjust according to the facts.

For a more user-friendly experience such as keyboard input, see the following section `Wirelessly connecting to a WIFI ADB with built-in root privileges`.
After completing adb connect to LAMDA, install [Genymobile/scrcpy](https://github.com/Genymobile/scrcpy) or [barry-ran/QtScrcpy](https://github.com/barry-ran/QtScrcpy), see their documentation for details.

## File Uploads

You can upload files/folders to the device by directly **dragging files or directories to the terminal** on the right from this page, multiple files or folders are supported at the same time, individual files must not exceed a maximum of 256MB, only up to 2k files can be uploaded at the same time, any files uploaded have permission 644, files will always be uploaded to the `/data/local/tmp` directory.

## File downloads

LAMDA allows you to browse directories on your device and download files via your browser, simply open the link `http://192.168.0.2:65000/fs/` in your browser (note the `/` at the end).

## Mobile Proxy

There may be times when your app may experience errors under certain network conditions, or if you want to do some testing on the same network IP as your device.
LAMDA's tunnel2 feature, which allows you to use the device running LAMDA as an http network proxy, also inherits the power of LAMDA: you can be on nearly the same network as the device from anywhere. You can get a quick taste of this by using the curl command below, or you can set port `192.168.0.2` to `65000` as a proxy in Firefox Settings - Configure Proxy Manually and check `Use this proxy for HTTPS too` so that your Firefox will have the same outgoing IP as the device.

```bash
# The default agent does not require any authentication, but when you start it with --certificate
# Then the login user name is lamda and the password is the same as the remote desktop login token
curl -x http://192.168.0.2:65000 https://httpbin.org/ip
```

Custom Proxy Configuration
If you want to use a mobile network (4G/5G) as a proxy outlet, it should be noted that rmnet mobile data may not be enabled when you are connected to a WIFI network, and that WIFI is usually not enabled when you are connected to mobile data. This means that when you are connected to WIFI, the default is to go out through WIFI, and when you are disconnected from WIFI, the default is to go out through data traffic, and there is a certain mutual exclusivity between them (which may vary between system versions). So configuring the iface parameter becomes an optional option and is only provided as an additional possibility, unless you make both the rmnet and wlan NICs active yourself. The following example only changes the login user information for the default agent.

```ini
# Append to properties.local configuration file
tunnel2.login=lamda
tunnel2.password=mypassword
# It is not recommended to configure the iface parameter unless you know what you are doing
# tunnel2.iface=wlan0
```

If you want to be able to use the device as a proxy from any location, see the `Making LAMDA connectable from any location` section.

## Connecting devices

> Now, this will be accompanied by an introduction to the lamda library, before you start, make sure you have installed the client library correctly according to the `Client installation` section above.

It is recommended to go through the source code of the client in passing, not so much to understand it, but just so you can get an idea of what parameters are actually available.

```python
from lamda.client import *

d = Device("192.168.0.2")
# If certificate is enabled on the server side please connect like this
d = Device("192.168.0.2", certificate="/path/to/lamda.pem")
```

Or, if you are familiar with uiautomator2, you can also use some of the automation functions via u2

```python
import uiautomator2 as u2

# Note: Only about 70% of the major interfaces are compatible and the certificate option is not enabled on the server side
d = u2.connect("http://192.168.0.2:65000")
```

Or, just execute the command
```bash
# Note that the DEVICE parameter is an IP, replace it with your own
python3 -m lamda.client -device 192.168.0.2
# You can then type the following directly into this shell
```

> `d` in the following will always be assumed to be the `d = Device("192.168.0.2")` instance.

## Let's start with a warm up

The following method will cause your phone to beep once, when there are a bunch of devices and you need to locate one of them, you can call this interface. (Requires the phone to be non-silent)

```python
d.beep()
```

## Setting up a system proxy

Only http and socks5 proxies are supported, IPv6 is not supported


> Assuming you get a proxy from your service provider at http://123.123.123.123:8080
> Just a few lines of code to allow tcp traffic on the device to pass through this proxy

```python
profile = GproxyProfile()
profile.type = GproxyType.HTTP_CONNECT

# This option is optional if you need it or not
profile.drop_udp = True
profile.host = "123.123.123.123"
profile.port = 8080

d.start_gproxy(profile)
```

> Detailed parameter configuration information

```python
profile = GproxyProfile()
# socks5 proxy is GproxyType.SOCKS5
profile.type = GproxyType.HTTP_CONNECT
# If you need to redirect DNS queries to 114.114.114.114
# Note that this DNS is system global and all DNS issued by the system will be forwarded
# If you are co-locating with OpenVPN, do not set it to be the intranet DNS server for OpenVPN, as this may cause a complete disconnection
# Remove the nameserver configuration line and the system default DNS will be used
#
# Why this option is there: you can modify the dns domain resolution for some applications
profile.nameserver = "114.114.114.114"
profile.host = "Proxy server address"
profile.port = proxy server port

# If this proxy server requires login information (note: if it does not, comment out or delete the following two lines)
profile.password = "proxy server login password"
profile.login = "Proxy login user"

# socks5 mode supports udp proxies, but http proxies are not supported
# Since udp will not be proxied in most cases, it is a good idea to disable udp traffic
# Application/system UDP traffic will be blocked when drop_udp is True, default is False
profile.drop_udp = False

# Whether local traffic needs to *not* go through a proxy, if True, local traffic
# If True, local traffic such as 192.168.x.x 10.x.x.x etc. on the router's internal network will not go through the proxy, default is False
# Note: If udp_proxy is enabled, this option will not work for UDP traffic
profile.bypass_local_subnet = True

# Whether proxy udp traffic is required
# Note that the http proxy service does not support the proxy udp protocol, to enable this option you must use socks5 as a proxy server
# (GproxyType.SOCKS5), and the socks5 proxy server must be configured to enable udp proxy mode.
# A slightly more complex server configuration is required, to avoid pitfalls please refer to tools/socks5 for installation and configuration
# This setting will be ignored if you are using an http proxy or if the drop_udp option is True
profile.udp_proxy = False

# If you need to use a proxy only for a specific application (e.g. Android browser, remove these two lines if global)
app = d.application("com.android.browser")
profile.application.set(app)

# Cautions and tips.
# Running applications will not use the set proxy immediately after it is set
# because the tcp connection was established before the proxy was set
# So, you need to manually close the application and start it before it will establish a connection via the proxy
# That is, if you are doing man-in-the-middle traffic analysis, then after setting up the proxy
# You'll need to close the app and reopen it before you see the app's requests
#
# Note: Local DNS traffic will always not go through the proxy

# Start the proxy
d.start_gproxy(profile)
# Shut down the proxy
d.stop_gproxy()
```

> Quickly setup a socks5 proxy

LAMDA provides an out-of-the-box socks5 proxy service docker with udp support in tools/, go to tools/socks5 for README.en.md.

> Automatically connect to the proxy when LAMDA starts

Copy the following configuration and change the relevant configuration to your proxy information

```txt
gproxy.enable=true
gproxy.type=http-connect
gproxy.host=123.333.333.333
gproxy.port=8080
gproxy.password=
gproxy.login=
```

Append or write this to properties.local and restart LAMDA.

## Installing the man-in-the-middle certificate

> It is recommended that you use or refer to the startmitm.py, globalmitm tool in the tools/ directory, which is already wrapped, and the interface described here.

Please make sure you have the certificates from fiddler, mitmproxy and for mitmproxy
For mitmproxy, the certificate given to you is in pem format as in the example below. For fiddler, it may be in crt format, so just provide the file path
as a parameter and you don't need to care about any conversion/filename issues.

To avoid wasting unnecessary time, we recommend using `mitmproxy` here.
If you are using `Charles` etc, I cannot guarantee that you will be able to set it up in one go.
As these applications are more complex to configure and you may need to understand the various proxy types in order to configure the SSL broker correctly.
If you must use it, it is recommended that you use Charles' socks5 as a proxy protocol.

Note: Android may not be supported 13

```python
import os

# Splice the path to the mitmproxy-ca-cert.pem file
HOME = os.path.expanduser("~")
cert_path = os.path.join(HOME, ".mitmproxy", "mitmproxy-ca-cert.pem")
# Using mitmproxy as an example, install the certificate using the following code
d.install_ca_certificate(cert_path)

# Uninstall the certificate using the following code (it is not recommended to install and uninstall frequently if it does not change often)
d.uninstall_ca_certificate(cert_path)
# This certificate installation interface is generic, you can use it to install any certificate that your application requires you to install
# You can also use it to install certificates that Fiddler/Charles asks you to install
# Just provide the file path
```

Next, look at the ``Set up http/socks5 proxy`` section and just set the proxy to the address that the middleman application is listening to.
If no traffic is intercepted after following the process please attend the **Special Note** in the section on setting up proxies.

## Setting up OpenVPN

> This OpenVPN only supports login with credentials and can coexist with http/socks5 proxies.
> Note that this feature only contains the main functionality of OpenVPN, other than the `DNS` configuration, no other configuration information pushed by the server can be applied at this time.
> These include, but are not limited to, PAC proxy, http proxy configuration, etc. To save you the trouble of installing the service, the
> LAMDA provides an out-of-the-box OpenVPN docker image which has scripts to generate the configuration below, please read on.

It is highly recommended to use the OpenVPN docker installation in tools and generate the following connection configuration.

```python
profile = OpenVPNProfile()

# Whether to have a global VPN or not, False only routes server-side pushes to specific segments
profile.all_traffic = True
# Server-side open connection protocol (or OpenVPNProto.TCP)
profile.proto = OpenVPNProto.UDP
profile.host = "OpenVPN server address"
profile.port = OpenVPN server port
# Server-side channel encryption method
profile.cipher = OpenVPNCipher.AES_256_GCM

profile.tls_encryption = OpenVPNEncryption.TLS_CRYPT
profile.tls_key_direction = OpenVPNKeyDirection.KEY_DIRECTION_NONE
profile.tls_key = """
-----BEGIN OpenVPN Static key V1-----
tls key / tls auth
-----END OpenVPN Static key V1-----
"""

profile.ca = """
-----BEGIN CERTIFICATE-----
Server-side configured ca certificate
-----END CERTIFICATE-----
"""

profile.cert = """
-----BEGIN CERTIFICATE-----
Client certificate
-----END CERTIFICATE-----
"""

profile.key = """
-----BEGIN PRIVATE KEY-----
Client private key
-----END PRIVATE KEY-----
"""

# Start OpenVPN
d.start_openvpn(profile)
# Shut down OpenVPN
d.stop_openvpn()
```

> Setup an OpenVPN service quickly

LAMDA provides an out-of-the-box OpenVPN docker in tools/, go to tools/openvpn for README.en.md.

> Automatically connect to the VPN when LAMDA starts

You can use the command provided in tools/openvpn to generate the properties.local configuration, please do not write it yourself.

## Connecting to the built-in FRIDA

> No need to read this section for non-reverse work

Before and after starting this framework, **please do not** start any frida-server again on your own, otherwise you risk crashing your system. You only need to use the built-in frida via the following code.

1. connect via the code

```python
# when using LAMDA
device = d.frida
device.enumerate_processes()
```

is equivalent to

```python
# Just an example, please try to connect using the above method
manager = frida.get_device_manager()
device = manager.add_remote_device("192.168.0.2:65000")
device.enumerate_processes()
```

2. Use from the command line

For all official frida command line tools you just need to add the parameter `-H 192.168.0.2:65000`.

```bash
frida -H 192.168.0.2:65000 -f com.android.settings
# If you specify the certificate option when starting the server, please note that you also need to add the --certificate parameter here e.g.
frida -H 192.168.0.2:65000 -f com.android.settings --certificate /path/to/lamda.pem
```

For objection and r0capture etc, these third party tools may not follow the command line usage of the native frida tools exactly, if you need to use these third party tools you need to make sure that LAMDA is started **without** the `-certificate` parameter (encrypted transfer), as these tools may not have a parameter to pass the parameter for PEM certificates.

```bash
# objection example connection method (-N -h 192.168.0.2 -p 65000)
objection -N -h 192.168.0.2 -p 65000 -g com.android.settings explore
```

```bash
# r0capture Example connection method (-H 192.168.0.2:65000)
python3 r0capture.py -H 192.168.0.2:65000 -f com.some.package
```

```bash
# jnitrace example connection method (-R 192.168.0.2:65000)
jnitrace -R 192.168.0.2:65000 -l libc.so com.some.package
```

```bash
# frida-dexdump sample connection method (-H 192.168.0.2:65000)
frida-dexdump -H 192.168.0.2:65000 -p PID
```

For other third party tools not mentioned please check their usage yourself.

## Exposing Java interfaces using FRIDA

This feature requires you to be proficient in writing frida scripts.

> Please go to the tools directory to see how to use it.

This feature requires you to be able to write frida scripts. Please refer to the test-fridarpc.js file for the script used in the example, and note in particular that the parameters and return values of the functions defined by rpc.exports in the frida script can only be int/float/string/list/jsdict or any js **serialisable** by JSON. Assume that the device IP is 192.168.0.2.

> Execute the following command to inject RPC into com.android.settings (watch for errors), the relevant files are in the tools directory

```bash
python3 fridarpc.py -f test-fridarpc.js -a com.android.settings -d 192.168.0.2
```

Now that the interface is exposed, you can simply request `http://192.168.0.2:65000/fridarpc/myRpcName/getMyString?args=["A", "B"]` to get the results of the methods within the script, the link can also be opened with a browser, the interface supports both POST and GET, the argument list can also use multiple arguments at the same time, an empty list means no arguments, note that the maximum **serialised string in the args argument here cannot exceed ** `32KB`.

The two string parameters `A`, `B` in the link are the positional parameters of the method `getMyString(paramA, paramB)` in the injected script.

Note that the parameters are provided in **double quotes**, please **not hand typed** or **string spliced** this parameter, always use json.dumps(["A", "B"])

> call with requests

```python
import json
import requests
url = "http://192.168.0.2:65000/fridarpc/myRpcName/getMyString"
# Request api
res = requests.post(url, data={"args": json.dumps(["A","B"])})
print (res.status_code, res.json()["result"])

#* Status code 200 Everything is fine
#* Status code 410 Script needs to be re-injected or script not injected (automatic re-injection is not currently supported)
#* Status code 500 Script or parameter exception
#* Status code 400 Parameter error
```

The format of the response result is fixed and can be opened in a browser for viewing. Again, in conjunction with the following section, you will be able to use the interface directly on the public network.

## Using the built-in timed tasks

There is a built-in cron service for executing timed tasks so that you can run scripts on the device at regular intervals and all rules will be executed as root.

> This feature requires you to be able to write crontab rules, so if you are not familiar with crontab, please find out for yourself first.

Now, open the web console or a ssh/adb shell connected to your device and execute the command `crontab -e`, you will enter edit mode, press `i` in the English input mode, then write the rule and press `ESC`, `SHIFT` + `:`, type `wq` and press enter to save it. Due to the Android hibernation mechanism, timed tasks may not run at the time you expect after the screen is rested and you may need to set the device to always on.

> Some example rules

```
@reboot     echo Executed when the framework is started/reloaded (reloaded)
0 */1 * * * echo Execute every hour
* * * * *   echo Execute every minute
0 8 * * *   echo Execute at eight o'clock every day
```

## Make LAMDA connectable from any location

Sometimes you may be in a situation where your phone is at home and you are not how to use it.
Before you start, you may need to prepare a public server. For security reasons, the most conservative configuration is used here, and it will be explained at the end how to do the functions described in full.

Because of the public server, lamda has a number of ways to do this, using **OpenVPN** for a more elegant implementation. The most convenient way is to use the frp. tools folder, which provides docker images of the service and which can be used to generate the following configuration information with a single click, you can go to tools to see how to use it.

This service uses the more mature port forwarding program [fatedier/frp](https://github.com/fatedier/frp), please explore how to configure the server side in this project. Note: Do not bind the forwarded port to a public address. Make sure that your public server has all unnecessary ports closed.
Here you are given the easiest and safest configuration to start the server directly using the following command.

> First start frps on your public server by executing the following command (note that you may also need to configure a firewall)

```bash
frps --token lamda --bind_addr 0.0.0.0 --bind_port 6009 --proxy_bind_addr 127.0.0.1 --allow_ports 10000-15000
```

> then write properties.local

Copy the following configuration and change the **server address** to your server's public IP

```txt
fwd.host=server address
fwd.port=6009
fwd.rport=12345
fwd.token=lamda
fwd.protocol=tcp
fwd.enable=true
```

Append or write to properties.local, restart LAMDA and you're done.

> How to use lamda with the above forwarding (needs to be used on the same public server where frps is deployed, as we have bound the forwarding port to 127.0.0.1)

```python
from lamda.client import *
# Port is rport as above
d = Device("127.0.0.1", port=12345)
# The remote desktop can be accessed by opening a browser at http://127.0.0.1:12345
# Any remaining interface calls are implemented uniformly, no changes are needed
```

> How to bulk forward without rewriting the rport configuration each time

If you need to set up multiple machines at once and don't care which port each machine is bound to
you can change the `fwd.rport` value in the above configuration to 0, which will cause your devices to be bound to a random port range of `10000-15000`.
You can locate the corresponding port for device forwarding bindings by rotating the port range later.

> I just want to be able to connect to the device from anywhere

Firstly, this is not recommended for security reasons, but if you do need to use this, it is recommended that you use OpenVPN to access the device on the same network segment as your computer.
If you are still prepared to use the frp method above for arbitrary access, first ensure that the LAMDA service is started with **PEM certificates** and change the `--proxy_bind_addr 127.0.0.1` to `--proxy_bind_addr 127.0.0.1` when starting the frps command.
to `--proxy_bind_addr 0.0.0.0`, which will cause port 12345 to bind directly to the public network. If you start lamda without the PEM certificate, anyone will be able to access it, which is **very, very dangerous**.
The second thing to note is that web remote desktop traffic is always http, and if someone is manning the middleman between you and the server communication, your login credentials could be stolen. Of course, this is not a problem if the web desktop is not used in the meantime.


## Read and write system properties

> set/read system properties

```python
## Get the value of ro.secure
d.getprop("ro.secure")

# Set the value of ro.secure
d.setprop("ro.secure", "0")
```

## Read and write system settings

> Set/read Android system settings

```python
settings = d.stub("Settings")

# If you are confused by strings such as screen_brightness below, please see the following documentation. Some constants
# may not be compatible in different versions of Android, as well as some vendors will have custom variables that need to be noted.

# https://developer.android.com/reference/android/provider/Settings.System
# https://developer.android.com/reference/android/provider/Settings.Secure
# https://developer.android.com/reference/android/provider/Settings.Global

# You can set the brightness of the system screen to manual using the following code
settings.put_system("screen_brightness_mode", "0")

# Example: Get and modify the screen brightness to 5 (0-255)
settings.get_system("screen_brightness")
settings.put_system("screen_brightness", "5")

# Example: Turn off developer options
settings.get_global("development_settings_enabled")
settings.put_global("development_settings_enabled", "0")

# Example
settings.get_secure("screensaver_enabled")
settings.put_secure("screensaver_enabled", "0)
```

## Get device running status

```python
status = d.stub("Status")

## Get the device boot time
status.get_boot_time()

# Get the device's disk usage
status.get_disk_usage(mountpoint="/data")

# Get battery information
status.get_battery_info()
# Get CPU usage
status.get_cpu_info()
# Get overall disk reads and writes
status.get_overall_disk_io_info()
# Get the user data disk reads and writes (userdata)
status.get_userdata_disk_io_info()
# Get the overall network send/receive situation
status.get_overall_net_io_info()
# Get the network traffic of the wlan0 interface
status.get_net_io_info("wlan0")
# Get memory usage
status.get_mem_info()
```

## Execute commands on the device

> Execute shell scripts/commands in the background of the device, in the foreground

```python
## Execute foreground scripts (scripts with short execution times (within 0-10 seconds))
cmd = d.execute_script("whoami")
print (cmd.exitstatus)
print (cmd.stdout)
print (cmd.stderr)

# Execute background scripts (scripts that take a long time to execute)
# For background scripts, due to the possibility of users writing dead-loop scripts with infinite output that fill up memory, etc.
# The result of the execution is not known at the moment
ID = d.execute_background_script("sleep 100; exit 0;")
# Check if the background script has finished
d.is_background_script_finished(ID)
# Force the background script to end
d.kill_background_script(ID)
```

## Make system debuggable

If you need to use dynamic analysis with JEB, IDA, etc., you may need to set this flag to do so, but of course it is built in and you can do this without having to permanently modify `ro.debuggable`.
But remember, you don't always need to call this interface, only use it if you see any articles/tutorials that tell you to modify `ro.debuggable`.

Note: After a successful call to this interface, the system will automatically reboot and you may still have to wait a while for the framework to resume as it did when you first started it!

> use with caution, this feature may be unstable and may be removed at any time

```python
debug = d.stub("Debug")

r = debug.set_debuggable()
print (r)
```

## Start IDA Debugging Service

> IDA 7.5 server is built in

```python
debug = d.stub("Debug")

## Start IDA 32 server (port is customizable)
debug.start_ida(port=22032)
# Check if it is started
debug.is_ida_running()
# Shut down the IDA 32 server
debug.stop_ida()
# If you are debugging a 64-bit application, replace ida in the method name with ida64
# For example
debug.start_ida64(port=22064)
#debug.start_ida64(port=22064)
# If you need to customize the ida-server environment variable e.g. IDA_LIBC_PATH (also applies to start_ida)
debug.start_ida64(port=22064, IDA_LIBC_PATH="/apex/com.android.runtime/lib64/bionic/libc.so")
# Use start_ida when the target application you are debugging is 32-bit
# otherwise use start_ida64
# start_ida64 will be invalid when your device system is a 32-bit platform
```

## Wireless connection built-in WIFI ADB

This ADB is not a full-featured adb, it only supports shell, pull, push, forward, reverse and other common functions.
With this feature you will be able to connect to the highest privileged adb **without having to enable developer mode**.

> Note: jdwp debugging-related features are unique and conflict with the system's built-in features, so this adb **is not** currently supported.

```python
# LAMDA's built-in adb service is completely independent of the adb service provided by the system itself
# So before you can use it, you need to install your adb public key on the device by calling the following interface manually
# Otherwise, connecting directly will show that you are not authorised (the secret key authorised in the system settings developer mode is not common to the built-in adb)
#
# adb_pubkey.py in the tools directory encapsulates the installation process for the following interface
# You can use this script to allow local connections with a single click, see its README, the following code is for illustrative purposes only
#
# The secret key file is located on your computer at ~/.android or C:\\Users\xxxx\.android and is called adbkey.pub
# If this file does not exist but the file adbkey exists, switch to that directory and execute the command
# adb pubkey adbkey >adbkey.pub to generate adbkey.pub
# adb pubkey
# Then use python code to stitch together the generated adbkey.pub path
import os
keypath = os.path.join("~", ".android", "adbkey.pub")
abs_keypath = os.path.expanduser(keypath)
print (abs_keypath)
#
# Then install this adbkey.pub to LAMDA
d.install_adb_pubkey(abs_keypath)
# This will allow you to connect to the built-in adb
# Connect to the device via the command adb connect 192.168.0.2:65000
# You can think of it exactly as a WIFI ADB
#
# Or if you need to remove the public key from the LAMDA built-in adb
d.uninstall_adb_pubkey(abs_keypath)
```

## File manipulation

> Upload files to or download files from a device (large files are supported)

```python
## Download a file locally
d.download_file("/verity_key", "local file to write to")

# Download file to memory/opened file
from io import BytesIO
fd = BytesIO()
d.download_fd("/verity_key", fd)
print (fd.getvalue())

# Note that the file being written to must be opened in w+b mode
fd = open("Local file written to", "wb")
d.download_fd("/verity_key", fd)

# Upload a file to the device
d.upload_file("local_file_path.txt", "/data/local/tmp/upload_file_to_device.txt")

# Upload file from memory/opened file
from io import BytesIO
d.upload_fd(BytesIO(b "fileContent"), "/data/local/tmp/uploaded_file_to_device.txt")

# Note that the file must be opened using rb mode
fd = open("myfile.txt", "rb")
d.upload_fd(fd, "/data/local/tmp/upload_file_to_device.txt")

# Delete the file on the device
d.delete_file("/data/local/tmp/file.txt")

# Modify file permissions on the device
d.file_chmod("/data/local/tmp/files.txt", mode=0o777)

# Get information about the files on the device
d.file_stat("/data/local/tmp/files.txt")
```

## Shutdown and restart

```python
## Shutdown the system (equal to shutting down the computer)
d.shutdown()
# Reboot the system (equal to reboot)
d.reboot()

# Shut down the LAMDA service running on the device
d.exit()
```

## Application Operations

> List the IDs of all applications installed on the system

```python
d.enumerate_all_pkg_names()
```

> List all running applications on the device

```python
d.enumerate_running_processes()
```

> Get the applications currently in the foreground

```python
d.current_application()

# Equivalent to
d.application(d.current_application().applicationId)

# Get the current foreground activity
d.current_application().activity
```

> Launching, getting Activity

```python
# import FLAG_ACTIVITY* constant definition
from lamda.const import *

# Get the 5 most recent activities in the system (up to 12)
activities = d.get_last_activities(count=5)
print (activities)

# You can just replay the last activity (note that not all activities can be replayed)
activity = activities[-1]
print (activity)
d.start_activity(**activity)

# Assemble activity information manually
# Only boolean, int, short, long, double, float and string types are supported for appending data
d.start_activity(action="***", category="***", component="***",
                 extras={"boolean": False, "int": 1, "string": "act", "float": 1.123},
                 flags=FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TASK,
                 data="***", debug=False)

# Please refer to the documentation for the definition of flags
# https://developer.android.com/reference/android/content/Intent#FLAG_ACTIVITY_BROUGHT_TO_FRONT
# flags and debug parameters are not required, they are just one more possibility

# Call 10000 Customer Service
d.start_activity(action="android.intent.action.CALL", data="tel:10000")

# debug parameter stands for: whether to start the activity in debug mode
# If you know about Waiting for debugger, then it might be useful for you
# You can start an application in debug mode like this (your device or app needs to be debuggable)
la = d.application("com.android.settings").query_launch_activity()
d.start_activity(**la, debug=True)

# e.g. launch the settings APP (which of course is almost equivalent to launching the app directly)
d.start_activity(action="android.intent.action.MAIN",
                 category="android.intent.category.LAUNCHER",
                 component="com.android.settings/.Settings")

# For example, to access the certificate settings
d.start_activity(action="com.android.settings.TRUSTED_CREDENTIALS")
```

> Grant/Revoke APP Permissions

Note that you should set permissions when the APP is not launched, calling it when the APP requests permissions will not have the effect of helping you click allow.

```python
app = d.application("com.my.app")

# Import the PERMISSION_READ_PHONE_STATE constant (version > 3.90)
from lamda.const import *

# Get all permissions for the app
app.permissions()
# Grant READ_PHONE_STATE permissions
app.grant(PERMISSION_READ_PHONE_STATE, mode=GrantType.GRANT_ALLOW)
# Deny the READ_PHONE_STATE permission
app.grant(PERMISSION_READ_PHONE_STATE, mode=GrantType.GRANT_DENY)
# Check if permission has been granted
app.is_permission_granted(PERMISSION_READ_PHONE_STATE)
# Revoke a permission that has been granted
app.revoke(PERMISSION_READ_PHONE_STATE)
```

> clear application cache, reset application

```python
# Delete the application's cached data
app = d.application("com.my.app")
app.delete_cache()
# Reset the application data
app.reset_data()
```

> start/stop the app

``` python
app = d.application("com.my.app")

# Start the application
app.start()
# Check if the application is running in the foreground
app.is_foreground()
# Close the app
app.stop()
```

> Other

```python
app = d.application("com.my.app")
# Get information about the application
app.info()

# Check if the application is installed
app.is_installed()
# Uninstall the application
app.uninstall()

# Query the app's launch Activity (entry activity)
app.query_launch_activity()

# Enable the application
app.enable()
# Disable the application
app.disable()
```

## WIFI operation

Currently some of the functions of WIFI operation are not implemented due to possible device anomalies, only some of the implemented functions are described

```python
wifi = d.stub("Wifi")

# Get wifi bssid,ssid ip and other related information
wifi.status()

# Get all bssid's in the blacklist
wifi.blacklist_get_all()

# Add the bssid to the blacklist (it will not be shown in the wifi list)
wifi.blacklist_add("3c:06:aa:8a:55:66")

# Clear all blacklists
wifi.blacklist_clear()

# Perform a wifi scan
wifi.scan()

# Get the results of a neighborhood wifi scan
wifi.scan_results()

# Get the mac address of the current wifi
wifi.get_mac_addr()

# Get wifi signal strength, link rate
wifi.signal_poll()
```

## Basic UI Operations

> Get device information

```python
d.device_info()
```

> screen-off/bright screen related

```python
# Sleep
d.sleep()
# screen on
d.wake_up()
# Whether the screen is lit or not
d.is_screen_on()
# Whether the screen is locked or not
d.is_screen_locked()
```

> clipboard

``` python
d.set_clipboard("Clipboard contents")

# Get clipboard contents (not supported on Android 10+)
d.get_clipboard()
```

> physical keys

``` python
# This method works with the following 17 keys
# KEY_BACK
# KEY_CAMERA
# KEY_CENTER
# KEY_DELETE
# KEY_DOWN
# KEY_ENTER
# KEY_HOME
# KEY_LEFT
# KEY_MENU
# KEY_POWER
# KEY_RECENT
# KEY_RIGHT
# KEY_SEARCH
# KEY_UP
# KEY_VOLUME_DOWN
# KEY_VOLUME_MUTE
# KEY_VOLUME_UP
d.press_key(Keys.KEY_BACK)

# Also to allow more keys to be used, this method can be used
d.press_keycode(KeyCodes.KEYCODE_CALL)
# The KEYCODEs that can be used can be found in this document
# https://developer.android.com/reference/android/view/KeyEvent#KEYCODE_0
```

> Screenshot

``` python
quality = 60 # screenshot quality, defaults to full quality
d.screenshot(quality).save("screenshot.png")
# Screenshot a specific area of the screen
# Definitions of Bound parameters top, left etc.

# top: count top pixels down from the top of the screen
# bottom: count down from the top of the screen to the bottom pixel
# left: count left pixels from the left side of the screen to the right
# right: count right pixels to the left of the screen

# top is always smaller than bottom and left is always smaller than right in normal circumstances
bound = Bound(top=50, bottom=80, left=50, right=80)
d.screenshot(quality, bound=bound).save("partial.png")
```

> Click on a point on the screen

```python
d.click(Point(x=100, y=100))
```

> click on point A and drag it to point B

```python
A = Point(x=100, y=100)
B = Point(x=500, y=500)

d.drag(A, B)
```

> slide from point A to point B

```python
A = Point(x=100, y=100)
B = Point(x=500, y=500)

d.swipe(A, B)
```

> Slightly more complex multipoint swipe (nine-box unlock)

```python
p1 = Point(x=100, y=100)
p2 = Point(x=500, y=500)
p3 = Point(x=200, y=200)

# Swipe from point P1 to point P2 and then to point P3, any point
d.swipe_points(p1, p2, p3)
```

> open the notification bar/shortcut settings bar

```python
d.open_notification()
d.open_quick_settings()
```

> get page layout description XML

```python
d.dump_window_hierarchy().getvalue()
```

> wait for the interface layout to stop refreshing

```python
# The unit is milliseconds, 5*1000 means 5 seconds
d.wait_for_idle(5*1000)
```

## Advanced UI Operations

> Selector

For the interface layout review, first you need to open the device's web remote desktop. Afterwards, mouse click on the left screen to ensure that the focus falls on the cast screen (otherwise the focus may be captured by the terminal on the right).
Then press the shortcut `CTRL+I` (to start the layout view), you will no longer be able to swipe the left screen, you can click on the dotted box on the screen to see the information about the corresponding element, you can use some of its properties as parameters for the Selector.
Pressing `CTRL+I` again will close the layout view, which will not be refreshed as the page changes, it will always be the layout of the screen at the moment you press the shortcut key, if you need to refresh the layout press `CTRL+R` manually.

Normally we would only use `resourceId`, `clickable`, `text`, `description` as parameters.
If the element has a normal resourceId, it will be used as Selector in preference, i.e.: `Selector(resourceId="com.android.systemui:id/mobile_signal_single"`.
For no resourceId, its text will be used, i.e.: `Selector(text="click to enter")`, or more vaguely `Selector(textContains="click")`
Description is the same as text, but description is used less often.

Of course, Selector can take more than one parameter, and you can make other combinations, e.g. `Selector(text="click through", clickable=True)`

> Note: it is rare to use Selector() directly; in most cases, d() is used.

All common match parameters.

```
textText              Exact match
textContains          text contains match
textStartsWith        textStarts
className             class name match
description           Description Exact match
descriptionContains   descriptionIncludes match
descriptionStartsWith descriptionStartsMatch
clickable             can be clicked
longClickable         can be long pressed
scrollable            scrollable
resourceId            Resource ID match
```

For the most part, you won't use `Selector` directly, but indirect use is ubiquitous.

> Element manipulation

The above has all covered how to coordinate clicks on something as arbitrary as this, now it's on to how to manipulate fixed target elements. First, you need to know how to select the element.

```python
# Select the element on the interface that contains the text App under test
element = d(textContains="APP under test")
# Of course, you don't have to assign to element this way, you can also just use d(textContains="APP under test")
```

OK, now you know how to get the element, but of course, it's not getting it at this point, it just means that you want to manipulate the element in the current interface, so here goes.

```python
# We now assume that the app under test in the interface is the name of the app under test icon on the phone (the name below the icon).
element = d(textContains="APP under test")
# Whether or not the element exists
element.exists()
# Click on the element, if it does not exist an exception will be thrown
# COR_CENTER means click on the centre of the element, you can look at the COR_CENTER definition for other clickable positions
element.click(corner=Corner.COR_CENTER)

# Click on the element, no exception will be thrown if it doesn't exist
element.click_exists(corner=Corner.COR_CENTER)

# Long click on the element, not present throws an exception
element.long_click(corner=Corner.COR_CENTER)

# Get information about the element
element.info()

# Get the centroid of the element
element.info().bounds.center()

# Get the upper left point of the element
element.info().bounds.corner("top-left")

# Get the height of the element
element.info().bounds.height

# Get the width of the element
element.info().bounds.width

# Get the number of elements
element.count()

# Wait for an element to appear, up to 10 seconds
element.wait_for_exists(10*1000)

# Wait for elements to disappear, up to 10 seconds
element.wait_until_gone(10*1000)

# Get a screenshot of the element (not full screen, just the element)
# quality is the quality of the screenshot 1 - 100
element.screenshot(quality=60)

# Drag and drop this APP into the shopping folder (modify as appropriate)
element.drag_to(Selector(text="shopping"))

#########
# Find sibling or sub-level elements
#########
# Sometimes there are duplicate elements or elements with no obvious features that are difficult to locate
# In this case you can narrow the search by looking for sub/sib elements
# Sub-level elements, e.g. a chat login box with an input box that is a sub-level element of the login box
# sibling elements, e.g. a chat input box where the username and password boxes are siblings (in the normal case)
form = d(resourceId="login_form")
form.child(index=1)
# This will fetch the element under login_form with index 0
form.child(index=1).sibling()
# You can also do this to find the password retrieval button at the same level as login_form
# (you don't need to do this if you can already tell by the string, this is just a demonstration)
form.sibling(textContains="Retrieve password")
# They are an element in their own right, you can do anything with them as an element


############################
# Now the element changes its meaning and becomes a selected input box
############################

# Example: Enter the app under test in the search box on the OnePlus search app screen

# Note that you should not type directly into what appears to be an input box, it may not be entered
# Some input boxes need to be clicked once to get to the real input box, so use the resource ID of the real input box
element = d(resourceId="net.oneplus.launcher:id/search_all_apps")
element.set_text("App under test")

# Get the content of the input
element.get_text()

# Clear the text you just entered
element.clear_text_field()

# Combine with a click search to complete a human-like search operation.


# Sliding operations (sliding the list up and down to turn the page)
# Note that these operations do not guarantee precision, and none of the following methods normally require a selector.
# But you can add your own selectors as appropriate

# Slide up, step is adjustable, the more you do, the slower it will be, better for precision sliding
d().swipe(direction=Direction.DIR_UP, step=32)
# Other swipe directions.
#DIR_UP Swipe up
#DIR_LEFT Swipe left
#DIR_DOWN slide down
#DIR_RIGHT Swipe to the right

#########
#fling: flinging, the act of a normal person swiping the screen, faster
#########
# FLINGING from top down
d().fling_from_top_to_bottom()
# from bottom to top
d().fling_from_bottom_to_top()
# left to right
d().fling_from_left_to_right()
# right to left
d().fling_from_right_to_left()

# Other, keep sliding down/up left/right until it reaches the end
# Because it is not always possible to slide to the end or detect a slide to the end
# So the max_swipes parameter is required
d().fling_from_top_to_bottom_to_end(max_swipes=32)
d().fling_from_bottom_to_top_to_end(max_swipes=32)
d().fling_from_left_to_right_to_end(max_swipes=32)
d().fling_from_right_to_left_to_end(max_swipes=32)

#########
# scroll: more mechanical sliding
#########
step = 60
max_swipes = 32
# scroll from top to bottom step step
d().scroll_from_top_to_bottom(step)
# scroll from bottom to top step
d().scroll_from_bottom_to_top(step)
# Scroll from left to right step
d().scroll_from_left_to_right(step)
# slide from right to left step
d().scroll_from_right_to_left(step)

# Other, keep sliding down/up left/right until you reach the end
# Same as above fling description
d().scroll_from_top_to_bottom_to_end(max_swipes, step)
d().scroll_from_bottom_to_top_to_end(max_swipes, step)
d().scroll_from_left_to_right_to_end(max_swipes, step)
d().scroll_from_right_to_left_to_end(max_swipes, step)
```

> Monitor

Monitors are used to listen for changes to the interface and perform set actions (clicking on elements or keystrokes) when conditions are met, this can have an impact on performance or when manual intervention is required so please use with caution, it is not enabled by default.

```python
# Start the watcher loop
d.set_watcher_loop_enabled(True)

# Get if the watcher is started
d.get_watcher_loop_enabled()

# Remove all watchers applied to the system, it is recommended that this is done before each use to prevent the normal processing process from being affected by the previous task registration
d.remove_all_watchers()

# Get a list of all applied watchers in the system
d.get_applied_watchers()

# Remove a watcher completely
d.remove_watcher(name)

# Apply the watcher to the system (this watcher will take effect when watcher_loop is started)
d.set_watcher_enabled(name, True)
# Disable the application
d.set_watcher_enabled(name, False)

# Get whether this watcher is enabled or not
d.get_watcher_enabled(name)
```

> watch how many times an element appears in the system interface

```python
# Do some pre-test cleanup, though of course this is not required for every register
# Just to make sure the testing process is not interrupted
d.remove_all_watchers()
d.set_watcher_loop_enabled(True)

# The number of times the application watcher interface appears to be good
# The second argument is an array that can be given to multiple Selectors to indicate that the conditions are all met before they are logged
# But it is not recommended to have more than three
d.register_none_op_watcher("RecordElementAppearTimes", [Selector(textContains="good")])
d.set_watcher_enabled("RecordElementAppearTimes", True)

# ... Do the operations that satisfy the condition

# Get the number of times the record was appended
d.get_watcher_triggered_count("RecordElementAppearTimes")

# The number of times to reset the record
d.reset_watcher_triggered_count("RecordElementAppearTimes")

# Remove
d.remove_watcher("RecordElementAppearTimes")
```

> click on an element when a matching element appears in the interface

```python
# Do some pre-test cleanup, though of course this is not required for every register
# Just to make sure that the testing process is not interrupted
d.remove_all_watchers()
d.set_watcher_loop_enabled(True)

# Example is to automatically click agree when the user agreement appears after the app is launched
# The second parameter is an array that can be given to multiple Selectors to indicate that the conditions are all met before the click is made
# But it is not recommended to have more than three
d.register_click_target_selector_watcher("ClickAcceptWhenShowAggrement", [Selector(textContains="User Agreement")],
                                         Selector(textContains="Agree", clickable=True))
d.set_watcher_enabled("ClickAcceptWhenShowAggrement", True)

# ... Do the action that satisfies the condition

# Remove
d.remove_watcher("ClickAcceptWhenShowAggrement")
```

> Click the physical button when the matching element appears in the interface

```python
# Do some pre-test cleanup, though of course this is not required for every register
# Just to make sure that the testing process is not interrupted
d.remove_all_watchers()
d.set_watcher_loop_enabled(True)

# Example is to return to the start screen by pressing the HOME key when the Personal Centre is present in the interface
# The second argument is an array that can be given to multiple Selectors to indicate that the conditions are all met before the click is made
# But it is not recommended to have more than three
d.register_press_key_watcher("PressBackWhenHomePageShows", [Selector(textContains="Personal Centre")], Keys.KEY_HOME)
d.set_watcher_enabled("PressBackWhenHomePageShows", True)

# ... Do the actions that satisfy the condition

# Remove
d.remove_watcher("PressBackWhenHomePageShows")
```

## Interface Lock

The basic functionality here allows you to lock the interface for use only by the current Device instance.

```python
# # Get a lock, this will be automatically released after 60 seconds and other clients will have access to the lock, you can change this time
# However, if you change it too high because the exception script quits, you will almost never be able to connect to the device and you may need to do a reboot
# This acquire_lock interface can be reentered and is equivalent to _refresh_lock when reentered, it is recommended to call it only once
d._acquire_lock(releaseTime=60)
# Refresh the lock and set the lock expiry time to this leaseTime after each call
# Make periodic calls to keep the device locked
d._refresh_lock(leaseTime=60)
# Release the lock, other clients will have access to it
d._release_lock()
```

## Using the internal terminal

The internal terminal is the terminal you connect to via the web remote desktop or ssh/internal adb, which has some commands and Python modules built in.
You can perform operations or run Python code directly in the terminal, or even perform self-control directly from within the terminal.

> Now, assuming that you have opened the web remote desktop, you should already see a linux terminal on the page.

Execute the command `cd` to switch to your home directory (by default `/data/usr`), which is your workspace and where you can store your files. The terminal supports command completion but not parameter completion. You can also enter partial commands in the terminal and subsequently fill in the history of commands automatically with the up and down keys. Also, a number of command aliases are provided internally, these and their functions are listed below.
```
l         = command ls
ll        = command ls -l
la        = command ls -la
py        = the command python
..        = switch to parent directory
...       = switch to the parent directory of the parent directory
p         = switch to the previous directory
t         = switch to /data/local/tmp
```

> Some other useful commands.

```
* python           (Python)
* strace           (syscall trace)
* ltrace           (libcall trace)
* curl             (cURL)
* fsmon            (file access monitoring)
* stunnel          (traffic encryption)
* redir            (port forwarding)
* scapy            (traffic analysis)
* iperf3           (network performance testing)
* nano             (file editor)
* vi               (file editor)
* ncdu             (find disk file occupancy)
* socat            (network tool)
* sqlite3          (reads SQLite databases, supports cipher)
* tcpdump          (traffic analysis)
* busybox          (command collection)
* MemDumper        (https://github.com/kp7742/MemDumper)
* frida            (frida-tools)
* frida-ps         (frida-tools)
* frida-trace      (frida-tools)
* frida-ls-devices (frida-tools)
* frida-discover   (frida-tools)
* frida-kill       (frida-tools)
* frida-apk        (frida-tools)
* frida-create     (frida-tools)
* frida-join       (frida-tools)
* and other basic linux commands
```

> Python also has some built-in three-party libraries, note that additional libraries cannot be installed via the PIP.

```
* lamda            (itself)
* capstone         (disassembly engine)
* keystone_engine  (assembly engine)
* unicorn          (CPU emulation engine)
* lief             (binary program parsing)
* lxml             (xml/html parsing)
* redis            (redis client)
* tornado          (web framework)
* pyOpenSSL        (OpenSSL)
* requests         (requests)
* scapy            (Traffic analysis)
* frida            (frida)
* pyaxmlparser     (APK parse)
* xmltodict        (xml to dict)
* msgpack_python   (msgpack)
```

How to use these commands or libraries will not be covered here.

# Tools and tutorials

A copy of the instructions for use is available in each of these folders.

## One-click middleman

Open [tools/README.en.md](tools/README.en.md) to view.

## International proxies for man-in-the-middle

Open [tools/README.en.md](tools/README.en.md) for viewing.

## Installing the ADB public key

Open [tools/README.en.md](tools/README.en.md) for viewing.

## OpenVPN service

Open [tools/README.en.md](tools/README.en.md) for viewing.

## SOCKS5 service

Open [tools/README.en.md](tools/README.en.md) for viewing.

## Port Forwarding Service

Open [tools/README.en.md](tools/README.en.md) for viewing.

## Injecting Frida RPC scripts

Open [tools/README.en.md](tools/README.en.md) to view.

## Generate encrypted connection certificate

Open [tools/README.en.md](tools/README.en.md) to view.

## List intranet devices

Open [tools/README.en.md](tools/README.en.md) to view.


If you still have questions, join the community discussion: [t.me/lamda_dev](https://t.me/lamda_dev) | [gitter.im/lamda-dev](https://gitter.im/lamda-dev/community)