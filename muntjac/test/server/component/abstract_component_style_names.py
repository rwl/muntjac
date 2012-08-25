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
from muntjac.ui.abstract_component import AbstractComponent


class TestAbstractComponentStyleNames(TestCase):

    def testSetMultiple(self):
        component = self.getComponent()
        component.setStyleName('style1 style2')
        self.assertEquals(component.getStyleName(), 'style1 style2')


    def testSetAdd(self):
        component = self.getComponent()
        component.setStyleName('style1')
        component.addStyleName('style2')
        self.assertEquals(component.getStyleName(), 'style1 style2')


    def testAddSame(self):
        component = self.getComponent()
        component.setStyleName('style1 style2')
        component.addStyleName('style1')
        self.assertEquals(component.getStyleName(), 'style1 style2')


    def testSetRemove(self):
        component = self.getComponent()
        component.setStyleName('style1 style2')
        component.removeStyleName('style1')
        self.assertEquals(component.getStyleName(), 'style2')


    def testAddRemove(self):
        component = self.getComponent()
        component.addStyleName('style1')
        component.addStyleName('style2')
        component.removeStyleName('style1')
        self.assertEquals(component.getStyleName(), 'style2')


    def testRemoveMultipleWithExtraSpaces(self):
        component = self.getComponent()
        component.setStyleName('style1 style2 style3')
        component.removeStyleName(' style1  style3 ')
        self.assertEquals(component.getStyleName(), 'style2')


    def testSetWithExtraSpaces(self):
        component = self.getComponent()
        component.setStyleName(' style1  style2 ')
        self.assertEquals(component.getStyleName(), 'style1 style2')


    def getComponent(self):
        return AbstractComponent()
