# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.VOrderedLayout import (VOrderedLayout,)


class VHorizontalLayout(VOrderedLayout):
    CLASSNAME = 'v-horizontallayout'

    def __init__(self):
        super(VHorizontalLayout, self)(self.CLASSNAME, self.ORIENTATION_HORIZONTAL)
