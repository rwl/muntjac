# Copyright (C) 2011 Vaadin Ltd
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from muntjac.ui.Component import Event
from muntjac.ui.Embedded import Embedded
from muntjac.ui.CustomComponent import CustomComponent
from muntjac.terminal.ApplicationResource import ApplicationResource
from muntjac.terminal.URIHandler import URIHandler
from muntjac.terminal.DownloadStream import DownloadStream
from muntjac.terminal.ParameterHandler import ParameterHandler

from muntjac.terminal.gwt.client.ApplicationConnection import ApplicationConnection


class LoginEvent(Event):
    """This event is sent when login form is submitted."""
    _params = None

    def __init__(self, params, _LoginForm_this):  # FIXME: translate inner class
        super(LoginEvent, self)(_LoginForm_this)
        self._params = params


    def getLoginParameter(self, name):
        """Access method to form values by field names.

        @param name
        @return value in given field
        """
        if name in self._params:
            return self._params.get(name)
        else:
            return None


class LoginListener(object):
    """Login listener is a class capable to listen LoginEvents sent from
    LoginBox
    """

    def onLogin(self, event):
        """This method is fired on each login form post.

        @param event
        """
        pass


class LoginForm(CustomComponent):
    """LoginForm is a Vaadin component to handle common problem among Ajax
    applications: browsers password managers don't fill dynamically created forms
    like all those UI elements created by Vaadin.
    <p>
    For developer it is easy to use: add component to a desired place in you UI
    and add LoginListener to validate form input. Behind the curtain LoginForm
    creates an iframe with static html that browsers detect.
    <p>
    Login form is by default 100% width and height, so consider using it inside a
    sized {@link Panel} or {@link Window}.
    <p>
    Login page html can be overridden by replacing protected getLoginHTML method.
    As the login page is actually an iframe, styles must be handled manually. By
    default component tries to guess the right place for theme css.
    <p>
    Note, this is a new Ajax terminal specific component and is likely to change.

    @since 5.3
    """

    def __init__(self):
        self._usernameCaption = 'Username'
        self._passwordCaption = 'Password'
        self._loginButtonCaption = 'Login'
        self._iframe = Embedded()

        self._window = None

        self._iframe.setType(Embedded.TYPE_BROWSER)
        self._iframe.setSizeFull()
        self.setSizeFull()
        self.setCompositionRoot(self._iframe)
        self.addStyleName('v-loginform')

        self.loginPage = LoginPage(self)  # FIXME: translate inner classes
        self.parameterHandler = ParameterHandler()
        self.uriHandler = UriHandler()


    def getLoginHTML(self):
        """Returns byte array containing login page html. If you need to override
        the login html, use the default html as basis. Login page sets its target
        with javascript.

        @return byte array containing login page html
        """
        appUri = str(self.getApplication().getURL()) \
                + self.getWindow().getName() + '/'

        return '<!DOCTYPE html PUBLIC \"-//W3C//DTD ' \
                + 'XHTML 1.0 Transitional//EN\" ' \
                + '\"http://www.w3.org/TR/xhtml1/' \
                + 'DTD/xhtml1-transitional.dtd\">\n' \
                + '<html>' \
                + '<head><script type=\'text/javascript\'>' \
                + 'var setTarget = function() {' \
                + 'var uri = \'' \
                + appUri \
                + 'loginHandler' \
                + '\'; var f = document.getElementById(\'loginf\');' \
                + 'document.forms[0].action = uri;document.forms[0].username.focus();};' \
                + '' + 'var styles = window.parent.document.styleSheets;' \
                + 'for(var j = 0; j < styles.length; j++) {\n' \
                + 'if(styles[j].href) {' \
                + 'var stylesheet = document.createElement(\'link\');\n' \
                + 'stylesheet.setAttribute(\'rel\', \'stylesheet\');\n' \
                + 'stylesheet.setAttribute(\'type\', \'text/css\');\n' \
                + 'stylesheet.setAttribute(\'href\', styles[j].href);\n' \
                + 'document.getElementsByTagName(\'head\')[0].appendChild(stylesheet);\n' \
                + '}' \
                + '}\n' \
                + 'function submitOnEnter(e) { var keycode = e.keyCode || e.which;' \
                + ' if (keycode == 13) {document.forms[0].submit();}  } \n' \
                + '</script>' \
                + '</head><body onload=\'setTarget();\' style=\'margin:0;padding:0; background:transparent;\' class=\"' \
                + ApplicationConnection.GENERATED_BODY_CLASSNAME \
                + '\">' + '<div class=\'v-app v-app-loginpage\' style=\"background:transparent;\">' \
                + '<iframe name=\'logintarget\' style=\'width:0;height:0;' \
                + 'border:0;margin:0;padding:0;\'></iframe>' \
                + '<form id=\'loginf\' target=\'logintarget\' onkeypress=\"submitOnEnter(event)\" method=\"post\">' \
                + '<div>' \
                + self._usernameCaption \
                + '</div><div >' \
                + '<input class=\'v-textfield\' style=\'display:block;\' type=\'text\' name=\'username\'></div>' \
                + '<div>' \
                + self._passwordCaption \
                + '</div>' \
                + '<div><input class=\'v-textfield\' style=\'display:block;\' type=\'password\' name=\'password\'></div>' \
                + '<div><div onclick=\"document.forms[0].submit();\" tabindex=\"0\" class=\"v-button\" role=\"button\" ><span class=\"v-button-wrap\"><span class=\"v-button-caption\">' \
                + self._loginButtonCaption \
                + '</span></span></div></div></form></div>' \
                + '</body></html>'


    def attach(self):
        super(LoginForm, self).attach()
        self.getApplication().addResource(self.loginPage)
        self.getWindow().addParameterHandler(self.paramHandler)
        self._iframe.setSource(self.loginPage)


    def detach(self):
        self.getApplication().removeResource(self.loginPage)
        self.getWindow().removeParameterHandler(self.paramHandler)
        # store window temporary to properly remove uri handler once
        # response is handled. (May happen if login handler removes login
        # form
        self._window = self.getWindow()
        if self._window.getParent() is not None:
            self._window = self._window.getParent()
        super(LoginForm, self).detach()


    _ON_LOGIN_METHOD = getattr(LoginListener, 'onLogin')  # FIXME: translate getDeclaredMethod
    _UNDEFINED_HEIGHT = '140px'
    _UNDEFINED_WIDTH = '200px'


    def addListener(self, listener):
        """Adds LoginListener to handle login logic

        @param listener
        """
        self.addListener(LoginEvent, listener, self._ON_LOGIN_METHOD)


    def removeListener(self, listener):
        """Removes LoginListener

        @param listener
        """
        self.removeListener(self.LoginEvent, listener, self._ON_LOGIN_METHOD)


    def setWidth(self, width, unit):
        super(LoginForm, self).setWidth(width, unit)
        if self._iframe is not None:
            if width < 0:
                self._iframe.setWidth(self._UNDEFINED_WIDTH)
            else:
                self._iframe.setWidth('100%')


    def setHeight(self, height, unit):
        super(LoginForm, self).setHeight(height, unit)
        if self._iframe is not None:
            if height < 0:
                self._iframe.setHeight(self._UNDEFINED_HEIGHT)
            else:
                self._iframe.setHeight('100%')


    def getUsernameCaption(self):
        """Returns the caption for the user name field.

        @return String
        """
        return self._usernameCaption


    def setUsernameCaption(self, usernameCaption):
        """Sets the caption to show for the user name field. The caption cannot be
        changed after the form has been shown to the user.

        @param usernameCaption
        """
        self._usernameCaption = usernameCaption


    def getPasswordCaption(self):
        """Returns the caption for the password field.

        @return String
        """
        return self._passwordCaption


    def setPasswordCaption(self, passwordCaption):
        """Sets the caption to show for the password field. The caption cannot be
        changed after the form has been shown to the user.

        @param passwordCaption
        """
        self._passwordCaption = passwordCaption


    def getLoginButtonCaption(self):
        """Returns the caption for the login button.

        @return String
        """
        return self._loginButtonCaption


    def setLoginButtonCaption(self, loginButtonCaption):
        """Sets the caption (button text) to show for the login button. The caption
        cannot be changed after the form has been shown to the user.

        @param loginButtonCaption
        """
        self._loginButtonCaption = loginButtonCaption




