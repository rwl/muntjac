# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.VSplitPanel import (VSplitPanel,)


class VSplitPanelHorizontal(VSplitPanel):

    def __init__(self):
        super(VSplitPanelHorizontal, self)(VSplitPanel.ORIENTATION_HORIZONTAL)
