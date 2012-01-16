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
from muntjac.data.util.indexed_container import IndexedContainer


class TestFooter(TestCase):
    """Test case for testing the footer API"""

    def testFooterVisibility(self):
        """Tests if setting the footer visibility works properly"""

        table = Table('Test table', self.createContainer())

        # The footer should by default be hidden
        self.assertFalse(table.isFooterVisible())

        # Set footer visibility to tru should be reflected in the
        # isFooterVisible() method
        table.setFooterVisible(True)
        self.assertTrue(table.isFooterVisible())


    def testAddingFooters(self):
        """Tests adding footers to the columns"""

        table = Table('Test table', self.createContainer())

        # Table should not contain any footers at initialization
        self.assertIsNone(table.getColumnFooter('col1'))
        self.assertIsNone(table.getColumnFooter('col2'))
        self.assertIsNone(table.getColumnFooter('col3'))

        # Adding column footer
        table.setColumnFooter('col1', 'Footer1')
        self.assertEquals('Footer1', table.getColumnFooter('col1'))

        # Add another footer
        table.setColumnFooter('col2', 'Footer2')
        self.assertEquals('Footer2', table.getColumnFooter('col2'))

        # Add footer for a non-existing column
        table.setColumnFooter('fail', 'FooterFail')


    def testRemovingFooters(self):
        """Test removing footers"""

        table = Table('Test table', self.createContainer())

        table.setColumnFooter('col1', 'Footer1')
        table.setColumnFooter('col2', 'Footer2')

        # Test removing footer
        self.assertNotEquals(table.getColumnFooter('col1'), None)
        table.setColumnFooter('col1', None)
        self.assertEquals(table.getColumnFooter('col1'), None)

        # The other footer should still be there
        self.assertNotEquals(table.getColumnFooter('col2'), None)

        # Remove non-existing footer
        table.setColumnFooter('fail', None)


    @classmethod
    def createContainer(cls):
        """Creates a container with three properties "col1,col2,col3"
        with 100 items

        @return: Returns the created table
        """
        container = IndexedContainer()
        container.addContainerProperty('col1', str, '')
        container.addContainerProperty('col2', str, '')
        container.addContainerProperty('col3', str, '')

        for i in range(100):
            item = container.addItem('item %d' % i)
            item.getItemProperty('col1').setValue('first%d' % i)
            item.getItemProperty('col2').setValue('middle%d' % i)
            item.getItemProperty('col3').setValue('last%d' % i)

        return container
