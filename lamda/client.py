# Copyright 2022 rev1si0n (https://github.com/rev1si0n). All rights reserved.
#
# Distributed under MIT license.
# See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
import os
import io
import re
import sys
import copy
import time
import uuid
import json
import base64
import posixpath
import hashlib
import platform
import warnings
import builtins
import logging
import msgpack
# fix protobuf>=4.0/win32, #10158
if sys.platform == "win32":
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
import grpc

import pem as Pem
import collections.abc
# fix pyreadline, py310, Windows
collections.Callable = collections.abc.Callable

from urllib.parse import quote
from collections import defaultdict
from cryptography.fernet import Fernet
from os.path import basename, dirname, expanduser, join as joinpath
from google.protobuf.json_format import MessageToDict, MessageToJson
from grpc_interceptor import ClientInterceptor
from google.protobuf.message import Message
from asn1crypto import pem, x509

try:
    import frida
    _frida_dma = frida.get_device_manager()
except (ImportError, AttributeError):
    _frida_dma = None

from . import __version__
from . types import AttributeDict, BytesIO
from . exceptions import (UnHandledException, DuplicateEntryError,
                          InvalidArgumentError, UiObjectNotFoundException,
                          IllegalStateException, InvalidOperationError)
from . import exceptions

handler = logging.StreamHandler()
logger = logging.getLogger("lamda.client")
formatter = logging.Formatter("%(asctime)s %(process)d %(levelname)7s@%(module)s:%(funcName)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

sys.path.append(joinpath(dirname(__file__)))
sys.path.append(joinpath(dirname(__file__), "rpc"))
# use native resolver to support mDNS
os.environ["GRPC_DNS_RESOLVER"] = "native"

protos, services = grpc.protos_and_services("services.proto")
__all__ = [
                "Corner",
                "Direction",
                "GproxyType",
                "GrantType",
                "Group",
                "CustomOcrBackend",
                "OcrEngine",
                "Key",
                "Keys",
                "KeyCode",
                "KeyCodes",
                "MetaKeyCode",
                "MetaKeyCodes",
                "BaseCryptor",
                "FernetCryptor",
                "OpenVPNAuth",
                "OpenVPNEncryption",
                "OpenVPNKeyDirection",
                "FindImageMethod",
                "FindImageArea",
                "ToastDuration",
                "OpenVPNCipher",
                "OpenVPNProto",
                "Orientation",
                "OpenVPNProfile",
                "GproxyProfile",
                "TouchBuilder",
                "ScriptRuntime",
                "DataEncode",
                "ImePolicy",
                "AudioStreamType",
                "PlayAudioProfile",
                "ApplicationInfo",
                "Selector",
                "TouchWait",
                "TouchMove",
                "TouchDown",
                "TouchUp",
                "TouchAction",
                "TouchSequence",
                "Point",
                "Bound",
                "load_proto",
                "to_dict",
                "Device",
                "logger",
]

def getXY(p):
    return p.x, p.y

def checkArgumentTyp(a, types):
    if not isinstance(a, types):
        raise InvalidArgumentError(a)

def touchSequenceSave(s, fpath):
    return BytesIO(s.SerializeToString()).save(fpath)

def touchSequenceLoad(s, fpath):
    return s.FromString(BytesIO.load(fpath).getvalue())

def touchSequenceIndexer(s, index):
    return s.sequence[index]

def touchSequenceIter(s):
    yield from s.sequence

def touchSequenceAppendAction(s, **kwargs):
    action = TouchAction(**kwargs)
    s.sequence.append(action)

def touchSequenceAppendDown(s, **kwargs):
    touchSequenceAppendAction(s, down=TouchDown(**kwargs))

def touchSequenceAppendMove(s, **kwargs):
    touchSequenceAppendAction(s, move=TouchMove(**kwargs))

def touchSequenceAppendWait(s, **kwargs):
    touchSequenceAppendAction(s, wait=TouchWait(**kwargs))

def touchSequenceAppendUp(s, **kwargs):
    touchSequenceAppendAction(s, up=TouchUp(**kwargs))

def touchActionRealAction(a):
    return getattr(a, a.type)

def touchActionType(a):
    return a.WhichOneof("action")

def touchMoveShiftX(a, offset):
    a.x = a.x + offset
    return a.x

def touchMoveShiftY(a, offset):
    a.y = a.y + offset
    return a.y

def touchWaitShift(w, offset):
    w.wait = w.wait + offset
    return w.wait

def applicationInfoSet(application, app):
    application.CopyFrom(app.info())

def height(b):
    return b.bottom - b.top

def width(b):
    return b.right - b.left

def center(b):
    x = int(b.left + (b.right - b.left)/2)
    y = int(b.top + (b.bottom - b.top)/2)
    return Point(x=x, y=y)

def contain(a, b):
    return all([b.top >= a.top,
                b.left >= a.left,
                b.bottom <= a.bottom,
                b.right <= a.right])

def equal(a, b):
    if not isinstance(b, protos.Bound):
        return False
    return all([b.top == a.top,
                b.left == a.left,
                b.bottom == a.bottom,
                b.right == a.right])

def corner(b, position):
    ca, cb = position.split("-")
    return Point(x=getattr(b, cb),
                 y=getattr(b, ca))

# enum types
Corner = protos.Corner
Direction = protos.Direction
GproxyType = protos.GproxyType
GrantType = protos.GrantType
ScriptRuntime = protos.ScriptRuntime
DataEncode = protos.DataEncode
ImePolicy = protos.ImePolicy

Group = protos.Group
Key = protos.Key
Keys = protos.Key # make an alias

KeyCode = protos.KeyCode
KeyCodes = protos.KeyCode # make an alias

MetaKeyCode = protos.MetaKeyCode
MetaKeyCodes = protos.MetaKeyCode # make an alias

OpenVPNAuth = protos.OpenVPNAuth
OpenVPNEncryption = protos.OpenVPNEncryption
OpenVPNKeyDirection = protos.OpenVPNKeyDirection
OpenVPNCipher = protos.OpenVPNCipher
OpenVPNProto = protos.OpenVPNProto
ToastDuration = protos.ToastDuration
Orientation = protos.Orientation

AudioStreamType = protos.AudioStreamType
PlayAudioProfile = protos.PlayAudioRequest

# proxy request alias
OpenVPNProfile = protos.OpenVPNConfigRequest
GproxyProfile = protos.GproxyConfigRequest

# multitouch
TouchMove = protos.TouchMove
TouchWait = protos.TouchWait
TouchDown = protos.TouchDown
TouchUp = protos.TouchUp

TouchSequence = protos.TouchSequence
TouchAction = protos.TouchAction

ApplicationInfo = protos.ApplicationInfo
# uiautomator types
_Selector = protos.Selector
Bound = protos.Bound
Point = protos.Point

Point.getXY = getXY
ApplicationInfo.set = applicationInfoSet

TouchWait.shift = touchWaitShift

TouchMove.shiftX = touchMoveShiftX
TouchMove.shiftY = touchMoveShiftY

TouchDown.shiftX = touchMoveShiftX
TouchDown.shiftY = touchMoveShiftY

TouchAction.type = property(touchActionType)
TouchAction.action = property(touchActionRealAction)

TouchSequence.load = classmethod(touchSequenceLoad)
TouchSequence.save = touchSequenceSave
TouchSequence.appendAction = touchSequenceAppendAction
TouchSequence.appendDown = touchSequenceAppendDown
TouchSequence.appendMove = touchSequenceAppendMove
TouchSequence.appendWait = touchSequenceAppendWait
TouchSequence.appendUp = touchSequenceAppendUp

TouchSequence.__getitem__ = touchSequenceIndexer
TouchSequence.__iter__ = touchSequenceIter

HookRpcRequest = protos.HookRpcRequest
HookRpcResponse = protos.HookRpcResponse

Bound.width = property(width)
Bound.height = property(height)

FindImageMethod = protos.FindImageMethod
FindImageArea = protos.FindImageArea

Bound.center = center
Bound.corner = corner
Bound.__contains__ = contain
Bound.__eq__ = equal


def load_proto(name):
    """Load related proto files from the package."""
    return grpc.protos_and_services(name)


def to_dict(prot):
    """Convert a proto response to a dict."""
    r = MessageToJson(prot, preserving_proto_field_name=True)
    return json.loads(r)


def Selector(**kwargs):
    """ Selector wrapper """
    fields = set(kwargs.pop("fields", []))
    fields.update(kwargs.keys())
    sel = _Selector(**kwargs, fields=fields)
    return sel


def child_sibling(s, name, **selector):
    s = copy.deepcopy(s)
    s.childOrSibling.append(name)
    s.childOrSiblingSelector.append(Selector(**selector))
    return s


def child(s, **selector):
    return child_sibling(s, "child", **selector)


def sibling(s, **selector):
    return child_sibling(s, "sibling", **selector)


# bind Selector level child sibling
_Selector.child = child
_Selector.sibling = sibling


class CustomOcrBackend(object):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
    def ocr(self, image):
        raise NotImplementedError


class BaseCryptor(object):
    def encrypt(self, data):
        return data
    def decrypt(self, data):
        return data


class BaseServiceStub(object):
    def __init__(self, stub):
        self.stub = stub


class FernetCryptor(BaseCryptor):
    def __init__(self, key=None):
        key = self._get_key(key)
        self.encoder = Fernet(key)
    def encrypt(self, data):
        return self.encoder.encrypt(data)
    def decrypt(self, data):
        return self.encoder.decrypt(data)
    def _get_key(self, key):
        key = (key or "").encode()
        key = hashlib.sha256(key).digest()
        key = base64.b64encode(key)
        return key


class TouchBuilder(object):
    def __init__(self):
        self.s = TouchSequence()
    def down(self, x, y, z=128, contact=0):
        self.s.appendDown(tid=contact, x=x, y=y,
                          pressure=z)
        return self
    def move(self, x, y, z=128, contact=0):
        self.s.appendMove(tid=contact, x=x, y=y,
                          pressure=z)
        return self
    def up(self, contact=0):
        self.s.appendUp(tid=contact)
        return self
    def wait(self, mills):
        self.s.appendWait(wait=mills)
        return self
    def build(self):
        sequence = TouchSequence()
        sequence.CopyFrom(self.s)
        return sequence


class MultiTouchContact:
    def __init__(self, builder, track):
        self.builder = builder
        self.track = track
    def down(self, x, y, z=128):
        self.builder.down(x, y, z=z, contact=self.track)
        return self
    def move(self, x, y, z=128):
        self.builder.move(x, y, z=z, contact=self.track)
        return self
    def wait(self, mills):
        self.builder.wait(mills)
        return self
    def up(self):
        self.builder.up(contact=self.track)
        return self


class MultiTouchOpStub:
    def __init__(self, caller, track=0,
                                builder=None):
        self.stub = caller.stub
        self.builder = builder or TouchBuilder()
        self.track = track
    def contact(self, id):
        return MultiTouchContact(self.builder, id)
    def wait(self, mills):
        self.builder.wait(mills)
    def reset(self):
        self.builder.s.ClearField("sequence")
    def record(self):
        ts = self.stub.recordTouch(protos.Empty())
        self.builder.s.CopyFrom(ts)
    def load(self, fpath):
        ts = self.builder.s.load(fpath)
        self.builder.s.CopyFrom(ts)
    def save(self, fpath):
        return self.builder.s.save(fpath)
    def perform(self, wait=True):
        tas = self.builder.build()
        req = protos.PerformTouchRequest(sequence=tas, wait=wait)
        r = self.stub.performTouch(req)
        return r.value


class ClientLoggingInterceptor(ClientInterceptor):
    def truncate_string(self, s):
        return "{:.1024}...".format(s) if len(s) > 1024 else s
    def intercept(self, function, request, details):
        """
        Log API calls and arguments.
        """
        displayable = isinstance(request, Message)
        args = MessageToDict(request) if displayable else "-"
        args = json.dumps(args, ensure_ascii=False, separators=(",", ":"))
        args = self.truncate_string(args)
        logger.debug("rpc {} {}".format(details.method, args))
        res = function(request, details)
        return res


class ClientSessionMetadataInterceptor(ClientInterceptor):
    def __init__(self, session):
        super(ClientSessionMetadataInterceptor, self).__init__()
        self.session = session
    def intercept(self, function, request, details):
        metadata = {}
        metadata["version"] = __version__
        default = (self.session, platform.node())
        session, name = self.session() if callable(self.session) else default
        metadata["instance"] = session
        metadata["hostname"] = quote(name)
        details = details._replace(metadata=metadata.items())
        return function(request, details)


class GrpcRemoteExceptionInterceptor(ClientInterceptor):
    def intercept(self, function, request, details):
        """
        Handle remote call errors and raise local exceptions.
        """
        res = function(request, details)
        self.raise_remote_exception(res)
        return res

    def remote_exception(self, exception):
        exc = json.loads(exception)
        name, args = exc["name"], exc["args"]
        default = lambda *p: UnHandledException(name, *p)
        clazz = getattr(builtins, name, default)
        clazz = getattr(exceptions, name, clazz)
        return clazz(*args)

    def raise_remote_exception(self, res):
        metadata = dict(res.initial_metadata() or [])
        exception = metadata.get("exception", None)
        if exception != None:
            raise self.remote_exception(exception)


class ObjectUiAutomatorOpStub:
    def __init__(self, caller, selector, display):
        """
        UiAutomator sub-interface that behaves like an instance.
        """
        self.display = display
        self._selector = selector
        self.selector = Selector(**selector)
        self.stub = caller.stub
        self.caller = caller
    def __str__(self):
        selector = ", ".join(["{}={}".format(k, v) \
                        for k, v in self._selector.items()])
        return "Object@{}: {}".format(self.display, selector)
    __repr__ = __str__
    def child(self, **selector):
        """
        Match child nodes within the selector.
        """
        selector = self.selector.child(**selector)
        s = MessageToDict(selector, preserving_proto_field_name=True)
        return self.__class__(self.caller, s, self.display)
    def sibling(self, **selector):
        """
        Match sibling nodes of the selector.
        """
        selector = self.selector.sibling(**selector)
        s = MessageToDict(selector, preserving_proto_field_name=True)
        return self.__class__(self.caller, s, self.display)
    def take_screenshot(self, quality=100):
        """
        Screenshot the selected element.
        """
        req = protos.SelectorTakeScreenshotRequest(display=self.display,
                                                   selector=self.selector,
                                                   quality=quality)
        r = self.stub.selectorTakeScreenshot(req)
        return BytesIO(r.value)
    def screenshot(self, quality=100):
        return self.take_screenshot(quality=quality)
    def get_text(self):
        """
        Get text from the selected input field.
        """
        req = protos.SelectorOnlyRequest(display=self.display,
                                         selector=self.selector)
        r = self.stub.selectorGetText(req)
        return r.value
    def clear_text_field(self):
        """
        Clear text in the selected input field.
        """
        req = protos.SelectorOnlyRequest(display=self.display,
                                         selector=self.selector)
        r = self.stub.selectorClearTextField(req)
        return r.value
    def set_text(self, text):
        """
        Fill text into the selected input field.
        """
        req = protos.SelectorSetTextRequest(display=self.display,
                                            selector=self.selector,
                                            text=text)
        r = self.stub.selectorSetText(req)
        return r.value
    def click(self, corner=Corner.COR_CENTER):
        """
        Click the selected widget.
        """
        req = protos.SelectorClickRequest(display=self.display,
                                          selector=self.selector,
                                          corner=corner)
        r = self.stub.selectorClick(req)
        return r.value
    def click_exists(self, corner=Corner.COR_CENTER):
        """
        Click the selected widget without raising if missing.
        """
        req = protos.SelectorClickRequest(display=self.display,
                                          selector=self.selector,
                                          corner=corner)
        r = self.stub.selectorClickExists(req)
        return r.value
    def long_click(self, corner=Corner.COR_CENTER, timeout=0):
        """
        Long-click the selected widget.
        """
        req = protos.SelectorClickRequest(display=self.display,
                                          selector=self.selector,
                                          corner=corner,
                                          timeout=timeout)
        r = self.stub.selectorLongClick(req)
        return r.value
    def exists(self):
        """
        Check whether the selected widget exists.
        """
        req = protos.SelectorOnlyRequest(display=self.display,
                                         selector=self.selector)
        r = self.stub.selectorExists(req)
        return r.value
    def info(self):
        """
        Get info for the selected widget.
        """
        req = protos.SelectorOnlyRequest(display=self.display,
                                         selector=self.selector)
        return self.stub.selectorObjInfo(req)
    def _chain(self, **kwargs):
        selector = copy.deepcopy(self._selector)
        child_sibling = selector.get("childOrSiblingSelector")
        target = child_sibling[-1] if child_sibling else selector
        target.update(**kwargs)
        fields = set(target.pop("fields", []))
        fields.update(target.keys())
        target["fields"] = fields
        return self.caller(**selector)
    def text(self, txt):
        return self._chain(text=txt)
    def resourceId(self, name):
        return self._chain(resourceId=name)
    def description(self, desc):
        return self._chain(description=desc)
    def packageName(self, name):
        return self._chain(packageName=name)
    def className(self, name):
        return self._chain(className=name)
    def textContains(self, needle):
        return self._chain(textContains=needle)
    def descriptionContains(self, needle):
        return self._chain(descriptionContains=needle)
    def textStartsWith(self, needle):
        return self._chain(textStartsWith=needle)
    def descriptionStartsWith(self, needle):
        return self._chain(descriptionStartsWith=needle)
    def textMatches(self, match):
        return self._chain(textMatches=match)
    def descriptionMatches(self, match):
        return self._chain(descriptionMatches=match)
    def resourceIdMatches(self, match):
        return self._chain(resourceIdMatches=match)
    def packageNameMatches(self, match):
        return self._chain(packageNameMatches=match)
    def classNameMatches(self, match):
        return self._chain(classNameMatches=match)
    def checkable(self, value):
        return self._chain(checkable=value)
    def clickable(self, value):
        return self._chain(clickable=value)
    def focusable(self, value):
        return self._chain(focusable=value)
    def scrollable(self, value):
        return self._chain(scrollable=value)
    def longClickable(self, value):
        return self._chain(longClickable=value)
    def enabled(self, value):
        return self._chain(enabled=value)
    def checked(self, value):
        return self._chain(checked=value)
    def focused(self, value):
        return self._chain(focused=value)
    def selected(self, value):
        return self._chain(selected=value)
    def resultIndex(self, idx):
        return self._chain(resultIndex=idx)
    def instance(self, idx):
        return self._chain(instance=idx)
    def index(self, idx):
        return self._chain(index=idx)
    def __iter__(self):
        """
        Iterate over all elements matching the selector.
        """
        yield from [self.resultIndex(i) for i in \
                            range(self.count())]
    def get(self, idx):
        """
        Get the Nth matching result of the selector.
        """
        return self.resultIndex(idx)
    def count(self):
        """
        Get the number of selected widgets.
        """
        req = protos.SelectorOnlyRequest(display=self.display,
                                         selector=self.selector)
        r = self.stub.selectorCount(req)
        return r.value
    def _set_target_Point(self, req, target):
        req.point.CopyFrom(target)
    def _set_target_Selector(self, req, target):
        req.target.CopyFrom(target)
    def drag_to(self, target, step=32):
        """
        Drag the selected widget to another selector or point.
        """
        checkArgumentTyp(target, (Point, _Selector))
        func = "_set_target_{}".format(target.DESCRIPTOR.name)
        req = protos.SelectorDragToRequest(display=self.display,
                                           selector=self.selector,
                                           step=step)
        getattr(self, func)(req, target)
        r = self.stub.selectorDragTo(req)
        return r.value
    def wait_for_exists(self, timeout):
        """
        Wait for the selected widget to appear.
        """
        req = protos.SelectorWaitRequest(display=self.display,
                                         selector=self.selector,
                                         timeout=timeout)
        r = self.stub.selectorWaitForExists(req)
        return r.value
    def wait_until_gone(self, timeout):
        """
        Wait for the selected widget to disappear.
        """
        req = protos.SelectorWaitRequest(display=self.display,
                                         selector=self.selector,
                                         timeout=timeout)
        r = self.stub.selectorWaitUntilGone(req)
        return r.value
    def swipe(self, direction=Direction.DIR_UP, step=32):
        """
        Swipe on the selected element.
        """
        req = protos.SelectorSwipeRequest(display=self.display,
                                          selector=self.selector,
                                          direction=direction,
                                          step=step)
        r = self.stub.selectorSwipe(req)
        return r.value
    def pinch_in(self, percent, step=16):
        """
        Pinch in.
        """
        req = protos.SelectorPinchRequest(display=self.display,
                                          selector=self.selector,
                                         percent=percent, step=step)
        r = self.stub.selectorPinchIn(req)
        return r.value
    def pinch_out(self, percent, step=16):
        """
        Pinch out.
        """
        req = protos.SelectorPinchRequest(display=self.display,
                                          selector=self.selector,
                                          percent=percent, step=step)
        r = self.stub.selectorPinchOut(req)
        return r.value
    def scroll_to(self, target, is_vertical=True):
        """
        Scroll a scrollable view until the target selector matches.
        """
        checkArgumentTyp(target, _Selector)
        req = protos.SelectorScrollRequest(display=self.display,
                                           selector=self.selector,
                                           vertical=is_vertical,
                                           target=target)
        r = self.stub.selectorScrollTo(req)
        return r.value
    def _fling_forward(self, is_vertical=True):
        req = protos.SelectorFlingRequest(display=self.display,
                                          selector=self.selector,
                                          vertical=is_vertical)
        r = self.stub.selectorFlingForward(req)
        return r.value
    def _fling_backward(self, is_vertical=True):
        req = protos.SelectorFlingRequest(display=self.display,
                                          selector=self.selector,
                                          vertical=is_vertical)
        r = self.stub.selectorFlingBackward(req)
        return r.value
    def _fling_to_end(self, max_swipes, is_vertical=True):
        req = protos.SelectorFlingRequest(display=self.display,
                                          selector=self.selector,
                                          maxSwipes=max_swipes,
                                          vertical=is_vertical)
        r = self.stub.selectorFlingToEnd(req)
        return r.value
    def _fling_to_beginning(self, max_swipes, is_vertical=True):
        req = protos.SelectorFlingRequest(display=self.display,
                                          selector=self.selector,
                                          maxSwipes=max_swipes,
                                          vertical=is_vertical)
        r = self.stub.selectorFlingToBeginning(req)
        return r.value
    def fling_from_top_to_bottom(self):
        """
        Perform one top-to-bottom reading swipe on the selected element.
        """
        return self._fling_backward(is_vertical=True)
    def fling_from_bottom_to_top(self):
        """
        Perform one bottom-to-top reading swipe on the selected element.
        """
        return self._fling_forward(is_vertical=True)
    def fling_from_left_to_right(self):
        """
        Perform one left-to-right reading swipe on the selected element.
        """
        return self._fling_backward(is_vertical=False)
    def fling_from_right_to_left(self):
        """
        Perform one right-to-left reading swipe on the selected element.
        """
        return self._fling_forward(is_vertical=False)
    def fling_from_top_to_bottom_to_end(self, max_swipes):
        """
        Swipe top-to-bottom until scrolling stops or max_swipes is reached.
        """
        return self._fling_to_beginning(max_swipes, is_vertical=True)
    def fling_from_bottom_to_top_to_end(self, max_swipes):
        """
        Swipe bottom-to-top until scrolling stops or max_swipes is reached.
        """
        return self._fling_to_end(max_swipes, is_vertical=True)
    def fling_from_left_to_right_to_end(self, max_swipes):
        """
        Swipe left-to-right until scrolling stops or max_swipes is reached.
        """
        return self._fling_to_beginning(max_swipes, is_vertical=False)
    def fling_from_right_to_left_to_end(self, max_swipes):
        """
        Swipe right-to-left until scrolling stops or max_swipes is reached.
        """
        return self._fling_to_end(max_swipes, is_vertical=False)
    def _scroll_forward(self, step, is_vertical=True):
        req = protos.SelectorScrollRequest(display=self.display,
                                           selector=self.selector,
                                           vertical=is_vertical,
                                           step=step)
        r = self.stub.selectorScrollForward(req)
        return r.value
    def _scroll_backward(self, step, is_vertical=True):
        req = protos.SelectorScrollRequest(display=self.display,
                                           selector=self.selector,
                                           vertical=is_vertical,
                                           step=step)
        r = self.stub.selectorScrollBackward(req)
        return r.value
    def _scroll_to_end(self, max_swipes, step, is_vertical=True):
        req = protos.SelectorScrollRequest(display=self.display,
                                           selector=self.selector,
                                           maxSwipes=max_swipes,
                                           vertical=is_vertical,
                                           step=step)
        r = self.stub.selectorScrollToEnd(req)
        return r.value
    def _scroll_to_beginning(self, max_swipes, step, is_vertical=True):
        req = protos.SelectorScrollRequest(display=self.display,
                                           selector=self.selector,
                                           maxSwipes=max_swipes,
                                           vertical=is_vertical,
                                           step=step)
        r = self.stub.selectorScrollToBeginning(req)
        return r.value
    def scroll_from_top_to_bottom(self, step):
        """
        Perform a normal top-to-bottom swipe on the selected element.
        """
        return self._scroll_backward(step, is_vertical=True)
    def scroll_from_bottom_to_top(self, step):
        """
        Perform a normal bottom-to-top swipe on the selected element.
        """
        return self._scroll_forward(step, is_vertical=True)
    def scroll_from_left_to_right(self, step):
        """
        Perform a normal left-to-right swipe on the selected element.
        """
        return self._scroll_backward(step, is_vertical=False)
    def scroll_from_right_to_left(self, step):
        """
        Perform a normal right-to-left swipe on the selected element.
        """
        return self._scroll_forward(step, is_vertical=False)
    def scroll_from_top_to_bottom_to_end(self, max_swipes, step):
        """
        Repeat normal top-to-bottom swipes until scrolling stops or max_swipes is reached.
        """
        return self._scroll_to_beginning(max_swipes, step, is_vertical=True)
    def scroll_from_bottom_to_top_to_end(self, max_swipes, step):
        """
        Repeat normal bottom-to-top swipes until scrolling stops or max_swipes is reached.
        """
        return self._scroll_to_end(max_swipes, step, is_vertical=True)
    def scroll_from_left_to_right_to_end(self, max_swipes, step):
        """
        Repeat normal left-to-right swipes until scrolling stops or max_swipes is reached.
        """
        return self._scroll_to_beginning(max_swipes, step, is_vertical=False)
    def scroll_from_right_to_left_to_end(self, max_swipes, step):
        """
        Repeat normal right-to-left swipes until scrolling stops or max_swipes is reached.
        """
        return self._scroll_to_end(max_swipes, step, is_vertical=False)


class UiAutomatorStub(BaseServiceStub):
    def __init__(self, *args, display=0, **kwargs):
        self.display = display
        super(UiAutomatorStub, self).__init__(*args, **kwargs)
    def device_info(self):
        """
        Get device and display info.
        """
        r = self.stub.deviceInfo(protos.Empty())
        return r
    def set_watcher_loop_enabled(self, enabled):
        """
        Enable or disable watcher UI checks on the device.
        """
        req = protos.WatcherControlRequest(display=self.display,
                                           enable=enabled)
        r = self.stub.setWatcherLoopEnabled(req)
        return r.value
    def get_watcher_loop_enabled(self):
        """
        Check whether watcher UI checks are enabled.
        """
        req = protos.WatcherControlRequest(display=self.display)
        r = self.stub.getWatcherLoopEnabled(req)
        return r.value
    def get_watcher_triggered_count(self, name):
        """
        Get how many times this watcher was triggered.
        """
        req = protos.WatcherControlRequest(display=self.display,
                                           name=name)
        r = self.stub.getWatcherTriggeredCount(req)
        return r.value
    def reset_watcher_triggered_count(self, name):
        """
        Reset this watcher's trigger count to 0.
        """
        req = protos.WatcherControlRequest(display=self.display,
                                           name=name)
        r = self.stub.resetWatcherTriggeredCount(req)
        return r.value
    def get_enabled_watchers(self):
        """
        Get enabled watchers applied on the system.
        """
        req = protos.WatcherControlRequest(display=self.display)
        return self.stub.getEnabledWatchers(req).watchers
    def get_watchers(self):
        """
        Get registered watchers applied on the system.
        """
        req = protos.WatcherControlRequest(display=self.display)
        return self.stub.getWatchers(req).watchers
    def remove_all_watchers(self):
        req = protos.WatcherControlRequest(display=self.display)
        r = self.stub.removeAllWatchers(req)
        return r.value
    def register_click_target_selector_watcher(self, name, conditions,
                                               target):
        """
        Register a watcher that clicks a selector when matched.
        """
        req = protos.WatcherControlRequest(display=self.display,
                                           name=name, selectors=conditions,
                                           target=target)
        r = self.stub.registerClickUiObjectWatcher(req)
        return r.value
    def register_press_key_watcher(self, name, conditions, key):
        """
        Register a watcher that presses a key when matched.
        """
        req = protos.WatcherControlRequest(display=self.display,
                                           name=name, selectors=conditions,
                                           key=key)
        r = self.stub.registerPressKeysWatcher(req)
        return r.value
    def register_none_op_watcher(self, name, conditions):
        """
        Register a watcher that does nothing when matched.
        """
        req = protos.WatcherControlRequest(display=self.display,
                                           name=name, selectors=conditions)
        r = self.stub.registerNoneOpWatcher(req)
        return r.value
    def set_watcher_enabled(self, name, enable):
        """
        Enable or disable this watcher.
        """
        req = protos.WatcherControlRequest(display=self.display,
                                           name=name, enable=enable)
        r = self.stub.setWatcherEnable(req)
        return r.value
    def get_watcher_enabled(self, name):
        """
        Check whether this watcher is enabled.
        """
        req = protos.WatcherControlRequest(display=self.display,
                                           name=name)
        r = self.stub.getWatcherEnable(req)
        return r.value
    def get_last_toast(self):
        """
        Get the last toast message.
        """
        r = self.stub.getLastToast(protos.Empty())
        return r
    def remove_watcher(self, name):
        """
        Remove a watcher.
        """
        req = protos.WatcherControlRequest(display=self.display,
                                           name=name)
        r = self.stub.removeWatcher(req)
        return r.value
    def long_click(self, point, timeout=0):
        req = protos.ClickPointRequest(display=self.display,
                                       point=point,
                                       timeout=timeout)
        r = self.stub.pointLongClick(req)
        return r.value
    def click(self, point):
        """
        Click a point on the screen.
        """
        req = protos.ClickPointRequest(display=self.display,
                                       point=point)
        r = self.stub.click(req)
        return r.value
    def drag(self, A, B, step=32):
        """
        Drag from point A to point B.
        """
        req = protos.DragPointRequest(display=self.display,
                                      A=A, B=B, step=step)
        r = self.stub.drag(req)
        return r.value
    def swipe(self, A, B, step=32):
        """
        Swipe from point A to point B.
        """
        req = protos.SwipePointRequest(display=self.display,
                                       A=A, B=B, step=step)
        r = self.stub.swipe(req)
        return r.value
    def swipe_points(self, *points, step=32):
        """
        Swipe across a sequence of points.
        """
        req = protos.SwipePointsRequest(display=self.display,
                                        points=points, step=step)
        r = self.stub.swipePoints(req)
        return r.value
    def open_notification(self):
        """
        Open the notification shade.
        """
        r = self.stub.openNotification(protos.Empty())
        return r.value
    def open_quick_settings(self):
        """
        Open the quick settings shade.
        """
        r = self.stub.openQuickSettings(protos.Empty())
        return r.value
    def wake_up(self):
        """
        Wake the device.
        """
        r = self.stub.wakeUp(protos.Empty())
        return r.value
    def sleep(self):
        """
        Sleep the device.
        """
        r = self.stub.sleep(protos.Empty())
        return r.value
    def is_screen_on(self):
        """
        Check whether the device is awake.
        """
        r = self.stub.isScreenOn(protos.Empty())
        return r.value
    def is_screen_locked(self):
        """
        Check whether the screen is locked.
        """
        r = self.stub.isScreenLocked(protos.Empty())
        return r.value
    def set_clipboard(self, text):
        """
        Set clipboard text.
        """
        req = protos.ClipboardRequest(ID=str(uuid.uuid4()), value=text)
        r = self.stub.setClipboard(req)
        return r.value
    def get_clipboard(self):
        """
        Get clipboard text before Android 10.
        """
        r = self.stub.getClipboard(protos.Empty())
        return r.value
    def _set_target_Area(self, req, area):
        req.area = area
    def _set_target_Bound(self, req, bound):
        req.bound.CopyFrom(bound)
    def find_similar_image(self, data, threshold=0.0, distance=250,
                           scale=1.0, area=FindImageArea.FIA_WHOLE_SCREEN,
                           method=FindImageMethod.FIM_TEMPLATE):
        """
        Find similar image positions on screen from a target image.
        """
        req = protos.FindImageRequest()
        checkArgumentTyp(area, (Bound, int))
        name = getattr(getattr(area, "DESCRIPTOR", None),
                                         "name", "Area")
        func = "_set_target_{}".format(name)
        getattr(self, func)(req, area)
        req.method = method
        req.display = self.display
        req.distance = distance
        req.threshold = threshold
        req.scale = scale
        req.partial = data
        r = self.stub.findSimilarImage(req)
        return r.bounds
    def freeze_rotation(self, freeze=True):
        """
        Lock screen rotation.
        """
        req = protos.FreezeRotationRequest(freeze=freeze,
                                           display=self.display)
        r = self.stub.freezeRotation(req)
        return r.value
    def set_orientation(self, orien=Orientation.ORIEN_NATURE):
        """
        Set screen rotation.
        """
        req = protos.OrientationRequest(orientation=orien,
                                        display=self.display)
        r = self.stub.setOrientation(req)
        return r.value
    def press_key(self, key):
        """
        Press a hardware key such as HOME, VOLUME, or BACK.
        """
        req = protos.PressKeyRequest(display=self.display, key=key)
        r = self.stub.pressKey(req)
        return r.value
    def press_keycode(self, code, meta=0):
        """
        Press an undefined key by integer keycode.
        ref: https://developer.android.com/reference/android/view/KeyEvent
        """
        req = protos.PressKeyRequest(display=self.display,
                                     code=code, meta=meta)
        r = self.stub.pressKeyCode(req)
        return r.value
    def take_screenshot(self, quality, bound=None):
        """
        Capture a full-screen screenshot.
        """
        req = protos.TakeScreenshotRequest(display=self.display,
                                           quality=quality,
                                           bound=bound)
        r = self.stub.takeScreenshot(req)
        return BytesIO(r.value)
    def screenshot(self, quality, bound=None):
        return self.take_screenshot(quality, bound=bound)
    def dump_window_hierarchy(self, compressed=False):
        """
        Get the current UI layout XML.
        """
        req = protos.DumpWindowHierarchyRequest(display=self.display,
                                                compressed=compressed)
        r = self.stub.dumpWindowHierarchy(req)
        return BytesIO(r.value)
    def wait_for_idle(self, timeout):
        """
        Wait until the current screen is idle.
        """
        r = self.stub.waitForIdle(protos.Integer(value=timeout))
        return r.value
    def __call__(self, **kwargs):
        return ObjectUiAutomatorOpStub(self, kwargs,
                                       self.display)


class VirtualDisplayStub(UiAutomatorStub):
    def __init__(self, *args, display=0, device=None, **kwargs):
        self._warning_global = True
        super(VirtualDisplayStub, self).__init__(*args,
                                    display=display, **kwargs)
        self.device = device
    def _create_virtual_display(self, width=None, height=None,
                                    densityDpi=None, name=None):
        default = self.stub.getDisplayInfo(protos.Integer(value=0))
        req = protos.CreateVirtualDisplayRequest(densityDpi=densityDpi or default.densityDpi,
                                                 width=width or default.width,
                                                 height=height or default.height)
        req.name = name or uuid.uuid4().hex[::6]
        return self.stub.createVirtualDisplay(req).value
    def _list_virtual_displays(self):
        return self.stub.listAllDisplays(protos.Empty()).displays
    def _release_virtual_display(self, display):
        req = protos.Integer(value=display)
        return self.stub.releaseVirtualDisplay(req).value
    def disable_global_method_warning(self):
        self._warning_global = False
    # Application compat
    def enumerate_installed_apps(self, user=0):
        self._warning_global_use("enumerate_installed_apps")
        return self.device.proxy("Application", display=self.display).enumerate_installed_apps(user=user)
    def enumerate_running_processes(self):
        self._warning_global_use("enumerate_running_processes")
        return self.device.proxy("Application", display=self.display).enumerate_running_processes()
    def current_application(self):
        return self.device.proxy("Application", display=self.display).current_application()
    def start_activity(self, **activity):
        return self.device.proxy("Application", display=self.display).start_activity(**activity)
    def get_application_by_name(self, name):
        return self.device.proxy("Application", display=self.display).get_application_by_name(name)
    def application(self, applicationId, user=0):
        return self.device.proxy("Application", display=self.display)(
                                             applicationId, user=user)
    # Display misc
    def release_virtual_display(self):
        return self._release_virtual_display(self.display)
    def get_display_info(self):
        return self.stub.getDisplayInfo(protos.Integer(value=self.display))
    def set_display_ime_policy(self, policy):
        req = protos.ImePolicyRequest(display=self.display, policy=policy)
        return self.stub.setDisplayImePolicy(req).value
    def get_display_ime_policy(self):
        req = protos.Integer(value=self.display)
        return self.stub.getDisplayImePolicy(req).value
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self._release_virtual_display(self.display)
    def ocr(self, index=0, **kwargs):
        return self.device.ocr(index=index, display=self.display,
                                                **kwargs)
    # Global-effect method overriding
    def device_info(self):
        self._warning_global_use("device_info")
        return super(VirtualDisplayStub, self).device_info()
    def get_last_toast(self):
        self._warning_global_use("get_last_toast")
        return super(VirtualDisplayStub, self).get_last_toast()
    def open_notification(self):
        self._warning_global_use("open_notification")
        return super(VirtualDisplayStub, self).open_notification()
    def open_quick_settings(self):
        self._warning_global_use("open_quick_settings")
        return super(VirtualDisplayStub, self).open_quick_settings()
    def wake_up(self):
        self._warning_global_use("wake_up")
        return super(VirtualDisplayStub, self).wake_up()
    def sleep(self):
        self._warning_global_use("sleep")
        return super(VirtualDisplayStub, self).sleep()
    def is_screen_on(self):
        self._warning_global_use("is_screen_on")
        return super(VirtualDisplayStub, self).is_screen_on()
    def is_screen_locked(self):
        self._warning_global_use("is_screen_locked")
        return super(VirtualDisplayStub, self).is_screen_locked()
    def set_clipboard(self, text):
        self._warning_global_use("set_clipboard")
        return super(VirtualDisplayStub, self).set_clipboard(text)
    def get_clipboard(self):
        self._warning_global_use("get_clipboard")
        return super(VirtualDisplayStub, self).get_clipboard()
    def wait_for_idle(self, timeout):
        self._warning_global_use("wait_for_idle")
        return super(VirtualDisplayStub, self).wait_for_idle(timeout)
    def _warning_global_use(self, method):
        if self._warning_global:
            logger.warning(f"Method '{method}' cannot be applied specifically to a virtual screen "
                            "as it has a global effect. Please use the corresponding global method, or call "\
                            "disable_global_method_warning() to suppress this warning.")


class AppScriptRpcInterface(object):
    def __init__(self, stub, application,
                                    name):
        self.application = application
        self.stub = stub
        self.name = name
    def __str__(self):
        return "{}:Script:{}".format(self.application,
                                            self.name)
    __repr__ = __str__
    def __call__(self, *args):
        call_args = dict()
        call_args["method"] = self.name
        call_args["args"] = args
        req = HookRpcRequest()
        req.package = self.application.applicationId
        req.user = self.application.user
        req.callinfo = json.dumps(call_args)
        result = self.stub.callScript(req)
        data = json.loads(result.callresult)
        return data


class ApplicationOpStub:
    def __init__(self, stub, applicationId, user=0, display=0):
        """
        Application sub-interface that behaves like an instance.
        """
        self.user = user
        self.display = display
        self.applicationId = applicationId
        self.stub = stub
    def __str__(self):
        return "Application:{}:{}@{}".format(self.applicationId,
                                        self.user, self.display)
    __repr__ = __str__
    def is_foreground(self):
        """
        Check whether the app is in the foreground.
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        req.display = self.display
        r = self.stub.isForeground(req)
        return r.value
    def permissions(self):
        """
        Get all app permissions.
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.getPermissions(req)
        return r.permissions
    def grant(self, permission, mode=GrantType.GRANT_ALLOW):
        """
        Grant a runtime permission to the app.
        """
        req = protos.ApplicationRequest(name=self.applicationId,
                                        permission=permission,
                                        mode=mode)
        req.user = self.user
        r = self.stub.grantPermission(req)
        return r.value
    def revoke(self, permission):
        """
        Revoke a runtime permission from the app.
        """
        req = protos.ApplicationRequest(name=self.applicationId,
                                        permission=permission)
        req.user = self.user
        r = self.stub.revokePermission(req)
        return r.value
    def query_launch_activity(self):
        """
        Get launch activity info.
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.queryLaunchActivity(req)
        return to_dict(r)
    def is_permission_granted(self, permission):
        """
        Check whether the app has a runtime permission.
        """
        req = protos.ApplicationRequest(name=self.applicationId,
                                        permission=permission)
        req.user = self.user
        r = self.stub.isPermissionGranted(req)
        return r.value
    def clear_cache(self):
        """
        Clear app cache data.
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.deleteApplicationCache(req)
        return r.value
    def reset(self):
        """
        Clear all app data.
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.resetApplicationData(req)
        return r.value
    def start(self):
        """
        Start the app.
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        req.display = self.display
        r = self.stub.startApplication(req)
        return r.value
    def stop(self):
        """
        Stop the app.
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.stopApplication(req)
        return r.value
    def info(self):
        """
        Get app info.
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.applicationInfo(req)
        return r
    def uninstall(self):
        """
        Uninstall the app (always returns true).
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.uninstallApplication(req)
        return r.value
    def enable(self):
        """
        Enable the app.
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.enableApplication(req)
        return r.value
    def disable(self):
        """
        Disable the app.
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.disableApplication(req)
        return r.value
    def is_installed(self):
        """
        Check whether the app is installed.
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.isInstalled(req)
        return r.value
    def attach_script(self, script, runtime=ScriptRuntime.RUNTIME_QJS,
                                                    emit="",
                                process=None,
                                encode=DataEncode.DATA_ENCODE_NONE,
                                spawn=False,
                                standup=5):
        """
        Inject a persistent hook script into the app.
        """
        s = isinstance(script, str)
        script = script.encode() if s else script
        req = protos.HookRequest()
        req.package     = self.applicationId
        req.script      = script
        req.runtime     = runtime
        req.standup     = standup
        req.spawn       = spawn
        req.destination = emit
        req.encode      = encode
        req.user        = self.user
        req.process     = process or ""
        r = self.stub.attachScript(req)
        return r.value
    def detach_script(self):
        """
        Remove the injected hook script.
        """
        req = protos.HookRequest()
        req.package     = self.applicationId
        req.user        = self.user
        r = self.stub.detachScript(req)
        return r.value
    def is_attached_script(self):
        """
        Check whether a hook script is injected into this app.
        """
        req = protos.HookRequest()
        req.package     = self.applicationId
        req.user        = self.user
        r = self.stub.isScriptAttached(req)
        return r.value
    def is_script_alive(self):
        """
        Check whether the hook script in this app is healthy.
        """
        req = protos.HookRequest()
        req.package     = self.applicationId
        req.user        = self.user
        r = self.stub.isScriptAlive(req)
        return r.value
    def __getattr__(self, name):
        """
        Call an exported method from the injected hook script.
        """
        return AppScriptRpcInterface(self.stub, self,
                                            name)


class ApplicationInstallSession(object):
    def __init__(self, device, session, tmpdir=None):
        self.tmpdir  = tmpdir or "/data/local/tmp"
        self.stub    = device.proxy("Application").stub
        self.device  = device
        self.session = session
    def _write(self, path, name=None, delete=False):
        req = protos.InstallSessionWriteRequest(session=self.session,
                                                path=path, name=name,
                                                delete=delete)
        return self.stub.installSessionWrite(req)
    def write(self, path, name=None):
        suffix = uuid.uuid4().hex[::4]
        dest = posixpath.join(self.tmpdir, "{}_{}.apk".format(
                                         self.session, suffix))
        info = self.device.upload_file(path, dest)
        self.device.file_chmod(info.path, mode=0o777)
        return self._write(info.path, name, True)
    def commit(self, wait=True, timeout=0):
        req = protos.InstallSessionCommitRequest(session=self.session,
                                                 wait=wait, timeout=timeout)
        return self.stub.installSessionCommit(req)
    def abandon(self):
        req = protos.InstallSessionAbandonRequest(session=self.session)
        return self.stub.installSessionAbandon(req).value
    def status(self):
        req = protos.InstallSessionQueryRequest(session=self.session)
        return self.stub.installSessionQuery(req)


class ApplicationStub(BaseServiceStub):
    def __init__(self, *args, display=0, device=None, **kwargs):
        super(ApplicationStub, self).__init__(*args, **kwargs)
        self.display = display
        self.device  = device
    def current_application(self):
        """
        Get the current foreground app info.
        """
        req = protos.Integer(value=self.display)
        top = self.stub.currentApplication(req)
        app = self.__call__(top.packageName, user=top.user)
        app.activity = top.activity
        return app
    def get_application_by_name(self, name, user=0):
        req = protos.String(value=name)
        r = self.stub.getIdentifierByLabel(req)
        app = self.__call__(r.value, user=user)
        return app
    def enumerate_running_processes(self):
        """
        List all running Android app processes.
        """
        r = self.stub.enumerateRunningProcesses(protos.Empty())
        return r.processes
    def enumerate_installed_apps(self, user=0):
        """
        List application IDs of all installed apps.
        """
        req = protos.Integer(value=user)
        r = self.stub.enumerateInstalledApps(req)
        return r.applications
    def _update_extras(self, msg, data):
        types = {bool: "bool_value", int: "int64_value",
                                                float: "double_value",
                                                str: "string_value",
                                                type(None): "null_value"}
        for k, v in data.items(): setattr(msg.fields[k], types[type(v)],
                                                0 if v is None else v)
    def start_activity(self, **activity):
        """
        Start an activity (always returns True).
        """
        activity.setdefault("extras", {})
        extras = activity.pop("extras")
        req = protos.ApplicationActivityRequest(**activity)
        self._update_extras(req.extras, extras)
        req.display = self.display
        r = self.stub.startActivity(req)
        return r.value
    def _create_install_session(self, user=0, size_bytes=0, package=None,
                               installer_package_name=None, dont_kill_app=False,
        replace_existing=True, allow_test=False, request_downgrade=False,
        grant_runtime_permissions=False, tmpdir=None):
        req = protos.InstallSessionCreateRequest(user=user)
        req.sizeBytes = size_bytes
        req.dontKillApp = dont_kill_app
        req.requestDowngrade = request_downgrade
        req.grantRuntimePermissions = grant_runtime_permissions
        req.replaceExisting = replace_existing
        req.allowTest = allow_test
        req.installerPackageName = installer_package_name or ""
        req.package = package or ""
        info = self.stub.installSessionCreate(req)
        params = dict(device=self.device, session=info.session,
                                               tmpdir=tmpdir)
        return ApplicationInstallSession(**params)
    def __call__(self, applicationId, user=0):
        return ApplicationOpStub(self.stub, applicationId,
                                    user=user, display=self.display)


class StorageOpStub:
    # Helpers for container value serialization.
    def _decrypt(self, data):
        return self.cryptor.decrypt(data)
    def _encrypt(self, data):
        return self.cryptor.encrypt(data)
    def _unpack(self, value):
        return msgpack.loads(self._decrypt(value))
    def _pack(self, value):
        return self._encrypt(msgpack.dumps(value))
    # This interface may not be portable across languages.
    def __init__(self, stub, name, cryptor=None):
        self.cryptor = cryptor
        self.name = name
        self.stub = stub
    def delete(self, key):
        """
        Delete a key.
        """
        req = protos.StorageRequest(key=key)
        req.container = self.name
        res = self.stub.delete(req)
        return res.value
    def exists(self, key):
        """
        Check whether a key exists.
        """
        req = protos.StorageRequest(key=key)
        req.container = self.name
        res = self.stub.exists(req)
        return res.value
    def get(self, key, default=None):
        """
        Get the value for a key.
        """
        req = protos.StorageRequest(key=key)
        req.container = self.name
        val = self.stub.get(req).value
        res = self._unpack(val) if val else default
        return res
    def set(self, key, value):
        """
        Set the value for a key.
        """
        value = self._pack(value)
        req = protos.StorageRequest(key=key, value=value)
        req.container = self.name
        res = self.stub.set(req)
        return res.value
    def setex(self, key, value, ttl):
        """
        Set a key value and expire it after TTL seconds.
        """
        value = self._pack(value)
        req = protos.StorageRequest(key=key, value=value)
        req.container = self.name
        req.ttl = ttl
        res = self.stub.setex(req)
        return res.value
    def setnx(self, key, value):
        """
        Set the value for a key only if it does not exist.
        """
        value = self._pack(value)
        req = protos.StorageRequest(key=key, value=value)
        req.container = self.name
        res = self.stub.setnx(req)
        return res.value
    def expire(self, key, ttl):
        """
        Set a key to expire after TTL seconds.
        """
        req = protos.StorageRequest(key=key, ttl=ttl)
        req.container = self.name
        res = self.stub.expire(req)
        return res.value
    def ttl(self, key):
        """
        Get the TTL for a key.
        """
        req = protos.StorageRequest(key=key)
        req.container = self.name
        res = self.stub.ttl(req)
        return res.value


class StorageStub(BaseServiceStub):
    def clear(self):
        """
        Delete all storage containers.
        """
        r = self.stub.clearAll(protos.Empty())
        return r.value
    def use(self, name, cryptor=BaseCryptor, **kwargs):
        """
        Use a storage container.
        """
        return StorageOpStub(self.stub, name, cryptor(**kwargs))
    def remove(self, name):
        """
        Delete a storage container.
        """
        req = protos.String(value=name)
        r = self.stub.clearContainer(req)
        return r.value


class UtilStub(BaseServiceStub):
    def _get_file_content(self, certfile):
        with open(certfile, "rb") as fd:
            return fd.read()
    def is_ca_certificate_installed(self, certfile):
        """
        Install a system certificate for MITM.
        """
        data = self._get_file_content(certfile)
        req = protos.CertifiRequest(cert=data)
        r = self.stub.isCACertificateInstalled(req)
        return r.value
    def install_ca_certificate(self, certfile):
        """
        Install a system certificate for MITM.
        """
        data = self._get_file_content(certfile)
        req = protos.CertifiRequest(cert=data)
        r = self.stub.installCACertificate(req)
        return r.value
    def uninstall_ca_certificate(self, certfile):
        """
        Remove a system certificate used for MITM.
        """
        data = self._get_file_content(certfile)
        req = protos.CertifiRequest(cert=data)
        r = self.stub.uninstallCACertificate(req)
        return r.value
    def reboot(self):
        """
        Reboot the host device.
        """
        r = self.stub.reboot(protos.Empty())
        return r.value
    def shutdown(self):
        """
        Shut down the host device.
        """
        r = self.stub.shutdown(protos.Empty())
        return r.value
    def reload(self, clean=False):
        """
        Reload the server running on the device.
        """
        req = protos.Boolean(value=clean)
        r = self.stub.reload(req)
        return r.value
    def exit(self):
        """
        Exit the server running on the device.
        """
        r = self.stub.exit(protos.Empty())
        return r.value
    def beep(self):
        """
        Play a beep to help locate the device.
        """
        r = self.stub.beepBeep(protos.Empty())
        return r.value
    def play_audio(self, file, type=AudioStreamType.AST_SYSTEM,
                                        loop=1, interval=0):
        """
        Play a WAV file.
        """
        profile = PlayAudioProfile()
        profile.file = file
        profile.type = type
        profile.loop = loop
        profile.interval = interval
        r = self.stub.playAudio(profile)
        return r.value
    def show_toast(self, text, duration=ToastDuration.TD_SHORT):
        """
        Show a toast message at the bottom of the screen.
        """
        req = protos.ShowToastRequest(text=text, duration=duration)
        r = self.stub.showToast(req)
        return r.value
    def setprop(self, name, value):
        """
        Set a system property, including read-only ro.xx values.
        """
        req = protos.SetPropRequest(name=name, value=value)
        r = self.stub.setProp(req)
        return r.value
    def getprop(self, name):
        """
        Get a system property.
        """
        req = protos.String(value=name)
        r = self.stub.getProp(req)
        return r.value
    def server_info(self):
        """
        Get server ID, version, and related info.
        """
        r = self.stub.serverInfo(protos.Empty())
        return r
    def hex_patch(self, pattern, replacement, path,
                                        maxreplace=-1,
                                        dryrun=False):
        """
        Replace bytes in a file on the device.
        """
        req = protos.HexPatchRequest()
        req.pattern     = pattern
        req.replacement = replacement
        req.path        = path
        req.maxreplace  = maxreplace
        req.dryrun      = dryrun
        return self.stub.hexPatch(req)


class DebugStub(BaseServiceStub):
    def _read_pubkey(self, pubkey):
        with open(pubkey, "rb") as fd:
            return fd.read()
    def install_adb_pubkey(self, pubkey):
        """
        Add a public key to the built-in adb service.
        """
        req = protos.ADBDConfigRequest()
        req.adb_pubkey = self._read_pubkey(pubkey)
        r = self.stub.installADBPubKey(req)
        return r.value
    def uninstall_adb_pubkey(self, pubkey):
        """
        Remove a public key from the built-in adb service.
        """
        req = protos.ADBDConfigRequest()
        req.adb_pubkey = self._read_pubkey(pubkey)
        r = self.stub.uninstallADBPubKey(req)
        return r.value
    def is_android_debug_bridge_running(self):
        """
        Check whether the remote adb daemon is running.
        """
        r = self.stub.isAndroidDebugBridgeRunning(protos.Empty())
        return r.value
    def start_android_debug_bridge(self):
        """
        Start the built-in adbd.
        """
        r = self.stub.startAndroidDebugBridge(protos.Empty())
        return r.value
    def stop_android_debug_bridge(self):
        """
        Stop the built-in adb daemon.
        """
        r = self.stub.stopAndroidDebugBridge(protos.Empty())
        return r.value


class SettingsStub(BaseServiceStub):
    def _put(self, group, name, value):
        req = protos.SettingsRequest(group=group, name=name,
                                            value=value)
        r = self.stub.putSettings(req)
        return r.value
    def _get(self, group, name):
        req = protos.SettingsRequest(group=group,name=name)
        r = self.stub.getSettings(req)
        return r.value
    def get_system(self, name):
        """
        Equivalent to settings get system xxxx.
        """
        return self._get(Group.GROUP_SYSTEM, name)
    def put_system(self, name, value):
        """
        Equivalent to settings put system xxxx xxxx.
        """
        return self._put(Group.GROUP_SYSTEM, name, value)
    def get_global(self, name):
        """
        Equivalent to settings get global xxxx.
        """
        return self._get(Group.GROUP_GLOBAL, name)
    def put_global(self, name, value):
        """
        Equivalent to settings put global xxxx xxxx.
        """
        return self._put(Group.GROUP_GLOBAL, name, value)
    def get_secure(self, name):
        """
        Equivalent to settings get secure xxxx.
        """
        return self._get(Group.GROUP_SECURE, name)
    def put_secure(self, name, value):
        """
        Equivalent to settings put secure xxxx xxxx.
        """
        return self._put(Group.GROUP_SECURE, name, value)


class ShellStub(BaseServiceStub):
    def execute_script(self, script, alias=None,
                                    timeout=60):
        """
        Run a script in the foreground.
        """
        req = protos.ShellRequest(name=alias, script=script,
                                            timeout=timeout)
        r = self.stub.executeForeground(req)
        return r
    def execute_background_script(self, script, alias=None):
        """
        Run a script in the background.
        """
        req = protos.ShellRequest(name=alias, script=script)
        r = self.stub.executeBackground(req)
        return r.tid
    def is_background_script_finished(self, tid):
        """
        Check whether the background script has finished.
        """
        req = protos.ShellTask(tid=tid)
        r = self.stub.isBackgroundFinished(req)
        return r.value
    def kill_background_script(self, tid):
        """
        Force-stop the background script.
        """
        req = protos.ShellTask(tid=tid)
        r = self.stub.killBackground(req)
        return r.value


class StatusStub(BaseServiceStub):
    def get_boot_time(self):
        """
        Get the device boot time as a Unix timestamp.
        """
        r = self.stub.getBootTime(protos.Empty())
        return r.value
    def get_disk_usage(self, mountpoint="/data"):
        """
        Get partition usage stats.
        """
        req = protos.String(value=mountpoint)
        r = self.stub.getDiskUsage(req)
        return r
    def get_battery_info(self):
        """
        Get battery info.
        """
        r = self.stub.getBatteryInfo(protos.Empty())
        return r
    def get_cpu_info(self):
        """
        Get CPU usage and related stats.
        """
        r = self.stub.getCpuInfo(protos.Empty())
        return r
    def get_overall_disk_io_info(self):
        """
        Get global disk I/O stats.
        """
        r = self.stub.getOverallDiskIOInfo(protos.Empty())
        return r
    def get_overall_net_io_info(self):
        """
        Get global network traffic stats.
        """
        r = self.stub.getOverallNetIOInfo(protos.Empty())
        return r
    def get_userdata_disk_io_info(self):
        """
        Get user-data disk I/O stats.
        """
        r = self.stub.getUserDataDiskIOInfo(protos.Empty())
        return r
    def get_net_io_info(self, interface):
        """
        Get network traffic stats for a specific interface.
        """
        req = protos.String(value=interface)
        r = self.stub.getNetIOInfo(req)
        return r
    def get_mem_info(self):
        """
        Get memory stats.
        """
        r = self.stub.getMemInfo(protos.Empty())
        return r


class ProxyStub(BaseServiceStub):
    def is_openvpn_running(self):
        """
        Check whether OPENVPN is running.
        """
        r = self.stub.isOpenVPNRunning(protos.Empty())
        return r.value
    def is_gproxy_running(self):
        """
        Check whether GPROXY is running.
        """
        r = self.stub.isGproxyRunning(protos.Empty())
        return r.value
    def start_openvpn(self, profile):
        """
        Start OPENVPN.
        """
        checkArgumentTyp(profile, OpenVPNProfile)
        r = self.stub.startOpenVPN(profile)
        return r.value
    def start_gproxy(self, profile):
        """
        Start GPROXY.
        """
        checkArgumentTyp(profile, GproxyProfile)
        r = self.stub.startGproxy(profile)
        return r.value
    def stop_openvpn(self):
        """
        Stop OPENVPN.
        """
        r = self.stub.stopOpenVPN(protos.Empty())
        return r.value
    def stop_gproxy(self):
        """
        Stop GPROXY.
        """
        r = self.stub.stopGproxy(protos.Empty())
        return r.value


class SelinuxPolicyStub(BaseServiceStub):
    def allow(self, source, target, tclass, action):
        """
        selinux allow
        """
        req = protos.SelinuxPolicyRequest(source=source, target=target,
                                          tclass=tclass, action=action)
        r = self.stub.policySetAllow(req)
        return r.value
    def disallow(self, source, target, tclass, action):
        """
        selinux disallow
        """
        req = protos.SelinuxPolicyRequest(source=source, target=target,
                                          tclass=tclass, action=action)
        r = self.stub.policySetDisallow(req)
        return r.value
    def get_enforce(self):
        """
        Get the current SELinux enforce state.
        """
        r = self.stub.getEnforce(protos.Empty())
        return r.value
    def set_enforce(self, enforced=True):
        """
        Set the current SELinux enforce state.
        """
        req = protos.Boolean(value=enforced)
        r = self.stub.setEnforce(req)
        return r.value
    def enabled(self):
        """
        Check whether SELinux is enabled on the device.
        """
        r = self.stub.isEnabled(protos.Empty())
        return r.value
    def enforce(self, name):
        """
        Set a domain to enforce.
        """
        req = protos.String(value=name)
        r = self.stub.policySetEnforce(req)
        return r.value
    def permissive(self, name):
        """
        Set a domain to permissive.
        """
        req = protos.String(value=name)
        r = self.stub.policySetPermissive(req)
        return r.value
    def create_domain(self, name):
        """
        Create a new SELinux domain.
        """
        req = protos.String(value=name)
        r = self.stub.policyCreateDomain(req)
        return r.value


class FileStub(BaseServiceStub):
    def _fd_stream_read(self, fd, chunksize):
        for chunk in iter(lambda: fd.read(chunksize), bytes()):
            yield chunk
    def _fd_streaming_send(self, fd, dest, chunksize):
        yield protos.FileRequest(path=dest)
        for chunk in self._fd_stream_read(fd, chunksize):
            yield protos.FileRequest(payload=chunk)
    def _fd_streaming_recv(self, fd, iterator):
        for chunk in iterator:
            fd.write(chunk.payload)
    def download_fd(self, fpath, fd):
        """
        Download a file from the device to a file descriptor.
        """
        req = protos.FileRequest(path=fpath)
        iterator = self.stub.downloadFile(req)
        self._fd_streaming_recv(fd, iterator)
        st = self.file_stat(fpath)
        return st
    def upload_fd(self, fd, dest):
        """
        Upload a file descriptor to the device.
        """
        chunksize = 1024*1024*1
        streaming = self._fd_streaming_send(fd, dest,
                                              chunksize)
        self.stub.uploadFile(streaming)
        st = self.file_stat(dest)
        return st
    def download_file(self, fpath, dest):
        """
        Download a file from the device to local storage.
        """
        with io.open(dest, mode="wb") as fd:
            return self.download_fd(fpath, fd)
    def upload_file(self, fpath, dest):
        """
        Upload a local file to the device.
        """
        with io.open(fpath, mode="rb") as fd:
            return self.upload_fd(fd, dest)
    def delete_file(self, fpath):
        """
        Delete a file on the device.
        """
        req = protos.FileRequest(path=fpath)
        r = self.stub.deleteFile(req)
        return r.value
    def file_chmod(self, fpath, mode=0o644):
        """
        Change file permissions on the device.
        """
        req = protos.FileRequest(path=fpath, mode=mode)
        r = self.stub.fileChmod(req)
        return r
    def file_stat(self, fpath):
        """
        Get file info on the device.
        """
        req = protos.FileRequest(path=fpath)
        r = self.stub.fileStat(req)
        return r


class LockStub(BaseServiceStub):
    def acquire_lock(self, leaseTime=60):
        """
        Acquire the device control lock and raise if it is busy.
        """
        req = protos.Integer(value=leaseTime)
        r = self.stub.acquireLock(req)
        return r.value
    def get_session_token(self):
        """
        Get the current session token.
        """
        r = self.stub.getSessionToken(protos.Empty())
        return r.value
    def refresh_lock(self, leaseTime=60):
        """
        Refresh the device control lock within 60 seconds to keep the session.
        """
        req = protos.Integer(value=leaseTime)
        r = self.stub.refreshLock(req)
        return r.value
    def release_lock(self):
        """
        Release the device control lock.
        """
        r = self.stub.releaseLock(protos.Empty())
        return r.value


class WifiStub(BaseServiceStub):
    def status(self):
        """
        Get info for the currently connected Wi-Fi.
        """
        r = self.stub.status(protos.Empty())
        return r
    def blacklist_add(self, bssid):
        """
        Add a BSSID to the Wi-Fi blacklist.
        """
        r = self.stub.blacklistAdd(protos.String(value=bssid))
        return r.value
    def blacklist_clear(self):
        """
        Clear the Wi-Fi BSSID blacklist.
        """
        r = self.stub.blacklistClear(protos.Empty())
        return r.value
    def blacklist_get_all(self):
        """
        Get all blacklisted Wi-Fi BSSIDs.
        """
        r = self.stub.blacklistAll(protos.Empty())
        return r.bssids
    def scan(self):
        """
        Request a nearby Wi-Fi scan.
        """
        r = self.stub.scan(protos.Empty())
        return r.value
    def scan_results(self):
        """
        Get scanned nearby Wi-Fi networks.
        """
        r = self.stub.scanResults(protos.Empty())
        return r.stations
    def get_mac_addr(self):
        """
        Get the current Wi-Fi MAC address.
        """
        r = self.stub.getMacAddr(protos.Empty())
        return r.value
    def signal_poll(self):
        """
        Get current Wi-Fi signal info.
        """
        r = self.stub.signalPoll(protos.Empty())
        return r
    def list_networks(self):
        """
        List previously connected Wi-Fi networks.
        """
        r = self.stub.listNetworks(protos.Empty())
        return r.networks
    def select_network(self, networkId):
        raise NotImplementedError
    def enable_network(self, networkId):
        raise NotImplementedError
    def disable_network(self, networkId):
        raise NotImplementedError
    def add_network(self):
        raise NotImplementedError
    def remove_network(self, networkId):
        raise NotImplementedError
    def set_network_config(self, networkId, name, value):
        raise NotImplementedError
    def get_network_config(self, networkId, name):
        raise NotImplementedError
    def disconnect(self):
        """
        Disconnect Wi-Fi.
        """
        r = self.stub.disconnect(protos.Empty())
        return r.value
    def reconnect(self):
        """
        Reconnect Wi-Fi.
        """
        r = self.stub.reconnect(protos.Empty())
        return r.value
    def set_config(self, name, value):
        raise NotImplementedError
    def set_auto_connect(self, auto=True):
        raise NotImplementedError
    def save_config(self):
        raise NotImplementedError


class OcrOperator(object):
    def __init__(self, device, elements=None,
                                    display=0,
                                    **kwargs):
        self.elements = elements
        self.index = kwargs.pop("index", 0)
        self.func, self.rule = kwargs.popitem()
        self.match = getattr(self, self.func)
        self.automator = device.proxy("UiAutomator",
                                        display=display)
    def text(self, item):
        return self.rule == item["text"]
    def textMatches(self, item):
        return bool(re.match(self.rule, item["text"],
                                        re.DOTALL))
    def textContains(self, item):
        return self.rule in item["text"]
    def find_target_item(self):
        m = [e for e in self.elements \
                            if self.match(e)]
        o = (m and len(m) > self.index) != True
        return None if o else m[self.index]
    def find_item_or_throw(self):
        item = self.find_target_item()
        msg = "OcrSelector[{}={}]".format(self.func, self.rule)
        item or self.throw(UiObjectNotFoundException, msg)
        return item
    def find_cb(self, func, ret, *args):
        item = self.find_target_item()
        return func(item, *args) if item else ret
    def find_or_throw_cb(self, func, *args):
        item = self.find_item_or_throw()
        return func(item, *args)
    def throw(self, exception, *args):
        raise exception(*args)
    def _screenshot(self, item, quality):
        return self.automator.screenshot(quality, bound=item["bound"])
    def _click(self, item):
        point = item["bound"].center()
        return self.automator.click(point)
    def __str__(self):
        return "Ocr: {}={}".format(self.func, self.rule)
    __repr__ = __str__
    def exists(self):
        """
        OCR: check whether the element exists.
        """
        return bool(self.find_target_item())
    def click(self):
        """
        OCR: click the element or raise if missing.
        """
        return self.find_or_throw_cb(self._click)
    def click_exists(self):
        """
        OCR: click the element without raising if missing.
        """
        return self.find_cb(self._click, False)
    def screenshot(self, quality=100):
        """
        OCR: screenshot the element.
        """
        return self.find_or_throw_cb(self._screenshot,
                                            quality)
    def take_screenshot(self, quality=100):
        """
        OCR: screenshot the element.
        """
        return self.screenshot(quality)
    def info(self):
        """
        OCR: get info for the matched element.
        """
        item = self.find_item_or_throw()
        return item


class OcrEngine(object):
    def __init__(self, service, *args,
                                     **kwargs):
        args = list(args)
        if type(service) == type:
            args.insert(0, service)
            service = "custom"
        func = getattr(self, "init_{}".format(service))
        func(*args, **kwargs)
    def init_paddleocr(self, *args, **kwargs):
        from paddleocr import PaddleOCR
        self._service = PaddleOCR(*args, **kwargs)
        self._ocr = self.ocr_paddleocr
    def init_easyocr(self, *args, **kwargs):
        from easyocr import Reader
        self._service = Reader(*args, **kwargs)
        self._ocr = self.ocr_easyocr
    def init_custom(self, service, *args, **kwargs):
        self._service = service(*args, **kwargs)
        self._ocr = self.ocr_custom
    def ocr_custom(self, image):
        result = self._service.ocr(image)
        return result
    def ocr_paddleocr(self, image):
        r = self._service.ocr(image)
        n = bool(r and r[0] and type(r[0][-1])==float)
        result = (r if n else r[0]) or []
        output = [[n[0], n[1][0], n[1][1]] for n in result]
        return output
    def ocr_easyocr(self, image):
        result = self._service.readtext(image)
        return result
    def ocr(self, screenshot):
        img = screenshot.getvalue()
        result = self._ocr(img) or []
        output = [self.format(*n) for n in result]
        return output
    def format(self, box, text, confidence):
        bound = Bound()
        bound.left      = int(min(p[0] for p in box))
        bound.top       = int(min(p[1] for p in box))
        bound.bottom    = int(max(p[1] for p in box))
        bound.right     = int(max(p[0] for p in box))
        info = dict(text=text, confidence=confidence,
                                        bound=bound)
        return info


class Device(object):
    def __init__(self, host, port=65000,
                                        certificate=None,
                                        session=None):
        self.certificate = certificate
        self.server = "{0}:{1}".format(host, port)
        policy = dict()
        policy["maxAttempts"] = 5
        policy["retryableStatusCodes"] = ["UNAVAILABLE"]
        policy["backoffMultiplier"] = 2
        policy["initialBackoff"] = "0.5s"
        policy["maxBackoff"] = "15s"
        config = json.dumps(dict(methodConfig=[{"name": [{}],
                                 "retryPolicy": policy,}]))
        option = dict()
        option["grpc.max_send_message_length"] = 64*1024*1024
        option["grpc.max_receive_message_length"] = 128*1024*1024
        option["grpc.keepalive_time_ms"] = 60*1000
        option["grpc.keepalive_timeout_ms"] = 20*1000
        option["grpc.keepalive_permit_without_calls"] = True
        option["grpc.max_pings_without_data"] = 0
        option["grpc.service_config"] = config
        option["grpc.enable_http_proxy"] = 0
        if certificate is not None:
            with open(certificate, "rb") as fd:
                key, crt, ca = self._parse_certdata(fd.read())
            creds = grpc.ssl_channel_credentials(root_certificates=ca,
                                                 certificate_chain=crt,
                                                 private_key=key)
            self._chan = grpc.secure_channel(self.server, creds,
                    options=(("grpc.ssl_target_name_override",
                                self._parse_cname(crt)),
                             *tuple(option.items()),))
        else:
            self._chan = grpc.insecure_channel(self.server,
                    options=(*tuple(option.items()),)
            )
        session = session or uuid.uuid4().hex
        interceptors = [ClientSessionMetadataInterceptor(session),
                        GrpcRemoteExceptionInterceptor(),
                        ClientLoggingInterceptor()]
        self._ocr = None
        self._ocr_img_quality = 75
        self.channel = grpc.intercept_channel(self._chan,
                        *interceptors)
        self.session = session
    @property
    def frida(self):
        if _frida_dma is None:
            raise ModuleNotFoundError("frida")
        try:
            device = _frida_dma.get_device_matching(
                        lambda d: d.name==self.server)
            # make a call to check server connectivity
            device.query_system_parameters()
            return device
        except:
            """ No-op """
        kwargs = {}
        if self.certificate is not None:
            kwargs["certificate"] = self.certificate
        if self._get_session_token():
            kwargs["token"] = self._get_session_token()
        try:
            _frida_dma.remove_remote_device(self.server)
        except frida.InvalidArgumentError:
            """ No-op """
        device = _frida_dma.add_remote_device(self.server,
                                        **kwargs)
        return device
    def fix_execute_only_memory(self):
        """
        Restore read permission on execute-only (``--x`` / XOM) segments
        of system libraries inside zygote processes.

        Some OEM ROMs (e.g. MIUI) map system libraries as execute-only
        memory. When the frida runtime embedded in the server hooks the
        zygote fork path, it fails to read the target memory while
        building trampolines (SEGV_ACCERR), which makes every spawned
        application crash at startup - apps get stuck on the splash
        screen or die immediately after ``spawn()`` / ``resume()``.

        This method walks ``--x`` ranges of zygote (64/32-bit) whose
        backing file lives under /system, /apex or /vendor and calls
        ``mprotect()`` to restore ``r-x`` on them, so that processes
        forked from zygote inherit readable segments again.

        It must be re-invoked after each device reboot or server restart,
        before spawning/injecting applications. Requires the server to
        run as root (default).

        Returns a dict keyed by process name::

            {
                "zygote64": {"fixed": 294, "failed": 0},
                ...
            }

        Processes that do not exist on the device are skipped, errors
        while attaching are reported as {"error": "..."} entries.
        """
        if _frida_dma is None:
            raise ModuleNotFoundError("frida")
        device = self.frida
        results = {}
        for proc in device.enumerate_processes():
            if proc.name not in ("zygote64", "zygote"):
                continue
            try:
                session = device.attach(proc.pid)
                res = {}
                def on_message(msg, data):
                    if msg.get("type") == "send":
                        res.update(msg["payload"])
                script = session.create_script(self.XOM_FIX_SCRIPT)
                script.on("message", on_message)
                script.load()
                time.sleep(5)
                session.detach()
                results[proc.name] = {"fixed": res.get("fixed", 0),
                                      "failed": res.get("failed", 0)}
            except Exception as e:
                results[proc.name] = {"error": str(e)}
        return results
    # JS: mprotect --x ranges backed by system libs back to r-x.
    # Module.getExportByName is removed since frida 17, fall back
    # progressively for older embedded runtimes.
    XOM_FIX_SCRIPT = r"""
        var resolve = null;
        if (typeof Module != "undefined" && Module.getGlobalExportByName)
            resolve = function (n) { return Module.getGlobalExportByName(n); };
        else if (typeof Module != "undefined" && Module.getExportByName)
            resolve = function (n) { return Module.getExportByName(null, n); };
        else
            resolve = function (n) { return Module.findExportByName(null, n); };
        var mprotect = new NativeFunction(resolve("mprotect"),
                                          "int", ["pointer", "uint", "int"]);
        var fixed = 0, failed = 0;
        Process.enumerateRanges("--x").forEach(function (r) {
            var p = r.file ? (r.file.path || "") : "";
            if (p.indexOf("/system") === 0 || p.indexOf("/apex") === 0
                    || p.indexOf("/vendor") === 0) {
                if (mprotect(r.base, r.size, 5) === 0) fixed++;
                else failed++;
            }
        });
        send({fixed: fixed, failed: failed});
    """
    def __str__(self):
        return "Device@{}".format(self.server)
    __repr__ = __str__
    def _parse_certdata(self, data):
        key, crt, ca = Pem.parse(data)
        ca = ca.as_bytes()
        crt = crt.as_bytes()
        key = key.as_bytes()
        return key, crt, ca
    def _parse_cname(self, crt):
        _, _, der = pem.unarmor(crt)
        subject = x509.Certificate.load(der).subject
        return subject.native["common_name"]
    def stub(self, module):
        return self.proxy(module)
    def proxy(self, module, clazz=None, **kwargs):
        this = sys.modules[__name__]
        stub = getattr(services, "{0}Stub".format(module))(self.channel)
        wrap = getattr(this, "{0}Stub".format(clazz or module))
        return wrap(stub, **kwargs)
    # Shortcut: File
    def download_fd(self, fpath, fd):
        return self.stub("File").download_fd(fpath, fd)
    def upload_fd(self, fd, dest):
        return self.stub("File").upload_fd(fd, dest)
    def download_file(self, fpath, dest):
        return self.stub("File").download_file(fpath, dest)
    def upload_file(self, fpath, dest):
        return self.stub("File").upload_file(fpath, dest)
    def delete_file(self, fpath):
        return self.stub("File").delete_file(fpath)
    def file_chmod(self, fpath, mode=0o644):
        return self.stub("File").file_chmod(fpath, mode=mode)
    def file_stat(self, fpath):
        return self.stub("File").file_stat(fpath)
    # Shortcut: Application
    def create_install_session(self, user=0, size_bytes=0, package=None,
                               installer_package_name=None, dont_kill_app=False,
        replace_existing=True, allow_test=False, request_downgrade=False,
        grant_runtime_permissions=False, tmpdir=None):
        kwargs = dict(user=user)
        kwargs["size_bytes"] = size_bytes
        kwargs["package"] = package
        kwargs["request_downgrade"] = request_downgrade
        kwargs["grant_runtime_permissions"] = grant_runtime_permissions
        kwargs["installer_package_name"] = installer_package_name
        kwargs["dont_kill_app"] = dont_kill_app
        kwargs["replace_existing"] = replace_existing
        kwargs["allow_test"] = allow_test
        kwargs["tmpdir"] = tmpdir
        proxy = self.proxy("Application", device=self)
        return proxy._create_install_session(**kwargs)
    def current_application(self):
        return self.stub("Application").current_application()
    def enumerate_installed_apps(self, user=0):
        return self.stub("Application").enumerate_installed_apps(user=user)
    def enumerate_running_processes(self):
        return self.stub("Application").enumerate_running_processes()
    def start_activity(self, **activity):
        return self.stub("Application").start_activity(**activity)
    def get_application_by_name(self, name):
        return self.stub("Application").get_application_by_name(name)
    def application(self, applicationId, user=0):
        return self.stub("Application")(applicationId, user=user)
    # Shortcut: Util
    def touch(self):
        return MultiTouchOpStub(self.stub("Util"))
    def show_toast(self, text, duration=ToastDuration.TD_SHORT):
        return self.stub("Util").show_toast(text, duration=duration)
    def is_ca_certificate_installed(self, certdata):
        return self.stub("Util").is_ca_certificate_installed(certdata)
    def uninstall_ca_certificate(self, certfile):
        return self.stub("Util").uninstall_ca_certificate(certfile)
    def install_ca_certificate(self, certfile):
        return self.stub("Util").install_ca_certificate(certfile)
    def reboot(self):
        return self.stub("Util").reboot()
    def shutdown(self):
        return self.stub("Util").shutdown()
    def exit(self):
        return self.stub("Util").exit()
    def reload(self, clean=False):
        return self.stub("Util").reload(clean)
    def beep(self):
        return self.stub("Util").beep()
    def play_audio(self, file, type=AudioStreamType.AST_SYSTEM,
                                        loop=1, interval=0):
        return self.stub("Util").play_audio(file, type=type, loop=loop,
                                        interval=interval)
    def setprop(self, name, value):
        return self.stub("Util").setprop(name, value)
    def getprop(self, name):
        return self.stub("Util").getprop(name)
    def hex_patch(self, pattern, replacement, path,
                            maxreplace=-1, dryrun=False):
        return self.stub("Util").hex_patch(pattern, replacement, path,
                                    maxreplace=maxreplace,
                                    dryrun=dryrun)
    # Shortcut: Debug
    def install_adb_pubkey(self, pubkey):
        return self.stub("Debug").install_adb_pubkey(pubkey)
    def uninstall_adb_pubkey(self, pubkey):
        return self.stub("Debug").uninstall_adb_pubkey(pubkey)
    def start_android_debug_bridge(self):
        return self.stub("Debug").start_android_debug_bridge()
    def is_android_debug_bridge_running(self):
        return self.stub("Debug").is_android_debug_bridge_running()
    def stop_android_debug_bridge(self):
        return self.stub("Debug").stop_android_debug_bridge()
    # Shortcut: Proxy
    def is_openvpn_running(self):
        return self.stub("Proxy").is_openvpn_running()
    def is_gproxy_running(self):
        return self.stub("Proxy").is_gproxy_running()
    def start_openvpn(self, profile):
        return self.stub("Proxy").start_openvpn(profile)
    def start_gproxy(self, profile):
        return self.stub("Proxy").start_gproxy(profile)
    def stop_openvpn(self):
        return self.stub("Proxy").stop_openvpn()
    def stop_gproxy(self):
        return self.stub("Proxy").stop_gproxy()
    # Virtual Display
    def get_virtual_display_by_id(self, display):
        return self.proxy("UiAutomator", clazz="VirtualDisplay",
                            display=display, device=self)
    def create_virtual_display(self, width=None, height=None, densityDpi=None, name=None):
        display = self.proxy("UiAutomator", clazz="VirtualDisplay")._create_virtual_display(
                                                    width, height, densityDpi, name=name)
        return self.get_virtual_display_by_id(display)
    # Shortcut: Shell
    def execute_script(self, script, alias=None, timeout=60):
        return self.stub("Shell").execute_script(script, alias=alias,
                                                        timeout=timeout)
    def execute_background_script(self, script, alias=None):
        return self.stub("Shell").execute_background_script(script, alias=alias)
    def is_background_script_finished(self, tid):
        return self.stub("Shell").is_background_script_finished(tid)
    def kill_background_script(self, tid):
        return self.stub("Shell").kill_background_script(tid)
    # Shortcut: UiAutomator
    def click(self, point):
        return self.stub("UiAutomator").click(point)
    def long_click(self, point, timeout=0):
        return self.stub("UiAutomator").long_click(point, timeout=timeout)
    def drag(self, A, B, step=32):
        return self.stub("UiAutomator").drag(A, B, step=step)
    def swipe(self, A, B, step=32):
        return self.stub("UiAutomator").swipe(A, B, step=step)
    def swipe_points(self, *points, step=32):
        return self.stub("UiAutomator").swipe_points(*points, step=step)
    def open_notification(self):
        return self.stub("UiAutomator").open_notification()
    def open_quick_settings(self):
        return self.stub("UiAutomator").open_quick_settings()
    def wake_up(self):
        return self.stub("UiAutomator").wake_up()
    def sleep(self):
        return self.stub("UiAutomator").sleep()
    def is_screen_on(self):
        return self.stub("UiAutomator").is_screen_on()
    def is_screen_locked(self):
        return self.stub("UiAutomator").is_screen_locked()
    def set_clipboard(self, text):
        return self.stub("UiAutomator").set_clipboard(text)
    def get_clipboard(self):
        return self.stub("UiAutomator").get_clipboard()
    def freeze_rotation(self, freeze=True):
        return self.stub("UiAutomator").freeze_rotation(freeze=freeze)
    def set_orientation(self, orien=Orientation.ORIEN_NATURE):
        return self.stub("UiAutomator").set_orientation(orien)
    def press_key(self, key):
        return self.stub("UiAutomator").press_key(key)
    def press_keycode(self, code, meta=0):
        return self.stub("UiAutomator").press_keycode(code, meta)
    def take_screenshot(self, quality=100, bound=None):
        return self.stub("UiAutomator").take_screenshot(quality, bound=bound)
    def screenshot(self, quality=100, bound=None):
        return self.stub("UiAutomator").screenshot(quality, bound=bound)
    def dump_window_hierarchy(self, compressed=False):
        return self.stub("UiAutomator").dump_window_hierarchy(compressed=compressed)
    def wait_for_idle(self, timeout):
        return self.stub("UiAutomator").wait_for_idle(timeout)
    def get_last_toast(self):
        return self.stub("UiAutomator").get_last_toast()
    def find_similar_image(self, data, threshold=0.0, distance=250,
                                scale=1.0, area=FindImageArea.FIA_WHOLE_SCREEN,
                                method=FindImageMethod.FIM_TEMPLATE):
        return self.stub("UiAutomator").find_similar_image(data, threshold=threshold,
                                distance=distance, scale=scale,
                                area=area, method=method)
    # watcher
    def remove_all_watchers(self):
        return self.stub("UiAutomator").remove_all_watchers()
    def set_watcher_loop_enabled(self, enabled):
        return self.stub("UiAutomator").set_watcher_loop_enabled(enabled)
    def get_watcher_loop_enabled(self):
        return self.stub("UiAutomator").get_watcher_loop_enabled()
    def get_watcher_triggered_count(self, name):
        return self.stub("UiAutomator").get_watcher_triggered_count(name)
    def reset_watcher_triggered_count(self, name):
        return self.stub("UiAutomator").reset_watcher_triggered_count(name)
    def get_enabled_watchers(self):
        return self.stub("UiAutomator").get_enabled_watchers()
    def get_watchers(self):
        return self.stub("UiAutomator").get_watchers()
    def register_click_target_selector_watcher(self, name, conditions,
                                               target):
        return self.stub("UiAutomator").register_click_target_selector_watcher(
                                                name, conditions, target
        )
    def register_press_key_watcher(self, name, conditions, key):
        return self.stub("UiAutomator").register_press_key_watcher(
                                                name, conditions, key
        )
    def register_none_op_watcher(self, name, conditions):
        return self.stub("UiAutomator").register_none_op_watcher(
                                                name, conditions
        )
    def set_watcher_enabled(self, name, enable):
        return self.stub("UiAutomator").set_watcher_enabled(name, enable)
    def get_watcher_enabled(self, name):
        return self.stub("UiAutomator").get_watcher_enabled(name)
    def remove_watcher(self, name):
        return self.stub("UiAutomator").remove_watcher(name)
    def device_info(self):
        return self.stub("UiAutomator").device_info()
    def server_info(self):
        return self.stub("Util").server_info()
    def __call__(self, **kwargs):
        return self.stub("UiAutomator")(**kwargs)
    # OCR extension.
    def ocr(self, index=0, display=0, **kwargs):
        if not isinstance(self._ocr, OcrEngine):
            raise IllegalStateException("Ocr engine is not setted up")
        if any(r not in ["text", "textContains", "textMatches"] \
                                        for r in kwargs.keys()):
            raise InvalidArgumentError("Only text* matches are supported")
        if len(kwargs) != 1:
            raise InvalidArgumentError("Only or at least one rule can be used")
        image = self.proxy("UiAutomator", display=display).screenshot(
                                        self._ocr_img_quality)
        return OcrOperator(self,
        elements=self._ocr.ocr(image),
                            index=index,
                            display=display,
                            **kwargs
        )
    def setup_ocr_backend(self, service, *args, quality=75,
                                                **kwargs):
        self._ocr_img_quality = quality
        self._ocr = OcrEngine(service, *args,
                                    **kwargs)
    # Logging control.
    def set_debug_log_enabled(self, enable):
        level = logging.DEBUG if enable else logging.WARN
        logger.setLevel(level)
        return enable
    # Lock API.
    def _get_session_token(self):
        return self.stub("Lock").get_session_token()
    def _acquire_lock(self, leaseTime=60):
        return self.stub("Lock").acquire_lock(leaseTime)
    def _refresh_lock(self, leaseTime=60):
        return self.stub("Lock").refresh_lock(leaseTime)
    def _release_lock(self):
        return self.stub("Lock").release_lock()
    def __enter__(self):
        self._acquire_lock(leaseTime=sys.maxsize)
        return self
    def __exit__(self, type, value, traceback):
        self._release_lock()


if __name__ == "__main__":
    import code
    import readline
    import rlcompleter
    import argparse

    parser = argparse.ArgumentParser()
    crt = os.environ.get("CERTIFICATE", None)
    port = int(os.environ.get("PORT", 65000))
    parser.add_argument("-device", type=str, default="127.0.0.1",
                                   help="service ip address")
    parser.add_argument("-port", type=int, default=port,
                                   help="service port")
    parser.add_argument("-cert", type=str, default=crt,
                                   help="ssl cert")
    args = parser.parse_args()

    readline.parse_and_bind("tab: complete")
    d = Device(args.device, port=args.port,
                        certificate=args.cert)
    code.interact(local=globals())