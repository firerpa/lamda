#!/system/bin/sh
if [ ! -f "$1" ]; then
        echo launch.sh path not provided.
exit 1
fi
OUTFILE=/sdcard/statistics.txt
echo "collecting lamda statistics"
rm $OUTFILE >/dev/null 2>&1
{
echo "BEGIN LAMDA REPORT $(date +%Y-%m-%d.%H:%M:%S)"
echo "---------------------------------------------"
echo "enforced:                 $(getenforce)"
echo "ashmem:                   $(! grep ashmem /proc/misc >/dev/null 2>&1; echo $?)"
echo "binder:                   $(! grep binder proc/filesystems >/dev/null 2>&1; echo $?)"
echo "uname:                    $(uname -a)"
echo ""
echo "ro.boot.hardware:         $(getprop ro.boot.hardware)"
echo "ro.boot.selinux:          $(getprop ro.boot.selinux)"
echo ""
echo "ro.build.version.sdk:     $(getprop ro.build.version.sdk)"
echo "ro.build.fingerprint:     $(getprop ro.build.fingerprint)"
echo "ro.build.type:            $(getprop ro.build.type)"
echo ""
echo "ro.product.brand:         $(getprop ro.product.brand)"
echo "ro.product.board:         $(getprop ro.product.board)"
echo "ro.product.cpu.abi:       $(getprop ro.product.cpu.abi)"
echo "ro.product.cpu.abilist:   $(getprop ro.product.cpu.abilist)"
echo "ro.product.device:        $(getprop ro.product.device)"
echo "ro.product.model:         $(getprop ro.product.model)"
echo "ro.debuggable:            $(getprop ro.debuggable)"
echo ""
echo "persist.sys.timezone:     $(getprop persist.sys.timezone)"
echo "persist.sys.locale:       $(getprop persist.sys.locale)"
echo ""

echo "IP-tables check:"
echo "IP-tables nat:            $(! iptables -L -n -t nat >/dev/null; echo $?)"
echo ""

echo "IP-route check:"
echo "ip link:                  $(! ip link >/dev/null; echo $?)"
echo "ip tunnel:                $(! ip tunnel >/dev/null; echo $?)"
echo "ip tuntap:                $(! ip tuntap >/dev/null; echo $?)"
echo "ip route:                 $(! ip route >/dev/null; echo $?)"
echo "ip rule:                  $(! ip rule >/dev/null; echo $?)"
echo ""

echo "lsmod:"
lsmod
echo ""

} >>$OUTFILE 2>&1

DMESG=$(mktemp)
LOGCAT=$(mktemp)
PIDS=

dmesg -C
logcat --clear

dmesg -w >$DMESG 2>&1 &
PIDS+="$PIDS $!"
logcat >$LOGCAT 2>&1 &
PIDS+="$PIDS $!"

echo "please wait..."
sh $@ >> $OUTFILE 2>&1

sleep 60
kill -TERM $PIDS

{
echo "-------- BEGIN dmesg"
cat $DMESG
echo "-------- BEGIN logcat"
cat $LOGCAT
} >>$OUTFILE 2>&1
echo "report: $OUTFILE"
echo "finished"
exit 0