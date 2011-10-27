
from muntjac.api import VerticalLayout
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.terminal.external_resource import ExternalResource
from muntjac.ui.link import Link


class LinkSizedWindowExample(VerticalLayout):

    _CAPTION = 'Open Google in small window'
    _TOOLTIP = 'http://www.google.com (opens in small window)'
    _ICON = ThemeResource('../sampler/icons/icon_world.gif')
    _TARGET = ExternalResource('http://www.google.com/m')

    def __init__(self):
        super(LinkSizedWindowExample, self).__init__()

        self.setSpacing(True)

        # Link w/ text and tooltip
        l = Link(self._CAPTION, self._TARGET)
        l.setTargetName('_blank')
        l.setTargetWidth(300)
        l.setTargetHeight(300)
        l.setTargetBorder(Link.TARGET_BORDER_NONE)
        l.setDescription(self._TOOLTIP)
        self.addComponent(l)

        # Link w/ text, icon and tooltip
        l = Link(self._CAPTION, self._TARGET)
        l.setTargetName('_blank')
        l.setTargetWidth(300)
        l.setTargetHeight(300)
        l.setTargetBorder(Link.TARGET_BORDER_NONE)
        l.setDescription(self._TOOLTIP)
        l.setIcon(self._ICON)
        self.addComponent(l)

        # Link w/ icon and tooltip
        l = Link()
        l.setResource(self._TARGET)
        l.setTargetName('_blank')
        l.setTargetWidth(300)
        l.setTargetHeight(300)
        l.setTargetBorder(Link.TARGET_BORDER_NONE)
        l.setDescription(self._TOOLTIP)
        l.setIcon(self._ICON)
        self.addComponent(l)
