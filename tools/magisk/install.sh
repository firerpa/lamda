#!/system/bin/sh
ABI=$(getprop ro.product.cpu.abi)
SERVER=$TMPDIR/lamda-server-$ABI.tar.gz
BB="/data/adb/magisk/busybox"
USRDIR=/data/usr

if [ -d "/data/adb/ksu/" ]; then
BB="/data/adb/ksu/bin/busybox"
fi

export LATESTARTSERVICE=true

ui_print ".____                       ________      _____    "
ui_print "|    |    _____     _____   \______ \    /  _  \   "
ui_print "|    |    \__  \   /     \   |    |  \  /  /_\  \  "
ui_print "|    |___  / __ \_|  Y Y  \  |    |   \/    |    \ "
ui_print "|_______ \(____  /|__|_|  / /_______  /\____|__  / "
ui_print "        \/     \/       \/          \/         \/  "
ui_print "                                       installer   "

pushd $(pwd)
cd $MODPATH
if [ ! -f $SERVER ]; then
abort "lamda-server-${ABI}.tar.gz not found in archive"
fi

ui_print "- Extracting server files"
$BB tar -xzf $SERVER

ui_print "- Placing configs"
mkdir -p ${USRDIR}

cp -af $TMPDIR/adb_keys ${USRDIR}/.adb_keys

cp -af $TMPDIR/properties.local ${USRDIR}
cp -af $TMPDIR/lamda.pem ${USRDIR}

ui_print "- Please reboot your device"
popd