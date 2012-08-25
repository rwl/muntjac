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