class LoginPage(ApplicationResource):

    def __init__(self, _LoginForm_this_):
        self._LoginForm_this_ = _LoginForm_this_


    def getApplication(self):
        return self._LoginForm_this_.getApplication()


    def getBufferSize(self):
        return len(self._LoginForm_this_.getLoginHTML())


    def getCacheTime(self):
        return -1


    def getFilename(self):
        return "login"


    def getStream(self):
        return DownloadStream(StringIO(self._LoginForm_this_.getLoginHTML()),
                              self._LoginForm_this_.getMIMEType(),
                              self._LoginForm_this_.getFilename())


    def getMIMEType(self):
        return "text/html; charset=utf-8"


class ParamHandler(ParameterHandler):

    def handleParameters(self, parameters):
        if 'username' in parameters:
            self.getWindow().addURIHandler(self.uriHandler)
            params = dict()
            # expecting single params
            _0 = True
            it = parameters.keys()
            while True:
                if _0 is True:
                    _0 = False
                if not it.hasNext():
                    break
                key = it.next()
                value = parameters[key][0]
                params.put(key, value)
            event = LoginEvent(params)
            self.fireEvent(event)


class UriHandler(URIHandler):

    def __init__(self):
        self._responce = '<html><body>Login form handeled.' \
            + '<script type=\'text/javascript\'>top.vaadin.forceSync();' \
            + '</script></body></html>'


    def handleURI(self, context, relativeUri):
        if relativeUri is not None and relativeUri.contains('loginHandler'):
            if self.window is not None:
                self.window.removeURIHandler(self)
            downloadStream = DownloadStream(StringIO(), 'text/html', 'loginSuccesfull')
            downloadStream.setCacheTime(-1)
            return downloadStream
        else:
            return None