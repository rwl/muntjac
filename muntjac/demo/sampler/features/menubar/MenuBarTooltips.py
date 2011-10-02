# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.menubar.MenuBarHiddenItems import (MenuBarHiddenItems,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.menubar.MenuBarWithIcons import (MenuBarWithIcons,)
from com.vaadin.demo.sampler.features.menubar.MenuBarItemStyles import (MenuBarItemStyles,)
from com.vaadin.demo.sampler.features.menubar.MenuBarCollapsing import (MenuBarCollapsing,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class MenuBarTooltips(Feature):

    def getName(self):
        return 'MenuBar, tooltips'

    def getDescription(self):
        return 'You can add tooltips to all items in the menu bar. ' + 'Hoover the mouse over an item to see the tooltip.'

    def getRelatedResources(self):
        return None

    def getRelatedAPI(self):
        return [APIResource(MenuBar)]

    def getRelatedFeatures(self):
        return [MenuBarWithIcons, MenuBarCollapsing, MenuBarHiddenItems, MenuBarItemStyles]

    def getSinceVersion(self):
        return Version.V65
