
from muntjac.api import VerticalLayout, button, CheckBox
from muntjac.terminal.theme_resource import ThemeResource


class CheckBoxesExample(VerticalLayout, button.IClickListener):

    _CAPTION = 'Allow HTML'
    _TOOLTIP = 'Allow/disallow HTML in comments'
    _ICON = ThemeResource('../sampler/icons/page_code.gif')

    def __init__(self):
        self.setSpacing(True)

        # Button w/ text and tooltip
        cb = CheckBox(self._CAPTION)
        cb.setDescription(self._TOOLTIP)
        cb.setImmediate(True)
        cb.addListener(self)  # react to clicks
        self.addComponent(cb)

        # Button w/ text, icon and tooltip
        cb = CheckBox(self._CAPTION)
        cb.setDescription(self._TOOLTIP)
        cb.setIcon(self._ICON)
        cb.setImmediate(True)
        cb.addListener(self)  # react to clicks
        self.addComponent(cb)

        # Button w/ icon and tooltip
        cb = CheckBox()
        cb.setDescription(self._TOOLTIP)
        cb.setIcon(self._ICON)
        cb.setImmediate(True)
        cb.addListener(self)  # react to clicks
        self.addComponent(cb)

    # Shows a notification when a checkbox is clicked.
    def buttonClick(self, event):
        enabled = event.getButton().booleanValue()
        self.getWindow().showNotification('HTML '
                + ('enabled' if enabled else 'disabled'))
