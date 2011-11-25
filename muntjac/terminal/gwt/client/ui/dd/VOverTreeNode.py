# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VOverTreeNode(VAcceptCriterion):

    def accept(self, drag, configuration):
        containsKey = drag.getDropDetails().get('itemIdOverIsNode')
        return containsKey is not None and containsKey.booleanValue()
