#!/usr/bin/env python3
#encoding=utf-8
import sys
from hashlib import md5
from OpenSSL import crypto

CN = "lamda"
if len(sys.argv) == 2:
    CN = sys.argv[1]

pk = crypto.PKey()
pk.generate_key(crypto.TYPE_RSA, 2048)
cert = crypto.X509()

cert.get_subject().O    = "lamda"
cert.get_subject().CN   = CN

cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(315360000)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(pk)
cert.sign(pk, "sha256")

pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, pk)
cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)

asn1_pk = crypto.dump_privatekey(crypto.FILETYPE_ASN1, pk)
passwd = md5(asn1_pk).hexdigest().encode()

f = open("{}.pem".format(CN), "wb")
f.write(b"# Certificate Used BY LAMDA")
f.write(", CN={}".format(CN).encode())

f.write(b"\n")
f.write(cert.strip())
f.write(b"\n")
f.write(pkey.strip())
f.write(b"\n")

f.write(passwd.strip())
f.write(b"\n")
f.close()
