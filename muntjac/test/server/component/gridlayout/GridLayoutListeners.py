# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.GridLayout import (GridLayout,)


class GridLayoutListeners(AbstractListenerMethodsTest):

    def testLayoutClickListenerAddGetRemove(self):
        self.testListenerAddGetRemove(GridLayout, LayoutClickEvent, LayoutClickListener)
