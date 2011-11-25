# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VContainsDataFlavor(VAcceptCriterion):

    def accept(self, drag, configuration):
        name = configuration.getStringAttribute('p')
        return drag.getTransferable().getDataFlavors().contains(name)
