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
