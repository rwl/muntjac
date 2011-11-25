# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.dd.VDragAndDropManager import (VDragAndDropManager,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VSourceIsTarget(VAcceptCriterion):

    def accept(self, drag, configuration):
        dragSource = drag.getTransferable().getDragSource()
        paintable = VDragAndDropManager.get().getCurrentDropHandler().getPaintable()
        return paintable == dragSource
