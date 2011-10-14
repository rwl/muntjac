# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.event.LayoutEvents.LayoutClickEvent import (LayoutClickEvent,)
# from com.vaadin.event.LayoutEvents.LayoutClickListener import (LayoutClickListener,)


class AbsoluteLayoutListeners(AbstractListenerMethodsTest):

    def testLayoutClickListenerAddGetRemove(self):
        self.testListenerAddGetRemove(AbsoluteLayout, LayoutClickEvent, LayoutClickListener)
