#!/usr/bin/env python3
#encoding=utf-8
import os
import sys
import random
from hashlib import sha256
from OpenSSL import crypto

CN = "lamda"
if len(sys.argv) == 2:
    CN = sys.argv[1]

if os.path.isfile("root.key"):
    data = open("root.key", "rb").read()
    rk = crypto.load_privatekey(crypto.FILETYPE_PEM, data)
else:
    rk = crypto.PKey()
    rk.generate_key(crypto.TYPE_RSA, 2048)

    data = crypto.dump_privatekey(crypto.FILETYPE_PEM, rk)
    open("root.key", "wb").write(data)

if os.path.isfile("root.crt"):
    data = open("root.crt", "rb").read()
    root = crypto.load_certificate(crypto.FILETYPE_PEM, data)
else:
    root = crypto.X509()

    root.get_subject().O    = "LAMDA"

    root.gmtime_adj_notBefore(0)
    root.gmtime_adj_notAfter(315360000)
    root.set_issuer(root.get_subject())
    root.set_pubkey(rk)
    root.sign(rk, "sha256")

    data = crypto.dump_certificate(crypto.FILETYPE_PEM, root)
    open("root.crt", "wb").write(data)

if not os.path.isfile("{}.pem".format(CN)):
    pk = crypto.PKey()
    pk.generate_key(crypto.TYPE_RSA, 2048)

    req = crypto.X509Req()
    req.set_version(0)
    req.get_subject().CN    = CN
    req.set_pubkey(pk)
    req.sign(pk, "sha256")

    cert = crypto.X509()
    cert.set_version(2)
    cert.set_subject(req.get_subject())
    cert.set_serial_number(random.randint(1, 2**128))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(315360000)
    cert.set_issuer(root.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(rk, "sha256")

    pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, pk)
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
    root = crypto.dump_certificate(crypto.FILETYPE_PEM, root)

    d = pk.to_cryptography_key().private_numbers().d
    pd = d.to_bytes((d.bit_length() + 7) // 8, "little")
    cred = sha256(pd).hexdigest()[::3]

    f = open("{}.pem".format(CN), "wb")
    hdr = "LAMDA SSL CERTIFICATE (CN={},PASSWD={})".format(CN, cred)
    os.chmod(f.name, 0o600)

    f.write(hdr.encode())
    f.write(b"\n")
    f.write(pkey.strip())
    f.write(b"\n")
    f.write(cert.strip())
    f.write(b"\n")
    f.write(root.strip())
    f.write(b"\n")
    f.close()