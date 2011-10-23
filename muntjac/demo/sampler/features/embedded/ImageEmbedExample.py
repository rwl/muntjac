
from muntjac.api import VerticalLayout
from muntjac.ui.embedded import Embedded
from muntjac.terminal.theme_resource import ThemeResource


class ImageEmbedExample(VerticalLayout):

    def __init__(self):
        e = Embedded('Image from a theme resource',
                ThemeResource('../runo/icons/64/document.png'))
        self.addComponent(e)
