# -*- coding: utf-8 -*-
# from com.vaadin.terminal.Resource import (Resource,)


class LinkSizedWindowExample(VerticalLayout):
    _CAPTION = 'Open Google in small window'
    _TOOLTIP = 'http://www.google.com (opens in small window)'
    _ICON = ThemeResource('../sampler/icons/icon_world.gif')
    _TARGET = ExternalResource('http://www.google.com/m')

    def __init__(self):
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
