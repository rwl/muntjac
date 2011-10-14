# -*- coding: utf-8 -*-
# from com.vaadin.ui.TabSheet import (TabSheet,)
# from com.vaadin.ui.TabSheet.Tab import (Tab,)
# from org.junit.Assert.assertEquals import (assertEquals,)
# from org.junit.Assert.assertNotNull import (assertNotNull,)
# from org.junit.Test import (Test,)


class TestTabSheet(object):

    def addExistingComponent(self):
        c = Label('abc')
        tabSheet = TabSheet()
        tabSheet.addComponent(c)
        tabSheet.addComponent(c)
        iter = tabSheet.getComponentIterator()
        assertEquals(c, iter.next())
        assertEquals(False, iter.hasNext())
        assertNotNull(tabSheet.getTab(c))

    def getComponentFromTab(self):
        c = Label('abc')
        tabSheet = TabSheet()
        tab = tabSheet.addTab(c)
        assertEquals(c, tab.getComponent())

    def addTabWithComponentOnly(self):
        tabSheet = TabSheet()
        tab1 = tabSheet.addTab(Label('aaa'))
        tab2 = tabSheet.addTab(Label('bbb'))
        tab3 = tabSheet.addTab(Label('ccc'))
        # Check right order of tabs
        assertEquals(0, tabSheet.getTabPosition(tab1))
        assertEquals(1, tabSheet.getTabPosition(tab2))
        assertEquals(2, tabSheet.getTabPosition(tab3))
        # Calling addTab with existing component does not move tab
        tabSheet.addTab(tab1.getComponent())
        # Check right order of tabs
        assertEquals(0, tabSheet.getTabPosition(tab1))
        assertEquals(1, tabSheet.getTabPosition(tab2))
        assertEquals(2, tabSheet.getTabPosition(tab3))

    def addTabWithComponentAndIndex(self):
        tabSheet = TabSheet()
        tab1 = tabSheet.addTab(Label('aaa'))
        tab2 = tabSheet.addTab(Label('bbb'))
        tab3 = tabSheet.addTab(Label('ccc'))
        tab4 = tabSheet.addTab(Label('ddd'), 1)
        tab5 = tabSheet.addTab(Label('eee'), 3)
        assertEquals(0, tabSheet.getTabPosition(tab1))
        assertEquals(1, tabSheet.getTabPosition(tab4))
        assertEquals(2, tabSheet.getTabPosition(tab2))
        assertEquals(3, tabSheet.getTabPosition(tab5))
        assertEquals(4, tabSheet.getTabPosition(tab3))
        # Calling addTab with existing component does not move tab
        tabSheet.addTab(tab1.getComponent(), 3)
        assertEquals(0, tabSheet.getTabPosition(tab1))
        assertEquals(1, tabSheet.getTabPosition(tab4))
        assertEquals(2, tabSheet.getTabPosition(tab2))
        assertEquals(3, tabSheet.getTabPosition(tab5))
        assertEquals(4, tabSheet.getTabPosition(tab3))

    def addTabWithAllParameters(self):
        tabSheet = TabSheet()
        tab1 = tabSheet.addTab(Label('aaa'))
        tab2 = tabSheet.addTab(Label('bbb'))
        tab3 = tabSheet.addTab(Label('ccc'))
        tab4 = tabSheet.addTab(Label('ddd'), 'ddd', None, 1)
        tab5 = tabSheet.addTab(Label('eee'), 'eee', None, 3)
        assertEquals(0, tabSheet.getTabPosition(tab1))
        assertEquals(1, tabSheet.getTabPosition(tab4))
        assertEquals(2, tabSheet.getTabPosition(tab2))
        assertEquals(3, tabSheet.getTabPosition(tab5))
        assertEquals(4, tabSheet.getTabPosition(tab3))
        # Calling addTab with existing component does not move tab
        tabSheet.addTab(tab1.getComponent(), 'xxx', None, 3)
        assertEquals(0, tabSheet.getTabPosition(tab1))
        assertEquals(1, tabSheet.getTabPosition(tab4))
        assertEquals(2, tabSheet.getTabPosition(tab2))
        assertEquals(3, tabSheet.getTabPosition(tab5))
        assertEquals(4, tabSheet.getTabPosition(tab3))

    def getTabByPosition(self):
        tabSheet = TabSheet()
        tab1 = tabSheet.addTab(Label('aaa'))
        tab2 = tabSheet.addTab(Label('bbb'))
        tab3 = tabSheet.addTab(Label('ccc'))
        assertEquals(tab1, tabSheet.getTab(0))
        assertEquals(tab2, tabSheet.getTab(1))
        assertEquals(tab3, tabSheet.getTab(2))
