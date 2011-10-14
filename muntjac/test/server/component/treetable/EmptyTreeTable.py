# -*- coding: utf-8 -*-
# from com.vaadin.ui.TreeTable import (TreeTable,)
# from junit.framework.TestCase import (TestCase,)


class EmptyTreeTable(TestCase):

    def testLastId(self):
        treeTable = TreeTable()
        self.assertFalse(treeTable.isLastId(treeTable.getValue()))
