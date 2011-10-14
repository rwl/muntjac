# -*- coding: utf-8 -*-
# from com.vaadin.ui.AbstractSelect.MultiSelectMode import (MultiSelectMode,)
# from java.util.Arrays import (Arrays,)
# from junit.framework.TestCase import (TestCase,)


class TestMultipleSelection(TestCase):

    def testSetMultipleItems(self):
        """Tests weather the multiple select mode is set when using Table.set"""
        table = Table('', self.createTestContainer())
        # Tests if multiple selection is set
        table.setMultiSelect(True)
        self.assertTrue(table.isMultiSelect())
        # Test multiselect by setting several items at once
        table.setValue(Arrays.asList('1', ['3']))
        self.assertEquals(2, len(table.getValue()))

    def testSetMultiSelectMode(self):
        """Tests setting the multiselect mode of the Table. The multiselect mode
        affects how mouse selection is made in the table by the user.
        """
        table = Table('', self.createTestContainer())
        # Default multiselect mode should be MultiSelectMode.DEFAULT
        self.assertEquals(MultiSelectMode.DEFAULT, table.getMultiSelectMode())
        # Tests if multiselectmode is set
        table.setMultiSelectMode(MultiSelectMode.SIMPLE)
        self.assertEquals(MultiSelectMode.SIMPLE, table.getMultiSelectMode())

    def createTestContainer(self):
        """Creates a testing container for the tests

        @return A new container with test items
        """
        container = IndexedContainer(Arrays.asList('1', ['2', '3', '4']))
        return container
