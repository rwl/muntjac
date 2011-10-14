# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.AbstractSplitPanel.SplitterClickEvent import (SplitterClickEvent,)
# from com.vaadin.ui.AbstractSplitPanel.SplitterClickListener import (SplitterClickListener,)
# from com.vaadin.ui.HorizontalSplitPanel import (HorizontalSplitPanel,)


class TestAbstractSplitPanelListeners(AbstractListenerMethodsTest):

    def testSplitterClickListenerAddGetRemove(self):
        self.testListenerAddGetRemove(HorizontalSplitPanel, SplitterClickEvent, SplitterClickListener)
