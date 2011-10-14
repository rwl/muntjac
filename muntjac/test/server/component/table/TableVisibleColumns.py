# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.table.TableGenerator import (TableGenerator,)
# from org.junit.Assert.assertArrayEquals import (assertArrayEquals,)
# from org.junit.Test import (Test,)


class TableVisibleColumns(object):
    _defaultColumns3 = ['Property 0', 'Property 1', 'Property 2']

    def defaultVisibleColumns(self):
        _0 = True
        properties = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                properties += 1
            if not (properties < 10):
                break
            t = TableGenerator.createTableWithDefaultContainer(properties, 10)
            expected = [None] * properties
            _1 = True
            i = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    i += 1
                if not (i < properties):
                    break
                expected[i] = 'Property ' + i
            self.org.junit.Assert.assertArrayEquals('getVisibleColumns', expected, t.getVisibleColumns())

    def explicitVisibleColumns(self):
        t = TableGenerator.createTableWithDefaultContainer(5, 10)
        newVisibleColumns = ['Property 1', 'Property 2']
        t.setVisibleColumns(newVisibleColumns)
        assertArrayEquals('Explicit visible columns, 5 properties', newVisibleColumns, t.getVisibleColumns())

    def invalidVisibleColumnIds(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 10)
        # OK, expected
        try:
            t.setVisibleColumns(['a', 'Property 2', 'Property 3'])
            self.junit.framework.Assert.fail('IllegalArgumentException expected')
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        assertArrayEquals(self._defaultColumns3, t.getVisibleColumns())

    def duplicateVisibleColumnIds(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 10)
        # OK, expected
        # FIXME: Multiple properties in the Object array should be detected
        # (#6476)
        # assertArrayEquals(defaultColumns3, t.getVisibleColumns());
        try:
            t.setVisibleColumns(['Property 0', 'Property 1', 'Property 2', 'Property 1'])
            # FIXME: Multiple properties in the Object array should be detected
            # (#6476)
            # junit.framework.Assert.fail("IllegalArgumentException expected");
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]

    def noVisibleColumns(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 10)
        t.setVisibleColumns([])
        assertArrayEquals([], t.getVisibleColumns())
