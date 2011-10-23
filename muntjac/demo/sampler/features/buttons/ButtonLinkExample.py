
from muntjac.api import VerticalLayout, Button, button
from muntjac.ui.themes import BaseTheme

from muntjac.terminal.theme_resource import ThemeResource


class ButtonLinkExample(VerticalLayout, button.IClickListener):

    _CAPTION = 'Help'
    _TOOLTIP = 'Show help'
    _ICON = ThemeResource('../sampler/icons/icon_info.gif')
    _NOTIFICATION = 'Help clicked'

    def __init__(self):
        self.setSpacing(True)

        # Button w/ text and tooltip
        b = Button(self._CAPTION)
        b.setStyleName(BaseTheme.BUTTON_LINK)
        b.setDescription(self._TOOLTIP)
        b.addListener(self)  # react to clicks
        self.addComponent(b)

        # Button w/ text, icon and tooltip
        b = Button(self._CAPTION)
        b.setStyleName(BaseTheme.BUTTON_LINK)
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self)  # react to clicks
        self.addComponent(b)

        # Button w/ icon and tooltip
        b = Button()
        b.setStyleName(BaseTheme.BUTTON_LINK)
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self)
        # react to clicks
        self.addComponent(b)

    # Shows a notification when a button is clicked.
    def buttonClick(self, event):
        self.getWindow().showNotification(self._NOTIFICATION)
