
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.menu_bar import MenuBar


class MenuBarWithIcons(Feature):

    def getSinceVersion(self):
        return Version.V62


    def getName(self):
        return 'MenuBar with icons'


    def getDescription(self):
        return ('You can add icons to individual MenuBar items, to make '
            'it faster for the user to distinguish separate items.')


    def getRelatedAPI(self):
        return [APIResource(MenuBar)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.menubar.BasicMenuBar import BasicMenuBar
        from muntjac.demo.sampler.features.menubar.MenuBarTooltips import MenuBarTooltips
        from muntjac.demo.sampler.features.menubar.MenuBarHiddenItems import MenuBarHiddenItems
        from muntjac.demo.sampler.features.menubar.MenuBarItemStyles import MenuBarItemStyles
        from muntjac.demo.sampler.features.menubar.MenuBarCollapsing import MenuBarCollapsing

        return [
            BasicMenuBar,
            MenuBarCollapsing,
            MenuBarHiddenItems,
            MenuBarItemStyles,
            MenuBarTooltips
        ]


    def getRelatedResources(self):
        return None
