# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.menubar.BasicMenuBar import (BasicMenuBar,)
from com.vaadin.demo.sampler.features.menubar.MenuBarTooltips import (MenuBarTooltips,)
from com.vaadin.demo.sampler.features.menubar.MenuBarHiddenItems import (MenuBarHiddenItems,)
from com.vaadin.demo.sampler.NamedExternalResource import (NamedExternalResource,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.menubar.MenuBarWithIcons import (MenuBarWithIcons,)
from com.vaadin.demo.sampler.features.menubar.MenuBarCollapsing import (MenuBarCollapsing,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class MenuBarItemStyles(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'MenuBar item styles'

    def getDescription(self):
        return 'Individual MenuBar menu items can have additional styles applied to them with CSS.'

    def getRelatedAPI(self):
        return [APIResource(MenuBar)]

    def getRelatedFeatures(self):
        return [BasicMenuBar, MenuBarWithIcons, MenuBarCollapsing, MenuBarHiddenItems, MenuBarTooltips]

    def getRelatedResources(self):
        return [NamedExternalResource('CSS for the menubar', self.getThemeBase() + 'misc/item-styles.css')]
