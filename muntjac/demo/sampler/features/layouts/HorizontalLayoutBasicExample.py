# -*- coding: utf-8 -*-
# from com.vaadin.ui.TextField import (TextField,)


class HorizontalLayoutBasicExample(HorizontalLayout):

    def __init__(self):
        # this is a HorizontalLayout
        # First TextField
        tf = TextField()
        tf.setWidth('70px')
        self.addComponent(tf)
        # A dash
        dash = Label('-')
        self.addComponent(dash)
        self.setComponentAlignment(dash, Alignment.MIDDLE_LEFT)
        # Second TextField
        tf = TextField()
        tf.setWidth('70px')
        self.addComponent(tf)
        # Another dash
        dash = Label('-')
        self.addComponent(dash)
        self.setComponentAlignment(dash, Alignment.MIDDLE_LEFT)
        # Third TextField
        tf = TextField()
        tf.setWidth('70px')
        self.addComponent(tf)
        # Yet another dash
        dash = Label('-')
        self.addComponent(dash)
        self.setComponentAlignment(dash, Alignment.MIDDLE_LEFT)
        # Forth and last TextField
        tf = TextField()
        tf.setWidth('70px')
        self.addComponent(tf)
