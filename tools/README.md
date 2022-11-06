这些工具正常情况下只能工作于 linux/mac 系统之上，为个人常用功能的封装，并未特意考虑兼容 Windows 但是这不代表 lamda 不支持。如果你使用的是 Windows，以`.sh`结尾的脚本应该无法正常工作。

> 使用之前，请确保已经启动设备上的 lamda 服务端。

## 前置条件

部分功能需要安装 adb，如果要用到，请确保已安装 adb 且不要太过老旧。

**需要注意**：所有使用到 adb 的脚本均 只支持一台手机通过 USB (adb) 连接电脑，请确保 `adb devices` 中只有一个设备。

```bash
# 如果没有安装，请 自行搜索 如何安装，这里提供的只是基础建议
# Windows
https://developer.android.com/studio/releases/platform-tools
# Mac
brew install android-platform-tools
#brew cask install android-platform-tools
# Debian/Ubuntu
apt install adb
```

克隆代码到本地

```bash
git clone https://github.com/rev1si0n/lamda.git
# 如果不会使用或未安装 git，下载此文件到本地并解压
# https://github.com/rev1si0n/lamda/archive/refs/heads/master.zip
```

进入 tools 目录并安装所需的依赖包
```bash
# 切换到 tools/ 目录并执行
pip3 install -r requirements.txt
```

如果你在服务端启用了通信加密(certificate)，你需要在使用前设置环境变量 `CERTIFICATE`
```bash
# 对于 linux / Mac
export CERTIFICATE=/path/to/lamda.pem
# 对于 Windows（路径不能包含空格）
set CERTIFICATE=C:\Users\path\to\lamda.pem
```

如果你修改了 lamda 的默认端口 65000，也需要在使用前设置环境变量

```bash
# 对于 linux / Mac
export LAMDAPORT=8123
# 对于 Windows（路径不能包含空格）
set LAMDAPORT=8123
```

192.168.1.2 为示例IP，请自行获取设备的实际IP地址。

## cert.sh

用来生成用于传输加密的证书
```bash
bash cert.sh
```

如果你需要生成特定 CN 的证书
```bash
bash cert.sh device1.example.com
```

即可，当前目录下的 lamda.pem 或者 device1.example.com.pem 即为所需的证书。
在服务端应用该证书后，客户端也必须使用此证书来进行远程调用以及 ssh 连接。
应用此证书后，将会加密任何通过 client 库进行的操作，ssh 将不再使用默认的秘钥。
同时，web 控制页面将需要登录（你可以在证书最后一行找到此登录密码），

如果操作系统不方便使用此工具，当前目录下已经为你准备好了一个默认的 SSL 证书

```bash
test.pem    # 用于加密客户端与服务端通信的证书
```

## cert.py

用来生成用于传输加密的证书，等效于 `cert.sh` 只不过这个脚本同时可以运行于 Windows，用法等同于 cert.sh。

> 注：你有可能需要手动安装 pyOpenSSL 依赖库 `pip install pyOpenSSL`

## startmitm.py

启动中间人，这将会全自动的在设备上开启全局的中间人，你就可以截获应用的 http/s 流量，当然，也可以包括 DNS 请求（全局）。

首先确保当前电脑与设备在同一个网段，192.168.1.2 为运行了 lamda 的手机设备。
其次，确保你已在命令行验证 mitmproxy 已安装成功（在命令行输入 `mitmdump` 进行验证）。

当然，电脑与设备不在同一网段或者是远程设备，你也可以轻松 mitm，请继续看下去。

> 注意：mitmweb 并不适合长时间多请求，其截获的请求均存储于内存之中。所以在长时间使用的情况下你的内存会被吃光。
> 对于长时间的中间人操作，请改用 mitmdump，请自行了解使用方法。

执行
```bash
python3 -u startmitm.py 192.168.1.2
```
即可。

如果需要截获特定应用的流量而不是全局
```bash
# 这里的 com.some.package 是应用的 ID
python3 -u startmitm.py 192.168.1.2:com.some.package
```
即可。

如果需要传递其他参数到 mitmproxy，例如 -s，则执行
```bash
# 这样你就可以通过编写 http_flow_hook.py 实时修改请求或者响应
python3 -u startmitm.py 192.168.1.2 -s http_flow_hook.py
```

