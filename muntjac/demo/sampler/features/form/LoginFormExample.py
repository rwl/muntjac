# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.form.LoginForm import (LoginForm,)
# from com.vaadin.ui.LoginForm import (LoginForm,)
# from com.vaadin.ui.LoginForm.LoginEvent import (LoginEvent,)
# from com.vaadin.ui.VerticalLayout import (VerticalLayout,)


class LoginFormExample(VerticalLayout):

    def __init__(self):
        login = LoginForm()
        login.setWidth('100%')
        login.setHeight('300px')

        class _0_(LoginForm.LoginListener):

            def onLogin(self, event):
                self.getWindow().showNotification('New Login', 'Username: ' + event.getLoginParameter('username') + ', password: ' + event.getLoginParameter('password'))

        _0_ = _0_()
        login.addListener(_0_)
        self.addComponent(login)
