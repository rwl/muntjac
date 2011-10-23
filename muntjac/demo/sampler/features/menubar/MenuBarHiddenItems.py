
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.menu_bar import MenuBar


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

        from muntjac.demo.sampler.features.menubar.BasicMenuBar import BasicMenuBar
        from muntjac.demo.sampler.features.menubar.MenuBarTooltips import MenuBarTooltips
        from muntjac.demo.sampler.features.menubar.MenuBarWithIcons import MenuBarWithIcons
        from muntjac.demo.sampler.features.menubar.MenuBarItemStyles import MenuBarItemStyles
        from muntjac.demo.sampler.features.menubar.MenuBarCollapsing import MenuBarCollapsing

        return [
            BasicMenuBar,
            MenuBarWithIcons,
            MenuBarCollapsing,
            MenuBarItemStyles,
            MenuBarTooltips
        ]


    def getRelatedResources(self):
        return None
