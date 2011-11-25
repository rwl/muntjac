# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriteria import (VAcceptCriteria,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCallback import (VAcceptCallback,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VAnd(VAcceptCriterion, VAcceptCallback):
    _b1 = None

    @classmethod
    def getCriteria(cls, drag, configuration, i):
        childUIDL = configuration.getChildUIDL(i)
        return VAcceptCriteria.get(childUIDL.getStringAttribute('name'))

    def accept(self, drag, configuration):
        childCount = configuration.getChildCount()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < childCount):
                break
            crit = self.getCriteria(drag, configuration, i)
            self._b1 = False
            crit.accept(drag, configuration.getChildUIDL(i), self)
            if not self._b1:
                return False
        return True

    def accepted(self, event):
        self._b1 = True
