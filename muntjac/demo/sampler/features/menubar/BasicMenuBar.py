# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.menubar.MenuBarTooltips import (MenuBarTooltips,)
from com.vaadin.demo.sampler.features.menubar.MenuBarHiddenItems import (MenuBarHiddenItems,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.menubar.MenuBarWithIcons import (MenuBarWithIcons,)
from com.vaadin.demo.sampler.features.menubar.MenuBarItemStyles import (MenuBarItemStyles,)
from com.vaadin.demo.sampler.features.menubar.MenuBarCollapsing import (MenuBarCollapsing,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class BasicMenuBar(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Basic MenuBar'

    def getDescription(self):
        return 'The drop down menus can have separators between menu items and single items can be disabled.'

    def getRelatedAPI(self):
        return [APIResource(MenuBar)]

    def getRelatedFeatures(self):
        return [MenuBarWithIcons, MenuBarCollapsing, MenuBarHiddenItems, MenuBarItemStyles, MenuBarTooltips]

    def getRelatedResources(self):
        return None
