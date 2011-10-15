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

# from com.vaadin.data.Container import (Container,)
# from com.vaadin.data.Item import (Item,)
# from com.vaadin.data.util.IndexedContainer import (IndexedContainer,)
# from com.vaadin.ui.Table import (Table,)
# from junit.framework.TestCase import (TestCase,)


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
        self.assertNull(table.getColumnFooter('col1'))
        self.assertNull(table.getColumnFooter('col2'))
        self.assertNull(table.getColumnFooter('col3'))
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
        self.assertNotNull(table.getColumnFooter('col1'))
        table.setColumnFooter('col1', None)
        self.assertNull(table.getColumnFooter('col1'))
        # The other footer should still be there
        self.assertNotNull(table.getColumnFooter('col2'))
        # Remove non-existing footer
        table.setColumnFooter('fail', None)

    @classmethod
    def createContainer(cls):
        """Creates a container with three properties "col1,col2,col3" with 100 items

        @return Returns the created table
        """
        container = IndexedContainer()
        container.addContainerProperty('col1', str, '')
        container.addContainerProperty('col2', str, '')
        container.addContainerProperty('col3', str, '')
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 100):
                break
            item = container.addItem('item ' + i)
            item.getItemProperty('col1').setValue('first' + i)
            item.getItemProperty('col2').setValue('middle' + i)
            item.getItemProperty('col3').setValue('last' + i)
        return container
