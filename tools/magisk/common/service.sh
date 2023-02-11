#!/system/bin/sh
base=${0%/*}
ABI=$(getprop ro.product.cpu.abi)
launch="sh ${base}/${ABI}/bin/launch.sh"
cert=${base}/config/lamda.pem
port=65000

sleep 30
# where to locate properties.local
export CFGDIR=${base}/etc
export ca_store_remount=true
if [ -f "${cert}" ]; then
$launch --port=${port} --certificate=${cert}
else
$launch --port=${port}
fi