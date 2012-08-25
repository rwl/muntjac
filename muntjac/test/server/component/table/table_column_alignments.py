# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

from unittest import TestCase

from muntjac.test.server.component.table.table_generator import TableGenerator
from muntjac.ui.table import Table


class TableColumnAlignments(TestCase):

    def testDefaultColumnAlignments(self):
        for properties in range(10):
            t = TableGenerator.createTableWithDefaultContainer(properties, 10)
            expected = [None] * properties
            for i in range(properties):
                expected[i] = Table.ALIGN_LEFT
            self.assertEquals(expected, t.getColumnAlignments(),
                    'getColumnAlignments')


    def testExplicitColumnAlignments(self):
        properties = 5
        t = TableGenerator.createTableWithDefaultContainer(properties, 10)
        explicitAlignments = [Table.ALIGN_CENTER, Table.ALIGN_LEFT,
                Table.ALIGN_RIGHT, Table.ALIGN_RIGHT, Table.ALIGN_LEFT]
        t.setColumnAlignments(explicitAlignments)
        self.assertEquals(explicitAlignments, t.getColumnAlignments(),
                'Explicit visible columns, 5 properties')


    def testInvalidColumnAlignmentStrings(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 7)
        defaultAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT,
                Table.ALIGN_LEFT]

        try:
            t.setColumnAlignments(['a', 'b', 'c'])
            self.fail('No exception thrown for invalid array length')
        except ValueError:
            pass  # Ok, expected

        self.assertEquals(defaultAlignments, t.getColumnAlignments(),
                'Invalid change affected alignments')


    def testInvalidColumnAlignmentString(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 7)
        defaultAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT,
                Table.ALIGN_LEFT]

        try:
            t.setColumnAlignment('Property 1', 'a')
            self.fail('No exception thrown for invalid array length')
        except ValueError:
            pass  # Ok, expected

        self.assertEquals(defaultAlignments, t.getColumnAlignments(),
                'Invalid change affected alignments')


    def testColumnAlignmentForPropertyNotInContainer(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 7)
        defaultAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT,
                Table.ALIGN_LEFT]

        try:
            t.setColumnAlignment('Property 1200', Table.ALIGN_LEFT)
            # FIXME: Uncomment as there should be an exception (#6475)
            #self.fail("No exception thrown for property not in container")
        except ValueError:
            pass  # Ok, expected

        self.assertEquals(defaultAlignments, t.getColumnAlignments(),
                'Invalid change affected alignments')

        # FIXME: Uncomment as null should be returned (#6474)
        # self.assertEquals(
        # None, t.getColumnAlignment("Property 1200"),
        # "Column alignment for property not in container returned")


    def testInvalidColumnAlignmentsLength(self):
        t = TableGenerator.createTableWithDefaultContainer(7, 7)
        defaultAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT,
                Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT,
                Table.ALIGN_LEFT, Table.ALIGN_LEFT]

        try:
            t.setColumnAlignments([Table.ALIGN_LEFT])
            self.fail('No exception thrown for invalid array length')
        except ValueError:
            pass  # Ok, expected

        self.assertEquals(defaultAlignments, t.getColumnAlignments(),
                'Invalid change affected alignments')

        try:
            t.setColumnAlignments([])
            self.fail('No exception thrown for invalid array length')
        except ValueError:
            pass  # Ok, expected

        self.assertEquals(defaultAlignments, t.getColumnAlignments(),
                'Invalid change affected alignments')

        try:
            t.setColumnAlignments([Table.ALIGN_LEFT, Table.ALIGN_LEFT,
                    Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT,
                    Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT])
            self.fail('No exception thrown for invalid array length')
        except ValueError:
            pass  # Ok, expected

        self.assertEquals(defaultAlignments, t.getColumnAlignments(),
                'Invalid change affected alignments')


    def testExplicitColumnAlignmentOneByOne(self):
        properties = 5
        t = TableGenerator.createTableWithDefaultContainer(properties, 10)
        explicitAlignments = [Table.ALIGN_CENTER, Table.ALIGN_LEFT,
                Table.ALIGN_RIGHT, Table.ALIGN_RIGHT, Table.ALIGN_LEFT]

        currentAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT,
                Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT]

        for i in range(properties):
            t.setColumnAlignment('Property %d' % i, explicitAlignments[i])
            currentAlignments[i] = explicitAlignments[i]
            self.assertEquals(currentAlignments, t.getColumnAlignments(),
                    'Explicit visible columns, %d alignments set' % i)
