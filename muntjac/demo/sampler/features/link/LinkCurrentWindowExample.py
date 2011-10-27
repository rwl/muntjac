
from muntjac.api import VerticalLayout, Link
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.terminal.external_resource import ExternalResource


class LinkCurrentWindowExample(VerticalLayout):

    _CAPTION = 'Open Google'
    _TOOLTIP = 'http://www.google.com'
    _ICON = ThemeResource('../sampler/icons/icon_world.gif')

    def __init__(self):
        super(LinkCurrentWindowExample, self).__init__()

        self.setSpacing(True)

        # Link w/ text and tooltip
        l = Link(self._CAPTION, ExternalResource('http://www.google.com'))
        l.setDescription(self._TOOLTIP)
        self.addComponent(l)

        # Link w/ text, icon and tooltip
        l = Link(self._CAPTION, ExternalResource('http://www.google.com'))
        l.setDescription(self._TOOLTIP)
        l.setIcon(self._ICON)
        self.addComponent(l)

        # Link w/ icon and tooltip
        l = Link()
        l.setResource(ExternalResource('http://www.google.com'))
        l.setDescription(self._TOOLTIP)
        l.setIcon(self._ICON)
        self.addComponent(l)
