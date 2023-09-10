#!/bin/bash
[ $# -lt 2 ] && exit 1
DEFAULT_ID_RSA=$(mktemp)
PORT=${PORT:-65000}
case "$1" in
                *':'*)
                                p1=root@$1
                                p2=$2
                ;;
                *)
                                p1=$1
                                p2=root@$2
                ;;
esac
umask 077
if [ ! -f "${CERTIFICATE}" ]; then
# this is the default id_rsa for ssh service
cat <<EOL >$DEFAULT_ID_RSA
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEA4QHmY32OT+F+maERMn1cvBRuIOIXH9yOALG+GMCngtjRJzSR
n09dInmXE+PjiAqNRWvknVEjFywv0v1v/H2qSRJKR/togPgySjiABhigqDHdirNd
Dh63oN2e+d0yythoLzsQrH5BSVtw05Atpkr7bW4KdfMveWuddvDACnQ3mvCXq50X
IK3cOlmHXwcJrX55BhEXxgHIqw0upf0A7DC3Afz5xjOA6+K/O2EzZIIJ+sWw7/Ko
5+3m98Et0zwcxe20uNxzYf7JSMu3490YNckLiQcDrZVRUXNS70HO9HWCXKdjFJPi
GgPtKUQNHjChwzSCQQGzqitXdwa60i9Sy1U09wIBIwKCAQAzbiYIHLLQbg5PAD5x
8MS9Rn+SfNIV6UUHeRWCACZJyyh9/WMdGXRfpsNyQreqEQpZArfpcaGe5YdGK0zL
/3dhKMCFe0sWKhofl+K/kJnAC2XWj2W6FaZQp69PDfz7KiZxMhJwkeMJc/yIIPR9
x/70cOxyuz4NH+l6Rag8510qujhxn6lGc1+ZNHGeAYmUD7wFz9/QYDZU9C0YcylA
2+Q5woU3L4b3y3JKqB6/dnsP9uF7R5KBR+qiqOwVm0nhvVU5uwbpQwTXeklopXyN
rI/NeYcsDoEyb8NquVXX/GkOgY0FhqblGUR9kSdTLHq6VamelHc+dczZgMxcsq1c
mnnLAoGBAP2FPssFpHJRhSr38Fq5A7mEjQeiPq2WgYV7kCpJT5F5OymcCCETIjEH
4pTk5zCWUuIBx5LlzSa0XnQSYb0100ZzvDgfm1NPmqdkpPwkkbh2xyoHYTTPJ3WG
TDur8Qyi83NteveszO1TCAGBTe3zN+2ov9qzl5Y7QHF94GVFDo4NAoGBAOM1Q8eG
0KeqjutTz/UMtejoFpz0Hi1g32PfdQInHx8MDslYu3Fcpnos3xf59H7+mrRy0fUM
hh27v7DiUvxUfhlojf0F3kDKeg9VZBslZF3vTCpFdKdFouZ2Cru3lCoaPSau69BC
6HQw4P+RABrgxc6CeE9FUGEEMss+wTcRItITAoGBAO8ImkpkZ9mAD9gOV6X+5kEz
1W2Y+USVOEqns9AZPGSW4AKpDvqdAvsHbzvtxAk9RtUXnumW118B1WYf9cEG3SUr
SxBYUJ8B6ZaDdvxc/mwYOCBQGdK0sCz692t2OwvqGL1J95kQo/W0r8bnoT9wSqzg
72fN5rI33azVxPHExJSPAoGAGfd1deOFj4E057HOn6muY8LAwXr8InF4nbMjULQD
joUJARF0gfv1xNHtnFcUoMyj912UVoUWpE/4poBD/5SgsnJZXr7XkmBIdsfuLvz1
hxQItF+1j3WsN5h2QVbPGsErj2RyuLcwgk66oN1fGQO+1cXEm1hg9SUNHorUQM7C
JqMCgYEAofxXJ8dOWUaFIHmKLE7Y+0+i3D1yXVIyu/puuaQGbNFHxjcJ9ZdubhLN
IyzJvngtM7mC90FtUETxvErMGdTzFeKtSKBZsJ8BiLCszRCEuJf5RX6uNrFUQ2pT
PEmns088Gs4KUDwjTG0zQtj3pNc5zDynDMpFKp96spefqLJqw3s=
-----END RSA PRIVATE KEY-----
EOL
else
DEFAULT_ID_RSA=$CERTIFICATE
fi
exec rsync -avz ${@:3} -e "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o LogLevel=ERROR -i $DEFAULT_ID_RSA -p $PORT" $p1 $p2
