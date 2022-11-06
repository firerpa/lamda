#!/bin/bash
# generate a certificate for lamda
# default expire days is 3650 = 10 years
set -e
CN=${1:-lamda}
PSW="secret"
DAYS=3650
BITS=2048

openssl genrsa  -passout pass:$PSW -des3 -out ${CN}.key ${BITS}
# the subject O must be lamda
openssl req     -passin pass:$PSW -new -key ${CN}.key -out ${CN}.csr -subj "/O=lamda/CN=${CN}"
openssl x509    -passin pass:$PSW -req -days ${DAYS} -in ${CN}.csr -signkey ${CN}.key -out ${CN}.crt
openssl rsa     -passin pass:$PSW -in ${CN}.key -out ${CN}.key

openssl x509 -in ${CN}.crt -text -noout                           >${CN}.pem
cat ${CN}.{crt,key}                                              >>${CN}.pem
openssl rsa -in ${CN}.key -outform der 2>/dev/null | openssl md5 | awk '{print $NF}' >>${CN}.pem

echo certificate: $(pwd)/${CN}.pem
rm ${CN}.{csr,crt,key}
