# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.TabSheet.SelectedTabChangeEvent import (SelectedTabChangeEvent,)
# from com.vaadin.ui.TabSheet.SelectedTabChangeListener import (SelectedTabChangeListener,)


class TabSheetListeners(AbstractListenerMethodsTest):

    def testSelectedTabChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(TabSheet, SelectedTabChangeEvent, SelectedTabChangeListener)
