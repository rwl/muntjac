# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.menubar.BasicMenuBar import (BasicMenuBar,)
from com.vaadin.demo.sampler.features.menubar.MenuBarHiddenItems import (MenuBarHiddenItems,)
from com.vaadin.demo.sampler.features.menubar.MenuBarWithIconsExample import (MenuBarWithIconsExample,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.menubar.MenuBarWithIcons import (MenuBarWithIcons,)
from com.vaadin.demo.sampler.features.menubar.MenuBarItemStyles import (MenuBarItemStyles,)
from com.vaadin.demo.sampler.features.menubar.MenuBarCollapsing import (MenuBarCollapsing,)
from com.vaadin.demo.sampler.Feature import (Feature,)
# from com.vaadin.ui.Component import (Component,)
# from com.vaadin.ui.MenuBar import (MenuBar,)
Version = Feature.Version


class MenuBarKeyboardNavigation(Feature):

    def getDescription(self):
        return 'As well as using the mouse you can also use the ' + 'keyboard to select items from the menu bar. Make sure ' + 'that the menu bar has keyboard focus and use the arrow ' + 'keys to navigate in the menu. To select an item use the ' + 'Enter and to close the menu use the Esc key.'

    def getName(self):
        return 'MenuBar keyboard navigation'

    def getRelatedAPI(self):
        return [APIResource(MenuBar)]

    def getRelatedFeatures(self):
        return [BasicMenuBar, MenuBarWithIcons, MenuBarCollapsing, MenuBarHiddenItems, MenuBarItemStyles]

    def getRelatedResources(self):
        return None

    def getSinceVersion(self):
        return Version.V64

    def getExample(self):
        return MenuBarWithIconsExample()
