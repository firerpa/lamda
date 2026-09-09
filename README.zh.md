# **FIRERPA Android** ｜ AI-Powered Automation

<img src="image/logo.svg" alt="FIRERPA" width="200" align="right" />

<p>
<img src="https://img.shields.io/badge/python-3.6+-blue.svg?logo=python&labelColor=yellow" />
<img src="https://img.shields.io/badge/android-6.0+-blue.svg?logo=android&labelColor=white" />
<img src="https://img.shields.io/badge/root/non--root--mode-green.svg?logo=android&labelColor=black" />
<img src="https://img.shields.io/badge/Built--in%20MCP-000.svg?logo=anthropic&labelColor=black" />
</p>

<h6>一个集下一代技术于一体的全能型 Android 自动化框架，融合了强大的端侧服务、AI 就绪型智能体以及可扩展的工具调用能力。</h6>

<p align="left"><a href="https://device-farm.com/docs/en/">Documentation</a> | <a href="https://device-farm.com/docs/zh/">使用文档</a> | <a href="https://device-farm.com/contact#telegram">TELEGRAM</a> | <a href="https://device-farm.com/contact#QQ">QQ 群</a> | <a href="https://github.com/firerpa/skills">SKILLS</a> | <a href="https://device-farm.com/llms-full.txt">llms-full.txt</a> | <a href="README.zh.md">中文版本</a></p>

FIRERPA 是面向 Android 的**一体化设备控制平台**。服务端直接在设备上运行，**无需额外运行时依赖**；**适配多代 Android 系统**，**无论是否 Root 均可使用**。PC 端通过 Python 客户端库统一调度，将 UI 自动化、远程运维、流量截获、Hook 逆向、网络代理、分布式组网、AI Agent / **MCP** 等能力收敛到同一套服务与 API 中。相比把 Appium、mitmproxy、frida-server、adb、uiautomator2 等自研脚本和各类运维工具拼凑使用，FIRERPA 的优势在于：**能力同源、配置统一、链路打通、适合多设备长期运行与工程化管理**。

## 远程桌面与实时投屏

FIRERPA 提供基于浏览器的远程桌面，无需在 PC 安装专用客户端即可实时查看和操作设备屏幕，支持局域网与跨网络访问。投屏链路同时支持 **MJPEG** 与 **H.264** 编码，并提供软编/硬编双后端，可按设备算力与网络状况调节帧率（最高 60fps）、分辨率缩放、码率与画质，在弱网环境下显著降低带宽占用、提升流畅度。进一步支持 **WebRTC** 传输，并可配置 STUN/TURN 服务器，改善 NAT 穿透与端到端延迟，适合公网、跨地域远程调试场景。

远程桌面支持**多用户同时接入**，便于协作排查、演示与培训。支持**双向剪贴板**共享与**实时音频**推送（Android 10+），并在同一 Web 界面集成终端、文件拖拽上传、目录浏览下载等运维能力，单端口即可完成日常操作。内置**可视化布局检视**：元素高亮、Tab 键遍历、坐标与 RGB 显示、XML 布局树导出，可在远程桌面内直接验证选择器与自动化逻辑，大幅缩短「看界面 → 写脚本」的闭环时间。

<p align="center">
<img src="https://raw.githubusercontent.com/wiki/firerpa/lamda/images/demo.gif" alt="demo" width="100%">
</p>

远程桌面与 RPC 接口支持 **TLS 全链路加密**与服务证书访问控制，可自定义 WebUI 登录密码，降低公网暴露风险。远程桌面能力还可通过 WebSocket 嵌入自有 Web 应用（实时视频、触控、终端、按键等），并可通过 `allow_origin` 配置跨域集成，适合将真机控制能力产品化。

## UI 自动化

FIRERPA 提供完整的选择器自动化体系，支持 text、resourceId、description、scrollable 等常见匹配方式，并支持 **child / sibling** 链式定位，应对重复元素、层级复杂或无显著特征的控件。元素级支持截图、等待出现/消失、角点/中心坐标获取、exists 判断等细粒度操作，支持 Unicode 输入、step 滑动、fling 快速翻页、滑动至底等交互。可与 Android 8.0+ 上**其他无障碍服务共存**，并增强 WebView 节点查找能力，提升混合应用自动化成功率。

**界面监视器（Watcher）** 可实时监听 UI 变化，在满足预设条件时自动执行点击、按键或计数，适用于自动跳过协议弹窗、更新提示、广告页等干扰流程；支持多 Selector 条件组合与事件独立启停，可统计一闪而过界面的出现次数。

**虚拟屏幕（Virtual Display）** 是 FIRERPA 的差异化能力之一：可在设备上创建独立的后台显示器，在虚拟屏中运行 App 与自动化脚本，**不影响主屏幕正常使用**——例如虚拟屏后台自动处理消息，主屏仍可刷视频、手动操作。虚拟屏 API 与主设备 API 高度一致，现有 `d.xxx` 脚本可平滑切换为 `vd.xxx`；Watcher 也可限定在虚拟屏内生效。WebUI 支持**多屏幕展示与切换**，可在远程桌面中选择操作或查看不同 Display，适合后台保活、并行任务与「前台人工 + 后台机器」混合场景。

