# -*- coding: utf-8 -*-
# from com.vaadin.ui.Alignment import (Alignment,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
# from com.vaadin.ui.VerticalLayout import (VerticalLayout,)
# from com.vaadin.ui.themes.BaseTheme import (BaseTheme,)


class ProminentPrimaryActionExample(VerticalLayout, Button.ClickListener):

    def __init__(self):
        # Cancel / Save
        # Sign up / Sign in
        # Login / Forgot password?
        # Shows a notification when a button is clicked.
        self.setSpacing(True)
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

    def buttonClick(self, event):
        self.getWindow().showNotification('\"' + event.getButton().getCaption() + '\" clicked')
