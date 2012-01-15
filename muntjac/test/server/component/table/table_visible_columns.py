# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from unittest import TestCase

from muntjac.test.server.component.table.table_generator import TableGenerator


class TableVisibleColumns(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self._defaultColumns3 = ['Property 0', 'Property 1', 'Property 2']


    def testDefaultVisibleColumns(self):
        for properties in range(10):
            t = TableGenerator.createTableWithDefaultContainer(properties, 10)
            expected = [None] * properties
            for i in range(properties):
                expected[i] = 'Property %d' % i
            self.assertEquals(expected, t.getVisibleColumns(),
                    'getVisibleColumns')


    def testExplicitVisibleColumns(self):
        t = TableGenerator.createTableWithDefaultContainer(5, 10)
        newVisibleColumns = ['Property 1', 'Property 2']
        t.setVisibleColumns(newVisibleColumns)
        self.assertEquals(newVisibleColumns, t.getVisibleColumns(),
                'Explicit visible columns, 5 properties')


    def testInvalidVisibleColumnIds(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 10)

        try:
            t.setVisibleColumns(['a', 'Property 2', 'Property 3'])
            self.fail('IllegalArgumentException expected')
        except ValueError:
            pass  # OK, expected

        self.assertEquals(self._defaultColumns3, t.getVisibleColumns())


    def testDuplicateVisibleColumnIds(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 10)

        try:
            t.setVisibleColumns(['Property 0', 'Property 1', 'Property 2',
                    'Property 1'])
            # FIXME: Multiple properties in the Object array should be detected
            # (#6476)
            #self.fail("IllegalArgumentException expected")
        except ValueError:
            pass  # OK, expected

        # FIXME: Multiple properties in the Object array should be detected
        # (#6476)
        # assertArrayEquals(defaultColumns3, t.getVisibleColumns());


    def noVisibleColumns(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 10)
        t.setVisibleColumns([])
        self.assertEquals([], t.getVisibleColumns())
