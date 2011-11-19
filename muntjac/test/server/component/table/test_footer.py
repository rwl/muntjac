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
