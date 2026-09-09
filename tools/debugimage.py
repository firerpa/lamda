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
parser.add_argument("-p", "--port", type=str,
                        default=port, help="service port")
parser.add_argument("-f", "--method", type=str,
                        help="find method", default="0")
parser.add_argument("-i", "--image", type=argparse.FileType("rb"),
                        help="find image path", required=True)
parser.add_argument("-a", "--area", type=str,
                        help="area", default="0")
parser.add_argument("-s", "--scale", type=float,
                        help="scale", default=1.0)
parser.add_argument("-t", "--threshold", type=float,
                        help="threshold", default=0)
parser.add_argument("-m", "--distance", type=int,
                        help="max distance", default=0)
parser.add_argument("-cert", type=str, default=cert,
                                help="ssl cert")
args = parser.parse_args()


d = Device(args.device, port=args.port,
                certificate=args.cert)
image = Image.open(d.screenshot(95))

draw = ImageDraw.Draw(image)
for r in d.find_similar_image(args.image.read(),
                                area=eval(args.area),
                                method=eval(args.method),
                                distance=args.distance,
                                threshold=args.threshold,
                                scale=args.scale):
    p1 = r.corner("top-left")
    p2 = r.corner("bottom-right")
    draw.rectangle(((p1.x, p1.y), (p2.x, p2.y)),
                    outline="#00ff00", width=3)
image.show()