# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.VOrderedLayout import (VOrderedLayout,)


class VVerticalLayout(VOrderedLayout):
    CLASSNAME = 'v-verticallayout'

    def __init__(self):
        super(VVerticalLayout, self)(self.CLASSNAME, self.ORIENTATION_VERTICAL)
