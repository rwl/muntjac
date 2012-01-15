# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.window import \
    Window, ResizeEvent, IResizeListener, CloseEvent, ICloseListener

from muntjac.event.field_events import \
    FocusEvent, IFocusListener, BlurEvent, IBlurListener


class WindowListeners(AbstractListenerMethodsTest):

    def testFocusListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Window, FocusEvent, IFocusListener)


    def testBlurListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Window, BlurEvent, IBlurListener)


    def testResizeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Window, ResizeEvent, IResizeListener)


    def testCloseListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Window, CloseEvent, ICloseListener)
