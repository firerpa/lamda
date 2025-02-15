<p align="center">
<img src="image/logo.svg" alt="FIRERPA" width="345">
</p>

<p align="center">安卓 RPA 机器人框架，下一代移动端数据自动化机器人</p>

<p align="center">
<img src="https://img.shields.io/badge/python-3.6+-blue.svg?logo=python&labelColor=yellow" />
<img src="https://img.shields.io/badge/android-6.0--15-blue.svg?logo=android&labelColor=white" />
<img src="https://img.shields.io/badge/root%20require-red.svg?logo=android&labelColor=black" />
<img src="https://img.shields.io/github/downloads/rev1si0n/lamda/total" />
<img src="https://img.shields.io/github/v/release/rev1si0n/lamda" />
</p>

<p align="center"><a href="https://device-farm.com/doc/index.html">使用文档</a> | <a href="https://t.me/lamda_dev">TELEGRAM</a> | <a href="https://qm.qq.com/q/zDaX2a594I">QQ 群组</a> | <a href="https://device-farm.com/doc/版本历史.html">更新历史</a></p>

智能机崛起，传统网页端的普及度也开始显著减弱，数据与应用正加速向移动端转移。越来越多的人选择通过智能手机和平板等移动设备来获取信息和服务。随着移动设备的普及，用户享受到更便捷访问体验，传统的网页内容模式面临重新审视。与此同时，数据采集的技术也亟需适应这一趋势。过去，许多数据采集工具专注于网页内容，在移动端环境中，尤其是在移动端封闭的黑盒中，现今的常规技术也面临着新的挑战，FIRERPA 创造了可能，将这一切变得更加简单快捷。

FIRERPA 是**安卓领域的集大成者**，设计为减少**安全分析**及**应用测试**或**自动化**工作的时间和琐碎问题，经过超 500 台设备集群的生产环境考验，稳定应用于多个大型系统，包括自动化取证，云平台，数据采集，合规分析等，完全商业级软件的质量和稳定性，仅需 root 权限即可正常运行。具备 **ARM/X86** 全架构，安卓 **6.0-15** 的广泛兼容性（[16 KB page size](https://developer.android.com/guide/practices/page-sizes) 的安卓 15 适配中），支持 **模拟器**、**真机**、**云手机**、 **WSA**（Windows Subsystem for Android™️）、**RK开发板** （所有 ARM 架构）以及 **Redroid** 等大多数运行安卓系统的设备。为**移动端 RPA 和数据自动化**提供稳定的解决方案，以**编程化**的**接口**替代大量手动操作，**易部署**，没有那些复杂花哨不跨平台的安装流程，你所需要的能力他大概率能做到并且做的更好。他并不是一个单一功能的框架，他是集 Appium、uiautomator **自动化**的超集同时具备**逆向**领域如 **Hook** **抓包** **证书安装** **组网** **API跟踪** **手机自控** 等等各种能力的框架。当然，FIRERPA 可以做到的远不止于此，你可以阅读使用文档尽情探索他的所有能力。


<h3><p align="center">适用广泛的服务架构设计</p></h3>

<p align="center">FIRERPA 不同于任何其他同类或者子集软件，在设计之初即考虑到了各种可能的应用环境，可在非侵入的情况下运行在当下绝大部分的安卓设备内，即插即用，没有任何外部依赖，无需任何多余设置，原生即是为大型的业务场景设计，易于系统化的管理及更新。而此时，其他具备相似功能的软件还在经历掉线、不稳定、兼容性差、无人维护、管理难度大等各种问题。</p>

<h3><p align="center">丰富编程接口为业务赋能</p></h3>

<p align="center">提供多达 160 条编程 API 接口，让你可以对安卓设备进行无微不至的管理和操作，提供了包括命令执行，系统设置，系统状态，应用相关，自动化控制，代理以及文件等十几个大类的接口。同时提供了封装完整的 Python 库让你可以快速上手使用。规范及稳定的服务和接口让你可以无忧的通过代码控制每一个细节，甚至可以让其和 AI 进行互联，让大模型自动编写以及执行任务。</p>

<h3><p align="center">简洁易用的远程桌面</p></h3>

<p align="center">
<img src="image/demo.gif" alt="动图演示" width="95%">
</p>

<h3><p align="center">一键中间人流量分析及更多其他功能</p></h3>

支持常规以及国际APP流量分析，DNS流量分析，得益于 [mitmproxy flow hook](https://docs.mitmproxy.org/stable/api/events.html)，你可以对任何请求做到最大限度的掌控，mitmproxy 功能足够丰富，你可以使用 Python 脚本实时修改或者捕获应用的请求，也可以通过其 `Export` 选项导出特定请求的 `curl` 命令或者 `HTTPie` 命令，分析重放、拦截修改、功能组合足以替代你用过的任何此类商业/非商业软件。如果你仍不清楚 mitmproxy 是什么以及其具有的能力，请务必先查找相关文档，因为 FIRERPA 将会使用 mitmproxy 为你展现应用请求。

<p align="center">
<img src="image/mitm.gif" alt="动图演示" width="95%">
</p>

<p align="center">
当然，FIRERPA 提供的能力不止于这些，他是你强有力的设备控制及管理工具，感兴趣请转到 使用文档。
</p>