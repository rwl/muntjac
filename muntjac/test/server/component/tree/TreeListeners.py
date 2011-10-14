# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)


class TreeListeners(AbstractListenerMethodsTest):

    def testExpandListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Tree, ExpandEvent, ExpandListener)

    def testItemClickListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Tree, ItemClickEvent, ItemClickListener)

    def testCollapseListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Tree, CollapseEvent, CollapseListener)
