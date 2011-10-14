# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)


class TestAbstractOrderedLayoutListeners(AbstractListenerMethodsTest):

    def testLayoutClickListenerAddGetRemove(self):
        self.testListenerAddGetRemove(VerticalLayout, LayoutClickEvent, LayoutClickListener)
