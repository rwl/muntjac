# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.dd.VDragAndDropManager import (VDragAndDropManager,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VDragSourceIs(VAcceptCriterion):
    """TODO Javadoc!

    @since 6.3
    """

    def accept(self, drag, configuration):
        try:
            component = drag.getTransferable().getDragSource()
            c = configuration.getIntAttribute('c')
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < c):
                    break
                requiredPid = configuration.getStringAttribute('component' + i)
                paintable = VDragAndDropManager.get().getCurrentDropHandler().getApplicationConnection().getPaintable(requiredPid)
                if paintable == component:
                    return True
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        return False
