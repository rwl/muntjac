# -*- coding: utf-8 -*-
# from com.vaadin.terminal.ThemeResource import (ThemeResource,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.CheckBox import (CheckBox,)
# from com.vaadin.ui.VerticalLayout import (VerticalLayout,)


class CheckBoxesExample(VerticalLayout, Button.ClickListener):
    _CAPTION = 'Allow HTML'
    _TOOLTIP = 'Allow/disallow HTML in comments'
    _ICON = ThemeResource('../sampler/icons/page_code.gif')

    def __init__(self):
        # Shows a notification when a checkbox is clicked.
        self.setSpacing(True)
        # Button w/ text and tooltip
        cb = CheckBox(self._CAPTION)
        cb.setDescription(self._TOOLTIP)
        cb.setImmediate(True)
        cb.addListener(self)
        # react to clicks
        self.addComponent(cb)
        # Button w/ text, icon and tooltip
        cb = CheckBox(self._CAPTION)
        cb.setDescription(self._TOOLTIP)
        cb.setIcon(self._ICON)
        cb.setImmediate(True)
        cb.addListener(self)
        # react to clicks
        self.addComponent(cb)
        # Button w/ icon and tooltip
        cb = CheckBox()
        cb.setDescription(self._TOOLTIP)
        cb.setIcon(self._ICON)
        cb.setImmediate(True)
        cb.addListener(self)
        # react to clicks
        self.addComponent(cb)

    def buttonClick(self, event):
        enabled = event.getButton().booleanValue()
        self.getWindow().showNotification('HTML ' + ('enabled' if enabled else 'disabled'))
