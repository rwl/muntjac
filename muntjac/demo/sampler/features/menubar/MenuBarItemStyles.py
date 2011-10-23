
from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.menu_bar import MenuBar


class MenuBarItemStyles(Feature):

    def getSinceVersion(self):
        return Version.V62


    def getName(self):
        return 'MenuBar item styles'


    def getDescription(self):
        return ('Individual MenuBar menu items can have additional '
            'styles applied to them with CSS.')


    def getRelatedAPI(self):
        return [APIResource(MenuBar)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.menubar.BasicMenuBar import BasicMenuBar
        from muntjac.demo.sampler.features.menubar.MenuBarTooltips import MenuBarTooltips
        from muntjac.demo.sampler.features.menubar.MenuBarHiddenItems import MenuBarHiddenItems
        from muntjac.demo.sampler.features.menubar.MenuBarWithIcons import MenuBarWithIcons
        from muntjac.demo.sampler.features.menubar.MenuBarCollapsing import MenuBarCollapsing

        return [
            BasicMenuBar,
            MenuBarWithIcons,
            MenuBarCollapsing,
            MenuBarHiddenItems,
            MenuBarTooltips
        ]


    def getRelatedResources(self):
        return [NamedExternalResource('CSS for the menubar',
                self.getThemeBase() + 'misc/item-styles.css')]
