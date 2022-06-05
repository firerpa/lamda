#!/usr/bin/python3
# Copyright 2022 rev1si0n (ihaven0emmail@gmail.com). All rights reserved.
import setuptools

exec(open("lamda/__init__.py", "rt").read())

setuptools.setup(
    name            = "lamda",
    version         = "{}.{}".format(__version__, __build__),
    url             = "https://github.com/rev1si0n",
    author          = "rev1si0n",
    python_requires = ">=3.6,<4.0",
    zip_safe        = False,
    extras_require  = {
        "frida": ["frida>=15.0.0,<16.0.0,!=15.1.15,!=15.1.16,!=15.1.17"],
        ":sys_platform == \"win32\"": [
            "pyreadline==2.1",
        ],
    },
    install_requires= [
        "grpcio-tools>=1.35.0,<=1.40.0",
        "grpc-interceptor>=0.13.0,<0.14.0",
        "grpcio>=1.35.0,<=1.40.0",
        "asn1crypto>=1.0.0",
    ],
    package_data    = {
        "lamda": ["*.py", "*.proto"],
        "lamda.google.protobuf.compiler": ["*.proto"],
        "lamda.google.protobuf": ["*.proto"],
        "lamda.rpc": ["*.proto"],
    },
    packages        = [
        "lamda.google.protobuf.compiler",
        "lamda.google.protobuf",
        "lamda.rpc",
        "lamda",
    ],
)
