#!/usr/bin/python3
# Copyright 2022 rev1si0n (lamda.devel@gmail.com). All rights reserved.
import setuptools

exec(open("lamda/__init__.py", "rt").read())

setuptools.setup(
    name            = "lamda",
    version         = "{}".format(__version__),
    description     = "Android reverse engineering & automation framework (Client API)",
    url             = "https://github.com/firerpa/lamda",
    author          = "rev1si0n",
    python_requires = ">=3.6,<3.13",
    zip_safe        = False,
    extras_require  = {
        "full": ["frida>=16.0.0,<17.0.0"],
        ":sys_platform == \"win32\"": [
            "pyreadline==2.1",
        ],
    },
    install_requires= [
        "grpcio-tools>=1.35.0,<=1.68.0",
        "grpc-interceptor>=0.13.0,<=0.15.4",
        "grpcio>=1.35.0,<=1.68.0",
        "cryptography>=35.0.0",
        "msgpack>=1.0.0",
        "asn1crypto>=1.0.0,<2",
        "pem==23.1.0",
    ],
    classifiers = [
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
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
