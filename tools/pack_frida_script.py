#!/usr/bin/env python3
# Copyright 2025 rev1si0n (lamda.devel@gmail.com). All rights reserved.
#
# Distributed under MIT license.
# See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
#encoding=utf-8
import os
import sys
import base64
import importlib.util


def embed_bridge(source, lang):
    # https://github.com/frida/frida/issues/3460#issuecomment-3066016776
    tools_dir = os.path.dirname(importlib.util.find_spec("frida_tools").origin)
    fmt = '(function() { %s; Object.defineProperty(globalThis, "%s", { value: bridge }); })(); %s'
    bridge = os.path.join(tools_dir, "bridges", f"{lang.lower()}.js")
    with open(bridge, "r", encoding="utf-8") as f:
        return fmt % (f.read(), lang, source)


if __name__ == "__main__":
    script = sys.argv[1]
    source = embed_bridge(open(script, "rt", encoding="utf-8").read(),
                                                            "Java")
    open("%s-packed" % script, "w").write(source)
    encoded = base64.b64encode(source.encode("utf-8")).decode()
    open("%s-packed-modules-script.yaml" % script, "w").write(
"""enable: true
application: "YOUR_APPLICATION"
version: "N/A"
user: 0
runtime: "qjs"
script: !!binary "%s"
emit: "http://myserver/reportData"
encode: "none"
standup: 10
spawn: false""" % encoded)