# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.ComponentContainer.ComponentAttachEvent import (ComponentAttachEvent,)
# from com.vaadin.ui.ComponentContainer.ComponentAttachListener import (ComponentAttachListener,)
# from com.vaadin.ui.ComponentContainer.ComponentDetachEvent import (ComponentDetachEvent,)
# from com.vaadin.ui.ComponentContainer.ComponentDetachListener import (ComponentDetachListener,)
# from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
# from com.vaadin.ui.VerticalLayout import (VerticalLayout,)


class TestAbstractComponentContainerListeners(AbstractListenerMethodsTest):

    def testComponentDetachListenerAddGetRemove(self):
        self.testListenerAddGetRemove(HorizontalLayout, ComponentDetachEvent, ComponentDetachListener)

    def testComponentAttachListenerAddGetRemove(self):
        self.testListenerAddGetRemove(VerticalLayout, ComponentAttachEvent, ComponentAttachListener)
