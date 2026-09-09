# Copyright 2025 rev1si0n (lamda.devel@gmail.com). All rights reserved.
#
# Distributed under MIT license.
# See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
import base64

from lamda.utils import getprop
from lamda.extensions import BaseMcpExtension
from lamda.mcp import mcp, Annotated, TextContent, BlobResourceContents


class ExampleMcpExtension(BaseMcpExtension):
    route = "/model-context-protocol/mcp/"
    name = "example-mcp-extension"
    version = "1.0.0"
    @mcp("tool", description="Send a greeting to others.")
    def greeting(self, ctx, msg: Annotated[str, "Greeting message"],
                            to: Annotated[str, "Greeting to who"] = "John"):
        return TextContent(text=f"mcp greeting! {msg}, {to}!")
    @mcp("tool", description="Read android system property by name.")
    def getprop(self, ctx, name: Annotated[str, "Android system property name."]):
        return TextContent(text=getprop(name) or "")
    @mcp("resource", uri="file://{absolute_path}")
    def get_file(self, ctx, absolute_path: Annotated[str, "Absolute file path"]):
        """ Read file content on the device by full path """
        blob = base64.b64encode(open(absolute_path, "rb").read()).decode()
        return BlobResourceContents(blob=blob, uri=f"file://{absolute_path}",
                                    mimeType="text/plain")