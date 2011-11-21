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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

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
