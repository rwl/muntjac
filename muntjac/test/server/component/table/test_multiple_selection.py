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
