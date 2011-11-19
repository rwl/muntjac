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

from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.label import Label


class TestOrderedLayout(TestCase):

    def testVLIteration(self):
        self._testIndexing(VerticalLayout(), 10)


    def testHLIteration(self):
        self._testIndexing(HorizontalLayout(), 12)


    def _testIndexing(self, aol, nrComponents):
        components = self.generateComponents(nrComponents)
        for c in components:
            aol.addComponent(c)

        for i in range(nrComponents):
            assert aol.getComponent(i) == components[i]
            assert aol.getComponentIndex(components[i]) == i

        # Iteration should be in indexed order
        idx = 0
        for c in aol.getComponentIterator():
            assert aol.getComponentIndex(c) == idx
            idx += 1


    def generateComponents(self, nr):
        components = [None] * nr
        for i in range(nr):
            components[i] = Label('%d' % i)
        return components
