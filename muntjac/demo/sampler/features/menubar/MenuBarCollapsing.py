
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.menu_bar import MenuBar


class MenuBarCollapsing(Feature):

    def getSinceVersion(self):
        return Version.V62


    def getName(self):
        return 'MenuBar, collapsing items'


    def getDescription(self):
        return ('If the root level menu has more items that can fit in view '
            '(and if the MenuBar has a specified width), overflowing items '
            'will be collapsed to a generated sub-menu last in the root '
            'menu, indicated by an arrow.<br /><br/>Resize the browser '
            'window to collapse/expand more items.')


    def getRelatedAPI(self):
        return [APIResource(MenuBar)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.menubar.BasicMenuBar import BasicMenuBar
        from muntjac.demo.sampler.features.menubar.MenuBarTooltips import MenuBarTooltips
        from muntjac.demo.sampler.features.menubar.MenuBarHiddenItems import MenuBarHiddenItems
        from muntjac.demo.sampler.features.menubar.MenuBarWithIcons import MenuBarWithIcons
        from muntjac.demo.sampler.features.menubar.MenuBarItemStyles import MenuBarItemStyles

        return [
            BasicMenuBar,
            MenuBarWithIcons,
            MenuBarHiddenItems,
            MenuBarItemStyles,
            MenuBarTooltips
        ]


    def getRelatedResources(self):
        return None
