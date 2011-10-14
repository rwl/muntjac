# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.Select import (Select,)


class SelectListeners(AbstractListenerMethodsTest):

    def testFocusListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Select, FocusEvent, FocusListener)

    def testBlurListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Select, BlurEvent, BlurListener)
