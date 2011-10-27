
from muntjac.api import VerticalLayout, Link
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.terminal.external_resource import ExternalResource


class LinkNoDecorationsExample(VerticalLayout):

    _CAPTION = 'Open Google in new window'
    _TOOLTIP = 'http://www.google.com (opens in new window)'
    _ICON = ThemeResource('../sampler/icons/icon_world.gif')

    def __init__(self):
        super(LinkNoDecorationsExample, self).__init__()

        self.setSpacing(True)

        # Link w/ text and tooltip
        l = Link(self._CAPTION, ExternalResource('http://www.google.com'))
        l.setTargetName('_blank')
        l.setTargetBorder(Link.TARGET_BORDER_NONE)
        l.setDescription(self._TOOLTIP)
        self.addComponent(l)

        # Link w/ text, icon and tooltip
        l = Link(self._CAPTION, ExternalResource('http://www.google.com'))
        l.setTargetName('_blank')
        l.setTargetBorder(Link.TARGET_BORDER_NONE)
        l.setDescription(self._TOOLTIP)
        l.setIcon(self._ICON)
        self.addComponent(l)

        # Link w/ icon and tooltip
        l = Link()
        l.setResource(ExternalResource('http://www.google.com'))
        l.setTargetName('_blank')
        l.setTargetBorder(Link.TARGET_BORDER_NONE)
        l.setDescription(self._TOOLTIP)
        l.setIcon(self._ICON)
        self.addComponent(l)
