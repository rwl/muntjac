# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.event.MouseEvents.ClickEvent import (ClickEvent,)
# from com.vaadin.event.MouseEvents.ClickListener import (ClickListener,)
# from com.vaadin.ui.Embedded import (Embedded,)


class EmbeddedListeners(AbstractListenerMethodsTest):

    def testClickListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Embedded, ClickEvent, ClickListener)