关于如何编写 `http_flow_hook.py` 脚本，请参考 [docs.mitmproxy.org/stable/addons-examples](https://docs.mitmproxy.org/stable/addons-examples/)

> 任何 192.168.1.2 之后的参数将传递给 mitmproxy 本身

即使手机与当前电脑不在同一网段，你仍然可以使用在本机截获流量，但是**需要确保当前设备已通过USB接入**电脑且已ADB授权。
```bash
python3 -u startmitm.py localhost
```

如果手机不在身边，也和你的电脑不在同一网段，但是你可以访问 lamda 的端口，
**这种情况通常为**：你使用了内置 frp 服务转发了 lamda 到远程服务器，
或者你自行通过某种方式仅转发了 lamda 的 65000 端口到某个地方，这种情况下你和 lamda 之间
**仅有这一个端口**可以直接交流，其他端口是无法访问的。这种情况下，手机无法直接访问到本机的任何端口，需要通过以下方式来完成。（注意 OpenVPN 并不属于这个情况）

这时，需要通过稍微繁琐的组合方式来进行，下面介绍如何操作。

首先，使用 `adb_pubkey.py` 或者自行调用接口将自身的 adb 公钥安装到设备上（请在本文档搜索），
随后，确保当前电脑没有任何 USB ADB 设备连接（`adb devices` 显示无设备）。

现在执行以下命令

```bash
adb kill-server
# 如果你使用了内置 frp 或者自行使用了 ssh 转发，
# 这里的 x.x.x.x 通常为 127.0.0.1，请依据事实修改
# 而这里的 65000 也非固定，依据你实际设置的目的转发端口做修改
adb connect x.x.x.x:65000
```

最后，按照和上文 通过USB 一样的方法操作
```bash
# localhost 代表使用 adb 设备
python3 -u startmitm.py localhost
```

即可。

注意：你可能需要完全结束APP并重新打开才会显示流量数据。

按下一次 `CONTROL` + `C` 退出脚本。

### DNS 中间人

截获 DNS 请求需要确保 mitmproxy 的版本 >= 8.1.0（且 Python>=3.9)，且需要以**管理员**或者**root**身份运行脚本。
```bash
python3 -u startmitm.py 192.168.1.2 --set dns_server=true
```
即可。

> 注意：由于实现原因，DNS中间人不支持使用 `startmitm.py localhost` 方式

这些DNS请求默认会从本机发出，你也可以将这些 DNS 请求转发到指定的上游DNS服务器例如 `1.1.1.1`。
```bash
python3 -u startmitm.py 192.168.1.2 --set dns_server=true --set dns_mode=reverse:1.1.1.1
```

hook 脚本的方法名称定义有一些变化，正常 http 请求为 `response()`，截获 DNS 时需要使用 `dns_response()`。

```python
def response(flow):
    print (flow, type(flow))

def dns_response(flow):
    print (flow, type(flow))
```

具体请查看 mitmproxy 的文档。

## adb_pubkey.py

用于安装本机的 adb pubkey 到 lamda 的脚本，否则 adb 连接将会显示未授权

```bash
# 安装 adb pubkey
python3 -u adb_pubkey.py install 192.168.1.2
# 卸载 adb pubkey
python3 -u adb_pubkey.py uninstall 192.168.1.2
```

安装后，执行
```bash
adb kill-server
adb connect 192.168.1.2:65000
adb -s 192.168.1.2:65000 shell
```
来连接 lamda adb。

## ssh.sh

连接入手机上的 shell 终端。

执行
```bash
bash ssh.sh 192.168.1.2
```
即可。

同样，对于不同网段但通过USB连接的设备，也可以
```bash
bash ssh.sh localhost
```

## scp.sh

使用 `scp` 复制设备上的文件到本地。

将 192.168.1.2 的 `/sdcard/DCIM` 目录复制到当前目录

```bash
bash scp.sh 192.168.1.2:/sdcard/DCIM .
```

将本地目录/文件 `test/` 复制到设备 192.168.1.2 的 `/sdcard/`

```bash
bash scp.sh test/ 192.168.1.2:/sdcard
```

## discover.py

列出**本地网络**中所有在线的设备（部分网络情况下可能一些设备没有列出，请多次尝试）

```bash
python3 discover.py
```

## fridarpc.py

一个 fridarpc 功能的简单封装。

此功能需要你能熟练编写 frida 脚本。示例中使用的脚本请参照 test-fridarpc.js 文件，特别注意: frida 脚本中 rpc.exports 定义的函数返回值只能为 string/list/json 或者任意 js 中可以被 json 序列化的值。假设设备IP为 192.168.0.2。

> 执行以下命令注入 RPC 到 com.android.settings（注意查看是否有报错）

```bash
python3 fridarpc.py -f test-fridarpc.js -a com.android.settings -d 192.168.0.2
```

现在已经将接口拿出来了，只需要请求 `http://192.168.0.2:65000/fridarpc/myRpcName/getMyString?args=["A","B"]` 即可得到脚本内方法的返回结果，链接也可以用浏览器打开，接口同时支持 POST 以及 GET，参数列表也可以同时使用多个参数。

注意参数的提供形式，是**双引号**，建议使用 json.dumps(["A", "B"])

> 用 requests 调用
```python
import json
import requests
url = "http://192.168.0.2:65000/fridarpc/myRpcName/getMyString"
data = requests.post(url, data={"args": json.dumps(["A", "B"])}).json()
print (data["result"])

#* 状态码 200 一切正常
#* 状态码 410 需要重新注入脚本或者脚本未注入（目前不支持自动重新注入）
#* 状态码 500 脚本或参数异常
#* 状态码 400 参数错误
```

响应结果的格式是固定的，可在浏览器打开查看。

## emu-install.sh

仅适用于主流模拟器的服务端安装脚本，需要设备开启 WIFI adb，需要提前下载
对应架构服务端安装包到当前运行目录。

```bash
bash emu-install 192.168.1.2
```


## 各种服务脚本 (Docker)

> 所有镜像均为 x86 平台，在 ARM 处理器的 Linux/Mac 上使用你可能要自行做出修改并重新生成。

### openvpn

开箱即用的 OpenVPN 服务

### globalmitm

用于分析需要透过 ss 实现需要代理才能连接的国外APP的流量

### frps

开箱即用的 frp 端口转发

### socks5

开箱即用的 socks5 代理服务
