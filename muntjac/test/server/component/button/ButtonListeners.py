# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.Button.ClickListener import (ClickListener,)


class ButtonListeners(AbstractListenerMethodsTest):

    def testFocusListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Button, FocusEvent, FocusListener)

    def testBlurListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Button, BlurEvent, BlurListener)

    def testClickListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Button, ClickEvent, ClickListener)
