#!/system/bin/sh
ABI=$(getprop ro.product.cpu.abi)
SERVER=$TMPDIR/$ABI.tar.gz
BB="/data/adb/magisk/busybox"
CONFDIR="$MODPATH/config"

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
abort "${ABI}.tar.gz not found in archive"
fi

ui_print "- Extracting server files"
$BB tar -xzf $SERVER

ui_print "- Placing configs"
mkdir -p /data/usr
cp -af $TMPDIR/adb_keys /data/usr/.adb_keys

mkdir -p $CONFDIR

cp -af $TMPDIR/properties.local $CONFDIR
cp -af $TMPDIR/lamda.pem $CONFDIR

ui_print "- Please reboot your device"
popd