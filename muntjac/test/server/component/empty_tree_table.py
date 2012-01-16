# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from unittest import TestCase

from muntjac.ui.tree_table import TreeTable


class EmptyTreeTable(TestCase):

    def testLastId(self):
        treeTable = TreeTable()
        self.assertFalse(treeTable.isLastId(treeTable.getValue()))