针对无标准 View 树的场景（如游戏、自绘 UI），FIRERPA 提供 **OCR** 与**图像匹配**能力。OCR 支持 paddleocr、easyocr 及自定义 HTTP 后端，集群场景可将识别算力集中到服务端，避免每台 PC 重复加载模型；支持 GPU 加速与多种文本匹配模式。图像匹配在**设备端**执行模板匹配或 SIFT，不占 PC 资源；SIFT 对旋转、缩放、光照变化更鲁棒。此外提供**多指触控**能力，支持轨迹录制、重放、代码构造与二进制持久化，可表达复杂手势与压力值。

在架构定位上，FIRERPA 采用 C/S 模式，相较 AutoJS 等「设备自跑脚本」方案更利于**中心化调度、版本管理与集群管控**；相较 Appium 更轻量；相较 uiautomator2 在多设备场景下**稳定性更好**。文档将其定位为常见安卓自动化方案的**功能超集**——自动化与抓包、Hook、运维可在同一平台用代码串联，而不必在多套工具间切换。

## 抓包与 MITM

FIRERPA 提供**一键 MITM 抓包**能力：自动安装系统级根证书、配置代理、处理 Android 版本差异，并在退出时自动恢复设备网络状态，无需手工装证、切代理。支持全局抓包、按包名抓包、实时改包、共享 mitmweb 界面，并可通过上游 HTTP 代理实现**国际流量**经指定链路抓包。内置 **QUIC 降级**处理，降低 QUIC 对抓包的影响。即使 PC 与设备仅能通过单一 FIRERPA 端口通信（如 ADB connect、frp 转发），仍可实施抓包，适配苛刻网络拓扑。

除一键脚本外，MITM 相关能力均可 API 化：系统级根证书安装/卸载通吃 mitmproxy、Fiddler、Charles 等格式，抓包流程可嵌入自动化流水线，与 UI 操作、Frida Hook 在同一任务中完成。提供 Windows 免 Python 的 `startmitm.exe`，降低环境门槛。

## 网络、代理与组网

FIRERPA 在设备侧提供完整代理能力，支持 **HTTP / HTTPS / SOCKS5 / Shadowsocks**（多种加密算法），可按 App（含多开 user）粒度代理，支持 DNS 代理、UDP 代理、绕过局域网、与 OpenVPN 共存，并可在服务启动时**自动连接**预设代理。代理能力支持 **IPv6 与 UDP**，适配更复杂的网络环境。

**设备 HTTP 桥接代理（tunnel2）** 提供反向代理能力：将 PC 或浏览器的 HTTP 代理指向手机后，流量经手机网络出口转发，对外 IP 与手机一致，可选 Wi‑Fi 或 4G（rmnet）作为出站接口，适合联调、国际化业务、多设备 IP 池等场景。

内置 **OpenVPN 客户端**，支持证书、用户名密码及混合认证等多种登录模式，可与系统代理共存；配套提供 **OpenVPN Docker 镜像**与配置生成脚本，自动生成设备侧连接代码与自启动配置，降低手写 OpenVPN 配置出错概率。内置 **frp 客户端**，通过 `fwd.*` 配置即可将设备服务转发至公网服务器，支持加密与 TLS。

提供 **mDNS 服务发现**，启用后可通过 `{device_id}.local` 域名访问远程桌面等服务，并可附加 TXT 元数据（型号、ABI、设备 ID 等），便于局域网内批量发现与管理设备。

## Frida 与逆向

FIRERPA **内置最新版 Frida**，无需单独部署 frida-server；在远程桌面终端内可直接使用 frida 相关命令，无需 `-U`、`-H` 等繁琐参数。内置 Frida 集成开源隐藏补丁与自研隐藏能力，并持续迭代对抗检测；连接采用 Token 鉴权，经 FIRERPA 端口安全接入。提供 objection 补丁与 Frida 17.x java-bridge 封装工具，降低官方变更带来的迁移成本。

支持 **Frida 脚本持久化**：App 崩溃或退出后可自动重注入；支持 YAML 脱机持久化、目录监控与热更新。Frida RPC 可**映射为 Python 方法**，并支持 **HTTP + JSON-RPC 2.0** 远程调用，可在 JVM 线程、UI 主线程或纯 JS 上下文执行。脚本内 `emit` 数据可上报至 **HTTP / Redis / RabbitMQ(MQTT)**，附带设备与应用元数据，支持 zlib 压缩、HTTP 重试与 MQTT TLS。

## ADB、SSH 与内置终端

FIRERPA 提供**独立于系统 ADB 的内置 ADB 服务**，可在**不开启系统开发者模式**的情况下无线连接高权限 ADB，有利于规避「开发者选项」类检测；Magisk 模块可预置 `adb_keys` 实现默认授权。内置 **SSH 服务**与 `ssh.sh` / `scp.sh` 工具脚本，便于远程 Shell 与文件传输。

