<p align="center">
<img src="image/logo.svg" alt="LAMDA" width="256">
</p>

<p align="center">Android reverse engineering & automation framework</p>

LAMDA 是一个用于逆向及自动化的辅助框架，它设计为减少安全分析以及应用测试人员的时间及琐碎问题，以编程化的接口替代大量手动操作，它并不是一个单一功能的框架。为了让你大概了解它的用处：你是否会在手机上安装各类代理、插件或者点来点去的设置来完成你的工作？你是否要在异地操作远在千里之外的手机？你是否有编程控制手机的需求？是否还在某些云手机厂商那里购买昂贵的**IP切换**、**远程ADB调试**、**RPA自动化**甚至连 **logcat 日志**都要付费的服务？如果有，那么对了，只需一个 LAMDA 即可解决这些问题。并且，LAMDA 更注重**分布式**，事实上，你可以在一台公网服务器上管理散布在世界各地各种网络环境中的设备。当然，LAMDA 可以做到的不止于此。

* 零依赖，只需 **root** 即可
* 通过接口轻松设置根证书，配合 http/socks5 代理实现中间人
* 通过 frida 暴露内部 Java 接口（类 [virjar/sekiro](https://github.com/virjar/sekiro) 但基于 frida）
* 近乎商业级软件的质量和稳定性，ARM/X86全架构
* 较高的安全性，支持接口及登录认证
* 部分兼容 uiautomator2
* 设备状态/资源消耗读取
* 系统配置/属性读取修改
* 界面布局检视
* 无线连接内置 root 权限的 WIFI ADB
* 支持自定义启动配置
* 支持模拟器及真机、云手机/无头开发板、redroid
* 支持安卓 6.0 (M, API 23) - 13 (T, API 33)
* 支持 WSA (Windows Subsystem for Android™️)
* 支持 UDP 协议代理（socks5 UDP 模式）
* 支持 OpenVPN 与代理共存
* 支持 Magisk 开机自启动
* 封装了大量常用接口，只需要会写 Python
* 完全网络化，脱离 USB 数据线/USB 集线器等实体
* 大文件上传下载
* 大大降低门槛以及闲杂琐事上的时间成本
* 唤起应用的 Activity
* 可使用 ssh 登录设备终端
* 只要有网即可连接任意地方运行了 LAMDA 的设备
* 前后台运行 shell 命令，授予撤销应用权限等
* 内置 http/socks5 代理，可设置系统/指定应用的代理
* 内置 frida 15.x, IDA 7.5 server 等工具
* 内置 crontab 定时任务
* 内置 Python3.9 及部分常用模块
* 内置 OpenVPN 可实现全局/非全局的 VPN
* WIFI 远程桌面（web）
* WEB 端文件上传下载
* UI自动化，通过接口实现自动化操作

## 无视恶意软件对抗

MOMO (vvb2060) 是我们认为目前最强的ROOT特征检测软件，如 MOMO 所说：我们的目标是提高用户的知识水平。注意这段描述的功能**并不属于 LAMDA 框架的能力范畴**，它是由 LAMDA 和**未公开**的基建项目共同组成，我们只是以此来引出：你可以相信 LAMDA。

![反检测动图演示](image/detection.gif)

## 一键中间人流量分析

支持常规以及国际APP流量分析，DNS流量分析，得益于 [mitmproxy flow hook](https://docs.mitmproxy.org/stable/api/events.html)，你可以对任何请求做到最大限度的掌控，mitmproxy 功能足够丰富，你可以通过其 `Export` 选项导出特定请求的 `curl` 命令或者 `HTTPie` 命令，分析重放、拦截修改、功能组合足以替代你用过的任何此类商业/非商业软件。如果你仍不清楚 mitmproxy 是什么以及其具有的能力，请务必先查找相关文档，因为 LAMDA 将会使用 mitmproxy 为你展现应用请求。

通过 tools/ 目录下的 `globalmitm`，`startmitm.py` 实现，使用方法请看其同目录 README。

![中间人流量分析动图演示](image/mitm.gif)

## 拖拽上传

可直接在远程桌面拖拽上传，支持上传整个目录，最大支持单个 256MB 的文件，文件将始终被上传到 `/data/local/tmp` 目录下。

![拖拽上传动图演示](image/upload.gif)

## 远程桌面连接

即使手机不在身边也可以使用浏览器随时操作界面，并且内置了 Python 以及相关 frida 工具，是你的另一个在线 shell。

![远程桌面动图演示](image/lamda.gif)

## 通过代码自动化

直接通过代码点点点，可以替代大部分手动操作。

![自动化动图演示](image/automation.gif)

## 界面布局检视

可在远程桌面即时检视安卓应用的界面布局用以编写自动化代码，在远程桌面按下 `CTRL + I` 即可进入模式，
按下 `CTRL + R` 刷新布局，再次按下 `CTRL + I` 退出。

![界面布局检视](image/inspect.gif)

## 设备目录索引

你可以在浏览器浏览设备上的文件，同时你也可以点击文件名来下载所需的文件。

![目录索引动图演示](image/listing.gif)

## 在线浏览 .db 数据库

对于安卓系统数据库 (sqlite)，可以点击文件名后方的小箭头来在线浏览。
无需再将应用产生的数据库文件下载到本地再使用其他软件打开进行分析，全程在线即可完成。

![数据库在线浏览](image/dbview.gif)


如果你希望继续看下去，请确保：有一台已经 root 且运行内存大于 2GB，可用存储空间大于 1GB 的安卓设备或者安卓模拟器（推荐使用最新版**夜神**，**雷电**模拟器，或者 AVD [Android Studio Virtual Device]）。**不完全支持** 网易 Mumu，**不支持**腾讯手游助手、蓝叠以及安卓内虚拟如 VMOS 等），对于真机，推荐运行最接近原生系统的设备如谷歌系、一加、安卓开发板等，或系统仅经过轻度改造的设备。如果你使用的是OPPO/VIVO/华为/小米的设备，经过尝试后无法正常运行，建议改用模拟器。

对于**云手机**，支持阿里云/华为云手机，不支持X手指、X多云、X电、X云兔、X子星、X马云及任何其他品牌。

<br>

# 目录

- [目录](#目录)
- [免责声明及条款](#免责声明及条款)
- [前言](#前言)
- [安装 LAMDA](#安装-lamda)
  - [注意事项](#注意事项)
    - [基础要求](#基础要求)
    - [系统设置](#系统设置)
    - [网络设置](#网络设置)
    - [其他设置](#其他设置)
  - [安装客户端](#安装客户端)
  - [安装服务端](#安装服务端)
    - [通过 Magisk 安装](#通过-magisk-安装)
    - [手动安装](#手动安装)
      - [方式 1](#方式-1)
      - [方式 2](#方式-2)
  - [启动服务端](#启动服务端)
  - [退出服务端](#退出服务端)
  - [卸载服务端](#卸载服务端)
- [使用 LAMDA](#使用-lamda)
  - [远程桌面](#远程桌面)
  - [文件上传](#文件上传)
  - [文件下载](#文件下载)
  - [连接设备](#连接设备)
  - [先来一个热身](#先来一个热身)
  - [设置系统代理](#设置系统代理)
  - [安装中间人证书](#安装中间人证书)
  - [设置 OpenVPN](#设置-openvpn)
  - [连接内置的 FRIDA](#连接内置的-frida)
  - [使用 FRIDA 暴露 Java 接口](#使用-frida-暴露-java-接口)
  - [使用内置的定时任务](#使用内置的定时任务)
  - [使 LAMDA 可被任意地点连接](#使-lamda-可被任意地点连接)
  - [读写系统属性](#读写系统属性)
  - [读写系统设置](#读写系统设置)
  - [获取设备运行状态](#获取设备运行状态)
  - [在设备上执行命令](#在设备上执行命令)
  - [使系统可调试](#使系统可调试)
  - [启动 IDA 调试服务](#启动-ida-调试服务)
  - [无线连接内置的 WIFI ADB](#无线连接内置的-wifi-adb)
  - [文件操作](#文件操作)
  - [关机重启](#关机重启)
  - [应用操作](#应用操作)
  - [WIFI操作](#wifi操作)
  - [基本UI操作](#基本ui操作)
  - [进阶UI操作](#进阶ui操作)
  - [接口锁](#接口锁)
  - [使用内置终端](#使用内置终端)
- [工具及教程](#工具及教程)
  - [一键中间人](#一键中间人)
  - [国际代理进行中间人](#国际代理进行中间人)
  - [安装 ADB 公钥](#安装-adb-公钥)
  - [OpenVPN 服务](#openvpn-服务)
  - [SOCKS5 服务](#socks5-服务)
  - [端口转发服务](#端口转发服务)
  - [注入 Frida RPC 脚本](#注入-frida-rpc-脚本)
  - [生成加密连接证书](#生成加密连接证书)
  - [列出内网设备](#列出内网设备)

# 免责声明及条款

为了下载使用由 rev1si0n (账号 github.com/rev1si0n)（以下简称“本人”）个人开发的软件 LAMDA ，您应当阅读并遵守《用户使用协议》（以下简称“本协议”）。请您务必审慎阅读、充分理解各条款内容，特别是免除或者限制责任的条款，并选择接受或不接受；除非您已阅读并接受本协议所有条款，否则您将无权下载、安装或使用本软件及相关服务。您的下载、安装、使用、获取账号、登录等行为即视为您已阅读并同意受到上述协议的约束；若您需要获得本服务，您（以下称"用户"）应当同意本协议的全部条款并按照页面上的提示完成全部申请使用程序。您可以在本文档的相同目录找到 [DISCLAIMER.TXT](DISCLAIMER.TXT)，或者点此 [免责声明](DISCLAIMER.TXT) 查阅。由于并未完全开源，除以上条款外：**授权您对 LAMDA 本身进行以恶意代码分析为目的的逆向**。

请确认您已阅读并接受本协议所有条款，否则您将无权下载、安装或使用本软件及相关服务。

# 前言

LAMDA 是个人开发的免费软件 (freeware)，目前仅客户端及协议是开源的，但个人承诺它没有任何对您违规或多余的行为，如果仍有担心，您可以**立即离开**或者选择**付费**寻求心理安慰。互相尊重，使用请遵守使用条款。合作交流请在 [ISSUE](https://github.com/rev1si0n/lamda/issues/new) 中留下联系方式。

为什么部分开源？因为 LAMDA 很容易被不法分子利用使作者处于危险之中，所以请尊重条款使用。

建议在 Linux 或者 Mac 系统上操作文档及样例中的代码。部分功能需要配合 `tools/` 目录下的工具实现，如何使用请参照 [tools/README.md](tools/README.md)。

**特别注意**：**请勿在自用设备上运行，当有可能在公网或不信任的网络中使用时，务必确保在启动时指定了PEM证书**

> 使用后的副作用

你可能会把 Python 代码中的 `lambda` 写成 lamda，这是正常现象。

> 问题反馈及建议

因为安卓被各种设备广泛使用，无法保证百分百的兼容性，可能会有运行异常等各种未知情况，出现的异常情况包括：无故重启，APP经常崩溃，触摸失效或无故乱动等等，冻屏等情况。如果经常遇到，建议停止使用。
点此 [报告问题/建议](https://github.com/rev1si0n/lamda/issues/new)，请详细描述并附上机型系统等信息。

社区讨论：https://gitter.im/lamda-dev/community

> 顺便支持作者

如果需要购入服务器，可以选择通过下方的**推广链接**购买云服务。

<a href="https://lamda.run/referral/aliyun"><img src="image/logo-aliyun.png" alt="阿里云" height="40"></a>
<a href="https://lamda.run/referral/tencent"><img src="image/logo-tencent.svg" alt="腾讯云" height="40"></a>

<br>

# 安装 LAMDA

> 分为客户端以及服务端，客户端主要是 Python 相关库及接口，服务端则是运行在设备/手机上的服务。

## 注意事项

### 基础要求

LAMDA 最理想的运行环境是你刚刚 root（如：新建模拟器，自带权限的ROM，Magisk 刚 root），启动前**务必确保**：

```
* 必须关闭 Magisk Hide
* 必须关闭 frida-server
* 建议关闭 Xposed/Magisk 插件
* 确认完毕重启设备
```

并且不会在启动后启用任何上述任何标记为`必须`的条目。

### 系统设置

> 检查时区时间

打开系统设置，找到日期与时间，检查是否已自动设置**中国标准时间**或者你所在地的时区，检查时间是否正确或在可接受的误差范围内，如果没有请关闭**使用网络提供的时区** 以及**网络时间**，并手动设置时区及时间为你当前所在地的时区及时间。

> 关闭无障碍

打开系统设置，找到无障碍（系统或更多设置中），关闭或卸载所有使用无障碍的应用（例如 talkback，autojs 等）。

### 网络设置

对于真机，你只需要确保电脑与手机在同一网络下即可。
对于模拟器，默认创建的模拟器正常情况下与你的本机网络并不互通，如果你使用的是 android x86 (基于 VMWare 的安卓虚拟机)，
请尝试在虚拟机设置中将网络模式设置为桥接模式。对于雷电，夜神等模拟器，需要在其设置中根据提示安装驱动并开启桥接模式随后重启模拟器。
对于 Android Studio 的 Virtual Device，则没有相关设置，如果需要连接 AVD，请先执行 `adb forward tcp:65000 tcp:65000`，
并使用 `localhost` （不要使用 127.0.0.1）进行连接。


### 其他设置

> WSA (Windows Subsystem Android)

如果使用的是 WSA (Windows Subsystem Android)，请确保 WSA 版本不低于 2210.40000 并且已 root。随后打开 WSA 设置 -> Subsystem Resources -> 选择 Continuous，关闭 Advanced Networking。随后重启 WSA 子系统即可。

> AVD (Android Studio Virtual Device)

如果使用的是 AVD (Android Studio Virtual Device)，请先使用如下方式扩展默认存储空间的大小。

```bash
# Pixel_5_API_29 为虚拟机ID，可以使用命令 emulator -list-avds 列出
# -partition-size 部分新建的 AVD 可用存储空间可能只有百兆，这里修改为 2G
emulator -avd Pixel_5_API_29 -partition-size 2048 -no-snapshot-load
# 随后每次启动虚拟机时都使用该命令
#
# 可能会遇到找不到 emulator 命令的情况，
# 请参阅此文档获知此命令的位置 https://developer.android.com/studio/run/emulator-commandline?hl=zh-cn 并将其加入 PATH 变量中
#
# 如果你无法完成上面的命令，请手动点击 Android Studio 中的 Virtual Device Manager，新建一个虚拟机，随后找到对应虚拟机并点击后方的编辑按钮（一个笔的符号），
# 点击 Show Advanced Settings，找到 Storage -> Internal Storage 并将其设置为至少 2GB。
```

> Redroid (android in docker)

如果使用的是 Redroid (android in docker)，以官方建议的 `Ubuntu 20.04` 为例，首先安装 linux-modules-extra 相关模块，（注意下列方法可能不适合其他 Linux 发行版，如果你不熟悉 Linux，我们不太建议你继续下面的操作）。

```bash
apt install linux-modules-extra-`uname -r`
```

编辑文件 `/etc/modules`，将下列名称复制并插入文件底部，重启当前宿主机。

```bash
# redroid modules
mac80211_hwsim

binder_linux
ashmem_linux
```

**或者**每次宿主机重启后执行（注意如果不用上述的方法那么每次重启都要这么做）

```bash
modprobe mac80211_hwsim
modprobe binder_linux devices="binder,hwbinder,vndbinder"
modprobe ashmem_linux
```

最后使用以下命令启动，`redroid_gpu_mode` 请根据实际进行修改（注意这与官方写的命令有所不同）。

```bash
docker run -itd --rm --privileged --pull always -v /lib/modules:/lib/modules:ro -v ~/redroid:/data -p 5555:5555 redroid/redroid:12.0.0-latest androidboot.redroid_gpu_mode=guest
```


## 安装客户端

请使用 3.6 - 3.10 版本的 Python，建议有条件使用 Python 3.9

```bash
pip3 install -U lamda
# 即可
#
# 如果需要使用内置 frida，务必使用下列方法安装
# 你可能需要外网访问来安装 frida，否则可能会卡住许久(~10分钟)直至安装失败
# 即使之前安装过 frida，也应该重新执行以下命令
pip3 install -U --force-reinstall 'lamda[frida]'
# 请注意完成安装后，你需要同时使用 pip 更新任何依赖 frida
# 的第三方库例如 frida-tools objection 等（如果安装过的话）
# 否则后期使用可能会出现难以察觉的异常
```

安装完成后，执行命令 `python3 -m lamda.client` 检查是否安装正确。如果出现如下类似报错

```python
* AttributeError 'NoneType' object has no..
* TypeError: Couldn't build proto file..
```

可能是因为安装的其它依赖 protobuf 的包产生冲突。请尝试执行如下命令

```bash
pip3 install -U --force-reinstall lamda
```

如果仍然存在问题，请创建 virtualenv 来使用。


## 安装服务端

安装前，请先选择合适的架构，可以通过 adb shell 命令 `getprop ro.product.cpu.abi` 来获取当前的系统架构。
正常情况下，对于现时代的手机，可以直接选择 `arm64-v8a` 版本，而对于模拟器如雷电，你会在新建模拟器时选择32或64位版本的安卓系统，
32位模拟器系统对应 `x86`，64位则对应 `x86_64`，正常情况下，雷电模拟器默认创建的为基于 `x86` 的安卓 7.0 系统。

LAMDA 支持设备状态主动上报，你可以编写接口或使用 grafana 来记录设备运行状况，其中包含了系统、网络、内存、CPU、磁盘等等信息。

```bash
# 如果不清楚这个功能是什么请不要执行，注意替换掉以下链接
echo "stat-report.url=http://example.com/report" >>/data/local/tmp/properties.local
```

这样 LAMDA 会在启动后**每分钟**向此链接**POST**设备状态信息（JSON），由于字段较多，将不在此罗列。


LAMDA 会定期从 github 更新，默认频道更新频率约1-2月一次，stable 的更新频率为 3-6 月，建议定期手动从 github release 下载最新版本手动更新。如果该频率会影响到你的使用，在首次启动 LAMDA 之前执行以下命令创建更新配置。

```bash
# 进入 adb shell 执行
echo "upgrade.channel=stable" >>/data/local/tmp/properties.local
```

在开始前，有必要介绍一下上面的 `properties.local` 文件，
properties.local 为 LAMDA 的启动配置文件，通常存储于设备之上，其中包含了 `a=b` 类型的字符串，
通过编写此文件，你可以实现在 LAMDA 启动时自动连接到 OpenVPN、代理、端口转发等。
LAMDA 在启动时，会从 `/data/usr`、`/data/local/tmp`、`${CFGDIR:-/data/local}` 查找该文件并载入。
你可以在以上三个位置任意一个放置你的 properties.local 配置文件。

除了 `properties.local`，还有一个从加载远端配置的参数 `--properties.remote`，它可以让 LAMDA 在启动时从HTTP服务器下载配置，请继续看往启动 LAMDA 的章节。

关于如何编写配置，在各个功能中会有介绍。

> launch.sh 可能出现的错误及解决方法

```bash
# 显示 llllaamDaa started 则服务已经正常进入 daemon 模式，可以退出终端

already running     (已经在运行，请不要多次启动)
invalid TZ area     (时区未设置，在系统时间设置中设置时区即可，可能出现于国外或原生系统上)
not run as root     (没有以 root 身份运行)
unsupported sdk     (在不支持的安卓系统上运行)
abi not match       (使用了错误的 tar.gz 包)
```

### 通过 Magisk 安装

如果你的设备使用了 Magisk，那么你可以以最简单的方法完成安装，并且 LAMDA 可以**开机自启动**。需要确保 Magisk 版本 >= 20.4 且只支持在 **Magisk App** 中安装。同时，使用 Magisk 安装更便于统一化，你可以自定义配置，例如，你想要所有使用该 magisk 模块刷入后的 LAMDA 都启用接口认证（certificate），
或者希望这些设备都在启动时自动连接代理，你只需要编写 properties.local 或者生成PEM证书并重命名为 `lamda.pem`（请查看 tools/ 中的工具使用方法），
随后使用**压缩软件**打开 `lamda-magisk-module.zip`，并将其（`lamda.pem` 或者 `properties.local`）拖入 `common` 文件夹即可实现启动时自动配置！

现在，从 [lamda/releases](https://github.com/rev1si0n/lamda/releases) 页面下载 `lamda-magisk-module.zip`，并将其 push 到 `/sdcard`，打开 Magisk App，点击 模块->从本地安装，选择 lamda-magisk-module.zip 稍作等待即可。

刷入成功后，请重启设备。重启后，LAMDA 应该会在开机时自启动。但是为了避免可能的崩溃问题，lamda 会在 30 秒后启动而不是立即启动，你将有足够的时间去禁用 LAMDA 模块（请在开机后2分钟再连接使用 LAMDA）。安装完成后，你无需再看下段手动安装的内容，跳过即可。

### 手动安装

手动安装是通常做法，下面将会介绍两种方式，两种方式的区别是：部分老旧设备可能无法通过系统的 `tar` 命令来解压 tar.gz 后缀的文件，所以提供了 `*-install.sh` 用来作为补充，其内置了一个 busybox 用来解压。已知 getprop 获得的设备架构为 `arm64-v8a`，现在将设备连接到当前电脑并确保已授权 ADB、可以正常切换 root。

#### 方式 1

从 `release` 页面 [lamda/releases](https://github.com/rev1si0n/lamda/releases)
下载 `arm64-v8a.tar.gz-install.sh`。

```bash
# /data/local/tmp 是标准服务安装路径，但并不是强制要求
# 你可以放到除了 /sdcard 之外任何具备可读写权限的文件夹
adb push arm64-v8a.tar.gz-install.sh /data/local/tmp
# 进入 adb shell
adb shell
# 输入 su 确保为 root 身份
su
# 切换到目录
cd  /data/local/tmp
# 执行安装脚本并启动（这将解包并启动服务）
sh arm64-v8a.tar.gz-install.sh
# 删除安装包
rm arm64-v8a.tar.gz-install.sh
```

#### 方式 2

从 `release` 页面 [lamda/releases](https://github.com/rev1si0n/lamda/releases)
下载 `arm64-v8a.tar.gz`。

```bash
# /data/local/tmp 是标准服务安装路径，但并不是强制要求
# 你可以放到除了 /sdcard 之外任何具备可读写权限的文件夹
adb push arm64-v8a.tar.gz /data/local/tmp
```

完成后，进入 `adb shell`，解包文件：

```bash
# 你现在应该在 adb shell 内
cd /data/local/tmp
# 解包服务端文件
# 注意自带的 tar 命令可能因为不支持 z 选项导致解包失败，你可能需要使用 busybox tar 来解包
# 如果系统不附带 busybox 命令，请自行从 https://busybox.net/downloads/binaries/1.20.0 下载合适架构的版本
tar -xzf arm64-v8a.tar.gz
# 删除安装包
rm arm64-v8a.tar.gz
```

## 启动服务端

对于方式 1 安装，安装后会顺带启动服务，所以使用该方法**安装后**你无需执行下面的命令，但是按照下面的操作再来一次也并没有问题。
对于上面任意一种安装方法，你永远只需要在首次安装时操作，但是**启动服务**的过程则需要在每次 设备重启 或者 你手动关闭 LAMDA 后执行，因为 LAMDA 不会自己运行。

进入 adb shell，并切换为 `su` root 身份，执行：

```bash
# 你现在应该在 adb shell 内，切换到目录
cd /data/local/tmp
#
# 启动服务端
# 注意，arm64-v8a 这个目录根据平台不同名称也不同
# 如果你使用的是 x86 版本，那么这个目录名则是 x86/，你需要对命令做相应修改
sh arm64-v8a/bin/launch.sh
#
# 如果你想要启用加密传输
# 请先使用 tools/ 中的 cert.sh/py 来生成PEM证书
# 将其push到设备例如 /data/local/tmp/lamda.pem
# 并将其属主及权限设置为 root 以及 600 (chown root:root lamda.pem; chmod 600 lamda.pem)
# 并使用以下命令启动，lamda.pem 必须为绝对路径
sh arm64-v8a/bin/launch.sh --certificate=/data/local/tmp/lamda.pem
# 这将加密任何通过 LAMDA 客户端产生的通信流量
# 但不包括 webui 远程桌面的流量
#
# 从远端加载 properties.local
# 有时候你可能希望从链接加载启动配置，这时你可以将 properties.local 上传到服务器
# LAMDA 在下载此配置时，会提供当前设备的部分信息如，设备唯一ID，设备型号，当前版本等。
# 你也可以自行编写web服务来根据这些设备参数分发不同的启动配置
# 建议使用 HTTPS 链接增加安全性，请确保设备时间正确。
# 随后使用如下方式启动 LAMDA
sh arm64-v8a/bin/launch.sh --properties.remote=http://example.com/config/properties.local
# 对于开启了 Basic Auth 的静态文件服务，同样支持提供用户名密码
sh arm64-v8a/bin/launch.sh --properties.remote=http://user:password@example.com/config/properties.local
# 提示：LAMDA 会在超时或者返回 50x 状态码时重试请求，
# 如果连续 5 次仍然失败，LAMDA 会放弃尝试并继续启动。
#
# 当然，可以自定义重试次数但是注意，如果服务器持续无响应，LAMDA 也将永远卡在这里
# 什么时候需要设置重试次数：刚开机时设备可能并没有网络连接，如果你要在这时启动 LAMDA 你可以增大该值
sh arm64-v8a/bin/launch.sh --properties.remote=http://example.com/config/properties.local --properties.tries=30
# 重试机制的每轮等待秒数n会随着重试次数的增加而增加。所以请谨慎设置该值。
#
# 如果你需要 LAMDA 监听到特定端口而不是 65000
# 如果修改，请确保所有内网设备均以相同端口启动
# 否则设备发现等功能无法正常工作
sh arm64-v8a/bin/launch.sh --port=8123
# 请不要绑定 1024 以下的端口
```

静待退出，随即关闭终端，至此服务启动完成。

**注意**：首次启动时有几率出现远程桌面一直加载。发生这种情况时，请首先尝试重启设备并重新启动 lamda。
如果在启动或使用中多次遇到设备黑屏/重启卡顿等类似情况，建议停止使用。

## 退出服务端

LAMDA 设计为一个 7*24 小时后台运行的服务，不建议频繁启动关闭，如果确需这样做，请务必确保你通过以下两种方式关闭。如需使用接口关闭服务请参照下方 `关机重启` 章节，考虑到可能不方便使用接口，你也可以使用以下命令。

```bash
kill -SIGUSR2 $(cat /data/usr/lamda.pid)
```

LAMDA 服务完全退出可能需要十几秒的时间，请不要连续多次执行此命令。

## 卸载服务端

LAMDA 对于自身数据的规划非常规范，绝对不会在你的系统中随意放置文件。
你可以通过几条命令完全卸载 lamda，在进行前，请先按照上方 `关闭 LAMDA 服务` 执行并等待至少30秒以确保服务正常退出。

```bash
# 删除 LAMDA 相关目录
rm -rf /data/local/tmp/arm64-v8a /data/usr
# 重启设备
reboot
```

# 使用 LAMDA

设备上的 `65000` 端口为本服务的标准公用端口，可能需要记住，但是大部分情况下，你不需要显式提供此端口号。
下面请先在 WLAN 设置中取得**当前设备的IP地址**，你也可以通过 tools/ 目录里的工具来列出当前网络中的所有设备及IP，
下面将会一直**假设**设备的IP为 `192.168.0.2`。

## 远程桌面

在浏览器中打开 `http://192.168.0.2:65000` 可进入 web 远程桌面，你可以在此操作设备以及通过该界面的root模拟终端执行命令。
不支持多人访问，不保证兼容所有浏览器，建议使用 Chrome。如果启动服务端时指定了PEM证书 `--certificate`，远程桌面将需要你输入密码才能继续访问，你可以在PEM证书最后一行找到这个32位的固定密码。

web 端的远程桌面在复杂局域网下可能不太流畅，如果需要更加流畅的操作体验，请先看下面的章节 `无线连接内置 root 权限的 WIFI ADB`，
完成 adb connect 到 LAMDA 后，安装使用 [Genymobile/scrcpy](https://github.com/Genymobile/scrcpy) 或者 [barry-ran/QtScrcpy](https://github.com/barry-ran/QtScrcpy) 来获得更加流畅的操作体验，具体使用方法请查看其使用文档。

## 文件上传

你可以在此页面直接**拖动文件或目录到右侧终端**上来上传文件/文件夹到设备，支持同时拖动多个文件或文件夹，单个文件最大不得超过 256MB，最多只支持同时上传 2k 个文件，上传的任何文件权限均为 644，文件将始终上传到 `/data/local/tmp` 目录下。

## 文件下载

LAMDA 允许你通过浏览器浏览设备上的目录及下载文件，只需要在浏览器打开链接 `http://192.168.0.2:65000/fs/` 即可（注意最后面的 `/`）。

## 连接设备

> 现在，将配合 lamda 库进行介绍，在开始前，请先确保你已经根据上文 `客户端安装` 章节正确安装了客户端库。

建议顺带翻看客户端的源码，并不是需要理解，仅仅是让你能了解到底有什么参数可以使用。

```python
from lamda.client import *

d = Device("192.168.0.2")
# 如果在服务端启用了 certificate 请这样连接
d = Device("192.168.0.2", certificate="/path/to/lamda.pem")
```

或者，如果你熟悉 uiautomator2，也可以通过 u2 来使用自动化功能

```python
import uiautomator2 as u2

# 注意：只兼容约7成主要接口，并且服务端未启用 certificate 选项
d = u2.connect("http://192.168.0.2:65000")
```

或者，直接执行命令
```bash
# 注意这个DEVICE参数是IP，自行替换
python3 -m lamda.client -device 192.168.0.2
# 随后可以直接在此 shell 中输入下方语句
```

> 下文中的 `d` 将始终假设为 `d = Device("192.168.0.2")` 实例。

## 先来一个热身

如下方法可以使你的手机发出一声蜂鸣，需要手机为非静音状态。

```python
d.beep()
```

## 设置系统代理

只支持 http 以及 socks5 代理，不支持 IPv6


> 假设你从服务商处获得的代理为 http://123.123.123.123:8080，
> 仅需如下几行代码来让设备上的 tcp 流量通过此代理

```python
profile = GproxyProfile()
profile.type = GproxyType.HTTP_CONNECT

# 此选项请根据实际情况选择你是否需要
profile.drop_udp = True
profile.host = "123.123.123.123"
profile.port = 8080

d.start_gproxy(profile)
```

> 详细的参数配置信息

```python
profile = GproxyProfile()
# socks5 代理则为 GproxyType.SOCKS5
profile.type = GproxyType.HTTP_CONNECT
# 如果你需要重定向 DNS 查询到 114.114.114.114
# 注意此 DNS 是系统全局的，系统发出的所有DNS将会被转发
# 如果是与OpenVPN共存的情况，不要设置为OpenVPN的内网DNS服务器，否则可能会导致彻底断网
# 去掉 nameserver 配置行将使用系统默认 DNS
#
# 为什么有此选项：你可以修改一些应用的 dns 域名解析
profile.nameserver = "114.114.114.114"
profile.host = "代理服务器地址"
profile.port = 代理服务器端口

# 如果这个代理服务器需要登录信息（注意：如果没有，请注释或删除如下两行）
profile.password = "代理服务器登录密码"
profile.login = "代理服务器登录用户"

# socks5 模式支持 udp 代理，但是 http 代理并不支持
# 因为 udp 多数情况下并不会被代理，所以禁用 udp 流量是一个不错的选择
# 当 drop_udp 为 True 时，应用/系统的 UDP 流量将会被屏蔽，默认为 False
profile.drop_udp = False

# 本地流量是否需要*不经过*代理，如果为 True，本地流量
# 如 192.168.x.x 10.x.x.x 等路由器内网网段的流量将不会经过代理，默认为 False
# 注意：如果开启了 udp_proxy，此选项对于 UDP 流量无效
profile.bypass_local_subnet = True

# 是否需要代理 udp 流量
# 注意，http 代理服务不支持代理 udp 协议，开启此选项必须使用 socks5 作为代理服务器
# (GproxyType.SOCKS5)，且 socks5 代理服务器必须配置开启 udp 代理模式，
# 需要稍加复杂的服务器配置，为了避坑，请参照 tools/socks5 里的介绍进行安装配置
# 当你使用 http 代理或者 drop_udp 选项为 True，此设置将会被忽略
profile.udp_proxy = False

# 如果需要仅对特定应用使用代理（例如安卓浏览器，如果是全局则删除这两行）
app = d.application("com.android.browser")
profile.application.set(app)

#     注意事项以及提示：
# 设置代理后，正在运行的应用是不会立即使用设置的代理的
# 因为这些应用在设置代理之前就已经完成了 tcp 连接的建立
# 所以，需要你手动关闭应用并启动，应用才会通过代理建立连接
# 也就是说，如果你是做中间人流量分析，那设置代理后
# 你需要关闭应用再重新打开才会看到应用的请求
#
# 注：本机的 DNS 流量始终不会经过代理

# 启动代理
d.start_gproxy(profile)
# 关闭代理
d.stop_gproxy()
```

> 快速搭建一个 socks5 代理

LAMDA 在 tools/ 中提供了一个开箱即用同时支持 udp 的 socks5 代理服务 docker，请转到 tools/socks5 目录查看 README.md。

> 在 LAMDA 启动时自动连接代理

复制下列配置并修改相关配置为你的代理信息

```txt
gproxy.enable=true
gproxy.type=http-connect
gproxy.host=123.333.333.333
gproxy.port=8080
gproxy.password=
gproxy.login=
```

将其追加或者写入到 properties.local，重启 LAMDA 即可。

## 安装中间人证书

> 建议你使用或参考已经封装好的 tools/ 目录下的 startmitm.py, globalmitm 工具，这里介绍的是相关接口。

请先确保你已经准备好 fiddler, mitmproxy 给你的证书，对于 mitmproxy，
给你的证书为 pem 格式如下示例。而对于 fiddler，则可能是 crt 格式，直接将该文件路径
作为参数提供即可无需关心任何转换/文件名问题。

为了避免浪费不必要的时间，在这里推荐使用 `mitmproxy`，
如果你使用的是 `Charles` 等，我无法确保你可以一次性完成设置，
因为此类应用配置项目较为复杂且你可能需要理解各种代理类型才能正确配置SSL中间人，
如果你一定要使用，建议使用 Charles 的 socks5 作为代理协议。

注意：有可能不支持安卓 13

```python
import os

# 拼接 mitmproxy-ca-cert.pem 文件的路径
HOME = os.path.expanduser("~")
cert_path = os.path.join(HOME, ".mitmproxy", "mitmproxy-ca-cert.pem")
# 以 mitmproxy 为例，使用如下代码安装证书
d.install_ca_certificate(cert_path)

# 使用如下代码卸载证书（如不常变化不建议频繁安装卸载）
d.uninstall_ca_certificate(cert_path)
# 此证书安装接口是通用的，你可以用它安装任何应用要求你安装的证书
# 你同样可以用其安装 Fiddler/Charles 要求你安装的证书
# 只需要提供文件路径即可
```

接着，看 `设置 http/socks5 代理` 节，将代理设置为中间人应用监听的地址即可。
按照流程完成后如果没有截获到流量请参加设置代理部分的**特别注意**。

## 设置 OpenVPN

> 此 OpenVPN 只支持使用证书登录，可以与 http/socks5 代理共存。
> 需要注意的是，此功能只包含OpenVPN的主要功能，除了 `DNS` 配置，暂无法应用服务端推送的其他配置信息。
> 这些配置包括但不限于 PAC 代理，http 代理配置等。为了省却你安装服务的麻烦，
> LAMDA 提供了一个开箱即用的 OpenVPN docker 镜像，它有脚本可以生成下面这个配置，请继续往下看。

非常建议使用 tools 里的 OpenVPN docker 安装及生成如下连接配置。

```python
profile = OpenVPNProfile()

# 是否全局 VPN，为 False 时仅路由服务器端推送的特定网段
profile.all_traffic  = True
# 服务器端开启的连接协议 (或者为 OpenVPNProto.TCP)
profile.proto        = OpenVPNProto.UDP
profile.host         = "OpenVPN 服务器地址"
profile.port         = OpenVPN 服务器端口
# 服务器端通道加密方法
profile.cipher       = OpenVPNCipher.AES_256_GCM

profile.tls_encryption = OpenVPNEncryption.TLS_CRYPT
profile.tls_key_direction = OpenVPNKeyDirection.KEY_DIRECTION_NONE
profile.tls_key = """
-----BEGIN OpenVPN Static key V1-----
tls key / tls auth
-----END OpenVPN Static key V1-----
"""

profile.ca = """
-----BEGIN CERTIFICATE-----
服务端配置的 ca 证书
-----END CERTIFICATE-----
"""

profile.cert = """
-----BEGIN CERTIFICATE-----
客户端证书
-----END CERTIFICATE-----
"""

profile.key = """
-----BEGIN PRIVATE KEY-----
客户端私钥
-----END PRIVATE KEY-----
"""

# 启动 OpenVPN
d.start_openvpn(profile)
# 关闭 OpenVPN
d.stop_openvpn()
```

> 快速搭建一个 OpenVPN 服务

LAMDA 在 tools/ 中提供了一个开箱即用的 OpenVPN docker，请转到 tools/openvpn 目录查看 README.md。

> 在 LAMDA 启动时自动连接 VPN

你可以使用 tools/openvpn 提供的命令来生成 properties.local 配置，请不要自行编写。

## 连接内置的 FRIDA

> 非逆向工作无需阅读此节

启动本框架前后，**请勿**再次自行启动任何 frida-server，否则有可能会导致系统崩溃。你只需要通过下列代码使用内置 frida 即可。

1. 通过代码连接

```python
# 使用 LAMDA 时的做法
device = d.frida
device.enumerate_processes()
```

等效于

```python
# 只是示例，请尽量使用上述方法连接
manager = frida.get_device_manager()
device = manager.add_remote_device("192.168.0.2:65000")
device.enumerate_processes()
```

2. 通过命令行使用

对于所有 frida 官方命令行工具，你只需要加上参数 `-H 192.168.0.2:65000` 即可。

```bash
frida -H 192.168.0.2:65000 -f com.android.settings
# 如果你在服务端启动时指定了 certificate 选项，请注意也需要在此加入 --certificate 参数例如
frida -H 192.168.0.2:65000 -f com.android.settings --certificate /path/to/lamda.pem
```

对于 objection 以及 r0capture 等，这些第三方工具可能并不会完全遵循原生 frida 工具的命令行用法，如果你需要使用这些第三方工具，需要确保 LAMDA 启动时**没有使用** `--certificate` 参数（加密传输），因为这些工具可能并没有可以传递PEM证书的参数。

```bash
# objection 示例连接方法 (-N -h 192.168.0.2 -p 65000)
objection -N -h 192.168.0.2 -p 65000 -g com.android.settings explore
```

```bash
# r0capture 示例连接方法 (-H 192.168.0.2:65000)
python3 r0capture.py -H 192.168.0.2:65000 -f com.some.package
```

```bash
# jnitrace 示例连接方法 (-R 192.168.0.2:65000)
jnitrace -R 192.168.0.2:65000 -l libc.so com.some.package
```

```bash
# frida-dexdump 示例连接方法 (-H 192.168.0.2:65000)
frida-dexdump -H 192.168.0.2:65000 -p PID
```

其他未提及的第三方工具请自行查看其使用方法。

## 使用 FRIDA 暴露 Java 接口

这个功能类似于 [virjar/sekiro](https://github.com/virjar/sekiro)，关于它的用途请参考 virjar 大佬的
项目。此功能需要你能熟练编写 frida 脚本。

> 请转到 tools 目录查看使用方法。

此功能需要你能熟练编写 frida 脚本。示例中使用的脚本请参照 test-fridarpc.js 文件，特别注意: frida 脚本中 rpc.exports 定义的函数参数以及返回值只能为 int/float/string/list/jsdict 或者任意 js 中**可以被 JSON序列化**的值。假设设备IP为 192.168.0.2。

> 执行以下命令注入 RPC 到 com.android.settings（注意查看是否有报错），下面的相关文件在 tools 目录

```bash
python3 fridarpc.py -f test-fridarpc.js -a com.android.settings -d 192.168.0.2
```

现在已经将接口暴露出来了，只需要请求 `http://192.168.0.2:65000/fridarpc/myRpcName/getMyString?args=["A","B"]` 即可得到脚本内方法的返回结果，链接也可以用浏览器打开，接口同时支持 POST 以及 GET，参数列表也可以同时使用多个参数，空列表代表无参数，注意这里的 args 参数序列化后的字符串最长**不能超过** `32KB`。

链接中的两个字符串参数 "A", "B" 即为注入的脚本中的方法 `getMyString(paramA, paramB)` 的位置参数。

注意参数的提供形式，是**双引号**，请**不要手打**或者**字符串拼接**这个参数，务必使用 json.dumps(["A", "B"])

> 用 requests 调用
```python
import json
import requests
url = "http://192.168.0.2:65000/fridarpc/myRpcName/getMyString"
# 请求接口
res = requests.post(url, data={"args": json.dumps(["A","B"])})
print (res.status_code, res.json()["result"])

#* 状态码 200 一切正常
#* 状态码 410 需要重新注入脚本或者脚本未注入（目前不支持自动重新注入）
#* 状态码 500 脚本或参数异常
#* 状态码 400 参数错误
```

响应结果的格式是固定的，可在浏览器打开查看。同样，配合下面一节的内容，你将可以在公网直接使用接口。

## 使用内置的定时任务

内置了用于执行定时任务的 cron 服务，这样你可以在设备上定期执行一些脚本，所有规则都将以 root 身份执行。

> 此功能需要你会编写 crontab 规则，如果你不清楚 crontab，请先自行了解。

现在，请打开 web 控制台或者连接设备的 ssh/adb shell，执行命令 `crontab -e`，你将进入编辑模式，在英文输入模式下按下字母 `i`，随后写下相关规则，并依次按下 `ESC`，`SHIFT` + `:`，输入 `wq` 并按下回车来保存即可。受限于安卓休眠机制，息屏后定时任务可能并不会以你期望的时间运行，你可能需要将设备设置为常亮。

> 一些规则示例

```
@reboot      echo 框架启动/重载(reload)时执行
0 */1 * * *  echo 每一小时执行
* * * * *    echo 每一分钟执行
0 8 * * *    echo 每天八点执行
```

## 使 LAMDA 可被任意地点连接

有时候你可能遇到这种情况：你的手机在家里而你不在家该怎么使用呢。
开始前，你可能需要先准备一台公网服务器。为了安全考虑，这里使用的是最保守的配置，最后会说明如何做到完整介绍的功能。

因为有了公网服务器，lamda 有很多方法可以做到这个要求，使用 **OpenVPN** 来实现更加优雅。当然最方便的还是使用 frp。tools 文件夹内都提供了相关服务的 docker 镜像并且这些镜像可以一键命令生成下面的配置信息，可以转到 tools 查看使用方法。

本服务使用了较为成熟的端口转发程序 [fatedier/frp](https://github.com/fatedier/frp)，关于如何配置服务端，请在此项目中自行探索。注意：请勿将转发后的端口绑定到公网地址，请确保你的公网服务器关闭了所有不必要的端口。
这里给你一个最简单安全的配置，可以直接使用如下命令启动服务端。

> 首先在你的公网服务器上执行以下命令启动 frps（注意你可能还需要配置防火墙）

```bash
frps --token lamda --bind_addr 0.0.0.0 --bind_port 6009 --proxy_bind_addr 127.0.0.1 --allow_ports 10000-15000
```

> 然后编写 properties.local

复制下列配置并修改**服务器地址**为你的服务器公网IP

```txt
fwd.host=服务器地址
fwd.port=6009
fwd.rport=12345
fwd.token=lamda
fwd.protocol=tcp
fwd.enable=true
```

将其追加或者写入到 properties.local，重启 LAMDA 即可。

> 如何透过上面的转发使用 lamda（需要在部署 frps 的那台公网服务器上使用，因为我们绑定了转发的端口到 127.0.0.1）

```python
from lamda.client import *
# 端口为上面的 rport
d = Device("127.0.0.1", port=12345)
# 浏览器打开 http://127.0.0.1:12345 即可访问远程桌面
# 其余任何接口调用实现均统一，无需做任何改动
```

> 如何批量转发而不用每次都改写一下 rport 配置

如果你需要一次设置多台机器且不在乎每台机器绑定的端口，
你可以将上方配置中的 `fwd.rport` 值改为 0，这将导致你的设备被随机绑定到 `10000-15000` 的端口范围中，
你可以通过后期轮训端口范围来定位设备转发绑定的对应端口。

> 我就是想在任意地方都能连接到设备

首先，为了安全起见不建议这么做，如果确实需要这样用的话，建议使用 OpenVPN 将设备和你的电脑置于同一网段的方法来访问。
如果你仍准备使用上述 frp 的方法实现任意访问，请先确保 LAMDA 服务启动时使用了**PEM证书**，并将启动 frps 命令时的 `--proxy_bind_addr 127.0.0.1`
改为 `--proxy_bind_addr 0.0.0.0`，这将导致 12345 端口直接绑定到公网。如果你未使用PEM证书启动 lamda，任何人都将可以访问，这是**非常非常危险**的。
其次需要注意，web 远程桌面的流量始终都是 http 的，如果有人在你和服务器通信之间进行中间人，你的登录凭证可能会被窃取。当然，如果此期间不用 web 桌面将不存在这个问题。


## 读写系统属性

> 设置/读取系统属性

```python
# 获取 ro.secure 的值
d.getprop("ro.secure")

# 设置 ro.secure 的值
d.setprop("ro.secure", "0")
```

## 读写系统设置

> 设置/读取安卓系统设置

```python
settings = d.stub("Settings")

# 如果你对以下 screen_brightness 等字符串表示疑惑，请查看下列文档。有些常量
# 在不同版本的安卓可能并不兼容，以及部分厂商会有自定义的变量，需要注意。

# https://developer.android.com/reference/android/provider/Settings.System
# https://developer.android.com/reference/android/provider/Settings.Secure
# https://developer.android.com/reference/android/provider/Settings.Global

# 你可以使用如下代码将系统屏幕的亮度设置为手动
settings.put_system("screen_brightness_mode", "0")

# 示例：获取并修改屏幕亮度为 5 (0-255)
settings.get_system("screen_brightness")
settings.put_system("screen_brightness", "5")

# 示例：关闭开发者选项
settings.get_global("development_settings_enabled")
settings.put_global("development_settings_enabled", "0")

# 示例
settings.get_secure("screensaver_enabled")
settings.put_secure("screensaver_enabled", "0)
```

## 获取设备运行状态

```python
status = d.stub("Status")

# 获取设备启动时间
status.get_boot_time()

# 获取设备磁盘使用情况
status.get_disk_usage(mountpoint="/data")

# 获取电池信息
status.get_battery_info()
# 获取CPU使用情况
status.get_cpu_info()
# 获取总体磁盘读写情况
status.get_overall_disk_io_info()
# 获取用户数据磁盘的读写情况 (userdata)
status.get_userdata_disk_io_info()
# 获取总体网络收发情况
status.get_overall_net_io_info()
# 获取 wlan0 接口的网络收发情况
status.get_net_io_info("wlan0")
# 获取内存使用情况
status.get_mem_info()
```

## 在设备上执行命令

> 在设备后台，前台执行 shell 脚本/命令

```python
# 执行前台脚本（执行时间短（0-10秒内）的脚本）
cmd = d.execute_script("whoami")
print (cmd.exitstatus)
print (cmd.stdout)
print (cmd.stderr)

# 执行后台脚本（执行时间长的脚本）
# 对于后台脚本，因考虑可能用户写出死循环脚本无限输出导致内存占满等问题
# 暂时无法获知其执行结果
ID = d.execute_background_script("sleep 100; exit 0;")
# 检查后台脚本是否结束
d.is_background_script_finished(ID)
# 强制结束后台脚本
d.kill_background_script(ID)
```

## 使系统可调试

如果你需要使用JEB，IDA等动态分析，你可能需要设置此标志才能进行，当然也内置了这个功能，你可以这么做而无需永久修改 `ro.debuggable`。
但是记住，这个接口你并不是一定需要调用，仅当你看到任何文章/教程让你修改 `ro.debuggable` 时使用。

注意：调用此接口成功后，系统会自动重启，你可能仍需像首次启动时等待一段时间到本框架恢复

> 慎用，此功能可能不稳定且可能随时移除

```python
debug = d.stub("Debug")

r = debug.set_debuggable()
print (r)
```

## 启动 IDA 调试服务

> 内置了 IDA 7.5 服务端

```python
debug = d.stub("Debug")

# 启动 IDA 32 服务端（端口可自定义）
debug.start_ida(port=22032)
# 检查是否已启动
debug.is_ida_running()
# 关闭 IDA 32 服务端
debug.stop_ida()
# 如果调试的是64位程序，将方法名中的 ida 替换为 ida64 即可
# 例如
debug.start_ida64(port=22064)
#
# 如果需要自定义 ida-server 的环境变量例如 IDA_LIBC_PATH (同样适用于 start_ida)
debug.start_ida64(port=22064, IDA_LIBC_PATH="/apex/com.android.runtime/lib64/bionic/libc.so")
# 当你调试的目标程序是32位时使用 start_ida
# 否则使用 start_ida64
# 当你的设备系统为32位平台时，start_ida64 将会无效
```

## 无线连接内置的 WIFI ADB

此 ADB 非全功能 adb，仅支持 shell,pull,push,forward,reverse 等常用功能
通过此功能你将**无需开启开发者模式**即可连接最高权限的 adb。

> 注：jdwp 调试相关功能具有唯一性，与系统内置存在冲突所以此 adb **目前**不支持。

```python
# LAMDA 内置的 adb 服务完全独立于系统本身提供的 adb 服务
# 所以在使用之前需要先手动调用以下接口将你的 adb 公钥安装至设备上
# 否则直接连接将会显示未授权（系统设置开发者模式中授权的秘钥与内置 adb 并不通用）
#
# tools 目录下的 adb_pubkey.py 封装了下面接口的安装过程
# 你可以使用该脚本一键授权，允许本机连接，请查看其 README，以下代码仅做参考说明
#
# 这个秘钥文件位于你电脑上的 ~/.android 或者 C:\\Users\xxxx\.android，文件名为 adbkey.pub
# 如果不存在这个文件但是存在文件 adbkey，请切换到该目录并执行命令
# adb pubkey adbkey >adbkey.pub 来生成 adbkey.pub
#
# 随后使用 python 代码来拼接这个生成的 adbkey.pub 路径
import os
keypath = os.path.join("~", ".android", "adbkey.pub")
abs_keypath = os.path.expanduser(keypath)
print (abs_keypath)
#
# 然后安装这个 adbkey.pub 到 LAMDA
d.install_adb_pubkey(abs_keypath)
# 这样你就可以连接内置 adb 了
# 通过命令 adb connect 192.168.0.2:65000 连接到设备
# 你完全可以将其理解为 WIFI ADB
#
# 或者如果你需要从 LAMDA 内置 adb 移除这个公钥
d.uninstall_adb_pubkey(abs_keypath)
```

## 文件操作

> 将文件上传至设备或从其下载文件（支持大文件）

```python
# 下载文件到本地
d.download_file("/verity_key", "写入到的本地文件")

# 下载文件到 内存/已打开的文件
from io import BytesIO
fd = BytesIO()
d.download_fd("/verity_key", fd)
print (fd.getvalue())

# 注意必须使用 w+b 模式打开被写入文件
fd = open("写入到的本地文件", "wb")
d.download_fd("/verity_key", fd)

# 上传文件到设备
d.upload_file("本地文件路径.txt", "/data/local/tmp/上传到设备上的文件.txt")

# 从 内存/已打开的文件 上传文件
from io import BytesIO
d.upload_fd(BytesIO(b"fileContent"), "/data/local/tmp/上传到设备上的文件.txt")

# 注意必须使用 rb 模式打开文件
fd = open("myfile.txt", "rb")
d.upload_fd(fd, "/data/local/tmp/上传到设备上的文件.txt")

# 删除设备上的文件
d.delete_file("/data/local/tmp/文件.txt")

# 修改设备上的文件权限
d.file_chmod("/data/local/tmp/文件.txt", mode=0o777)

# 获取设备上文件的信息
d.file_stat("/data/local/tmp/文件.txt")
```

## 关机重启

```python
# 关闭系统（等于关机）
d.shutdown()
# 重启系统（等于重启）
d.reboot()

# 关闭设备上运行的 LAMDA 服务
d.exit()
```


## 应用操作

> 列出系统上已安装的所有应用的ID

```python
d.enumerate_all_pkg_names()
```

> 列出设备上所有正在运行的应用

```python
d.enumerate_running_processes()
```

> 获取当前处于前台的应用

```python
d.current_application()

# 等价于
d.application(d.current_application().applicationId)

# 获取当前前台的 activity
d.current_application().activity
```

> 启动 Activity
```python
# 导入 FLAG_ACTIVITY* 常量定义
from lamda.const import *
# 由于JSON标准，附加数据暂时只支持 boolean, int 以及 string 类型
d.start_activity(action="some", category="some", component="some",
                 extras={"boolean": False, "int": 1, "string": "me"},
                 flags=FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TASK,
                 debug=False)

# flags 的定义请参考文档
# https://developer.android.com/reference/android/content/Intent#FLAG_ACTIVITY_BROUGHT_TO_FRONT

# debug 参数代表：是否以调试模式启动该活动
# 如果你知道 Waitting for debugger，那么它可能对你有用
# 你可以像下面这样以调试模式启动一个应用（你的设备或者APP需要是可调试的）
la = d.application("com.android.settings").query_launch_activity()
d.start_activity(component=la.component, action=la.action,
                 categories=la.categories, debug=True)
# flags 以及 debug 参数不是必须的，只是多了一种可能

# 例如：启动 设置 APP（当然这几乎等价于直接启动app）
d.start_activity(action="android.intent.action.MAIN",
                 category="android.intent.category.LAUNCHER",
                 component="com.android.settings/.Settings")

# 例如：进入证书设置
d.start_activity(action="com.android.settings.TRUSTED_CREDENTIALS")
```

> 授予/撤销 APP 权限

注意，你应在APP未启动时进行权限设置，在APP请求权限时调用并不会产生帮你点击允许的效果。

```python
app = d.application("com.my.app")

#导入 PERMISSION_READ_PHONE_STATE 常量（版本>3.90）
from lamda.const import *

# 获取应用所有权限
app.permissions()
# 授予 READ_PHONE_STATE 权限
app.grant(PERMISSION_READ_PHONE_STATE, mode=GrantType.GRANT_ALLOW)
# 拒绝 READ_PHONE_STATE 权限
app.grant(PERMISSION_READ_PHONE_STATE, mode=GrantType.GRANT_DENY)
# 检查是否已授予权限
app.is_permission_granted(PERMISSION_READ_PHONE_STATE)
# 撤销已授予的权限
app.revoke(PERMISSION_READ_PHONE_STATE)
```

> 清除应用缓存，重置应用

```python
# 删除应用的缓存数据
app = d.application("com.my.app")
app.delete_cache()
# 重置应用数据
app.reset_data()
```

> 启动/停止应用

```python
app = d.application("com.my.app")

# 启动应用
app.start()
# 检查应用是否正在前台运行
app.is_foreground()
# 关闭应用
app.stop()
```

> 其他

```python
app = d.application("com.my.app")
# 获取应用信息
app.info()

# 检查应用是否已安装
app.is_installed()
# 卸载应用
app.uninstall()

# 查询该应用的启动 Activity（入口活动）
app.query_launch_activity()

# 启用应用
app.enable()
# 禁用应用
app.disable()
```

## WIFI操作

目前WIFI操作部分功能由于可能导致设备异常未实现，仅介绍部分实现的功能

```python
wifi = d.stub("Wifi")

# 获取wifi bssid,ssid ip 等相关信息
wifi.status()

# 获取黑名单中的所有 bssid
wifi.blacklist_get_all()

# 将bssid加入黑名单(将不会显示在wifi列表)
wifi.blacklist_add("3c:06:aa:8a:55:66")

# 清空所有黑名单
wifi.blacklist_clear()

# 执行 wifi 扫描
wifi.scan()

# 获取周边 wifi 扫描结果
wifi.scan_results()

# 获取当前wifi的mac地址
wifi.get_mac_addr()

# 获取 wifi 信号强度，链接速率
wifi.signal_poll()
```

## 基本UI操作

> 获取设备信息

```python
d.device_info()
```

> 息屏/亮屏相关

```python
# 息屏
d.sleep()
# 亮屏
d.wake_up()
# 屏幕是否点亮
d.is_screen_on()
# 屏幕是否已锁定
d.is_screen_locked()
```

> 剪切板

```python
d.set_clipboard("剪切板内容")

# 获取剪切板内容（不支持安卓10+）
d.get_clipboard()
```

> 物理按键

```python
# 此方法可使用如下17种按键
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

# 同时为了可以使用更多按键，也可以使用这个方法
d.press_keycode(KeyCodes.KEYCODE_CALL)
# 可使用的 KEYCODE 可以自行查看此文档
# https://developer.android.com/reference/android/view/KeyEvent#KEYCODE_0
```

> 屏幕截图

```python
quality = 60 # 截图质量，默认为全画质
d.screenshot(quality).save("screenshot.png")
# 截取屏幕上特定区域的图像
# Bound 的参数 top,left 等定义：

# top:     从距离屏幕顶部向下数 top 个像素
# bottom:  从距离屏幕顶部向下数 bottom 个像素
# left:    从距离屏幕左侧向右数 left 个像素
# right:   到距离屏幕左侧向右数 right 个像素

# 正常情况下 top 永远小于 bottom，left 永远小于 right
bound = Bound(top=50, bottom=80, left=50, right=80)
d.screenshot(quality, bound=bound).save("partial.png")
```

> 点击屏幕上的一个点

```python
d.click(Point(x=100, y=100))
```

> 点按点A并将其拖动到点B

```python
A = Point(x=100, y=100)
B = Point(x=500, y=500)

d.drag(A, B)
```

> 从点A滑动到点B

```python
A = Point(x=100, y=100)
B = Point(x=500, y=500)

d.swipe(A, B)
```

> 稍复杂的多点滑动（九宫格解锁）

```python
p1 = Point(x=100, y=100)
p2 = Point(x=500, y=500)
p3 = Point(x=200, y=200)

# 从点P1滑动到点P2随后滑动到点P3，可任意个点
d.swipe_points(p1, p2, p3)
```

> 打开通知栏/快捷设置栏

```python
d.open_notification()
d.open_quick_settings()
```

> 获取页面布局描述XML

```python
d.dump_window_hierarchy().getvalue()
```

> 等待界面布局停止刷新

```python
# 单位是毫秒，5*1000 代表5秒
d.wait_for_idle(5*1000)
```

## 进阶UI操作

> Selector

界面布局检视，首先你需要打开设备的 web 远程桌面。随后，鼠标点击左侧屏幕确保焦点落在投屏上（否则焦点可能会被右侧的终端捕获），
然后按下快捷键 `CTRL+I`(启动布局检视)，此时你将不能再滑动左侧屏幕，你可以点击屏幕上的虚线框来查看对应元素的信息，你可以将其中的部分属性作为 Selector 的参数。
再次按下 `CTRL+I` 将关闭布局检视，布局检视并不会随着页面的改变而刷新，它始终是你按下快捷键那一刻的屏幕布局，如果需要刷新布局请手动按下快捷键 `CTRL+R`。

正常情况下，我们只会使用 `resourceId`, `clickable`, `text`, `description` 作为参数。
如果元素存在正常的 resourceId，优先使用其作为 Selector，即：`Selector(resourceId="com.android.systemui:id/mobile_signal_single")`。
对于无 resourceId，则会使用其 text，即：`Selector(text="点击进入")`，或者更模糊一点 `Selector(textContains="点击")`
description 与 text 同理，但是 description 用的会比较少。

当然，Selector 不止可以使用一个参数，你可以做其他组合，例如 `Selector(text="点击进入", clickable=True)`

> 注意：很少直接用 Selector()，大部分情况下，使用 d() 来进行。

所有常见的匹配参数：

```
text                    文本完全匹配
textContains            文本包含匹配
textStartsWith          文本起始匹配
className               类名匹配
description             描述完全匹配
descriptionContains     描述包含匹配
descriptionStartsWith   描述起始匹配
clickable               可以点击
longClickable           可以长按
scrollable              可滚动
resourceId              资源ID匹配
```

大部分情况下，你不会直接用到 `Selector`，但是间接使用无处不在。

> 元素操作

上文都是介绍了如何坐标点击这种随意性的东西，现在开始介绍如何操作固定目标元素。首先，你需要知道如何选定元素。

```python
# 选择界面上的包含文字 被测APP 的元素
element = d(textContains="被测APP")
# 当然，你不一定要这样赋值到 element，也可直接使用 d(textContains="被测APP")
```

好了，现在你知道了如何获取元素了，当然，这时并没有获取到，只是代表，你想要在当前界面操作这个元素，下面开始操作。


```python
# 我们现在假设，界面上这个 被测APP 是手机上被测APP的图标名称（图标下面的名称）。
element = d(textContains="被测APP")
# 是否存在该元素
element.exists()
# 点击该元素，不存在则会抛出异常
# Corner.COR_CENTER 代表点击该元素中心点，你可查看 COR_CENTER 定义获取其他可点击的位置
element.click(corner=Corner.COR_CENTER)

# 点击该元素，不存在不会抛出异常
element.click_exists(corner=Corner.COR_CENTER)

# 长按该元素，不存在则会抛出异常
element.long_click(corner=Corner.COR_CENTER)

# 获取元素信息
element.info()

# 获取元素的中心点坐标
element.info().bounds.center()

# 获取元素的左上点坐标
element.info().bounds.corner("top-left")

# 获取元素的高度
element.info().bounds.height

# 获取元素的宽度
element.info().bounds.width

# 获取元素个数
element.count()

# 等待元素出现，最多等待10秒
element.wait_for_exists(10*1000)

# 等待元素消失，最多等待10秒
element.wait_until_gone(10*1000)

# 获取该元素的截图（不是全屏，只是该元素）
# quality 为截图质量 1-100
element.screenshot(quality=60)

# 将此 APP 拖动归类到 购物 文件夹（依据实际情况修改）
element.drag_to(Selector(text="购物"))

#########
# 查找同级或者子级元素
#########
# 有时候会有一些重复元素或者无明显特征的元素，很难去定位
# 这时你可以通过查找子级/同级元素的方法来缩小查找范围
# 子级元素，举例为：一个聊天登录框，里面的输入框即为登录框的子级元素
# 同级元素，举例为：聊天输入框里面的用户名和密码框为同级原始（正常情况下）
form = d(resourceId="login_form")
form.child(index=1)
# 这将获取到 login_form 下 index 为 0 的元素
form.child(index=1).sibling()
# 你也这样来找与 login_form 同级的找回密码按钮
#（其实已经可以通过字符串判断了，就不需要这样做了，这里只是演示）
form.sibling(textContains="找回密码")
# 它们本身就是一个element，你可以对其做任何 element 的操作


############################
# 现在 element 改变了其意义，变为选择了输入框
############################

# 示例为：在一加搜索应用界面的搜索框输入 被测APP

# 注意，不要直接往看似输入框的地方输入文字，可能并无法输入
# 有些输入框需要点击一次才会进入真正的输入框，请使用此真正输入框的资源ID
element = d(resourceId="net.oneplus.launcher:id/search_all_apps")
element.set_text("被测APP")

# 获取输入的内容
element.get_text()

# 清空刚刚输入的内容
element.clear_text_field()

# 配合点击搜索，来完成一次类人的搜索操作。


# 滑动操作（列表上下滑动翻页）
# 注意，这些操作并不保证精度，下面这些方法正常情况下都并不需要选择器，
# 但是你可根据实际情况自行加入选择器

# 向上滑动， step 自行调整，越多会越慢，比较适合精度要求较高的滑动
d().swipe(direction=Direction.DIR_UP, step=32)
# 其他滑动方向：
#DIR_UP     向上滑动
#DIR_LEFT   向左滑动
#DIR_DOWN   向下滑动
#DIR_RIGHT  向右滑动

#########
# fling：甩动，即正常人滑动屏幕的行为，较快
#########
# 从上向下
d().fling_from_top_to_bottom()
# 从下往上
d().fling_from_bottom_to_top()
# 从左往右
d().fling_from_left_to_right()
# 从右往左
d().fling_from_right_to_left()

# 其他，一直向下/左右上滑，直到滑动到底
# 因为并不是一定可以滑动到底或者检测到滑动到底
# 所以 max_swipes 参数是必须的
d().fling_from_top_to_bottom_to_end(max_swipes=32)
d().fling_from_bottom_to_top_to_end(max_swipes=32)
d().fling_from_left_to_right_to_end(max_swipes=32)
d().fling_from_right_to_left_to_end(max_swipes=32)

#########
# scroll: 比较机械性的滑动
#########
step = 60
max_swipes = 32
# 从上往下滑动 step 步
d().scroll_from_top_to_bottom(step)
# 从下往上滑动 step 步
d().scroll_from_bottom_to_top(step)
# 从左往右滑动 step 步
d().scroll_from_left_to_right(step)
# 从右往左滑动 step 步
d().scroll_from_right_to_left(step)

# 其他，一直向下/左右上滑，直到滑动到底
# 同上文 fling 描述
d().scroll_from_top_to_bottom_to_end(max_swipes, step)
d().scroll_from_bottom_to_top_to_end(max_swipes, step)
d().scroll_from_left_to_right_to_end(max_swipes, step)
d().scroll_from_right_to_left_to_end(max_swipes, step)
```

> 监视器

监视器用来监听界面变化并在满足条件时执行设定的操作（点击元素或者按键），这可能对性能或者需要人工介入时产生影响，所以请谨慎使用，默认未开启。

```python
# 启动监视器循环
d.set_watcher_loop_enabled(True)

# 获取监视器是否已启动
d.get_watcher_loop_enabled()

# 移除系统中应用的所有 watcher，建议每次使用前都执行防止前面任务注册的未删除影响正常处理流程
d.remove_all_watchers()

# 获取系统中所有已应用的 watcher 名称列表
d.get_applied_watchers()

# 彻底移除一个 watcher
d.remove_watcher(name)

# 应用watcher到系统中（当 watcher_loop 启动，此watcher将会生效）
d.set_watcher_enabled(name, True)
# 取消应用
d.set_watcher_enabled(name, False)

# 获取此 watcher 是否应用
d.get_watcher_enabled(name)
```

> 监视系统界面出现某个元素的次数

```python
# 做一些测试前的清理，当然，并不是每 register 一个就需要这样
# 只是为了确保测试过程不被干扰
d.remove_all_watchers()
d.set_watcher_loop_enabled(True)

# 应用监视界面出现 好的 的次数
# 第二个参数为数组，可以给多个 Selector 表示条件都满足才会记录
# 但是不建议超过三个
d.register_none_op_watcher("RecordElementAppearTimes", [Selector(textContains="好的")])
d.set_watcher_enabled("RecordElementAppearTimes", True)

# ... 做满足条件的操作

# 获取记录的次数
d.get_watcher_triggered_count("RecordElementAppearTimes")

# 重置记录的次数
d.reset_watcher_triggered_count("RecordElementAppearTimes")

# 移除
d.remove_watcher("RecordElementAppearTimes")
```


> 当界面出现匹配元素时点击某个元素

```python
# 做一些测试前的清理，当然，并不是每 register 一个就需要这样
# 只是为了确保测试过程不被干扰
d.remove_all_watchers()
d.set_watcher_loop_enabled(True)

# 示例为，当APP启动后出现用户协议时，自动点击同意
# 第二个参数为数组，可以给多个 Selector 表示条件都满足才会点击
# 但是不建议超过三个
d.register_click_target_selector_watcher("ClickAcceptWhenShowAggrement", [Selector(textContains="用户协议")],
                                         Selector(textContains="同意", clickable=True))
d.set_watcher_enabled("ClickAcceptWhenShowAggrement", True)

# ... 做满足条件的操作

# 移除
d.remove_watcher("ClickAcceptWhenShowAggrement")
```


> 当界面出现匹配元素时点击物理按键

```python
# 做一些测试前的清理，当然，并不是每 register 一个就需要这样
# 只是为了确保测试过程不被干扰
d.remove_all_watchers()
d.set_watcher_loop_enabled(True)

# 示例为，当界面存在 个人中心 时，按下HOME键回到启动屏幕
# 第二个参数为数组，可以给多个 Selector 表示条件都满足才会点击
# 但是不建议超过三个
d.register_press_key_watcher("PressBackWhenHomePageShows", [Selector(textContains="个人中心")], Keys.KEY_HOME)
d.set_watcher_enabled("PressBackWhenHomePageShows", True)

# ... 做满足条件的操作

# 移除
d.remove_watcher("PressBackWhenHomePageShows")
```

## 接口锁

这里的基本功能让你可以锁定接口只能为当前 Device 实例使用。

```python
# 获得锁，此锁将在60秒后被自动释放，其他客户端将可以获得锁，你可以更改此时间
# 但是，如果改得太高因为异常脚本退出，你将近乎永远无法连接设备，你可能需要进行重启
# 此获得锁接口可重入，重入时等价于 _refresh_lock，建议只调用一次
d._acquire_lock(leaseTime=60)
# 刷新锁，每次调用后将锁过期时间设为此 leaseTime
# 做定期调用来保持设备锁定
d._refresh_lock(leaseTime=60)
# 释放锁，其他客户端将可以获得锁
d._release_lock()
```

## 使用内置终端

这里的内部终端，指的是你通过 web 远程桌面或者 ssh/内置adb 连接的终端，里面内置了一些命令以及Python模块，你可以
直接在里面执行一些操作或者运行一些 Python 代码，甚至可以直接在终端内完成自控，由于兼容性考虑，adb 连接的终端不存在部分命令提示等功能。

> 现在假设你已经打开了 web 远程桌面，你应该已经在页面上看到了一个 linux 终端。
执行命令 `cd` 可以切换到家目录（默认为 `/data/usr`），这是你的工作区，你可以在此存储文件。终端支持命令补全但不支持参数补全，你也可以在终端输入部分命令，随后通过上下键自动填补历史命令。同时，内部提供了一些命令别名，这些命令别名及功能如下。
```
l                  = 命令 ls
ll                 = 命令 ls -l
la                 = 命令 ls -la
py                 = 命令 python
..                 = 切换到父目录
...                = 切换到父目录的父目录
p                  = 切换到上一个目录
t                  = 切换到 /data/local/tmp
```

> 其他一些实用命令。

```
* python           (Python)
* strace           (syscall trace)
* ltrace           (libcall trace)
* curl             (cURL)
* fsmon            (文件访问监控)
* iperf3           (网络性能测试)
* nano             (文件编辑器)
* vi               (文件编辑器)
* ncdu             (查找磁盘文件占用)
* socat            (网络工具)
* sqlite3          (读取 SQLite 数据库，支持 cipher)
* tcpdump          (流量分析)
* busybox          (命令集合)
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
* 等基础 linux 命令
```

> Python 也内置了一些三方库，注意无法通过 PIP 安装额外的库。

```
* lamda            (自身)
* capstone         (反汇编引擎)
* keystone_engine  (汇编引擎)
* unicorn          (CPU模拟引擎)
* lief             (二进制程序解析)
* lxml             (xml/html解析)
* redis            (redis客户端)
* tornado          (web框架)
* pyOpenSSL        (OpenSSL)
* requests         (requests)
* scapy            (流量分析)
* frida            (frida)
* pyaxmlparser     (APK解析)
* xmltodict        (xml转dict)
* msgpack_python   (msgpack)
```

这里不会介绍如何使用这些命令或库。


# 工具及教程

其中的每个文件夹下都有一份使用说明。

## 一键中间人

打开 [tools/README.md](tools/README.md) 查看。

## 国际代理进行中间人

打开 [tools/README.md](tools/README.md) 查看。

## 安装 ADB 公钥

打开 [tools/README.md](tools/README.md) 查看。

## OpenVPN 服务

打开 [tools/README.md](tools/README.md) 查看。

## SOCKS5 服务

打开 [tools/README.md](tools/README.md) 查看。

## 端口转发服务

打开 [tools/README.md](tools/README.md) 查看。

## 注入 Frida RPC 脚本

打开 [tools/README.md](tools/README.md) 查看。

## 生成加密连接证书

打开 [tools/README.md](tools/README.md) 查看。

## 列出内网设备

打开 [tools/README.md](tools/README.md) 查看。


如果仍有疑问，请加入社区讨论：[lamda-dev/community](https://gitter.im/lamda-dev/community)