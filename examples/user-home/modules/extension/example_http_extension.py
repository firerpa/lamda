# Copyright 2025 rev1si0n (lamda.devel@gmail.com). All rights reserved.
#
# Distributed under MIT license.
# See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
from lamda.extensions import *

# In order to accommodate users of various technical levels and avoid impacting the operation of the firerpa service, all HTTP rewrite methods must be implemented synchronously. These methods will run within threads and will not block the overall service.
# BaseHttpExtension is based on tornado.web.RequestHandler. If you need to use or override other methods such as set_header, initialize, etc., please refer to the official Tornado documentation.
# It is strongly discouraged to override Tornado-related methods like prepare and initialize.

# If you encounter the There is no current event loop in thread XXX exception, please call self.prepare_loop() in your overridden http_xxx method.

# 为了兼容各种技术层级的使用者以及不影响到 firerpa 服务的运行，所有 HTTP 重写方法均须为同步写法，方法将在线程内运行，不会阻塞整体服务。
# BaseHttpExtension 基于 tornado.web.RequestHandler，如需使用或重写其他方法如 set_header、initialize 等，请参照 tornado 官方文档。
# 我们不建议您重写 tornado 相关 prepare、initialize 方法。

# 如果您遇到 There is no current event loop in thread XXX 异常，请在您重写的 http_xxx 方法中调用 `self.prepare_loop()`

# REF: https://www.tornadoweb.org/en/stable/web.html

class ExampleHttpExtension(BaseHttpExtension):
    route = "/api/v1/hello-world" # API route
    def http_get(self, *args, **kwargs):
        """ GET Method Handler """
        self.write("Hello World")
    def http_post(self, *args, **kwargs):
        """ POST Method Handler """
        self.write("Hello World")
    def http_put(self, *args, **kwargs):
        """ PUT Method Handler """
        self.write("Hello World")
    def http_delete(self, *args, **kwargs):
        """ DELETE Method Handler """
        self.write("Hello World")
    def http_patch(self, *args, **kwargs):
        """ PATCH Method Handler """
        self.write("Hello World")