# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.menubar.BasicMenuBar import (BasicMenuBar,)
from com.vaadin.demo.sampler.features.menubar.MenuBarTooltips import (MenuBarTooltips,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.menubar.MenuBarWithIcons import (MenuBarWithIcons,)
from com.vaadin.demo.sampler.features.menubar.MenuBarItemStyles import (MenuBarItemStyles,)
from com.vaadin.demo.sampler.features.menubar.MenuBarCollapsing import (MenuBarCollapsing,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class MenuBarHiddenItems(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'MenuBar, hidden items'

    def getDescription(self):
        return 'Individual menu items can be enabled, disabled, visible or hidden.'

    def getRelatedAPI(self):
        return [APIResource(MenuBar)]

    def getRelatedFeatures(self):
        return [BasicMenuBar, MenuBarWithIcons, MenuBarCollapsing, MenuBarItemStyles, MenuBarTooltips]

    def getRelatedResources(self):
        return None
