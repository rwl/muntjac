# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
from com.vaadin.event.Action import (Listener,)
from com.vaadin.event.ShortcutAction import (ShortcutAction,)
# from com.vaadin.event.Action.Listener import (Listener,)


class ShortcutListener(ShortcutAction, Listener):
    _serialVersionUID = 1L

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            shorthandCaption, = _0
            super(ShortcutListener, self)(shorthandCaption)
        elif _1 == 2:
            shorthandCaption, modifierKeys = _0
            super(ShortcutListener, self)(shorthandCaption, modifierKeys)
        elif _1 == 3:
            caption, keyCode, modifierKeys = _0
            super(ShortcutListener, self)(caption, keyCode, modifierKeys)
        elif _1 == 4:
            caption, icon, keyCode, modifierKeys = _0
            super(ShortcutListener, self)(caption, icon, keyCode, modifierKeys)
        else:
            raise ARGERROR(1, 4)

    def handleAction(self, sender, target):
        pass
