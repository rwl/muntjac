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
