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
from muntjac.ui.label import Label
from muntjac.ui.tab_sheet import TabSheet


class TestTabSheet(TestCase):

    def testAddExistingComponent(self):
        c = Label('abc')
        tabSheet = TabSheet()
        tabSheet.addComponent(c)
        tabSheet.addComponent(c)
        itr = tabSheet.getComponentIterator()
        self.assertEquals(c, itr.next())
        self.assertRaises(StopIteration, itr.next)
        self.assertNotEquals(tabSheet.getTab(c), None)


    def testGetComponentFromTab(self):
        c = Label('abc')
        tabSheet = TabSheet()
        tab = tabSheet.addTab(c)
        self.assertEquals(c, tab.getComponent())


    def testAddTabWithComponentOnly(self):
        tabSheet = TabSheet()
        tab1 = tabSheet.addTab(Label('aaa'))
        tab2 = tabSheet.addTab(Label('bbb'))
        tab3 = tabSheet.addTab(Label('ccc'))

        # Check right order of tabs
        self.assertEquals(0, tabSheet.getTabPosition(tab1))
        self.assertEquals(1, tabSheet.getTabPosition(tab2))
        self.assertEquals(2, tabSheet.getTabPosition(tab3))

        # Calling addTab with existing component does not move tab
        tabSheet.addTab(tab1.getComponent())

        # Check right order of tabs
        self.assertEquals(0, tabSheet.getTabPosition(tab1))
        self.assertEquals(1, tabSheet.getTabPosition(tab2))
        self.assertEquals(2, tabSheet.getTabPosition(tab3))


    def testAddTabWithComponentAndIndex(self):
        tabSheet = TabSheet()
        tab1 = tabSheet.addTab(Label('aaa'))
        tab2 = tabSheet.addTab(Label('bbb'))
        tab3 = tabSheet.addTab(Label('ccc'))
        tab4 = tabSheet.addTab(Label('ddd'), 1)
        tab5 = tabSheet.addTab(Label('eee'), 3)

        self.assertEquals(0, tabSheet.getTabPosition(tab1))
        self.assertEquals(1, tabSheet.getTabPosition(tab4))
        self.assertEquals(2, tabSheet.getTabPosition(tab2))
        self.assertEquals(3, tabSheet.getTabPosition(tab5))
        self.assertEquals(4, tabSheet.getTabPosition(tab3))

        # Calling addTab with existing component does not move tab
        tabSheet.addTab(tab1.getComponent(), 3)
        self.assertEquals(0, tabSheet.getTabPosition(tab1))
        self.assertEquals(1, tabSheet.getTabPosition(tab4))
        self.assertEquals(2, tabSheet.getTabPosition(tab2))
        self.assertEquals(3, tabSheet.getTabPosition(tab5))
        self.assertEquals(4, tabSheet.getTabPosition(tab3))


    def testAddTabWithAllParameters(self):
        tabSheet = TabSheet()
        tab1 = tabSheet.addTab(Label('aaa'))
        tab2 = tabSheet.addTab(Label('bbb'))
        tab3 = tabSheet.addTab(Label('ccc'))
        tab4 = tabSheet.addTab(Label('ddd'), 'ddd', None, 1)
        tab5 = tabSheet.addTab(Label('eee'), 'eee', None, 3)

        self.assertEquals(0, tabSheet.getTabPosition(tab1))
        self.assertEquals(1, tabSheet.getTabPosition(tab4))
        self.assertEquals(2, tabSheet.getTabPosition(tab2))
        self.assertEquals(3, tabSheet.getTabPosition(tab5))
        self.assertEquals(4, tabSheet.getTabPosition(tab3))

        # Calling addTab with existing component does not move tab
        tabSheet.addTab(tab1.getComponent(), 'xxx', None, 3)
        self.assertEquals(0, tabSheet.getTabPosition(tab1))
        self.assertEquals(1, tabSheet.getTabPosition(tab4))
        self.assertEquals(2, tabSheet.getTabPosition(tab2))
        self.assertEquals(3, tabSheet.getTabPosition(tab5))
        self.assertEquals(4, tabSheet.getTabPosition(tab3))


    def testGetTabByPosition(self):
        tabSheet = TabSheet()
        tab1 = tabSheet.addTab(Label('aaa'))
        tab2 = tabSheet.addTab(Label('bbb'))
        tab3 = tabSheet.addTab(Label('ccc'))

        self.assertEquals(tab1, tabSheet.getTab(0))
        self.assertEquals(tab2, tabSheet.getTab(1))
        self.assertEquals(tab3, tabSheet.getTab(2))
