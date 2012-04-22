# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from unittest import TestCase

from muntjac.test.muntjac_classes import MuntjacClasses
from muntjac.ui.custom_layout import CustomLayout
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.label import Label


class AddRemoveComponentTest(TestCase):

    def testRemoveComponentFromWrongContainer(self, componentContainer=None):
        if componentContainer is None:
            containerClasses = MuntjacClasses.\
                getComponentContainersSupportingAddRemoveComponent()

            # No default constructor, special case
            containerClasses.remove(CustomLayout)
            self.testRemoveComponentFromWrongContainer(CustomLayout('dummy'))

            for c in containerClasses:
                self.testRemoveComponentFromWrongContainer( c() )
        else:
            hl = HorizontalLayout()
            label = Label()
            hl.addComponent(label)

            componentContainer.removeComponent(label)
            self.assertEquals(hl, label.getParent(), ('Parent no longer ' +
                    'correct for ' + componentContainer.__class__.__name__))
