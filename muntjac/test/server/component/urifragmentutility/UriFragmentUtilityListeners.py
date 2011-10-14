# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.UriFragmentUtility import (UriFragmentUtility,)
# from com.vaadin.ui.UriFragmentUtility.FragmentChangedEvent import (FragmentChangedEvent,)
# from com.vaadin.ui.UriFragmentUtility.FragmentChangedListener import (FragmentChangedListener,)


class UriFragmentUtilityListeners(AbstractListenerMethodsTest):

    def testFragmentChangedListenerAddGetRemove(self):
        self.testListenerAddGetRemove(UriFragmentUtility, FragmentChangedEvent, FragmentChangedListener)
