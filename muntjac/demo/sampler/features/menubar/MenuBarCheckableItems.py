
from muntjac.demo.sampler.features.menubar.BasicMenuBar import BasicMenuBar
from muntjac.demo.sampler.features.menubar.MenuBarTooltips import MenuBarTooltips
from muntjac.demo.sampler.features.menubar.MenuBarHiddenItems import MenuBarHiddenItems
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.menubar.MenuBarWithIcons import MenuBarWithIcons
from muntjac.demo.sampler.features.menubar.MenuBarItemStyles import MenuBarItemStyles
from muntjac.demo.sampler.features.menubar.MenuBarCollapsing import MenuBarCollapsing
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.menu_bar import MenuBar


class MenuBarCheckableItems(Feature):

    def getSinceVersion(self):
        return Version.V66


    def getName(self):
        return 'MenuBar checkable items'


    def getDescription(self):
        return 'Individual MenuBar menu items can be marked as checkable.'


    def getRelatedAPI(self):
        return [APIResource(MenuBar)]


    def getRelatedFeatures(self):
        return [
            BasicMenuBar,
            MenuBarWithIcons,
            MenuBarCollapsing,
            MenuBarHiddenItems,
            MenuBarTooltips,
            MenuBarItemStyles
        ]


    def getRelatedResources(self):
        return []
