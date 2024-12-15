<p align="center">
<img src="image/logo.svg" alt="LAMDA" width="345">
</p>

<p align="center">安卓 RPA 机器人框架，下一代移动端数据自动化机器人</p>

<p align="center">
<img src="https://img.shields.io/badge/python-3.6+-blue.svg?logo=python&labelColor=yellow" />
<img src="https://img.shields.io/badge/android-6.0+-blue.svg?logo=android&labelColor=white" />
<img src="https://img.shields.io/badge/root%20require-red.svg?logo=android&labelColor=black" />
<img src="https://img.shields.io/github/downloads/rev1si0n/lamda/total" />
<img src="https://img.shields.io/github/v/release/rev1si0n/lamda" />
</p>

<p align="center"><a href="https://device-farm.com/doc/index.html">使用文档</a> | <a href="https://t.me/lamda_dev">TELEGRAM</a> | <a href="https://lamda.run/join/qq">QQ 群组</a> | <a href="https://github.com/rev1si0n/lamda/blob/HEAD/CHANGELOG.txt">更新历史</a></p>

智能机的崛起，传统网页端的普及度也开始显著减弱，数据与应用正加速向移动端转移。越来越多的人选择通过智能手机和平板等移动设备来获取信息和服务。随着移动设备的普及，用户享受到更便捷、更即时的访问体验，传统的网页内容消费模式面临重新审视。与此同时，数据采集的技术也亟需适应这一趋势。过去，许多数据采集工具专注于网页内容，但在移动端环境中，尤其是在移动端封闭的黑盒中，现今的常规采集技术也面临着新的挑战。LAMDA 的诞生，为这一切创造了可能。

LAMDA 是一个**安卓领域的集大成者**，设计为减少**安全分析**及**应用测试**工作的时间和琐碎问题，为**移动端RPA数据采集**提供稳定的解决方案，以**编程化**的**接口**替代大量手动操作，**易部署**，没有那些复杂花哨不跨平台的安装流程，你所需要的能力他大概率能做到并且做的更好。他并不是一个单一功能的框架，他是集 Appium、uiautomator **自动化**的超集同时具备**逆向**领域如 **Hook** **抓包** **证书安装** **组网** **API跟踪** **手机自控** 等等各种能力的框架。为了让你大概了解它的用处：你是否会在手机上安装各类代理、插件或者点来点去的设置来完成你的工作？你是否要在异地操作远在千里之外的手机？你是否有编程控制手机的需求？是否还在某些云手机厂商那里购买昂贵的 **IP切换**、**远程ADB调试**、**RPA自动化**甚至连 **logcat 日志** 都要付费的服务？如果有，那么对了，只需一个 LAMDA 即可解决所有问题。并且，他更注重**分布式**，事实上，你可以在一台公网服务器上管理散布在世界各地各种网络环境中的设备。当然，LAMDA 可以做到的远不止于此，你可以阅读使用文档尽情探索他的所有能力。

<p align="center"><b>长期维护及更新，质量稳定，安全可靠，生产环境可用<br>现稳定应用于多个外部大型系统，包括自动化取证，云平台，数据采集，涉诈应用分析系统等<br>本框架已稳定运行于各种数据生产环境五年以上</b></p>

<p align="center">
<img src="image/wx.png" alt="公众号" width="234">
</p>
<p align="center"><small>关注公众号查看视频教程以及更多使用方法</small><br><small><a href="https://space.bilibili.com/1964784386/video">B站教程视频同步发布</a></small>
</p>

经过超 500 台设备的稳定生产环境考验，具有**商业级软件**的**质量**和**稳定性**，仅需 root 权限即可正常运行。具备 ARM/X86 全架构，安卓 6.0-14 的广泛兼容性，支持 **模拟器**、**真机**、**云手机**、 **WSA**（Windows Subsystem for Android™️）、**无头开发板** （RK3399、3588 及任何 ARM 架构开发板）以及 **Redroid** 等大多数运行安卓系统的设备。提供大量可编程接口，支持界面布局检视、获取/重放系统中最近的 Activity、唤起应用的 Activity 等功能。除此之外，它支持大文件上传下载，远程桌面，以及UI自动化编程接口，点击、截图、获取界面元素、执行 shell 命令、设备状态、资源读取、系统配置、属性读写、一键中间人等，可通过 SSH 或内置 ADB 登录设备终端。具备 socks5、OpenVPN 代理并可通过接口轻松设置系统证书及中间人，同时支持定时任务、Magisk开机自启动，你可以在任何地方通过网络连接运行着 LAMDA 设备。


<h3><p align="center">丰富的设备编程接口</p></h3>

<p align="center">LAMDA 提供多达 160 条编程 API 接口，让你可以对安卓设备进行无微不至的管理和操作，提供了包括命令执行，系统设置，系统状态，应用相关，自动化相关，代理以及文件等十几个大类的接口。同时提供了封装完整的 Python 库让你可以快速上手使用。</p>

<h3><p align="center">简洁易用的远程桌面</p></h3>

<p align="center">
<img src="image/demo.gif" alt="动图演示" width="95%">
</p>

<h3><p align="center">一键中间人流量分析及更多其他功能</p></h3>

支持常规以及国际APP流量分析，DNS流量分析，得益于 [mitmproxy flow hook](https://docs.mitmproxy.org/stable/api/events.html)，你可以对任何请求做到最大限度的掌控，mitmproxy 功能足够丰富，你可以使用 Python 脚本实时修改或者捕获应用的请求，也可以通过其 `Export` 选项导出特定请求的 `curl` 命令或者 `HTTPie` 命令，分析重放、拦截修改、功能组合足以替代你用过的任何此类商业/非商业软件。如果你仍不清楚 mitmproxy 是什么以及其具有的能力，请务必先查找相关文档，因为 LAMDA 将会使用 mitmproxy 为你展现应用请求。

<p align="center">
<img src="image/mitm.gif" alt="动图演示" width="95%">
</p>

<p align="center">
当然，LAMDA 提供的能力不止于这些，由于篇幅较长将不在此罗列，他是你强有力的设备控制及管理工具，如果你感兴趣，请转到 使用文档。
</p>