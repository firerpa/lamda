# Copyright 2022 rev1si0n (ihaven0emmail@gmail.com). All rights reserved.
#
# Distributed under MIT license.
# See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
import io
import codecs

__all__ = ["AttributeDict", "BytesIO"]


class AttributeDict(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value
    def remove(self, key):
        key in self and self.pop(key)


class BytesIO(io.BytesIO):
    @classmethod
    def decode_from(cls, data, encoding):
        return cls(codecs.decode(data, encoding))
    def encode(self, encoding):
        return codecs.encode(self.getvalue(), encoding)
    def decode(self, encoding):
        return codecs.decode(self.getvalue(), encoding)
    def save(self, fpath):
        with open(fpath, "wb") as fd:
            return fd.write(self.getvalue())
    @classmethod
    def load(cls, fpath):
        with open(fpath, "rb") as fd:
            return cls(fd.read())
