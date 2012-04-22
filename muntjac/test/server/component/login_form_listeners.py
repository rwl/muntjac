# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.login_form import LoginForm, LoginEvent, ILoginListener


class LoginFormListeners(AbstractListenerMethodsTest):

    def testLoginListenerAddGetRemove(self):
        self._testListenerAddGetRemove(LoginForm, LoginEvent, ILoginListener)
