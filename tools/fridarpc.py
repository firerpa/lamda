#!/usr/bin/env python3
if __name__ == "__main__":
    import os
    import time
    import argparse
    from lamda.client import *

    cert = os.environ.get("CERTIFICATE", None)
    port = int(os.environ.get("PORT", 65000))

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", type=str, dest="device",
                            help="service ip address", required=True)
    parser.add_argument("-a", type=str, dest="package",
                            help="target application Id", required=True)
    parser.add_argument("-p", type=str, dest="port", default=port,
                            help="service port")
    parser.add_argument("-f", type=argparse.FileType("r"), dest="script",
                            help="frida script", required=True)
    parser.add_argument("-delay", type=int, dest="delay", default=5,
                            help="attach after delay")
    parser.add_argument("-cert", type=str, default=cert,
                                   help="ssl cert")
    args = parser.parse_args()

    d = Device(args.device, port=args.port,
                    certificate=args.cert)

    app = d.application(args.package)
    app.detach_script()
    app.attach_script(args.script.read(),
                      standup=args.delay)
    exit (0)