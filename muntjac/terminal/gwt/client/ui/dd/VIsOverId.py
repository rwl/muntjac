# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.dd.VDragAndDropManager import (VDragAndDropManager,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VIsOverId(VAcceptCriterion):

    def accept(self, drag, configuration):
        try:
            pid = configuration.getStringAttribute('s')
            paintable = VDragAndDropManager.get().getCurrentDropHandler().getPaintable()
            pid2 = VDragAndDropManager.get().getCurrentDropHandler().getApplicationConnection().getPid(paintable)
            if pid2 == pid:
                searchedId = drag.getDropDetails().get('itemIdOver')
                stringArrayAttribute = configuration.getStringArrayAttribute('keys')
                for string in stringArrayAttribute:
                    if string == searchedId:
                        return True
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        return False
