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

from __pyjamas__ import (ARGERROR,)
# from muntjac.test.VaadinClasses import (VaadinClasses,)
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
