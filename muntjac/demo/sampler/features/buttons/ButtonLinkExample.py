# -*- coding: utf-8 -*-
# from com.vaadin.ui.themes.BaseTheme import (BaseTheme,)


class ButtonLinkExample(VerticalLayout, Button.ClickListener):
    _CAPTION = 'Help'
    _TOOLTIP = 'Show help'
    _ICON = ThemeResource('../sampler/icons/icon_info.gif')
    _NOTIFICATION = 'Help clicked'

    def __init__(self):
        # Shows a notification when a button is clicked.
        self.setSpacing(True)
        # Button w/ text and tooltip
        b = Button(self._CAPTION)
        b.setStyleName(BaseTheme.BUTTON_LINK)
        b.setDescription(self._TOOLTIP)
        b.addListener(self)
        # react to clicks
        self.addComponent(b)
        # Button w/ text, icon and tooltip
        b = Button(self._CAPTION)
        b.setStyleName(BaseTheme.BUTTON_LINK)
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self)
        # react to clicks
        self.addComponent(b)
        # Button w/ icon and tooltip
        b = Button()
        b.setStyleName(BaseTheme.BUTTON_LINK)
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self)
        # react to clicks
        self.addComponent(b)

    def buttonClick(self, event):
        self.getWindow().showNotification(self._NOTIFICATION)
