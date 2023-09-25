#!/system/bin/sh
base=${0%/*}
cert=/data/usr/lamda.pem
launch="sh ${base}/server/bin/launch.sh"
port=65000

sleep 25
export ca_store_remount=true
if [ -f "${cert}" ]; then
$launch --port=${port} --certificate=${cert}
else
$launch --port=${port}
fi