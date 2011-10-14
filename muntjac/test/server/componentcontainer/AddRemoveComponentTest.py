# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
# from com.vaadin.tests.VaadinClasses import (VaadinClasses,)
# from com.vaadin.ui.ComponentContainer import (ComponentContainer,)
# from com.vaadin.ui.CustomLayout import (CustomLayout,)
# from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
# from com.vaadin.ui.Label import (Label,)
# from java.util.List import (List,)
# from junit.framework.TestCase import (TestCase,)


class AddRemoveComponentTest(TestCase):

    def testRemoveComponentFromWrongContainer(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            containerClasses = VaadinClasses.getComponentContainersSupportingAddRemoveComponent()
            # No default constructor, special case
            containerClasses.remove(CustomLayout)
            self.testRemoveComponentFromWrongContainer(CustomLayout('dummy'))
            for c in containerClasses:
                self.testRemoveComponentFromWrongContainer(c())
        elif _1 == 1:
            componentContainer, = _0
            hl = HorizontalLayout()
            label = Label()
            hl.addComponent(label)
            componentContainer.removeComponent(label)
            self.assertEquals('Parent no longer correct for ' + componentContainer.getClass(), hl, label.getParent())
        else:
            raise ARGERROR(0, 1)
