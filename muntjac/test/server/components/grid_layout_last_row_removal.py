# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from unittest import TestCase

from muntjac.ui.grid_layout import GridLayout
from muntjac.ui.label import Label


class TestGridLayoutLastRowRemoval(TestCase):

    def testRemovingLastRow(self):
        grid = GridLayout(2, 1)
        grid.addComponent(Label('Col1'))
        grid.addComponent(Label('Col2'))

        try:
            # Removing the last row in the grid
            grid.removeRow(0)
        except ValueError:
            # Removing the last row should not throw a ValueError
            self.fail('removeRow(0) threw an ValueError '
                    'when removing the last row')

        # The column amount should be preserved
        self.assertEquals(2, grid.getColumns())

        # There should be one row left
        self.assertEquals(1, grid.getRows())

        # There should be no component left in the grid layout
        self.assertEquals(grid.getComponent(0, 0), None,
                'A component should not be left in the layout')
        self.assertEquals(grid.getComponent(1, 0), None,
                'A component should not be left in the layout')

        # The cursor should be in the first cell
        self.assertEquals(0, grid.getCursorX())
        self.assertEquals(0, grid.getCursorY())
