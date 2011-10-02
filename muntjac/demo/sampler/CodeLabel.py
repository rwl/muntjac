# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
# from com.vaadin.ui.Label import (Label,)


class CodeLabel(Label):

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setContentMode(self.CONTENT_PREFORMATTED)
        elif _1 == 1:
            content, = _0
            super(CodeLabel, self)(content, self.CONTENT_PREFORMATTED)
        else:
            raise ARGERROR(0, 1)

    def setContentMode(self, contentMode):
        if contentMode != self.CONTENT_PREFORMATTED:
            raise self.UnsupportedOperationException('Only preformatted content supported')
        super(CodeLabel, self).setContentMode(self.CONTENT_PREFORMATTED)
