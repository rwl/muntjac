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
