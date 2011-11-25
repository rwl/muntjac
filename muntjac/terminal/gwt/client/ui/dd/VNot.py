# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriteria import (VAcceptCriteria,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCallback import (VAcceptCallback,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VNot(VAcceptCriterion):
    """TODO implementation could now be simplified/optimized"""
    _b1 = None
    _crit1 = None

    def accept(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 2:
            drag, configuration = _0
            return False
            # not used
        elif _1 == 3:
            drag, configuration, callback = _0
            if self._crit1 is None:
                self._crit1 = self.getCriteria(drag, configuration, 0)
                if self._crit1 is None:
                    VConsole.log('Not criteria didn\'t found a child criteria')
                    return
            self._b1 = False

            class accept1cb(VAcceptCallback):

                def accepted(self, event):
                    VNot_this._b1 = True

            self._crit1.accept(drag, configuration.getChildUIDL(0), accept1cb)
            if not self._b1:
                callback.accepted(drag)
        else:
            raise ARGERROR(2, 3)

    def getCriteria(self, drag, configuration, i):
        childUIDL = configuration.getChildUIDL(i)
        return VAcceptCriteria.get(childUIDL.getStringAttribute('name'))

    def needsServerSideCheck(self, drag, criterioUIDL):
        return False
        # TODO enforce on server side
