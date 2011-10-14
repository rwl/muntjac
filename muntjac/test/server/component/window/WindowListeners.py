# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.Window import (Window,)
# from com.vaadin.ui.Window.CloseEvent import (CloseEvent,)
# from com.vaadin.ui.Window.CloseListener import (CloseListener,)
# from com.vaadin.ui.Window.ResizeEvent import (ResizeEvent,)
# from com.vaadin.ui.Window.ResizeListener import (ResizeListener,)


class WindowListeners(AbstractListenerMethodsTest):

    def testFocusListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Window, FocusEvent, FocusListener)

    def testBlurListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Window, BlurEvent, BlurListener)

    def testResizeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Window, ResizeEvent, ResizeListener)

    def testCloseListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Window, CloseEvent, CloseListener)
