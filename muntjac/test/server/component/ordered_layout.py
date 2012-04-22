# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

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
