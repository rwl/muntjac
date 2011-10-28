
from muntjac.api import \
    VerticalLayout, TextField, PasswordField, Button, Alignment
from muntjac.ui.button import IClickListener


class TextFieldSecretExample(VerticalLayout):

    def __init__(self):
        super(TextFieldSecretExample, self).__init__()

        self.setSizeUndefined()  # let content 'push' size

        self.setSpacing(True)
        # Username
        self._username = TextField('Username')
        self.addComponent(self._username)

        # Password
        self._password = PasswordField('Password')
        self.addComponent(self._password)

        # Login button
        loginButton = Button('Login', LoginListener(self))
        self.addComponent(loginButton)
        self.setComponentAlignment(loginButton, Alignment.TOP_RIGHT)


class LoginListener(IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c.getWindow().showNotification(
                'User: ' + self._c._username.getValue() +
                ' Password: ' + self._c._password.getValue())
