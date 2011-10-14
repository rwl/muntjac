# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.OptionGroup import (OptionGroup,)


class OptionGroupListeners(AbstractListenerMethodsTest):

    def testFocusListenerAddGetRemove(self):
        self.testListenerAddGetRemove(OptionGroup, FocusEvent, FocusListener)

    def testBlurListenerAddGetRemove(self):
        self.testListenerAddGetRemove(OptionGroup, BlurEvent, BlurListener)
