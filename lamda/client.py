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
                          IllegalStateException)
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

def checkDupEntry(a, entries):
    if a in entries:
        raise DuplicateEntryError(a)

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
    """ 载入包下面的相关 proto 文件 """
    return grpc.protos_and_services(name)


def to_dict(prot):
    """ 将 proto 返回值转换为字典 """
    r = MessageToJson(prot, preserving_proto_field_name=True)
    return json.loads(r)


def Selector(**kwargs):
    """ Selector wrapper """
    sel = _Selector(**kwargs, fields=kwargs.keys())
    return sel


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
    def down(self, x, y, pressure=50, track=0):
        self.s.appendDown(tid=track, x=x, y=y,
                          pressure=pressure)
        return self
    def move(self, x, y, pressure=50, track=0):
        self.s.appendMove(tid=track, x=x, y=y,
                          pressure=pressure)
        return self
    def up(self, track=0):
        self.s.appendUp(tid=track)
        return self
    def wait(self, mills):
        self.s.appendWait(wait=mills)
        return self
    def build(self):
        sequence = TouchSequence()
        sequence.CopyFrom(self.s)
        return sequence


class ClientLoggingInterceptor(ClientInterceptor):
    def truncate_string(self, s):
        return "{:.1024}...".format(s) if len(s) > 1024 else s
    def intercept(self, function, request, details):
        """
        日志记录各个接口的调用及参数
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
        metadata["instance"] = self.session
        metadata["hostname"] = quote(platform.node())
        details = details._replace(metadata=metadata.items())
        res = function(request, details)
        return res


class GrpcRemoteExceptionInterceptor(ClientInterceptor):
    def intercept(self, function, request, details):
        """
        处理远程调用中发生的异常并抛出本地异常
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
    def __init__(self, caller, selector):
        """
        UiAutomator 子接口，用来模拟出实例的意味
        """
        self._selector = selector
        self.selector = Selector(**selector)
        self.stub = caller.stub
        self.caller = caller
    def __str__(self):
        selector = ", ".join(["{}={}".format(k, v) \
                        for k, v in self._selector.items()])
        return "Object: {}".format(selector)
    __repr__ = __str__
    def _child_sibling(self, name, **selector):
        s = copy.deepcopy(self._selector)
        s.setdefault("childOrSibling", [])
        s.setdefault("childOrSiblingSelector", [])
        s["childOrSiblingSelector"].append(selector)
        s["childOrSibling"].append(name)
        return self.__class__(self.caller, s)
    def child(self, **selector):
        """
        匹配选择器里面的子节点
        """
        return self._child_sibling("child", **selector)
    def sibling(self, **selector):
        """
        匹配选择器的同级节点
        """
        return self._child_sibling("sibling", **selector)
    def take_screenshot(self, quality=100):
        """
        对选择器选中元素进行截图
        """
        req = protos.SelectorTakeScreenshotRequest(selector=self.selector,
                                                   quality=quality)
        r = self.stub.selectorTakeScreenshot(req)
        return BytesIO(r.value)
    def screenshot(self, quality=100):
        return self.take_screenshot(quality=quality)
    def get_text(self):
        """
        获取选择器选中输入控件中的文本
        """
        req = protos.SelectorOnlyRequest(selector=self.selector)
        r = self.stub.selectorGetText(req)
        return r.value
    def clear_text_field(self):
        """
        清空选择器选中输入控件中的文本
        """
        req = protos.SelectorOnlyRequest(selector=self.selector)
        r = self.stub.selectorClearTextField(req)
        return r.value
    def set_text(self, text):
        """
        向选择器选中输入控件中填入文本
        """
        req = protos.SelectorSetTextRequest(selector=self.selector,
                                            text=text)
        r = self.stub.selectorSetText(req)
        return r.value
    def click(self, corner=Corner.COR_CENTER):
        """
        点击选择器选中的控件
        """
        req = protos.SelectorClickRequest(selector=self.selector,
                                          corner=corner)
        r = self.stub.selectorClick(req)
        return r.value
    def click_exists(self, corner=Corner.COR_CENTER):
        """
        点击选择器选中的控件（不存在将不会产生异常）
        """
        req = protos.SelectorClickRequest(selector=self.selector,
                                          corner=corner)
        r = self.stub.selectorClickExists(req)
        return r.value
    def long_click(self, corner=Corner.COR_CENTER):
        """
        长按选择器选中的控件
        """
        req = protos.SelectorClickRequest(selector=self.selector,
                                          corner=corner)
        r = self.stub.selectorLongClick(req)
        return r.value
    def exists(self):
        """
        是否存在选择器选中的控件
        """
        req = protos.SelectorOnlyRequest(selector=self.selector)
        r = self.stub.selectorExists(req)
        return r.value
    def info(self):
        """
        获取选择器选中控件的信息
        """
        req = protos.SelectorOnlyRequest(selector=self.selector)
        return self.stub.selectorObjInfo(req)
    def _new_object(self, **kwargs):
        selector = copy.deepcopy(self._selector)
        selector.update(**kwargs)
        instance = self.caller(**selector)
        return instance
    def text(self, txt):
        return self._new_object(text=txt)
    def resourceId(self, name):
        return self._new_object(resourceId=name)
    def description(self, desc):
        return self._new_object(description=desc)
    def packageName(self, name):
        return self._new_object(packageName=name)
    def className(self, name):
        return self._new_object(className=name)
    def textContains(self, needle):
        return self._new_object(textContains=needle)
    def descriptionContains(self, needle):
        return self._new_object(descriptionContains=needle)
    def textStartsWith(self, needle):
        return self._new_object(textStartsWith=needle)
    def descriptionStartsWith(self, needle):
        return self._new_object(descriptionStartsWith=needle)
    def textMatches(self, match):
        return self._new_object(textMatches=match)
    def descriptionMatches(self, match):
        return self._new_object(descriptionMatches=match)
    def resourceIdMatches(self, match):
        return self._new_object(resourceIdMatches=match)
    def packageNameMatches(self, match):
        return self._new_object(packageNameMatches=match)
    def classNameMatches(self, match):
        return self._new_object(classNameMatches=match)
    def checkable(self, value):
        return self._new_object(checkable=value)
    def clickable(self, value):
        return self._new_object(clickable=value)
    def focusable(self, value):
        return self._new_object(focusable=value)
    def scrollable(self, value):
        return self._new_object(scrollable=value)
    def longClickable(self, value):
        return self._new_object(longClickable=value)
    def enabled(self, value):
        return self._new_object(enabled=value)
    def checked(self, value):
        return self._new_object(checked=value)
    def focused(self, value):
        return self._new_object(focused=value)
    def selected(self, value):
        return self._new_object(selected=value)
    def index(self, idx):
        return self._new_object(index=idx)
    def instance(self, idx):
        return self._new_object(instance=idx)
    def get(self, idx):
        """
        获取匹配的第 N 个索引的元素
        """
        return self.instance(idx)
    def __iter__(self):
        """
        遍历所有符合选择器条件的元素实例
        """
        yield from [self.instance(i) for i in \
                            range(self.count())]
    def count(self):
        """
        获取选择器选中控件的数量
        """
        req = protos.SelectorOnlyRequest(selector=self.selector)
        r = self.stub.selectorCount(req)
        return r.value
    def _set_target_Point(self, req, target):
        req.point.CopyFrom(target)
    def _set_target_Selector(self, req, target):
        req.target.CopyFrom(target)
    def drag_to(self, target, step=32):
        """
        将选择器选中的控件拖动到另一个选择器或者点上
        """
        checkArgumentTyp(target, (Point, _Selector))
        func = "_set_target_{}".format(target.DESCRIPTOR.name)
        req = protos.SelectorDragToRequest(selector=self.selector,
                                           step=step)
        getattr(self, func)(req, target)
        r = self.stub.selectorDragTo(req)
        return r.value
    def wait_for_exists(self, timeout):
        """
        等待选择器选中控件出现
        """
        req = protos.SelectorWaitRequest(selector=self.selector,
                                         timeout=timeout)
        r = self.stub.selectorWaitForExists(req)
        return r.value
    def wait_until_gone(self, timeout):
        """
        等待选择器选中控件消失
        """
        req = protos.SelectorWaitRequest(selector=self.selector,
                                         timeout=timeout)
        r = self.stub.selectorWaitUntilGone(req)
        return r.value
    def swipe(self, direction=Direction.DIR_UP, step=32):
        """
        在选择器选中的元素上进行滑动操作
        """
        req = protos.SelectorSwipeRequest(selector=self.selector,
                                          direction=direction,
                                          step=step)
        r = self.stub.selectorSwipe(req)
        return r.value
    def pinch_in(self, percent, step=16):
        """
        双指捏紧（缩小）
        """
        req = protos.SelectorPinchRequest(selector=self.selector,
                                         percent=percent, step=step)
        r = self.stub.selectorPinchIn(req)
        return r.value
    def pinch_out(self, percent, step=16):
        """
        双指放开（放大）
        """
        req = protos.SelectorPinchRequest(selector=self.selector,
                                          percent=percent, step=step)
        r = self.stub.selectorPinchOut(req)
        return r.value
    def scroll_to(self, target, is_vertical=True):
        """
        滚动 scrollable 直到匹配目标元素的选择器
        """
        checkArgumentTyp(target, _Selector)
        req = protos.SelectorScrollRequest(selector=self.selector,
                                           vertical=is_vertical,
                                           target=target)
        r = self.stub.selectorScrollTo(req)
        return r.value
    def _fling_forward(self, is_vertical=True):
        req = protos.SelectorFlingRequest(selector=self.selector,
                                          vertical=is_vertical)
        r = self.stub.selectorFlingForward(req)
        return r.value
    def _fling_backward(self, is_vertical=True):
        req = protos.SelectorFlingRequest(selector=self.selector,
                                          vertical=is_vertical)
        r = self.stub.selectorFlingBackward(req)
        return r.value
    def _fling_to_end(self, max_swipes, is_vertical=True):
        req = protos.SelectorFlingRequest(selector=self.selector,
                                          maxSwipes=max_swipes,
                                          vertical=is_vertical)
        r = self.stub.selectorFlingToEnd(req)
        return r.value
    def _fling_to_beginning(self, max_swipes, is_vertical=True):
        req = protos.SelectorFlingRequest(selector=self.selector,
                                          maxSwipes=max_swipes,
                                          vertical=is_vertical)
        r = self.stub.selectorFlingToBeginning(req)
        return r.value
    def fling_from_top_to_bottom(self):
        """
        在选择器选中元素上进行从上至下阅读式滑动（单次）
        """
        return self._fling_backward(is_vertical=True)
    def fling_from_bottom_to_top(self):
        """
        在选择器选中元素上进行从下至上阅读式滑动（单次）
        """
        return self._fling_forward(is_vertical=True)
    def fling_from_left_to_right(self):
        """
        在选择器选中元素上进行从左至右阅读式滑动（单次）
        """
        return self._fling_backward(is_vertical=False)
    def fling_from_right_to_left(self):
        """
        在选择器选中元素上进行从右至左阅读式滑动（单次）
        """
        return self._fling_forward(is_vertical=False)
    def fling_from_top_to_bottom_to_end(self, max_swipes):
        """
        在选择器选中元素上进行从上至下阅读式滑动直至无法滑动或达到 max_swipes 次
        """
        return self._fling_to_beginning(max_swipes, is_vertical=True)
    def fling_from_bottom_to_top_to_end(self, max_swipes):
        """
        在选择器选中元素上进行从下至上阅读式滑动直至无法滑动或达到 max_swipes 次
        """
        return self._fling_to_end(max_swipes, is_vertical=True)
    def fling_from_left_to_right_to_end(self, max_swipes):
        """
        在选择器选中元素上进行从左至右阅读式滑动直至无法滑动或达到 max_swipes 次
        """
        return self._fling_to_beginning(max_swipes, is_vertical=False)
    def fling_from_right_to_left_to_end(self, max_swipes):
        """
        在选择器选中元素上进行从右至左阅读式滑动直至无法滑动或达到 max_swipes 次
        """
        return self._fling_to_end(max_swipes, is_vertical=False)
    def _scroll_forward(self, step, is_vertical=True):
        req = protos.SelectorScrollRequest(selector=self.selector,
                                           vertical=is_vertical,
                                           step=step)
        r = self.stub.selectorScrollForward(req)
        return r.value
    def _scroll_backward(self, step, is_vertical=True):
        req = protos.SelectorScrollRequest(selector=self.selector,
                                           vertical=is_vertical,
                                           step=step)
        r = self.stub.selectorScrollBackward(req)
        return r.value
    def _scroll_to_end(self, max_swipes, step, is_vertical=True):
        req = protos.SelectorScrollRequest(selector=self.selector,
                                           maxSwipes=max_swipes,
                                           vertical=is_vertical,
                                           step=step)
        r = self.stub.selectorScrollToEnd(req)
        return r.value
    def _scroll_to_beginning(self, max_swipes, step, is_vertical=True):
        req = protos.SelectorScrollRequest(selector=self.selector,
                                           maxSwipes=max_swipes,
                                           vertical=is_vertical,
                                           step=step)
        r = self.stub.selectorScrollToBeginning(req)
        return r.value
    def scroll_from_top_to_bottom(self, step):
        """
        在选择器选中元素上进行从上至下普通滑动
        """
        return self._scroll_backward(step, is_vertical=True)
    def scroll_from_bottom_to_top(self, step):
        """
        在选择器选中元素上进行从下至上普通滑动
        """
        return self._scroll_forward(step, is_vertical=True)
    def scroll_from_left_to_right(self, step):
        """
        在选择器选中元素上进行从左至右普通滑动
        """
        return self._scroll_backward(step, is_vertical=False)
    def scroll_from_right_to_left(self, step):
        """
        在选择器选中元素上进行从右至左普通滑动
        """
        return self._scroll_forward(step, is_vertical=False)
    def scroll_from_top_to_bottom_to_end(self, max_swipes, step):
        """
        在选择器选中元素上进行从上至下普通滑动直至无法滑动或达到 max_swipes 次
        """
        return self._scroll_to_beginning(max_swipes, step, is_vertical=True)
    def scroll_from_bottom_to_top_to_end(self, max_swipes, step):
        """
        在选择器选中元素上进行从下至上普通滑动直至无法滑动或达到 max_swipes 次
        """
        return self._scroll_to_end(max_swipes, step, is_vertical=True)
    def scroll_from_left_to_right_to_end(self, max_swipes, step):
        """
        在选择器选中元素上进行从左至右普通滑动直至无法滑动或达到 max_swipes 次
        """
        return self._scroll_to_beginning(max_swipes, step, is_vertical=False)
    def scroll_from_right_to_left_to_end(self, max_swipes, step):
        """
        在选择器选中元素上进行从右至左普通滑动直至无法滑动或达到 max_swipes 次
        """
        return self._scroll_to_end(max_swipes, step, is_vertical=False)