**内置终端**预装 strace、ltrace、tcpdump、scapy、fsmon、frida-tools、MemDumper 等常用分析工具，并集成 Crypto、cv2、unicorn、capstone、keystone、redis、grpc 等 Python 生态。sqlite3 支持 **wxsqlite / sqlcipher / sqlcrypto**，为读取微信、企微、阿里系等加密数据库提供路径。内置终端与远程桌面、SSH、ADB 统一，可在设备端直接完成分析与自控，减少 PC ↔ 设备来回切换。

## 分布式与多设备管理

FIRERPA **星连平台（Hub + hub-bridge）** 提供中心化多设备接入方案，支持本地与远程设备统一管理与 **P2P** 访问，适合「设备在家、人在外」及多机协作场景。hub v3 采用 **SAPI** 统一请求，可同时连接本地与远程设备。除 Hub 外，亦支持 **frp 转发**与 **OpenVPN 组网**两种自建方案，文档与 Docker 配套完整。

9.0 起支持 **P2P Bridge 端端互联**与**内置分布式任务系统**；7.50 起提供组网订阅服务，可无需自建 frp/OpenVPN。整体面向云手机池、真机农场、模拟器集群等**批量设备、长期在线、无人值守**场景设计。

## AI / MCP / Agent

FIRERPA **内置 MCP 服务端**（API 路径 `/mcp/`），采用 **streamable-http** 协议，支持 tool call、resource read、prompts、进度通知与日志，可对接 **Claude、Cursor** 等 MCP 客户端。提供官方 MCP 扩展模块，支持在 `~/modules/extension` 自定义插件。

内置 **`agent` 命令**，对接任意 OpenAI 兼容 API + tool call，以**自然语言**驱动设备操作，支持 **Vision 视觉模式**；提供 **OpenAI 语义化任务执行器**。可与 **crontab** 组合实现定时 AI 任务，将大模型能力嵌入真机自动化流水线。

<p align="center">
<img src="https://raw.githubusercontent.com/wiki/firerpa/lamda/images/mcp.gif" alt="MCP" width="100%">
</p>

## 系统级控制与扩展

FIRERPA 提供 **160+ Python API**，覆盖应用操作、文件 I/O、命令执行、设备状态、WiFi、代理、OpenVPN、关机重启、服务日志等。`setprop` 可写入 **`ro.*`** 只读系统属性；Settings API 可读写亮度、开发者模式等系统设置；**SELinux** 支持域创建、permissive 切换与细粒度 allow/disallow 规则。支持多开 App 全 API、静默授权/撤销权限、启动未导出 Activity、禁用 App 以节省资源。

提供**二进制补丁**能力（十六进制通配符、glob 路径、dryrun），以及磁盘、电池、CPU、内存、网络 IO 等**运行时指标**采集。支持播放 WAV 音频、内部存储 API。设备端集成 **tflite-runtime** 且支持调用硬件计算，支持端侧推理。

**虚拟 Debian 环境**可在设备内运行完整 Debian 与 apt，编译 BPF、部署 OpenSSH、运行任意 Python 依赖，突破内置终端不可 pip/apt 的限制。

## 部署、安全与治理

FIRERPA 支持 **APP 一键部署**（Root 或 Shizuku）、**Magisk 模块开机自启**、手动解压与 **ROM 内置**等多种落地方式，面向 **7×24** 常驻运行设计。APP 内可**自动生成服务证书**；Magisk zip 可预置 properties 配置、lamda.pem 证书与 adb_keys。全部行为由 **ini 格式服务配置**集中管理：端口、WebUI 参数、证书、OpenVPN、gproxy、frp、tunnel2、cron、sshd、adb、mdns 等；WebUI 支持可视化编辑、Raw 文本模式与 Reload Service 热重载，并支持从远程文件服务器加载配置。

支持 root 与 shell 双身份运行；覆盖 arm64、armeabi-v7a、x86、x86_64 等架构；兼容真机、雷电/夜神等模拟器、Redroid、WSA、AVD、云手机等环境。卸载路径规范，不在系统中散落垃圾文件。**API 独占锁**防止多客户端争抢同一设备。隐私政策明确不收集通讯录、短信、地理位置等个人隐私，并支持**离线授权**。

## 工具生态与长期演进

FIRERPA 持续演进 **6 年+**，覆盖 Android 14–16 兼容修复，在远程桌面多用户、标准化触摸 API、MCP 协议、Frida 版本与隐藏性、代理 IPv6/UDP、P2P Bridge、分布式任务等方面持续迭代。

FIRERPA 的核心优势不在于某一单项功能，而在于将**远程桌面（WebRTC/H.264/多用户）、UI 自动化（含虚拟屏/Watcher/OCR/图匹配/多指触控）、一键抓包、内置 Frida、全栈代理与 VPN/frp/P2P 组网、ADB/SSH/内置终端、AI MCP/Agent、系统级控制、虚拟 Debian、持久 KV、脚本加密**等能力集成在同一台 Android 设备、同一套服务与同一 Python 客户端中，使安全测试、合规分析、协议还原、批量管控与自动化业务可以在**一条流水线**里完成，而不是在多个工具之间反复拼接。