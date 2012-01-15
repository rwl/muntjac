# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.button import Button, ClickEvent, IClickListener

from muntjac.event.field_events import FocusEvent, IFocusListener, BlurEvent,\
    IBlurListener


class ButtonListeners(AbstractListenerMethodsTest):

    def testFocusListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Button, FocusEvent, IFocusListener)


    def testBlurListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Button, BlurEvent, IBlurListener)


    def testClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Button, ClickEvent, IClickListener)
