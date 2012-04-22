# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from unittest import TestCase
from muntjac.ui.table import Table


class TableGenerator(TestCase):

    @classmethod
    def createTableWithDefaultContainer(cls, properties, items):
        t = Table()

        for i in range(properties):
            t.addContainerProperty('Property %d' % i, str, None)

        for j in range(items):
            item = t.addItem('Item %d' % j)
            for i in range(properties):
                v = 'Item %d/Property %d' % (j, i)
                item.getItemProperty('Property %d' % i).setValue(v)

        return t


    def testTableGenerator(self):
        t = self.createTableWithDefaultContainer(1, 1)
        self.assertEquals(len(t), 1)
        self.assertEquals(len(t.getContainerPropertyIds()), 1)

        t = self.createTableWithDefaultContainer(100, 50)
        self.assertEquals(len(t), 50)
        self.assertEquals(len(t.getContainerPropertyIds()), 100)
