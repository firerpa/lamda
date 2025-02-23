#!/usr/bin/env python3
import os
import sys
import random
import datetime

from hashlib import sha256
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import (
    Name,
    NameAttribute,
    CertificateBuilder,
    CertificateSigningRequestBuilder,
    DNSName,
    SubjectAlternativeName,
    load_pem_x509_certificate,
    BasicConstraints,
    KeyUsage,
)
from cryptography.x509.oid import NameOID

CN = "lamda"
if len(sys.argv) == 2:
    CN = sys.argv[1]

if os.path.isfile("root.key"):
    with open("root.key", "rb") as f:
        rk = serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend()
        )
else:
    rk = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    with open("root.key", "wb") as f:
        f.write(
            rk.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

if os.path.isfile("root.crt"):
    with open("root.crt", "rb") as f:
        root = load_pem_x509_certificate(f.read(), default_backend())
else:
    subject = issuer = Name(
        [
            NameAttribute(NameOID.ORGANIZATION_NAME, "LAMDA"),
            NameAttribute(NameOID.COMMON_NAME, "FireRPA LAMDA Root Trust"),
        ]
    )
    root = (
        CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))
        .public_key(rk.public_key())
        .serial_number(random.randint(1, 2**128))
        .add_extension(BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(rk, hashes.SHA256(), default_backend())
    )
    with open("root.crt", "wb") as f:
        f.write(root.public_bytes(serialization.Encoding.PEM))


if not os.path.isfile(f"{CN}.pem"):
    pk = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    csr = (
        CertificateSigningRequestBuilder()
        .subject_name(Name([NameAttribute(NameOID.COMMON_NAME, CN)]))
        .sign(pk, hashes.SHA256(), default_backend())
    )

    cert = (
        CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(root.subject)
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))
        .public_key(csr.public_key())
        .serial_number(random.randint(1, 2**128))
        .sign(rk, hashes.SHA256(), default_backend())
    )

    with open(f"{CN}.pem", "wb") as output:
        pem_private_key = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        pem_cert = cert.public_bytes(serialization.Encoding.PEM)
        pem_root = root.public_bytes(serialization.Encoding.PEM)

        d = pk.private_numbers().d
        pd = d.to_bytes((d.bit_length() + 7) // 8, "little")
        cred = sha256(pd).hexdigest()[::3]

        header = f"LAMDA SSL CERTIFICATE (CN={CN},PASSWD={cred})\n"
        output.write(header.encode())
        output.write(pem_private_key.strip())
        output.write(b"\n")
        output.write(pem_cert.strip())
        output.write(b"\n")
        output.write(pem_root.strip())
        output.write(b"\n")
