# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.test.server.component.table.TableGenerator import (TableGenerator,)
# from org.junit.Assert.assertArrayEquals import (assertArrayEquals,)
# from org.junit.Test import (Test,)


class TableColumnAlignments(object):

    def defaultColumnAlignments(self):
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
                expected[i] = Table.ALIGN_LEFT
            self.org.junit.Assert.assertArrayEquals('getColumnAlignments', expected, t.getColumnAlignments())

    def explicitColumnAlignments(self):
        properties = 5
        t = TableGenerator.createTableWithDefaultContainer(properties, 10)
        explicitAlignments = [Table.ALIGN_CENTER, Table.ALIGN_LEFT, Table.ALIGN_RIGHT, Table.ALIGN_RIGHT, Table.ALIGN_LEFT]
        t.setColumnAlignments(explicitAlignments)
        assertArrayEquals('Explicit visible columns, 5 properties', explicitAlignments, t.getColumnAlignments())

    def invalidColumnAlignmentStrings(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 7)
        defaultAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT]
        # Ok, expected
        try:
            t.setColumnAlignments(['a', 'b', 'c'])
            self.junit.framework.Assert.fail('No exception thrown for invalid array length')
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        assertArrayEquals('Invalid change affected alignments', defaultAlignments, t.getColumnAlignments())

    def invalidColumnAlignmentString(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 7)
        defaultAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT]
        # Ok, expected
        try:
            t.setColumnAlignment('Property 1', 'a')
            self.junit.framework.Assert.fail('No exception thrown for invalid array length')
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        assertArrayEquals('Invalid change affected alignments', defaultAlignments, t.getColumnAlignments())

    def columnAlignmentForPropertyNotInContainer(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 7)
        defaultAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT]
        # Ok, expected
        try:
            t.setColumnAlignment('Property 1200', Table.ALIGN_LEFT)
            # FIXME: Uncomment as there should be an exception (#6475)
            # junit.framework.Assert
            # .fail("No exception thrown for property not in container");
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        assertArrayEquals('Invalid change affected alignments', defaultAlignments, t.getColumnAlignments())
        # FIXME: Uncomment as null should be returned (#6474)
        # junit.framework.Assert.assertEquals(
        # "Column alignment for property not in container returned",
        # null, t.getColumnAlignment("Property 1200"));

    def invalidColumnAlignmentsLength(self):
        t = TableGenerator.createTableWithDefaultContainer(7, 7)
        defaultAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT]
        # Ok, expected
        try:
            t.setColumnAlignments([Table.ALIGN_LEFT])
            self.junit.framework.Assert.fail('No exception thrown for invalid array length')
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        assertArrayEquals('Invalid change affected alignments', defaultAlignments, t.getColumnAlignments())
        # Ok, expected
        try:
            t.setColumnAlignments([])
            self.junit.framework.Assert.fail('No exception thrown for invalid array length')
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        assertArrayEquals('Invalid change affected alignments', defaultAlignments, t.getColumnAlignments())
        # Ok, expected
        try:
            t.setColumnAlignments([Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT])
            self.junit.framework.Assert.fail('No exception thrown for invalid array length')
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        assertArrayEquals('Invalid change affected alignments', defaultAlignments, t.getColumnAlignments())

    def explicitColumnAlignmentOneByOne(self):
        properties = 5
        t = TableGenerator.createTableWithDefaultContainer(properties, 10)
        explicitAlignments = [Table.ALIGN_CENTER, Table.ALIGN_LEFT, Table.ALIGN_RIGHT, Table.ALIGN_RIGHT, Table.ALIGN_LEFT]
        currentAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT]
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < properties):
                break
            t.setColumnAlignment('Property ' + i, explicitAlignments[i])
            currentAlignments[i] = explicitAlignments[i]
            assertArrayEquals('Explicit visible columns, ' + i + ' alignments set', currentAlignments, t.getColumnAlignments())
