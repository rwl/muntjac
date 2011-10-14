# -*- coding: utf-8 -*-
from __pyjamas__ import (POSTINC,)
# from com.vaadin.ui.AbstractOrderedLayout import (AbstractOrderedLayout,)
# from java.util.Iterator import (Iterator,)
# from junit.framework.TestCase import (TestCase,)


class TestOrderedLayout(TestCase):

    def testVLIteration(self):
        self.testIndexing(VerticalLayout(), 10)

    def testHLIteration(self):
        self.testIndexing(HorizontalLayout(), 12)

    def testIndexing(self, aol, nrComponents):
        components = self.generateComponents(nrComponents)
        for c in components:
            aol.addComponent(c)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < nrComponents):
                break
            assert aol.getComponent(i) == components[i]
            assert aol.getComponentIndex(components[i]) == i
        # Iteration should be in indexed order
        idx = 0
        _1 = True
        i = aol.getComponentIterator()
        while True:
            if _1 is True:
                _1 = False
            if not i.hasNext():
                break
            c = i.next()
            assert aol.getComponentIndex(c) == POSTINC(globals(), locals(), 'idx')

    def generateComponents(self, nr):
        components = [None] * nr
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < nr):
                break
            components[i] = Label('' + i)
        return components
