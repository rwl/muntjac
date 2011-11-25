# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.VSplitPanel import (VSplitPanel,)


class VSplitPanelVertical(VSplitPanel):

    def __init__(self):
        super(VSplitPanelVertical, self)(VSplitPanel.ORIENTATION_VERTICAL)
