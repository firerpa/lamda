#!/bin/bash
DEVICE=$1
TARGET=/data/local/tmp

RED='\033[1;31m'
GRE='\033[1;32m'
RST='\033[0m'

echo -e "[@] -------------------------"
echo -e "[@]$GRE lamda 安装脚本，适用于夜神/雷电最新版模拟器 $RST"
echo -e "[@] -------------------------"
echo -e "[*] 连接设备 ${DEVICE}"
adb connect $DEVICE    >/dev/null 2>&1
adb -s $DEVICE wait-for-device
ABI=$(adb -s $DEVICE shell getprop ro.product.cpu.abi|tr -d '\r')
adb -s $DEVICE root    >/dev/null 2>&1
adb -s $DEVICE wait-for-device

if [ ! -f "${ABI}.tar.gz" ]; then
echo -e "[!]$RED 下载/复制 ${ABI}.tar.gz 到目录 $(pwd) 并重新运行此脚本 $RST"
exit 1
fi
if ! adb -s $DEVICE shell id|grep 'uid=0' >/dev/null; then
echo -e "[!]$RED ADB root 失败 $RST"
exit 1
fi
adb -s $DEVICE remount >/dev/null 2>&1
echo -e "[*] 正在上传 ${ABI}.tar.gz"
adb -s $DEVICE push ${ABI}.tar.gz ${TARGET}

adb -s $DEVICE shell rm -rf ${TARGET}/${ABI}/bin >/dev/null 2>&1
adb -s $DEVICE shell rm -rf ${TARGET}/${ABI}/lib >/dev/null 2>&1
adb -s $DEVICE shell rm -rf ${TARGET}/${ABI}/etc >/dev/null 2>&1

echo -e "[*] 正在解压 ${ABI}.tar.gz"
adb -s $DEVICE shell tar -C ${TARGET} -xzf ${TARGET}/${ABI}.tar.gz

echo -e "[*] 尝试安装为开机启动（仅雷电安卓9)"
adb -s $DEVICE shell mount -o rw,remount /system
adb -s $DEVICE shell mount -o rw,remount /

adb -s $DEVICE shell "sed -i 's,\(do_bootcomplete$\)\(.*\),\1; sh /data/launch.sh,' /system/etc/init.sh" >/dev/null 2>&1
adb -s $DEVICE shell "echo \"exec sh ${TARGET}/${ABI}/bin/launch.sh\" > /data/launch.sh"

if adb -s $DEVICE shell cat /system/etc/init.sh 2>/dev/null | grep launch.sh >/dev/null; then
echo -e "[*]$GRE 成功安装为开机启动 $RST"
echo -e "[#]$GRE 设备重启/开机后，服务将会自动启动 $RST"
echo -e "[#]$GRE 你将无需手动启动 $RST"
else
echo -e "[!]$RED 未能安装为开机启动 $RST"
echo -e "[#]$RED 每次设备重启/开机后，请进入ADB并以ROOT身份执行 $RST"
echo -e "[#]$RED sh /data/launch.sh $RST"
echo -e "[#]$RED 来启动服务 $RST"
fi
echo -e "[*] 正在首次启动"
adb -s $DEVICE shell sh /data/launch.sh
adb disconnect $DEVICE >/dev/null 2>&1
echo -e "[*] 已成功完成"
exit 0