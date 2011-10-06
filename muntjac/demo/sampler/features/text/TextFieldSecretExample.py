
from muntjac.ui import \
    VerticalLayout, TextField, PasswordField, button, Button, Alignment


class TextFieldSecretExample(VerticalLayout):

    def __init__(self):
        self.setSizeUndefined()  # let content 'push' size

        self.setSpacing(True)
        # Username
        self._username = TextField('Username')
        self.addComponent(self._username)

        # Password
        self._password = PasswordField('Password')
        self.addComponent(self._password)

        # Login button
        class LoginListener(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                self.getWindow().showNotification(
                        'User: ' + self._c._username.getValue() +
                        ' Password: ' + self._c._password.getValue())


        loginButton = Button('Login', LoginListener(self))
        self.addComponent(loginButton)
        self.setComponentAlignment(loginButton, Alignment.TOP_RIGHT)
