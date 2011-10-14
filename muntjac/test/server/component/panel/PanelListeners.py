# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.Panel import (Panel,)


class PanelListeners(AbstractListenerMethodsTest):

    def testClickListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Panel, ClickEvent, ClickListener)
