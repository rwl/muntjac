# -*- coding: utf-8 -*-
# from com.vaadin.terminal.UserError import (UserError,)
# from com.vaadin.ui.FormLayout import (FormLayout,)


class ErrorsExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)
        self.addComponent(ALabel('<h3>Errors in caption</h3>', ALabel.CONTENT_XHTML))
        self.addComponent(ALabel('Error indicators are usually placed on the right side of the component\'s caption.'))
        input = TextField('Field caption')
        input.setComponentError(UserError('This field is never satisfied'))
        self.addComponent(input)
        self.addComponent(ALabel('<h3>Errors without caption</h3>', ALabel.CONTENT_XHTML))
        self.addComponent(ALabel('If the component has no caption, the error indicator is usually placed on the right side of the component.'))
        input = TextField()
        input.setInputPrompt('This field has an error')
        input.setComponentError(UserError('This field is never satisfied.'))
        self.addComponent(input)
        self.addComponent(ALabel('<h3>Error icon placement depends on the layout</h3>', ALabel.CONTENT_XHTML))
        self.addComponent(ALabel('FormLayout for example places the error between the component caption and the actual field.'))
        fl = FormLayout()
        fl.setMargin(False)
        fl.setSpacing(False)
        self.addComponent(fl)
        input = TextField('Field caption')
        input.setInputPrompt('This field has an error')
        input.setComponentError(UserError('This field is never satisfied.'))
        fl.addComponent(input)
