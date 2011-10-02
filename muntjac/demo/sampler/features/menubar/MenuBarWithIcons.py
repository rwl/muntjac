# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.menubar.BasicMenuBar import (BasicMenuBar,)
from com.vaadin.demo.sampler.features.menubar.MenuBarTooltips import (MenuBarTooltips,)
from com.vaadin.demo.sampler.features.menubar.MenuBarHiddenItems import (MenuBarHiddenItems,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.menubar.MenuBarItemStyles import (MenuBarItemStyles,)
from com.vaadin.demo.sampler.features.menubar.MenuBarCollapsing import (MenuBarCollapsing,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class MenuBarWithIcons(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'MenuBar with icons'

    def getDescription(self):
        return 'You can add icons to individual MenuBar items, to make it faster for the user to distinguish separate items.'

    def getRelatedAPI(self):
        return [APIResource(MenuBar)]

    def getRelatedFeatures(self):
        return [BasicMenuBar, MenuBarCollapsing, MenuBarHiddenItems, MenuBarItemStyles, MenuBarTooltips]

    def getRelatedResources(self):
        return None
