#!/usr/bin/env python3
import os
import argparse

from PIL import Image, ImageDraw
from lamda.client import *


cert = os.environ.get("CERTIFICATE", None)
port = int(os.environ.get("PORT", 65000))

parser = argparse.ArgumentParser()
parser.add_argument("-d", type=str, dest="device",
                        help="service ip address", required=True)
parser.add_argument("-p", type=str, dest="port",
                        default=port,
                        help="service port")
parser.add_argument("-f", "--method", type=int,
                        dest="method",
                        help="find method", default=0)
parser.add_argument("-i", "--image", type=argparse.FileType("rb"),
                        dest="image",
                        help="find image path", required=True)
parser.add_argument("-t", "--threshold", type=float,
                        dest="threshold",
                        help="threshold", default=0)
parser.add_argument("-m", "--max-distance", type=int,
                        dest="distance",
                        help="max distance", default=0)
parser.add_argument("-cert", type=str, default=cert,
                                help="ssl cert")
args = parser.parse_args()


d = Device(args.device, port=args.port,
                certificate=args.cert)
image = Image.open(d.screenshot(60))

draw = ImageDraw.Draw(image)
for r in d.find_similar_image(args.image.read(),
                                method=args.method,
                                max_distance=args.distance,
                                threshold=args.threshold):
    p1 = r.corner("top-left")
    p2 = r.corner("bottom-right")
    draw.rectangle(((p1.x, p1.y), (p2.x, p2.y)),
                    outline="red", width=3)
image.show()
exit (0)