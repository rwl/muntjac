# -*- coding: utf-8 -*-
# from com.vaadin.terminal.ExternalResource import (ExternalResource,)
# from com.vaadin.terminal.ThemeResource import (ThemeResource,)
# from com.vaadin.ui.Link import (Link,)
# from com.vaadin.ui.VerticalLayout import (VerticalLayout,)


class LinkCurrentWindowExample(VerticalLayout):
    _CAPTION = 'Open Google'
    _TOOLTIP = 'http://www.google.com'
    _ICON = ThemeResource('../sampler/icons/icon_world.gif')

    def __init__(self):
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
