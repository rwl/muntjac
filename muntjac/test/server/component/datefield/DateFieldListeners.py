# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.DateField import (DateField,)


class DateFieldListeners(AbstractListenerMethodsTest):

    def testFocusListenerAddGetRemove(self):
        self.testListenerAddGetRemove(DateField, FocusEvent, FocusListener)

    def testBlurListenerAddGetRemove(self):
        self.testListenerAddGetRemove(DateField, BlurEvent, BlurListener)