class UiAutomatorStub(BaseServiceStub):
    def __init__(self, *args, **kwargs):
        super(UiAutomatorStub, self).__init__(*args, **kwargs)
        self.watchers = defaultdict(dict)
    def device_info(self):
        """
        获取设备基本/分辨率等信息
        """
        r = self.stub.deviceInfo(protos.Empty())
        return r
    def set_watcher_loop_enabled(self, enabled):
        """
        设置是否启用设备上的 watcher UI 检测
        """
        req = protos.Boolean(value=enabled)
        r = self.stub.setWatcherLoopEnabled(req)
        return r.value
    def get_watcher_loop_enabled(self):
        """
        获取是否启用设备上的 watcher UI 检测
        """
        r = self.stub.getWatcherLoopEnabled(protos.Empty())
        return r.value
    def get_watcher_triggered_count(self, name):
        """
        获取这个 watcher 被触发的次数
        """
        req = protos.String(value=name)
        r = self.stub.getWatcherTriggeredCount(req)
        return r.value
    def reset_watcher_triggered_count(self, name):
        """
        重置这个 watcher 的触发次数为 0
        """
        req = protos.String(value=name)
        r = self.stub.resetWatcherTriggeredCount(req)
        return r.value
    def get_applied_watchers(self):
        """
        获取已经在系统应用的 watcher 名称列表
        """
        r = self.stub.getAppliedWatchers(protos.Empty())
        return r.watchers
    # 注意：下面这些 watcher 实现不是安全的
    # 注册时都是统一存储到本地实例的变量中，直至 enable 时才会应用至服务端
    # 这样做的原因是让你知道你都干了什么，过多的 watcher 会影响性能
    def remove_all_watchers(self):
        """
        移除所有应用/未应用的 watcher
        """
        for name in list(self.get_applied_watchers()):
            self.remove_watcher(name)
        for name in list(self.watchers.keys()):
            self.remove_watcher(name)
    def register_click_target_selector_watcher(self, name, conditions,
                                               target):
        """
        注册一个满足条件点击 selector 的 watcher
        """
        checkDupEntry(name, self.watchers)
        req = protos.WatcherRegistRequest(name=name, selectors=conditions,
                                          target=target)
        self.watchers[name]["enabled"] = False
        func = lambda: self.stub.registerClickUiObjectWatcher(req).value
        self.watchers[name]["enable"] = func
    def register_press_key_watcher(self, name, conditions, key):
        """
        注册一个满足条件点击 key 的 watcher
        """
        checkDupEntry(name, self.watchers)
        req = protos.WatcherRegistRequest(name=name, selectors=conditions,
                                          key=key)
        self.watchers[name]["enabled"] = False
        func = lambda: self.stub.registerPressKeysWatcher(req).value
        self.watchers[name]["enable"] = func
    def register_none_op_watcher(self, name, conditions):
        """
        注册一个满足条件无操作的 watcher（用来检测是否出现过某个场景）
        """
        checkDupEntry(name, self.watchers)
        req = protos.WatcherRegistRequest(name=name, selectors=conditions)
        self.watchers[name]["enabled"] = False
        func = lambda: self.stub.registerNoneOpWatcher(req).value
        self.watchers[name]["enable"] = func
    def _remove_watcher(self, name):
        return self.stub.removeWatcher(protos.String(value=name)).value
    def set_watcher_enabled(self, name, enable):
        """
        设置是否启用此 watcher
        """
        if name not in self.watchers:
            return False
        self.watchers[name]["enabled"] = enable
        if self.watchers[name]["enabled"]:
            return self.watchers[name]["enable"]()
        return self._remove_watcher(name)
    def get_watcher_enabled(self, name):
        """
        获取此 watcher 是否启用
        """
        return self.watchers.get(name, {}).get("enable")
    def get_last_toast(self):
        """
        获取系统中最后一个 toast 消息
        """
        r = self.stub.getLastToast(protos.Empty())
        return r
    def remove_watcher(self, name):
        """
        移除一个 watcher
        """
        self.watchers.pop(name, None)
        return self._remove_watcher(name)
    def click(self, point):
        """
        点击屏幕中的某个点(Point)
        """
        req = protos.ClickPointRequest(point=point)
        r = self.stub.click(req)
        return r.value
    def drag(self, A, B, step=32):
        """
        从点(Point) A 拖动到点(Point) B
        """
        req = protos.DragPointRequest(A=A, B=B, step=step)
        r = self.stub.drag(req)
        return r.value
    def swipe(self, A, B, step=32):
        """
        从点(Point) A 滑动到点(Point) B
        """
        req = protos.SwipePointRequest(A=A, B=B, step=step)
        r = self.stub.swipe(req)
        return r.value
    def swipe_points(self, *points, step=32):
        """
        滑动一个点(Point)序列（超过两个点）
        """
        req = protos.SwipePointsRequest(points=points, step=step)
        r = self.stub.swipePoints(req)
        return r.value
    def open_notification(self):
        """
        打开通知栏（状态栏）
        """
        r = self.stub.openNotification(protos.Empty())
        return r.value
    def open_quick_settings(self):
        """
        打开设置栏（状态栏）
        """
        r = self.stub.openQuickSettings(protos.Empty())
        return r.value
    def wake_up(self):
        """
        唤醒设备（点亮屏幕）
        """
        r = self.stub.wakeUp(protos.Empty())
        return r.value
    def sleep(self):
        """
        关闭设备（熄灭屏幕）
        """
        r = self.stub.sleep(protos.Empty())
        return r.value
    def is_screen_on(self):
        """
        设备是否处于唤醒状态
        """
        r = self.stub.isScreenOn(protos.Empty())
        return r.value
    def is_screen_locked(self):
        """
        设备屏幕是否已经锁定
        """
        r = self.stub.isScreenLocked(protos.Empty())
        return r.value
    def set_clipboard(self, text):
        """
        设置剪切板文字
        """
        req = protos.ClipboardRequest(ID=str(uuid.uuid4()), value=text)
        r = self.stub.setClipboard(req)
        return r.value
    def get_clipboard(self):
        """
        获取剪切板文字（小于 Android10）
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
        根据提供的目标图片从屏幕中获取相似图片位置
        """
        req = protos.FindImageRequest()
        checkArgumentTyp(area, (Bound, int))
        name = getattr(getattr(area, "DESCRIPTOR", None),
                                         "name", "Area")
        func = "_set_target_{}".format(name)
        getattr(self, func)(req, area)
        req.method = method
        req.distance = distance
        req.threshold = threshold
        req.scale = scale
        req.partial = data
        r = self.stub.findSimilarImage(req)
        return r.bounds
    def freeze_rotation(self, freeze=True):
        """
        锁定屏幕旋转
        """
        r = self.stub.freezeRotation(protos.Boolean(value=freeze))
        return r.value
    def set_orientation(self, orien=Orientation.ORIEN_NATURE):
        """
        设置屏幕旋转方向
        """
        req = protos.OrientationRequest(orientation=orien)
        r = self.stub.setOrientation(req)
        return r.value
    def press_key(self, key):
        """
        按下设备物理按键（HOME/VOLUME/BACK)
        """
        req = protos.PressKeyRequest(key=key)
        r = self.stub.pressKey(req)
        return r.value
    def press_keycode(self, code, meta=0):
        """
        通过 Keycode(整数)按下未定义的按键
        ref: https://developer.android.com/reference/android/view/KeyEvent
        """
        req = protos.PressKeyRequest(code=code, meta=meta)
        r = self.stub.pressKeyCode(req)
        return r.value
    def take_screenshot(self, quality, bound=None):
        """
        截取全屏幕截图
        """
        req = protos.TakeScreenshotRequest(quality=quality,
                                           bound=bound)
        r = self.stub.takeScreenshot(req)
        return BytesIO(r.value)
    def screenshot(self, quality, bound=None):
        return self.take_screenshot(quality, bound=bound)
    def dump_window_hierarchy(self, compressed=False):
        """
        获取屏幕界面布局 XML 文档
        """
        req = protos.Boolean(value=compressed)
        r = self.stub.dumpWindowHierarchy(req)
        return BytesIO(r.value)
    def wait_for_idle(self, timeout):
        """
        等待当前屏幕处于闲置状态（无频繁活动切换）
        """
        r = self.stub.waitForIdle(protos.Integer(value=timeout))
        return r.value
    def __call__(self, **kwargs):
        return ObjectUiAutomatorOpStub(self, kwargs)


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
    def __init__(self, stub, applicationId, user=0):
        """
        Application 子接口，用来模拟出实例的意味
        """
        self.user = user
        self.applicationId = applicationId
        self.stub = stub
    def __str__(self):
        return "Application:{}@{}".format(self.applicationId,
                                          self.user)
    __repr__ = __str__
    def is_foreground(self):
        """
        应用是否正处于前台运行
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.isForeground(req)
        return r.value
    def permissions(self):
        """
        获取应用的所有权限列表
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.getPermissions(req)
        return r.permissions
    def grant(self, permission, mode=GrantType.GRANT_ALLOW):
        """
        授予应用某个权限（应用需要运行时获取的权限）
        """
        req = protos.ApplicationRequest(name=self.applicationId,
                                        permission=permission,
                                        mode=mode)
        req.user = self.user
        r = self.stub.grantPermission(req)
        return r.value
    def revoke(self, permission):
        """
        撤销授予应用的权限（应用需要运行时获取的权限）
        """
        req = protos.ApplicationRequest(name=self.applicationId,
                                        permission=permission)
        req.user = self.user
        r = self.stub.revokePermission(req)
        return r.value
    def query_launch_activity(self):
        """
        获取应用的启动 activity 信息
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.queryLaunchActivity(req)
        return to_dict(r)
    def is_permission_granted(self, permission):
        """
        检查是否已经授予应用某权限（应用需要运行时获取的权限）
        """
        req = protos.ApplicationRequest(name=self.applicationId,
                                        permission=permission)
        req.user = self.user
        r = self.stub.isPermissionGranted(req)
        return r.value
    def clear_cache(self):
        """
        清空应用的缓存数据（非数据仅缓存）
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.deleteApplicationCache(req)
        return r.value
    def reset(self):
        """
        清空应用的所有数据
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.resetApplicationData(req)
        return r.value
    def start(self):
        """
        启动应用
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.startApplication(req)
        return r.value
    def stop(self):
        """
        停止应用
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.stopApplication(req)
        return r.value
    def info(self):
        """
        获取应用信息
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.applicationInfo(req)
        return r
    def uninstall(self):
        """
        卸载应用 (always return true)
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.uninstallApplication(req)
        return r.value
    def enable(self):
        """
        启用应用
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.enableApplication(req)
        return r.value
    def disable(self):
        """
        禁用应用（这将使应用从启动器消失）
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.disableApplication(req)
        return r.value
    def add_to_doze_mode_whitelist(self):
        """
        将APP加入省电白名单（可以一直运行，可能不会覆盖所有系统）
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.addToDozeModeWhiteList(req)
        return True
    def remove_from_doze_mode_whitelist(self):
        """
        将APP移除省电白名单 (always return true)
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.removeFromDozeModeWhiteList(req)
        return True
    def is_installed(self):
        """
        检查应用是否已经安装
        """
        req = protos.ApplicationRequest(name=self.applicationId)
        req.user = self.user
        r = self.stub.isInstalled(req)
        return r.value
    def attach_script(self, script, runtime=ScriptRuntime.RUNTIME_QJS,
                                                    emit="",
                                encode=DataEncode.DATA_ENCODE_NONE,
                                spawn=False,
                                standup=5):
        """
        向应用注入持久化 Hook 脚本
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
        r = self.stub.attachScript(req)
        return r.value
    def detach_script(self):
        """
        移除注入应用的 Hook 脚本
        """
        req = protos.HookRequest()
        req.package     = self.applicationId
        req.user        = self.user
        r = self.stub.detachScript(req)
        return r.value
    def is_attached_script(self):
        """
        检查使用在此应用注入了 Hook 脚本
        """
        req = protos.HookRequest()
        req.package     = self.applicationId
        req.user        = self.user
        r = self.stub.isScriptAttached(req)
        return r.value
    def is_script_alive(self):
        """
        检查应用中的 Hook 脚本是否正常
        """
        req = protos.HookRequest()
        req.package     = self.applicationId
        req.user        = self.user
        r = self.stub.isScriptAlive(req)
        return r.value
    def __getattr__(self, name):
        """
        调用注入应用 Hook 脚本的导出方法
        """
        return AppScriptRpcInterface(self.stub, self,
                                            name)


