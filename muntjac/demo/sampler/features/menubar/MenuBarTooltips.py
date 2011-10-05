
from muntjac.demo.sampler.features.menubar.MenuBarHiddenItems import MenuBarHiddenItems
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.menubar.MenuBarWithIcons import MenuBarWithIcons
from muntjac.demo.sampler.features.menubar.MenuBarItemStyles import MenuBarItemStyles
from muntjac.demo.sampler.features.menubar.MenuBarCollapsing import MenuBarCollapsing
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.menu_bar import MenuBar


class MenuBarTooltips(Feature):

    def getName(self):
        return 'MenuBar, tooltips'


    def getDescription(self):
        return ('You can add tooltips to all items in the menu bar. '
            'Hoover the mouse over an item to see the tooltip.')


    def getRelatedResources(self):
        return None


    def getRelatedAPI(self):
        return [APIResource(MenuBar)]


    def getRelatedFeatures(self):
        return [
            MenuBarWithIcons,
            MenuBarCollapsing,
            MenuBarHiddenItems,
            MenuBarItemStyles
        ]


    def getSinceVersion(self):
        return Version.V65
