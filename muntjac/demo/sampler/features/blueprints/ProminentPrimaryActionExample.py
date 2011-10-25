
from muntjac.api import \
    VerticalLayout, HorizontalLayout, Button, Alignment

from muntjac.ui.themes import BaseTheme
from muntjac.ui.button import IClickListener


class ProminentPrimaryActionExample(VerticalLayout, IClickListener):

    def __init__(self):
        super(ProminentPrimaryActionExample, self).__init__()

        self.setSpacing(True)

        # Cancel / Save
        horiz = HorizontalLayout()
        horiz.setCaption('Save/cancel example:')
        horiz.setSpacing(True)
        horiz.setMargin(True)
        self.addComponent(horiz)
        secondary = Button('Cancel', self)
        secondary.setStyleName(BaseTheme.BUTTON_LINK)
        horiz.addComponent(secondary)
        primary = Button('Save', self)
        horiz.addComponent(primary)

        # Sign up / Sign in
        horiz = HorizontalLayout()
        horiz.setCaption('Sign up example:')
        horiz.setSpacing(True)
        horiz.setMargin(True)
        self.addComponent(horiz)
        primary = Button('Sign up', self)
        primary.addStyleName('primary')
        horiz.addComponent(primary)
        secondary = Button('or Sign in', self)
        secondary.setStyleName(BaseTheme.BUTTON_LINK)
        horiz.addComponent(secondary)
        horiz.setComponentAlignment(secondary, Alignment.MIDDLE_LEFT)

        # Login / Forgot password?
        vert = VerticalLayout()
        vert.setCaption('Login example:')
        vert.setSizeUndefined()
        vert.setSpacing(True)
        vert.setMargin(True)
        self.addComponent(vert)
        primary = Button('Login', self)
        vert.addComponent(primary)
        vert.setComponentAlignment(primary, Alignment.BOTTOM_RIGHT)
        secondary = Button('Forgot your password?', self)
        secondary.setStyleName(BaseTheme.BUTTON_LINK)
        vert.addComponent(secondary)
        vert.setComponentAlignment(secondary, Alignment.BOTTOM_RIGHT)


    # Shows a notification when a button is clicked.
    def buttonClick(self, event):
        self.getWindow().showNotification('\"'
                + event.getButton().getCaption() + '\" clicked')