class ApplicationStub(BaseServiceStub):
    def current_application(self):
        """
        获取当前处于前台的应用的信息
        """
        top = self.stub.currentApplication(protos.Empty())
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
        列出设备上所有正在运行的安卓应用进程
        """
        r = self.stub.enumerateRunningProcesses(protos.Empty())
        return r.processes
    def enumerate_all_pkg_names(self):
        """
        列出所有已安装的应用的 applicationId
        """
        r = self.stub.enumerateAllPkgNames(protos.Empty())
        return r.names
    def get_last_activities(self, count=3):
        """
        获取系统中最后一个活动的详细信息
        """
        req = protos.Integer(value=count)
        r = self.stub.getLastActivities(req).activities
        return list(map(to_dict, r))
    def start_activity(self, **activity):
        """
        启动 activity（总是返回 True）
        """
        activity.setdefault("extras", {})
        extras = activity.pop("extras")
        req = protos.ApplicationActivityRequest(**activity)
        req.extras.update(extras)
        r = self.stub.startActivity(req)
        return r.value
    def install_local_file(self, fpath):
        """
        安装设备上的 apk 文件（注意此路径为设备上的 apk 路径）
        """
        req = protos.ApplicationRequest(path=fpath)
        req.user = self.user
        r = self.stub.installFromLocalFile(req)
        return r
    def __call__(self, applicationId, user=0):
        return ApplicationOpStub(self.stub, applicationId, user)


class StorageOpStub:
    # 用于容器值序列化的方法
    def _decrypt(self, data):
        return self.cryptor.decrypt(data)
    def _encrypt(self, data):
        return self.cryptor.encrypt(data)
    def _unpack(self, value):
        return msgpack.loads(self._decrypt(value))
    def _pack(self, value):
        return self._encrypt(msgpack.dumps(value))
    # 注意：此接口可能并不是跨语言通用
    def __init__(self, stub, name, cryptor=None):
        self.cryptor = cryptor
        self.name = name
        self.stub = stub
    def delete(self, key):
        """
        删除一个 KEY
        """
        req = protos.StorageRequest(key=key)
        req.container = self.name
        res = self.stub.delete(req)
        return res.value
    def exists(self, key):
        """
        检查一个 KEY 是否存在
        """
        req = protos.StorageRequest(key=key)
        req.container = self.name
        res = self.stub.exists(req)
        return res.value
    def get(self, key, default=None):
        """
        获取 KEY 对应的键值
        """
        req = protos.StorageRequest(key=key)
        req.container = self.name
        val = self.stub.get(req).value
        res = self._unpack(val) if val else default
        return res
    def set(self, key, value):
        """
        设置 KEY 对应的键值
        """
        value = self._pack(value)
        req = protos.StorageRequest(key=key, value=value)
        req.container = self.name
        res = self.stub.set(req)
        return res.value
    def setex(self, key, value, ttl):
        """
        设置 KEY 对应的键值，该 KEY 在 TTL 秒后自动删除
        """
        value = self._pack(value)
        req = protos.StorageRequest(key=key, value=value)
        req.container = self.name
        req.ttl = ttl
        res = self.stub.setex(req)
        return res.value
    def setnx(self, key, value):
        """
        设置 KEY 对应的键值 (仅当该键不存在时)
        """
        value = self._pack(value)
        req = protos.StorageRequest(key=key, value=value)
        req.container = self.name
        res = self.stub.setnx(req)
        return res.value
    def expire(self, key, ttl):
        """
        设置 KEY 在 TTL 秒后过期
        """
        req = protos.StorageRequest(key=key, ttl=ttl)
        req.container = self.name
        res = self.stub.expire(req)
        return res.value
    def ttl(self, key):
        """
        获取 KEY 的 TTL (过期时间)
        """
        req = protos.StorageRequest(key=key)
        req.container = self.name
        res = self.stub.ttl(req)
        return res.value


class StorageStub(BaseServiceStub):
    def clear(self):
        """
        删除所有 Storage 容器
        """
        r = self.stub.clearAll(protos.Empty())
        return r.value
    def use(self, name, cryptor=BaseCryptor, **kwargs):
        """
        使用一个 Storage 容器
        """
        return StorageOpStub(self.stub, name, cryptor(**kwargs))
    def remove(self, name):
        """
        删除一个 Storage 容器
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
        安装系统证书（用于 MITM）
        """
        data = self._get_file_content(certfile)
        req = protos.CertifiRequest(cert=data)
        r = self.stub.isCACertificateInstalled(req)
        return r.value
    def install_ca_certificate(self, certfile):
        """
        安装系统证书（用于 MITM）
        """
        data = self._get_file_content(certfile)
        req = protos.CertifiRequest(cert=data)
        r = self.stub.installCACertificate(req)
        return r.value
    def uninstall_ca_certificate(self, certfile):
        """
        移除系统证书（用于 MITM）
        """
        data = self._get_file_content(certfile)
        req = protos.CertifiRequest(cert=data)
        r = self.stub.uninstallCACertificate(req)
        return r.value
    def record_touch(self):
        """
        录制滑动轨迹
        """
        r = self.stub.recordTouch(protos.Empty())
        return r
    def perform_touch(self, tas, wait=True):
        """
        在设备上进行真实滑动（重放录制的滑动轨迹）
        """
        checkArgumentTyp(tas, TouchSequence)
        req = protos.PerformTouchRequest(sequence=tas, wait=wait)
        r = self.stub.performTouch(req)
        return r.value
    def reboot(self):
        """
        重启系统（宿主设备）
        """
        r = self.stub.reboot(protos.Empty())
        return r.value
    def shutdown(self):
        """
        关闭系统（宿主设备）
        """
        r = self.stub.shutdown(protos.Empty())
        return r.value
    def reload(self, clean=False):
        """
        重载设备上运行的服务端
        """
        req = protos.Boolean(value=clean)
        r = self.stub.reload(req)
        return r.value
    def exit(self):
        """
        退出设备上运行的服务端
        """
        r = self.stub.exit(protos.Empty())
        return r.value
    def beep(self):
        """
        播放一声蜂鸣（物理查找）
        """
        r = self.stub.beepBeep(protos.Empty())
        return r.value
    def show_toast(self, text, duration=ToastDuration.TD_SHORT):
        """
        在系统界面底部显示一个 Toast 消息
        """
        req = protos.ShowToastRequest(text=text, duration=duration)
        r = self.stub.showToast(req)
        return r.value
    def setprop(self, name, value):
        """
        设置系统属性（aka: setprop，支持设置 ro.xx 只读属性）
        """
        req = protos.SetPropRequest(name=name, value=value)
        r = self.stub.setProp(req)
        return r.value
    def getprop(self, name):
        """
        获取系统属性（aka: getprop）
        """
        req = protos.String(value=name)
        r = self.stub.getProp(req)
        return r.value


class DebugStub(BaseServiceStub):
    def _read_pubkey(self, pubkey):
        with open(pubkey, "rb") as fd:
            return fd.read()
    def install_adb_pubkey(self, pubkey):
        """
        给内置 adb 服务添加公钥
        """
        req = protos.ADBDConfigRequest()
        req.adb_pubkey = self._read_pubkey(pubkey)
        r = self.stub.installADBPubKey(req)
        return r.value
    def uninstall_adb_pubkey(self, pubkey):
        """
        从内置 adb 服务移除公钥
        """
        req = protos.ADBDConfigRequest()
        req.adb_pubkey = self._read_pubkey(pubkey)
        r = self.stub.uninstallADBPubKey(req)
        return r.value
    def is_android_debug_bridge_running(self):
        """
        远端 adb daemon 是否在运行
        """
        r = self.stub.isAndroidDebugBridgeRunning(protos.Empty())
        return r.value
    def start_android_debug_bridge(self):
        """
        启动内置 adbd (默认随框架启动)
        """
        r = self.stub.startAndroidDebugBridge(protos.Empty())
        return r.value
    def stop_android_debug_bridge(self):
        """
        停止内置 adb daemon
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
        等价于 settings get system xxxx
        """
        return self._get(Group.GROUP_SYSTEM, name)
    def put_system(self, name, value):
        """
        等价于 settings put system xxxx xxxx
        """
        return self._put(Group.GROUP_SYSTEM, name, value)
    def get_global(self, name):
        """
        等价于 settings get global xxxx
        """
        return self._get(Group.GROUP_GLOBAL, name)
    def put_global(self, name, value):
        """
        等价于 settings put global xxxx xxxx
        """
        return self._put(Group.GROUP_GLOBAL, name, value)
    def get_secure(self, name):
        """
        等价于 settings get secure xxxx
        """
        return self._get(Group.GROUP_SECURE, name)
    def put_secure(self, name, value):
        """
        等价于 settings put secure xxxx xxxx
        """
        return self._put(Group.GROUP_SECURE, name, value)


class ShellStub(BaseServiceStub):
    def execute_script(self, script, alias=None,
                                    timeout=60):
        """
        前台执行一段脚本（支持标准的多行脚本）
        """
        req = protos.ShellRequest(name=alias, script=script,
                                            timeout=timeout)
        r = self.stub.executeForeground(req)
        return r
    def execute_background_script(self, script, alias=None):
        """
        后台执行一段脚本（支持标准的多行脚本）
        """
        req = protos.ShellRequest(name=alias, script=script)
        r = self.stub.executeBackground(req)
        return r.tid
    def is_background_script_finished(self, tid):
        """
        后台脚本是否已经结束
        """
        req = protos.ShellTask(tid=tid)
        r = self.stub.isBackgroundFinished(req)
        return r.value
    def kill_background_script(self, tid):
        """
        强行停止后台脚本
        """
        req = protos.ShellTask(tid=tid)
        r = self.stub.killBackground(req)
        return r.value


class StatusStub(BaseServiceStub):
    def get_boot_time(self):
        """
        获取设备启动时间 Unix 时间戳
        """
        r = self.stub.getBootTime(protos.Empty())
        return r.value
    def get_disk_usage(self, mountpoint="/data"):
        """
        获取分区数据使用情况
        """
        req = protos.String(value=mountpoint)
        r = self.stub.getDiskUsage(req)
        return r
    def get_battery_info(self):
        """
        获取电池信息
        """
        r = self.stub.getBatteryInfo(protos.Empty())
        return r
    def get_cpu_info(self):
        """
        获取 CPU 用量等信息
        """
        r = self.stub.getCpuInfo(protos.Empty())
        return r
    def get_overall_disk_io_info(self):
        """
        获取全局的设备磁盘读写状况
        """
        r = self.stub.getOverallDiskIOInfo(protos.Empty())
        return r
    def get_overall_net_io_info(self):
        """
        获取全局的设备网络收发状况
        """
        r = self.stub.getOverallNetIOInfo(protos.Empty())
        return r
    def get_userdata_disk_io_info(self):
        """
        获取用户数据设备磁盘读写状况
        """
        r = self.stub.getUserDataDiskIOInfo(protos.Empty())
        return r
    def get_net_io_info(self, interface):
        """
        获取特定接口的网络收发状况
        """
        req = protos.String(value=interface)
        r = self.stub.getNetIOInfo(req)
        return r
    def get_mem_info(self):
        """
        获取设备内存状况
        """
        r = self.stub.getMemInfo(protos.Empty())
        return r


class ProxyStub(BaseServiceStub):
    def is_openvpn_running(self):
        """
        检查 OPENVPN 是否正在运行
        """
        r = self.stub.isOpenVPNRunning(protos.Empty())
        return r.value
    def is_gproxy_running(self):
        """
        检查 GPROXY 是否正在运行
        """
        r = self.stub.isGproxyRunning(protos.Empty())
        return r.value
    def start_openvpn(self, profile):
        """
        启动 OPENVPN
        """
        checkArgumentTyp(profile, OpenVPNProfile)
        r = self.stub.startOpenVPN(profile)
        return r.value
    def start_gproxy(self, profile):
        """
        启动 GPROXY
        """
        checkArgumentTyp(profile, GproxyProfile)
        r = self.stub.startGproxy(profile)
        return r.value
    def stop_openvpn(self):
        """
        停止 OPENVPN
        """
        r = self.stub.stopOpenVPN(protos.Empty())
        return r.value
    def stop_gproxy(self):
        """
        停止 GPROXY
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
        获取当前 selinux enforce 状态
        """
        r = self.stub.getEnforce(protos.Empty())
        return r.value
    def set_enforce(self, enforced=True):
        """
        设置当前 selinux enforce 状态 (aka: setenforce 0/1)
        """
        req = protos.Boolean(value=enforced)
        r = self.stub.setEnforce(req)
        return r.value
    def enabled(self):
        """
        获取设备上的 selinux 是否已经启用
        """
        r = self.stub.isEnabled(protos.Empty())
        return r.value
    def enforce(self, name):
        """
        设置一个域为 enforce
        """
        req = protos.String(value=name)
        r = self.stub.policySetEnforce(req)
        return r.value
    def permissive(self, name):
        """
        设置一个域为 permissive
        """
        req = protos.String(value=name)
        r = self.stub.policySetPermissive(req)
        return r.value
    def create_domain(self, name):
        """
        新建一个 selinux 域
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
        从设备下载文件到文件描述符
        """
        req = protos.FileRequest(path=fpath)
        iterator = self.stub.downloadFile(req)
        self._fd_streaming_recv(fd, iterator)
        st = self.file_stat(fpath)
        return st
    def upload_fd(self, fd, dest):
        """
        上传文件描述符至设备
        """
        chunksize = 1024*1024*1
        streaming = self._fd_streaming_send(fd, dest,
                                              chunksize)
        self.stub.uploadFile(streaming)
        st = self.file_stat(dest)
        return st
    def download_file(self, fpath, dest):
        """
        从设备下载文件到本地
        """
        with io.open(dest, mode="wb") as fd:
            return self.download_fd(fpath, fd)
    def upload_file(self, fpath, dest):
        """
        上传本地文件至设备
        """
        with io.open(fpath, mode="rb") as fd:
            return self.upload_fd(fd, dest)
    def delete_file(self, fpath):
        """
        删除设备上的文件
        """
        req = protos.FileRequest(path=fpath)
        r = self.stub.deleteFile(req)
        return r.value
    def file_chmod(self, fpath, mode=0o644):
        """
        更改设备上文件的权限
        """
        req = protos.FileRequest(path=fpath, mode=mode)
        r = self.stub.fileChmod(req)
        return r
    def file_stat(self, fpath):
        """
        获取设备上文件的信息
        """
        req = protos.FileRequest(path=fpath)
        r = self.stub.fileStat(req)
        return r


class LockStub(BaseServiceStub):
    def acquire_lock(self, leaseTime=60):
        """
        获取用于控制设备的锁，成功返回 true，被占用则会引发异常提示
        """
        req = protos.Integer(value=leaseTime)
        r = self.stub.acquireLock(req)
        return r.value
    def get_session_token(self):
        """
        获取当前会话的动态令牌
        """
        r = self.stub.getSessionToken(protos.Empty())
        return r.value
    def refresh_lock(self, leaseTime=60):
        """
        刷新用于控制设备的锁，应该在定时任务每60s内调用以保持会话
        """
        req = protos.Integer(value=leaseTime)
        r = self.stub.refreshLock(req)
        return r.value
    def release_lock(self):
        """
        释放控制设备的锁，释放后该设备可被其他客户端控制
        """
        r = self.stub.releaseLock(protos.Empty())
        return r.value


class WifiStub(BaseServiceStub):
    def status(self):
        """
        获取当前已连接 WIFI 的信息
        """
        r = self.stub.status(protos.Empty())
        return r
    def blacklist_add(self, bssid):
        """
        将 BSSID 加入 WIFI BSSID 黑名单（将不会在WIFI列表显示）
        """
        r = self.stub.blacklistAdd(protos.String(value=bssid))
        return r.value
    def blacklist_clear(self):
        """
        清空 WIFI BSSID 黑名单
        """
        r = self.stub.blacklistClear(protos.Empty())
        return r.value
    def blacklist_get_all(self):
        """
        获取在 WIFI BSSID 黑名单中的所有 BSSID
        """
        r = self.stub.blacklistAll(protos.Empty())
        return r.bssids
    def scan(self):
        """
        请求扫描附近 WIFI
        """
        r = self.stub.scan(protos.Empty())
        return r.value
    def scan_results(self):
        """
        获取已扫描到的附近 WIFI
        """
        r = self.stub.scanResults(protos.Empty())
        return r.stations
    def get_mac_addr(self):
        """
        获取当前 WIFI 的 MAC 地址
        """
        r = self.stub.getMacAddr(protos.Empty())
        return r.value
    def signal_poll(self):
        """
        获取当前已连接 WIFI 的信号强度等信息
        """
        r = self.stub.signalPoll(protos.Empty())
        return r
    def list_networks(self):
        """
        列出已连接过的 WIFI 网络
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
        断开 WIFI 连接
        """
        r = self.stub.disconnect(protos.Empty())
        return r.value
    def reconnect(self):
        """
        重连 WIFI
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
                                    **kwargs):
        self.elements = elements
        self.index = kwargs.pop("index", 0)
        self.func, self.rule = kwargs.popitem()
        self.match = getattr(self, self.func)
        self.device = device
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
        return self.device.screenshot(quality,
                            bound=item["bound"])
    def _click(self, item):
        point = item["bound"].center()
        return self.device.click(point)
    def __str__(self):
        return "Ocr: {}={}".format(self.func, self.rule)
    __repr__ = __str__
    def exists(self):
        """
        OCR - 检查元素是否存在
        """
        return bool(self.find_target_item())
    def click(self):
        """
        OCR - 点击元素（不存在则报错）
        """
        return self.find_or_throw_cb(self._click)
    def click_exists(self):
        """
        OCR - 点击元素（不存在将不会产生异常）
        """
        return self.find_cb(self._click, False)
    def screenshot(self, quality=100):
        """
        OCR - 对元素进行截图
        """
        return self.find_or_throw_cb(self._screenshot,
                                            quality)
    def take_screenshot(self, quality=100):
        """
        OCR - 对元素进行截图
        """
        return self.screenshot(quality)
    def info(self):
        """
        OCR - 获取匹配元素的信息
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
        option["grpc.keepalive_time_ms"] = 30*1000
        option["grpc.keepalive_timeout_ms"] = 15*1000
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
    def _get_service_stub(self, module):
        stub = getattr(services, "{0}Stub".format(module))
        return stub(self.channel)
    def stub(self, module):
        modu = sys.modules[__name__]
        stub = self._get_service_stub(module)
        wrap = getattr(modu, "{0}Stub".format(module))
        inst = getattr(self, module, wrap(stub))
        self.__setattr__(module, inst)
        return inst
    # 快速调用: File
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
    # 快速调用: Application
    def install_local_file(self, rpath):
        return self.stub("Application").install_local_file(rpath)
    def current_application(self):
        return self.stub("Application").current_application()
    def enumerate_all_pkg_names(self):
        return self.stub("Application").enumerate_all_pkg_names()
    def enumerate_running_processes(self):
        return self.stub("Application").enumerate_running_processes()
    def get_last_activities(self, count=3):
        return self.stub("Application").get_last_activities(count=count)
    def start_activity(self, **activity):
        return self.stub("Application").start_activity(**activity)
    def get_application_by_name(self, name):
        return self.stub("Application").get_application_by_name(name)
    def application(self, applicationId, user=0):
        return self.stub("Application")(applicationId, user=user)
    # 快速调用: Util
    def record_touch(self):
        return self.stub("Util").record_touch()
    def perform_touch(self, sequence, wait=True):
        return self.stub("Util").perform_touch(sequence, wait=wait)
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
    def setprop(self, name, value):
        return self.stub("Util").setprop(name, value)
    def getprop(self, name):
        return self.stub("Util").getprop(name)
    # 快速调用: Debug
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
    # 快速调用: Proxy
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
    # 快速调用: Shell
    def execute_script(self, script, alias=None, timeout=60):
        return self.stub("Shell").execute_script(script, alias=alias,
                                                        timeout=timeout)
    def execute_background_script(self, script, alias=None):
        return self.stub("Shell").execute_background_script(script, alias=alias)
    def is_background_script_finished(self, tid):
        return self.stub("Shell").is_background_script_finished(tid)
    def kill_background_script(self, tid):
        return self.stub("Shell").kill_background_script(tid)
    # 快速调用: UiAutomator
    def click(self, point):
        return self.stub("UiAutomator").click(point)
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
    def get_applied_watchers(self):
        return self.stub("UiAutomator").get_applied_watchers()
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
    def __call__(self, **kwargs):
        return self.stub("UiAutomator")(**kwargs)
    # OCR 功能扩展
    def ocr(self, index=0, **kwargs):
        if not isinstance(self._ocr, OcrEngine):
            raise IllegalStateException("Ocr engine is not setted up")
        if any(r not in ["text", "textContains", "textMatches"] \
                                        for r in kwargs.keys()):
            raise InvalidArgumentError("Only text* matches are supported")
        if len(kwargs) != 1:
            raise InvalidArgumentError("Only or at least one rule can be used")
        image = self.screenshot(self._ocr_img_quality)
        return OcrOperator(self,
        elements=self._ocr.ocr(image),
                            index=index,
                            **kwargs
        )
    def setup_ocr_backend(self, service, *args, quality=75,
                                                **kwargs):
        self._ocr_img_quality = quality
        self._ocr = OcrEngine(service, *args,
                                    **kwargs)
    # 日志打印
    def set_debug_log_enabled(self, enable):
        level = logging.DEBUG if enable else logging.WARN
        logger.setLevel(level)
        return enable
    # 接口锁定
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
    parser.add_argument("-device", type=str, default="localhost",
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