# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.dd.VDragAndDropManager import (VDragAndDropManager,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VItemIdIs(VAcceptCriterion):

    def accept(self, drag, configuration):
        try:
            pid = configuration.getStringAttribute('s')
            dragSource = drag.getTransferable().getDragSource()
            pid2 = VDragAndDropManager.get().getCurrentDropHandler().getApplicationConnection().getPid(dragSource)
            if pid2 == pid:
                searchedId = drag.getTransferable().getData('itemId')
                stringArrayAttribute = configuration.getStringArrayAttribute('keys')
                for string in stringArrayAttribute:
                    if string == searchedId:
                        return True
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        return False
