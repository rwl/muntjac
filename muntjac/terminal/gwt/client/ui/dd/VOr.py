# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCallback import (VAcceptCallback,)
from com.vaadin.terminal.gwt.client.ui.dd.VAnd import (VAnd,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VOr(VAcceptCriterion, VAcceptCallback):
    _accepted = None

    def accept(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 2:
            drag, configuration = _0
            return False
            # not used here
        elif _1 == 3:
            drag, configuration, callback = _0
            childCount = configuration.getChildCount()
            self._accepted = False
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < childCount):
                    break
                crit = VAnd.getCriteria(drag, configuration, i)
                crit.accept(drag, configuration.getChildUIDL(i), self)
                if self._accepted == True:
                    callback.accepted(drag)
                    return
        else:
            raise ARGERROR(2, 3)

    def needsServerSideCheck(self, drag, criterioUIDL):
        return False

    def accepted(self, event):
        self._accepted = True
