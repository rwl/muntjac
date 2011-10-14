# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.ui.LoginForm import (LoginForm,)
# from com.vaadin.ui.LoginForm.LoginEvent import (LoginEvent,)
# from com.vaadin.ui.LoginForm.LoginListener import (LoginListener,)


class LoginFormListeners(AbstractListenerMethodsTest):

    def testLoginListenerAddGetRemove(self):
        self.testListenerAddGetRemove(LoginForm, LoginEvent, LoginListener)
