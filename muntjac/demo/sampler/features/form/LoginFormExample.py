
from muntjac.api import VerticalLayout
from muntjac.ui.login_form import LoginForm, ILoginListener


class LoginFormExample(VerticalLayout):

    def __init__(self):
        super(LoginFormExample, self).__init__()

        login = LoginForm()
        login.setWidth('100%')
        login.setHeight('300px')

        login.addListener(NewLoginListener(self), ILoginListener)
        self.addComponent(login)


class NewLoginListener(ILoginListener):

    def __init__(self, c):
        self._c = c

    def onLogin(self, event):
        self._c.getWindow().showNotification('New Login', 'Username: '
                + event.getLoginParameter('username')
                + ', password: ' + event.getLoginParameter('password'))