#!/usr/bin/python3
# Copyright 2022 rev1si0n (ihaven0emmail@gmail.com). All rights reserved.
import setuptools

exec(open("lamda/__init__.py", "rt").read())

setuptools.setup(
    name            = "lamda",
    version         = "{}.{}".format(__version__, __build__),
    description     = "Android reverse engineering & automation framework",
    url             = "https://github.com/rev1si0n/lamda",
    author          = "rev1si0n",
    python_requires = ">=3.6,<3.11",
    zip_safe        = False,
    extras_require  = {
        "frida": ["frida>=15.0.0,<16.0.0,!=15.1.15,!=15.1.16,!=15.1.17"],
        ":sys_platform == \"win32\"": [
            "pyreadline==2.1",
        ],
    },
    install_requires= [
        "grpcio-tools>=1.35.0,<1.48.0",
        "grpc-interceptor>=0.13.0,<0.14.2",
        "grpcio>=1.35.0,<1.48.0",
        "asn1crypto>=1.0.0,<2",
    ],
    classifiers = [
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Android",
        "Topic :: Security",
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
