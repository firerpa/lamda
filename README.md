<p align="center">
<img src="image/logo.svg" alt="LAMDA" width="365">
</p>

<p align="center">Android reverse engineering & automation framework, the super power.</p>

<p align="center">
<img src="https://img.shields.io/badge/python-3.6+-blue.svg?logo=python&labelColor=yellow" />
<img src="https://img.shields.io/badge/android-6.0+-blue.svg?logo=android&labelColor=white" />
<img src="https://img.shields.io/badge/root%20require-red.svg?logo=android&labelColor=black" />
<img src="https://img.shields.io/github/v/release/rev1si0n/lamda" />
</p>

<p align="center"><a href="https://github.com/rev1si0n/lamda/wiki">使用文档</a> | <a href="https://t.me/lamda_dev">TELEGRAM</a> | <a href="https://lamda.run/join/qq">QQ 群组</a></p>
<br>

LAMDA 是一个用于逆向及自动化的辅助框架，设计为减少安全分析以及应用测试人员的时间及琐碎问题，以编程化的接口替代大量手动操作，它并不是一个单一功能的框架，他是 Appium、uiautomator 的超集同时具备逆向领域的能力。为了让你大概了解它的用处：你是否会在手机上安装各类代理、插件或者点来点去的设置来完成你的工作？你是否要在异地操作远在千里之外的手机？你是否有编程控制手机的需求？是否还在某些云手机厂商那里购买昂贵的**IP切换**、**远程ADB调试**、**RPA自动化**甚至连 **logcat 日志**都要付费的服务？如果有，那么对了，只需一个 LAMDA 即可解决这些问题。并且，LAMDA 更注重**分布式**，事实上，你可以在一台公网服务器上管理散布在世界各地各种网络环境中的设备。当然，LAMDA 可以做到的不止于此。

经过超 500 台设备的稳定生产环境考验，具有近乎商业级软件的质量和稳定性，仅需 root 权限即可正常运行。具备 ARM/X86 全架构，安卓 6.0-14 的广泛兼容性，支持模拟器、真机、云手机、 WSA（Windows Subsystem for Android™️）、无头开发板以及 Redroid。提供大量可编程接口，支持界面布局检视、获取/重放系统中最近的 Activity、唤起应用的 Activity 等功能。除此之外，它支持大文件上传下载，远程桌面，以及UI自动化编程接口，点击、截图、获取界面元素、执行 shell 命令、设备状态、资源读取、系统配置、属性读写、一键中间人等，可通过 SSH 或内置 ADB 登录设备终端。具备 socks5、OpenVPN 代理并可通过接口轻松设置根证书，实现中间人攻击，以及 Frida、IDA 等工具等等，同时支持定时任务、Magisk开机自启动，你可以在任何地方通过网络连接运行着 LAMDA 设备。

![动图演示](image/demo.gif)

## 一键中间人流量分析

支持常规以及国际APP流量分析，DNS流量分析，得益于 [mitmproxy flow hook](https://docs.mitmproxy.org/stable/api/events.html)，你可以对任何请求做到最大限度的掌控，mitmproxy 功能足够丰富，你可以使用 Python 脚本实时修改或者捕获应用的请求，也可以通过其 `Export` 选项导出特定请求的 `curl` 命令或者 `HTTPie` 命令，分析重放、拦截修改、功能组合足以替代你用过的任何此类商业/非商业软件。如果你仍不清楚 mitmproxy 是什么以及其具有的能力，请务必先查找相关文档，因为 LAMDA 将会使用 mitmproxy 为你展现应用请求。

![中间人流量分析动图演示](image/mitm.gif)

当然，LAMDA 的能力不止于如上种种，他是你强有力的控制及管理工具，如果您感兴趣，请转到 [使用文档](https://github.com/rev1si0n/lamda/wiki)。