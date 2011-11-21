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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from unittest import TestCase
from muntjac.ui.table import Table
from muntjac.ui.abstract_select import MultiSelectMode
from muntjac.data.util.indexed_container import IndexedContainer


class TestMultipleSelection(TestCase):

    def testSetMultipleItems(self):
        """Tests weather the multiple select mode is set when using
        Table.set"""
        table = Table('', self.createTestContainer())

        # Tests if multiple selection is set
        table.setMultiSelect(True)
        self.assertTrue(table.isMultiSelect())

        # Test multiselect by setting several items at once
        table.setValue(['1', '3'])
        self.assertEquals(2, len(table.getValue()))


    def testSetMultiSelectMode(self):
        """Tests setting the multiselect mode of the Table. The multiselect
        mode affects how mouse selection is made in the table by the user.
        """
        table = Table('', self.createTestContainer())

        # Default multiselect mode should be MultiSelectMode.DEFAULT
        self.assertEquals(MultiSelectMode.DEFAULT, table.getMultiSelectMode())

        # Tests if multiselectmode is set
        table.setMultiSelectMode(MultiSelectMode.SIMPLE)
        self.assertEquals(MultiSelectMode.SIMPLE, table.getMultiSelectMode())


    def createTestContainer(self):
        """Creates a testing container for the tests

        @return: A new container with test items
        """
        container = IndexedContainer(['1', '2', '3', '4'])
        return container
