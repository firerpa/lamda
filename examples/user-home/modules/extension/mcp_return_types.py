#!/usr/bin/env python3
# Copyright 2025 rev1si0n (lamda.devel@gmail.com). All rights reserved.
#
# Distributed under MIT license.
# See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
#
# THIS IS THE OFFICIAL MCP TYPES equivalent made by firerpa authors (FUCKOFF pydantic)
# github.com/modelcontextprotocol/python-sdk/blob/v1.13.1/src/mcp/types.py
# WE ONLY LIST THE TYPES THAT YOU CAN USE
import msgspec

from msgspec import Struct, Meta
from typing import Dict, Any, Literal, List, Union, Annotated


Role = Literal["user", "assistant"]
LoggingLevel = Literal["debug", "info", "notice", "warning", "error", "critical", "alert", "emergency"]


class BaseModel(Struct, omit_defaults=False):
    def validate(self):
        return msgspec.json.decode(msgspec.json.encode(self),
                                            type=type(self))


class BaseStructuredModel(BaseModel):
    """ StructuredModel """


class Result(BaseModel):
    """Base class for JSON-RPC results."""


class Annotations(BaseModel):
    audience: Union[list[Role], None] = None
    priority: Union[Annotated[float, Meta(ge=0.0, le=1.0)], None] = None


class ResourceContents(BaseModel):
    """The contents of a specific resource or sub-resource."""

    uri: Annotated[str, Meta(min_length=5, max_length=2**16,
                              pattern="^[a-z0-9A-Z_-]+://.*$")]
    """The URI of this resource."""
    mimeType: Union[str, None] = None
    """The MIME type of this resource, if known."""


class TextResourceContents(ResourceContents, kw_only=True):
    """Text contents of a resource."""
    text: str
    """The text of the item."""


class BlobResourceContents(ResourceContents, kw_only=True):
    """Binary contents of a resource."""
    blob: str
    """A base64-encoded string representing the binary data of the item."""


class TextContent(BaseModel, kw_only=True):
    """Text content for a message."""

    type: Literal["text"] = "text"
    text: str
    """The text content of the message."""
    annotations: Union[Annotations, None] = None


class ImageContent(BaseModel, kw_only=True):
    """Image content for a message."""

    type: Literal["image"] = "image"
    data: str
    """The base64-encoded image data."""
    mimeType: str
    """The MIME type of the image."""
    annotations: Union[Annotations, None] = None


class EmbeddedResource(BaseModel, kw_only=True):
    """
    The contents of a resource, embedded into a prompt or tool call result.

    It is up to the client how best to render embedded resources for the benefit
    of the LLM and/or the user.
    """

    type: Literal["resource"] = "resource"
    resource: Union[TextResourceContents, BlobResourceContents]
    annotations: Union[Annotations, None] = None


class PromptMessage(BaseModel):
    """Describes a message returned as part of a prompt."""

    role: Role
    content: Union[TextContent, ImageContent, EmbeddedResource]


class GetPromptResult(Result, kw_only=True):
    """The server's response to a prompts/get request from the client."""

    description: Union[str, None] = ""
    """An optional description for the prompt."""
    messages: list[PromptMessage]


class EmptyResult(Result):
    """A response that indicates success but carries no data."""


class CallToolResult(Result):
    """The server's response to a tool call."""

    content: list[Union[TextContent, ImageContent, EmbeddedResource]]
    structuredContent: Union[Dict[str, Any], None] = None
    isError: bool = False


class ReadResourceResult(Result):
    """The server's response to a resources/read request from the client."""

    contents: List[Union[TextResourceContents, BlobResourceContents]]