# -*- coding: utf-8 -*-
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.data.Property.ValueChangeListener import (ValueChangeListener,)
# from com.vaadin.data.validator.CompositeValidator import (CompositeValidator,)
# from com.vaadin.data.validator.StringLengthValidator import (StringLengthValidator,)
# from com.vaadin.ui.TextField import (TextField,)
# from java.util.HashSet import (HashSet,)


class ValidationExample(VerticalLayout):
    _usernames = set()

    def __init__(self):
        self.setSpacing(True)
        pin = TextField('PIN')
        pin.setWidth('50px')
        # optional; validate at once instead of when clicking 'save' (e.g)
        pin.setImmediate(True)
        self.addComponent(pin)
        # add the validator
        pin.addValidator(StringLengthValidator('Must be 4-6 characters', 4, 6, False))
        username = TextField('Username')
        # optional; validate at once instead of when clicking 'save' (e.g)
        username.setImmediate(True)
        self.addComponent(username)
        usernameValidator = CompositeValidator()
        username.addValidator(usernameValidator)
        usernameValidator.addValidator(StringLengthValidator('Username must be at least 4 characters', 4, 255, False))

        class _0_(Validator):

            def isValid(self, value):
                return not (value in ValidationExample_this._usernames)

            def validate(self, value):
                if not self.isValid(value):
                    raise Validator.InvalidValueException('Username ' + value + ' already in use')

        _0_ = _0_()
        usernameValidator.addValidator(_0_)

        class _1_(ValueChangeListener):

            def valueChange(self, event):
                tf = event.getProperty()
                tf.validate()
                if tf.getValue() is not None:
                    ValidationExample_this._usernames.add(str(tf.getValue()))
                    self.addComponent(Label('Added ' + tf.getValue() + ' to usernames'))

        _1_ = _1_()
        username.addListener(_1_)
