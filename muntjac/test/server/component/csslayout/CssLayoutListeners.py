# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.CssLayout import (CssLayout,)


class CssLayoutListeners(AbstractListenerMethodsTest):

    def testLayoutClickListenerAddGetRemove(self):
        self.testListenerAddGetRemove(CssLayout, LayoutClickEvent, LayoutClickListener)
