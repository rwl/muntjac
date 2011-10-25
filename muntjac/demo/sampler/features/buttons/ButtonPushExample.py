
from muntjac.api import \
    HorizontalLayout, VerticalLayout, Button, NativeButton, Label

from muntjac.ui.button import IClickListener

from muntjac.terminal.theme_resource import ThemeResource


class ButtonPushExample(HorizontalLayout, IClickListener):

    _CAPTION = 'Save'
    _TOOLTIP = 'Save changes'
    _ICON = ThemeResource('../sampler/icons/action_save.gif')
    _NOTIFICATION = 'Changes have been saved'

    def __init__(self):
        super(ButtonPushExample, self).__init__()

        # Normal buttons (more themable)
        buttons = VerticalLayout()
        buttons.setSpacing(True)
        buttons.setMargin(False, True, False, False)
        self.addComponent(buttons)
        buttons.addComponent(Label("<h3>Normal buttons</h3>",
                Label.CONTENT_XHTML))

        # Button w/ text and tooltip
        b = Button(self._CAPTION)
        b.setDescription(self._TOOLTIP)
        b.addListener(self, IClickListener)  # react to clicks
        buttons.addComponent(b)

        # Button w/ text, icon and tooltip
        b = Button(self._CAPTION)
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self, IClickListener)  # react to clicks
        buttons.addComponent(b)

        # Button w/ icon and tooltip
        b = Button()
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self, IClickListener)  # react to clicks
        buttons.addComponent(b)

        # NativeButtons
        buttons = VerticalLayout()
        buttons.setSpacing(True)
        buttons.setMargin(False, False, False, True)
        self.addComponent(buttons)
        buttons.addComponent(Label("<h3>Native buttons</h3>",
                Label.CONTENT_XHTML));

        # NativeButton w/ text and tooltip
        b = NativeButton(self._CAPTION)
        b.setDescription(self._TOOLTIP)
        b.addListener(self, IClickListener)  # react to clicks
        buttons.addComponent(b)

        # NativeButton w/ text, icon and tooltip
        b = NativeButton(self._CAPTION)
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self, IClickListener)  # react to clicks
        buttons.addComponent(b)

        # NativeButton w/ icon and tooltip
        b = NativeButton()
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self, IClickListener)  # react to clicks
        buttons.addComponent(b)

    # Shows a notification when a button is clicked.
    def buttonClick(self, event):
        self.getWindow().showNotification(self._NOTIFICATION)
