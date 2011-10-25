
from muntjac.api import VerticalLayout, Button
from muntjac.ui.themes import BaseTheme
from muntjac.ui import button

from muntjac.terminal.theme_resource import ThemeResource


class ButtonLinkExample(VerticalLayout, button.IClickListener):

    _CAPTION = 'Help'
    _TOOLTIP = 'Show help'
    _ICON = ThemeResource('../sampler/icons/icon_info.gif')
    _NOTIFICATION = 'Help clicked'

    def __init__(self):
        super(ButtonLinkExample, self).__init__()

        self.setSpacing(True)

        # Button w/ text and tooltip
        b = Button(self._CAPTION)
        b.setStyleName(BaseTheme.BUTTON_LINK)
        b.setDescription(self._TOOLTIP)
        b.addListener(self, button.IClickListener)  # react to clicks
        self.addComponent(b)

        # Button w/ text, icon and tooltip
        b = Button(self._CAPTION)
        b.setStyleName(BaseTheme.BUTTON_LINK)
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self, button.IClickListener)  # react to clicks
        self.addComponent(b)

        # Button w/ icon and tooltip
        b = Button()
        b.setStyleName(BaseTheme.BUTTON_LINK)
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self, button.IClickListener)  # react to clicks
        self.addComponent(b)

    # Shows a notification when a button is clicked.
    def buttonClick(self, event):
        self.getWindow().showNotification(self._NOTIFICATION)
