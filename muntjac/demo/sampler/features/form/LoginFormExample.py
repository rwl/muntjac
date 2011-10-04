
from muntjac.demo.sampler.features.form.LoginForm import LoginForm
from muntjac.ui import VerticalLayout, login_form


class LoginFormExample(VerticalLayout):

    def __init__(self):
        login = LoginForm()
        login.setWidth('100%')
        login.setHeight('300px')


        class NewLoginListener(login_form.ILoginListener):

            def __init__(self, c):
                self._c = c

            def onLogin(self, event):
                self._c.getWindow().showNotification('New Login', 'Username: '
                        + event.getLoginParameter('username')
                        + ', password: ' + event.getLoginParameter('password'))


        login.addListener( NewLoginListener(self) )
        self.addComponent(login)
