
from muntjac.demo.sampler.features.menubar.BasicMenuBar import BasicMenuBar
from muntjac.demo.sampler.features.menubar.MenuBarHiddenItems import MenuBarHiddenItems
from muntjac.demo.sampler.features.menubar.MenuBarWithIconsExample import MenuBarWithIconsExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.menubar.MenuBarWithIcons import MenuBarWithIcons
from muntjac.demo.sampler.features.menubar.MenuBarItemStyles import MenuBarItemStyles
from muntjac.demo.sampler.features.menubar.MenuBarCollapsing import MenuBarCollapsing
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.menu_bar import MenuBar


class MenuBarKeyboardNavigation(Feature):

    def getDescription(self):
        return ('As well as using the mouse you can also use the '
            'keyboard to select items from the menu bar. Make sure '
            'that the menu bar has keyboard focus and use the arrow '
            'keys to navigate in the menu. To select an item use the '
            'Enter and to close the menu use the Esc key.')


    def getName(self):
        return 'MenuBar keyboard navigation'


    def getRelatedAPI(self):
        return [APIResource(MenuBar)]


    def getRelatedFeatures(self):
        return [
            BasicMenuBar,
            MenuBarWithIcons,
            MenuBarCollapsing,
            MenuBarHiddenItems,
            MenuBarItemStyles
        ]


    def getRelatedResources(self):
        return None


    def getSinceVersion(self):
        return Version.V64


    def getExample(self):
        return MenuBarWithIconsExample()
