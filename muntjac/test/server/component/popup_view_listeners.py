# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.popup_view import \
    PopupView, PopupVisibilityEvent, IPopupVisibilityListener

from muntjac.ui.label import Label


class PopupViewListeners(AbstractListenerMethodsTest):

    def testPopupVisibilityListenerAddGetRemove(self):
        self._testListenerAddGetRemove(PopupView, PopupVisibilityEvent,
                IPopupVisibilityListener, PopupView('', Label()))
