#!/system/bin/sh
base=${0%/*}
cert=${base}/config/lamda.pem
launch="sh ${base}/server/bin/launch.sh"
port=65000

sleep 30
# where to locate properties.local
export CFGDIR=${base}/config
export ca_store_remount=true
if [ -f "${cert}" ]; then
$launch --port=${port} --certificate=${cert}
else
$launch --port=${port}
fi