# -*- coding: utf-8 -*-
# from com.vaadin.ui.PasswordField import (PasswordField,)


class TextFieldInputPromptExample(VerticalLayout, Property.ValueChangeListener):

    def __init__(self):
        # add som 'air' to the layout
        self.setSpacing(True)
        self.setMargin(True, False, False, False)
        # Username field + input prompt
        username = TextField()
        username.setInputPrompt('Username')
        # configure & add to layout
        username.setImmediate(True)
        username.addListener(self)
        self.addComponent(username)
        # Password field + input prompt
        password = PasswordField()
        password.setInputPrompt('Password')
        # configure & add to layout
        password.setImmediate(True)
        password.addListener(self)
        self.addComponent(password)
        # Comment field + input prompt
        comment = self.com.vaadin.ui.TextArea()
        comment.setInputPrompt('Comment')
        # configure & add to layout
        comment.setRows(3)
        comment.setImmediate(True)
        comment.addListener(self)
        self.addComponent(comment)

    def valueChange(self, event):
        self.getWindow().showNotification('Received ' + event.getProperty())
