# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.PopupView import (PopupView,)
# from com.vaadin.ui.PopupView.PopupVisibilityEvent import (PopupVisibilityEvent,)
# from com.vaadin.ui.PopupView.PopupVisibilityListener import (PopupVisibilityListener,)


class PopupViewListeners(AbstractListenerMethodsTest):

    def testPopupVisibilityListenerAddGetRemove(self):
        self.testListenerAddGetRemove(PopupView, PopupVisibilityEvent, PopupVisibilityListener, PopupView('', Label()))
