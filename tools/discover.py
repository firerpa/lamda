#!/usr/bin/env python3
import os
import struct
from socket import *

from lamda import __version__
from lamda.client import load_proto

protos, services = load_proto("bcast.proto")

BcastHeader = protos.BcastHeader
BcastDiscoverInfo = protos.BcastDiscoverInfo
BcastResponse = protos.BcastResponse
BcastRequest = protos.BcastRequest

port = int(os.environ.get("PORT", 65000))


def BcastCallMethod(method):
    req = BcastRequest(method=method)
    # ASTBCAST + length (body,4byte) + body + feeedeed
    hdr = BcastHeader(magic=0x54534143,
                            version=__version__)
    req.header.CopyFrom(hdr)
    body = req.SerializeToString()
    buffer = []
    r = struct.pack("QH", 0x5453414342545341, len(body))
    buffer.append(r)
    r = struct.pack("{}s".format(len(body)), body)
    buffer.append(r)
    r = struct.pack("I", 0xeedeeefe)
    buffer.append(r)
    r = bytes().join(buffer)
    return r


sock = socket(AF_INET, SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
message = BcastCallMethod("DISCOVER")
sock.sendto(message, ("255.255.255.255", port))
sock.settimeout(3.0)

while True:
    try:
        data, remote = sock.recvfrom(4096)
    except timeout:
        break
    fmt = "<QH{}sI".format(len(data) - 14)
    magic, size, body, _magic = struct.unpack(fmt, data)
    res = BcastResponse.FromString(body)
    print (remote[0], end="\t")
    print (res.discoverinfo.ID, end="\t")
    print (res.discoverinfo.device, end="\t")
    print (res.discoverinfo.abi, end="\t")
    print (res.discoverinfo.sdk, end="\t")
    print (res.discoverinfo.version)
