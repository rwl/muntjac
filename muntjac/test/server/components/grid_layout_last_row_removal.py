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
