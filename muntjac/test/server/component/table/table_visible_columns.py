# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
