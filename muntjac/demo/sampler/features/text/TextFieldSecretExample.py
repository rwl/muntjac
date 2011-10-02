# -*- coding: utf-8 -*-


class TextFieldSecretExample(VerticalLayout):
    _username = None
    _password = None

    def __init__(self):
        self.setSizeUndefined()
        # let content 'push' size
        self.setSpacing(True)
        # Username
        self._username = TextField('Username')
        self.addComponent(self._username)
        # Password
        self._password = PasswordField('Password')
        self.addComponent(self._password)
        # Login button

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                self.getWindow().showNotification('User: ' + TextFieldSecretExample_this._username.getValue() + ' Password: ' + TextFieldSecretExample_this._password.getValue())

        _0_ = _0_()
        loginButton = Button('Login', _0_)
        self.addComponent(loginButton)
        self.setComponentAlignment(loginButton, Alignment.TOP_RIGHT)
