# -*- coding: utf-8 -*-
# from com.vaadin.ui.GridLayout import (GridLayout,)
# from com.vaadin.ui.Label import (Label,)
# from junit.framework.TestCase import (TestCase,)


class TestGridLayoutLastRowRemoval(TestCase):

    def testRemovingLastRow(self):
        grid = GridLayout(2, 1)
        grid.addComponent(Label('Col1'))
        grid.addComponent(Label('Col2'))
        # Removing the last row in the grid
        # Removing the last row should not throw an
        # IllegalArgumentException
        # The column amount should be preserved
        try:
            grid.removeRow(0)
        except self.IllegalArgumentException, iae:
            self.fail('removeRow(0) threw an IllegalArgumentExcetion when removing the last row')
        self.assertEquals(2, grid.getColumns())
        # There should be one row left
        self.assertEquals(1, grid.getRows())
        # There should be no component left in the grid layout
        self.assertNull('A component should not be left in the layout', grid.getComponent(0, 0))
        self.assertNull('A component should not be left in the layout', grid.getComponent(1, 0))
        # The cursor should be in the first cell
        self.assertEquals(0, grid.getCursorX())
        self.assertEquals(0, grid.getCursorY())
