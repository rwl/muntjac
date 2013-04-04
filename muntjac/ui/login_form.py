# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from muntjac.ui.component import Event
from muntjac.ui.embedded import Embedded
from muntjac.ui.custom_component import CustomComponent
from muntjac.terminal.application_resource import IApplicationResource
from muntjac.terminal.uri_handler import IUriHandler
from muntjac.terminal.download_stream import DownloadStream
from muntjac.terminal.parameter_handler import IParameterHandler

from muntjac.terminal.gwt.client.application_connection import \
    ApplicationConnection


class LoginEvent(Event):
    """This event is sent when login form is submitted."""

    def __init__(self, params, form):
        super(LoginEvent, self).__init__(form)
        self._params = params


    def getLoginParameter(self, name):
        """Access method to form values by field names.

        @return: value in given field
        """
        if name in self._params:
            return self._params.get(name)
        else:
            return None


class ILoginListener(object):
    """Login listener is a class capable to listen LoginEvents sent from
    LoginBox
    """

    def onLogin(self, event):
        """This method is fired on each login form post.
        """
        raise NotImplementedError


_ON_LOGIN_METHOD = getattr(ILoginListener, 'onLogin')


class LoginForm(CustomComponent):
    """LoginForm is a Muntjac component to handle common problem among Ajax
    applications: browsers password managers don't fill dynamically created
    forms like all those UI elements created by Muntjac.

    For developer it is easy to use: add component to a desired place in you
    UI and add ILoginListener to validate form input. Behind the curtain
    LoginForm creates an iframe with static html that browsers detect.

    Login form is by default 100% width and height, so consider using it
    inside a sized L{Panel} or L{Window}.

    Login page html can be overridden by replacing protected getLoginHTML
    method. As the login page is actually an iframe, styles must be handled
    manually. By default component tries to guess the right place for theme
    css.

    Note, this is a new Ajax terminal specific component and is likely to
    change.
    """

    def __init__(self):
        self._usernameCaption = 'Username'
        self._passwordCaption = 'Password'
        self._loginButtonCaption = 'Login'
        self._iframe = Embedded()

        self._window = None

        super(LoginForm, self).__init__()

        self._iframe.setType(Embedded.TYPE_BROWSER)
        self._iframe.setSizeFull()
        self.setSizeFull()
        self.setCompositionRoot(self._iframe)
        self.addStyleName('v-loginform')

        self.loginPage = LoginPage(self)
        self.parameterHandler = ParameterHandler(self)
        self.uriHandler = UriHandler(self)


    def getLoginHTML(self):
        """Returns byte array containing login page html. If you need to
        override the login html, use the default html as basis. Login page
        sets its target with javascript.

        @return: byte array containing login page html
        """
        appUri = str(self.getApplication().getURL()) \
                + self.getWindow().getName() + '/'

        return ('<!DOCTYPE html PUBLIC \"-//W3C//DTD '
                'XHTML 1.0 Transitional//EN\" '
                '\"http://www.w3.org/TR/xhtml1/'
                'DTD/xhtml1-transitional.dtd\">\n'
                '<html>'
                '<head><script type=\'text/javascript\'>'
                'var setTarget = function() {'
                'var uri = \''
                + appUri +
                'loginHandler'
                '\'; var f = document.getElementById(\'loginf\');'
                'document.forms[0].action = uri;document.forms[0].username.focus();};'
                '' + 'var styles = window.parent.document.styleSheets;'
                'for(var j = 0; j < styles.length; j++) {\n'
                'if(styles[j].href) {'
                'var stylesheet = document.createElement(\'link\');\n'
                'stylesheet.setAttribute(\'rel\', \'stylesheet\');\n'
                'stylesheet.setAttribute(\'type\', \'text/css\');\n'
                'stylesheet.setAttribute(\'href\', styles[j].href);\n'
                'document.getElementsByTagName(\'head\')[0].appendChild(stylesheet);\n'
                '}'
                '}\n'
                'function submitOnEnter(e) { var keycode = e.keyCode || e.which;'
                ' if (keycode == 13) {document.forms[0].submit();}  } \n'
                '</script>'
                '</head><body onload=\'setTarget();\' style=\'margin:0;padding:0; background:transparent;\' class=\"'
                + ApplicationConnection.GENERATED_BODY_CLASSNAME +
                '\">' + '<div class=\'v-app v-app-loginpage\' style=\"background:transparent;\">'
                '<iframe name=\'logintarget\' style=\'width:0;height:0;'
                'border:0;margin:0;padding:0;\'></iframe>'
                '<form id=\'loginf\' target=\'logintarget\' onkeypress=\"submitOnEnter(event)\" method=\"post\">'
                '<div>'
                + self._usernameCaption +
                '</div><div >'
                '<input class=\'v-textfield\' style=\'display:block;\' type=\'text\' name=\'username\'></div>'
                '<div>'
                + self._passwordCaption +
                '</div>'
                '<div><input class=\'v-textfield\' style=\'display:block;\' type=\'password\' name=\'password\'></div>'
                '<div><div onclick=\"document.forms[0].submit();\" tabindex=\"0\" class=\"v-button\" role=\"button\" ><span class=\"v-button-wrap\"><span class=\"v-button-caption\">'
                + self._loginButtonCaption +
                '</span></span></div></div></form></div>'
                '</body></html>').encode('utf-8')


    def attach(self):
        super(LoginForm, self).attach()
        self.getApplication().addResource(self.loginPage)
        self.getWindow().addParameterHandler(self.parameterHandler)
        self._iframe.setSource(self.loginPage)


    def detach(self):
        self.getApplication().removeResource(self.loginPage)
        self.getWindow().removeParameterHandler(self.parameterHandler)
        # store window temporary to properly remove uri handler once
        # response is handled. (May happen if login handler removes login
        # form
        self._window = self.getWindow()
        if self._window.getParent() is not None:
            self._window = self._window.getParent()
        super(LoginForm, self).detach()


    _UNDEFINED_HEIGHT = '140px'
    _UNDEFINED_WIDTH = '200px'


    def addListener(self, listener, iface=None):
        """Adds ILoginListener to handle login logic.
        """
        if (isinstance(listener, ILoginListener) and
                (iface is None or issubclass(iface, ILoginListener))):
            self.registerListener(LoginEvent, listener, _ON_LOGIN_METHOD)

        super(LoginForm, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, LoginEvent):
            self.registerCallback(LoginEvent, callback, None, *args)
        else:
            super(LoginForm, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        """Removes ILoginListener.
        """
        if (isinstance(listener, ILoginListener) and
                (iface is None or issubclass(iface, ILoginListener))):
            self.withdrawListener(LoginEvent, listener, _ON_LOGIN_METHOD)

        super(LoginForm, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, LoginEvent):
            self.withdrawCallback(LoginEvent, callback)
        else:
            super(LoginForm, self).removeCallback(callback, eventType)


    def setWidth(self, width, unit=None):
        if unit is not None:
            super(LoginForm, self).setWidth(width, unit)
            if self._iframe is not None:
                if width < 0:
                    self._iframe.setWidth(self._UNDEFINED_WIDTH)
                else:
                    self._iframe.setWidth('100%')
        else:
            super(LoginForm, self).setWidth(width)


    def setHeight(self, height, unit=None):
        if unit is not None:
            super(LoginForm, self).setHeight(height, unit)
            if self._iframe is not None:
                if height < 0:
                    self._iframe.setHeight(self._UNDEFINED_HEIGHT)
                else:
                    self._iframe.setHeight('100%')
        else:
            super(LoginForm, self).setHeight(height)


    def getUsernameCaption(self):
        """Returns the caption for the user name field.
        """
        return self._usernameCaption


    def setUsernameCaption(self, usernameCaption):
        """Sets the caption to show for the user name field. The caption
        cannot be changed after the form has been shown to the user.
        """
        self._usernameCaption = usernameCaption


    def getPasswordCaption(self):
        """Returns the caption for the password field.
        """
        return self._passwordCaption


    def setPasswordCaption(self, passwordCaption):
        """Sets the caption to show for the password field. The caption
        cannot be changed after the form has been shown to the user.
        """
        self._passwordCaption = passwordCaption


    def getLoginButtonCaption(self):
        """Returns the caption for the login button.
        """
        return self._loginButtonCaption


    def setLoginButtonCaption(self, loginButtonCaption):
        """Sets the caption (button text) to show for the login button. The
        caption cannot be changed after the form has been shown to the user.
        """
        self._loginButtonCaption = loginButtonCaption


class LoginPage(IApplicationResource):

    def __init__(self, form):
        self._form = form


    def getApplication(self):
        return self._form.getApplication()


    def getBufferSize(self):
        return len(self._form.getLoginHTML())


    def getCacheTime(self):
        return -1


    def getFilename(self):
        return "login"


    def getStream(self):
        return DownloadStream(StringIO(self._form.getLoginHTML()),
                self.getMIMEType(), self.getFilename())


    def getMIMEType(self):
        return "text/html; charset=utf-8"


class ParameterHandler(IParameterHandler):

    def __init__(self, form):
        self._form = form


    def handleParameters(self, parameters):
        if 'username' in parameters:
            self._form.getWindow().addURIHandler(self._form.uriHandler)
            params = dict()
            # expecting single params
            for key in parameters:
                value = parameters.get(key)
                params[key] = value
            event = LoginEvent(params, self._form)
            self._form.fireEvent(event)


class UriHandler(IUriHandler):

    def __init__(self, form):
        self._form = form
        self._responce = ('<html><body>Login form handeled.'
            + '<script type=\'text/javascript\'>top.vaadin.forceSync();'
            + '</script></body></html>')


    def handleURI(self, context, relativeUri):
        if relativeUri is not None and 'loginHandler' in relativeUri:
            if self._form._window is not None:
                self._form._window.removeURIHandler(self)
            downloadStream = DownloadStream(StringIO(self._responce),
                    'text/html', 'loginSuccesfull')
            downloadStream.setCacheTime(-1)
            return downloadStream
        else:
            return None
