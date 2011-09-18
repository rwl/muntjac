# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)


class UploadException(Exception):

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Exception):
                e, = _0
                super(UploadException, self)('Upload failed', e)
            else:
                msg, = _0
                super(UploadException, self)(msg)
        else:
            raise ARGERROR(1, 1)
