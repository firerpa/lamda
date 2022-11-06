#!/usr/bin/env python3
if __name__ == "__main__":
    import os
    import time
    import argparse
    from lamda.client import *

    cert = os.environ.get("CERTIFICATE", None)
    port = int(os.environ.get("LAMDAPORT", 65000))

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", type=str, dest="device",
                            help="service ip address", required=True)
    parser.add_argument("-a", type=str, dest="package",
                            help="target application Id", required=True)
    parser.add_argument("-p", type=str, dest="port", default=port,
                            help="service port")
    parser.add_argument("-f", type=argparse.FileType("r"), dest="script",
                            help="frida script", required=True)
    parser.add_argument("-delay", type=int, dest="delay", default=0,
                            help="attach after delay")
    parser.add_argument("-cert", type=str, default=cert,
                                   help="ssl cert")
    args = parser.parse_args()

    d = Device(args.device, port=args.port,
                    certificate=args.cert)
    pid = d.frida.spawn(args.package)
    d.frida.resume(pid)

    time.sleep(args.delay)
    session = d.frida.attach(pid)
    session.on("detached", print)

    sc = session.create_script(args.script.read())
    sc.on("destroyed", print)
    sc.on("message", print)

    sc.load()
    sc.eternalize()
    exit (0)
