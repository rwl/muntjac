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
