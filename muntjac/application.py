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

"""Defines a base class required for all Muntjac applications."""

import sys
import traceback
import logging

from warnings import warn

from muntjac.util import EventObject, IEventListener, defaultLocale
from muntjac.terminal.uri_handler import IUriHandler
from muntjac.terminal.sys_error import SysError
from muntjac.terminal.terminal import IErrorListener, ITerminal
from muntjac.terminal.parameter_handler import IErrorEvent
from muntjac.terminal.error_message import IErrorMessage
from muntjac.terminal.variable_owner import IErrorEvent as VariableOwnerErrorEvent
from muntjac.terminal.uri_handler import IErrorEvent as URIHandlerErrorEvent
from muntjac.terminal.parameter_handler import IErrorEvent as ParameterHandlerErrorEvent
from muntjac.terminal.gwt.server.change_variables_error_event import ChangeVariablesErrorEvent
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.window import Window
from muntjac.messages import SystemMessages


logger = logging.getLogger(__name__)


class Application(IUriHandler, ITerminal, IErrorListener):
    """Base class required for all Muntjac applications. This class provides
    all the basic services required by Muntjac. These services allow external
    discovery and manipulation of the user, L{com.vaadin.ui.Window windows} and
    themes, and starting and stopping the application.

    As mentioned, all Muntjac applications must inherit this class. However,
    this is almost all of what one needs to do to create a fully functional
    application. The only thing a class inheriting the C{Application}
    needs to do is implement the C{init} method where it creates the
    windows it needs to perform its function. Note that all applications must
    have at least one window: the main window. The first unnamed window
    constructed by an application automatically becomes the main window which
    behaves just like other windows with one exception: when accessing windows
    using URLs the main window corresponds to the application URL whereas other
    windows correspond to a URL gotten by catenating the window's name to the
    application URL.

    See the class C{muntjac.demo.HelloWorld} for a simple example of
    a fully working application.

    B{Window access.} C{Application} provides methods to
    list, add and remove the windows it contains.

    B{Execution control.} This class includes method to start and finish the
    execution of the application. Being finished means basically that no
    windows will be available from the application anymore.

    B{Theme selection.} The theme selection process allows a theme to be
    specified at three different levels. When a window's theme needs to be
    found out, the window itself is queried for a preferred theme. If the
    window does not prefer a specific theme, the application containing the
    window is queried. If neither the application prefers a theme, the default
    theme for the L{terminal<muntjac.terminal.terminal.ITerminal>} is used. The
    terminal always defines a default theme.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    #: The default SystemMessages (read-only). Change by overriding
    #  getSystemMessages() and returning CustomizedSystemMessages
    _DEFAULT_SYSTEM_MESSAGES = SystemMessages()


    def __init__(self):

        #: Id use for the next window that is opened. Access to this must be
        #  synchronized.
        self._nextWindowId = 1

        #: Application context the application is running in.
        self._context = None

        #: The current user or C{None} if no user has logged in.
        self._user = None

        #: Mapping from window name to window instance.
        self._windows = dict()

        #: Main window of the application.
        self._mainWindow = None

        #: The application's URL.
        self._applicationUrl = None

        #: Name of the theme currently used by the application.
        self.theme = None

        #: Application status.
        self._applicationIsRunning = False

        #: Application properties.
        self._properties = dict

        #: Default locale of the application.
        self._locale = None

        #: List of listeners listening user changes.
        self._userChangeListeners = list()

        self._userChangeCallbacks = dict()

        #: Window attach listeners.
        self._windowAttachListeners = list()

        self._windowAttachCallbacks = dict()

        #: Window detach listeners.
        self._windowDetachListeners = list()

        self._windowDetachCallbacks = dict()

        #: Application resource mapping: key <-> resource.
        self._resourceKeyMap = dict()
        self._keyResourceMap = dict()
        self._lastResourceKeyNumber = 0

        #: URL where the user is redirected to on application close, or null if
        #  application is just closed without redirection.
        self._logoutURL = None

        #: Application wide error handler which is used by default if an error
        #  is left unhandled.
        self._errorHandler = self


    def getWindow(self, name):
        """Gets a window by name. Returns C{None} if the application is
        not running or it does not contain a window corresponding to the name.

        All windows can be referenced by their names in url
        C{http://host:port/foo/bar/} where
        C{http://host:port/foo/} is the application url as returned by
        getURL() and C{bar} is the name of the window.

        One should note that this method can, as a side effect create new
        windows if needed by the application. This can be achieved by
        overriding the default implementation.

        If for some reason user opens another window with same url that is
        already open, name is modified by adding "_12345678" postfix to the
        name, where 12345678 is a random number. One can decide to create
        another window-object for those windows (recommended) or to discard
        the postfix. If the user has two browser windows pointing to the same
        window-object on server, synchronization errors are likely to occur.

        If no browser-level windowing is used, all defaults are fine and this
        method can be left as is. In case browser-level windows are needed, it
        is recommended to create new window-objects on this method from their
        names if the super.getWindow() does not find existing windows. See
        below for implementation example::

                # If we already have the requested window, use it
                w = super(Application, self).getWindow(name)
                if w == None:
                    # If no window found, create it
                    w = Window(name)
                    # set windows name to the one requested
                    w.setName(name)
                    # add it to this application
                    addWindow(w)
                    # ensure use of window specific url
                    w.open( ExternalResource(w.getURL()) )
                    # add some content
                    w.addComponent( Label("Test window") )

                return w

        B{Note} that all returned Window objects must be added to
        this application instance.

        The method should return null if the window does not exists (and is not
        created as a side-effect) or if the application is not running anymore.

        @param name:
                   the name of the window.
        @return: the window associated with the given URI or C{None}
        """
        # For closed app, do not give any windows
        if not self.isRunning():
            return None

        # Gets the window by name
        return self._windows.get(name)


    def addWindow(self, window):
        """Adds a new window to the application.

        This implicitly invokes the L{Window.setApplication} method.

        Note that all application-level windows can be accessed by their names
        in url C{http://host:port/foo/bar/} where C{http://host:port/foo/} is
        the application url as returned by getURL() and C{bar} is the name of
        the window. Also note that not all windows should be added to
        application - one can also add windows inside other windows - these
        windows show as smaller windows inside those windows.

        @param window:
                   the new C{Window} to add. If the name of the window
                   is C{None}, an unique name is automatically given
                   for the window.
        @raise ValueError:
                    if a window with the same name as the new window already
                    exists in the application.
        @raise ValueError:
                    if the given C{Window} is C{None}.
        """
        # Nulls can not be added to application
        if window is None:
            return

        # Check that one is not adding a sub-window to application
        if window.getParent() is not None:
            raise ValueError('Window was already added inside another window'
                    + ' - it can not be added to application also.')

        # Gets the naming proposal from window
        name = window.getName()

        # Checks that the application does not already contain
        # window having the same name
        if name is not None and name in self._windows:

            # If the window is already added
            if window == self._windows[name]:
                return

            # Otherwise complain
            raise ValueError('Window with name \'' + window.getName()
                    + '\' is already present in the application')

        # If the name of the window is null, the window is automatically named
        if name is None:
            accepted = False
            while not accepted:

                # Try another name
                name = str(self._nextWindowId)
                self._nextWindowId += 1

                if not (name in self._windows):
                    accepted = True

            window.setName(name)

        # Adds the window to application
        self._windows[name] = window
        window.setApplication(self)

        self._fireWindowAttachEvent(window)

        # If no main window is set, declare the window to be main window
        if self.getMainWindow() is None:
            self._mainWindow = window


    def _fireWindowAttachEvent(self, window):
        """Send information to all listeners about new Windows associated with
        this application.
        """
        # Fires the window attach event
        event = WindowAttachEvent(window)
        for l in self._windowAttachListeners:
            l.windowAttached(event)

        for callback, args in self._windowAttachCallbacks:
            callback(event, *args)


    def removeWindow(self, window):
        """Removes the specified window from the application.

        Removing the main window of the Application also sets the main window
        to null. One must another window to be the main window after this with
        L{setMainWindow}.

        Note that removing window from the application does not close the
        browser window - the window is only removed from the server-side.

        @param window:
                   the window to be removed.
        """
        if window is not None and window in self._windows.values():

            # Removes the window from application
            del self._windows[window.getName()]

            # If the window was main window, clear it
            if self.getMainWindow() == window:
                self.setMainWindow(None)

            # Removes the application from window
            if window.getApplication() == self:
                window.setApplication(None)

            self._fireWindowDetachEvent(window)


    def _fireWindowDetachEvent(self, window):
        # Fires the window detach event
        event = WindowDetachEvent(window)
        for l in self._windowDetachListeners:
            l.windowDetached(event)

        for callback, args in self._windowDetachCallbacks:
            callback(event, *args)


    def getUser(self):
        """Gets the user of the application.

        Muntjac doesn't define of use user object in any way - it only provides
        this getter and setter methods for convenience. The user is any object
        that has been stored to the application with L{setUser}.

        @return: the user of the application.
        """
        return self._user


    def setUser(self, user):
        """Sets the user of the application instance. An application instance
        may have a user associated to it. This can be set in login procedure or
        application initialization.

        A component performing the user login procedure can assign the user
        property of the application and make the user object available to other
        components of the application.

        Muntjac doesn't define of use user object in any way - it only provides
        getter and setter methods for convenience. The user reference stored to
        the application can be read with L{getUser}.

        @param user:
                   the new user.
        """
        prevUser = self._user
        if (user == prevUser) or (user is not None and user == prevUser):
            return

        self._user = user

        event = UserChangeEvent(self, user, prevUser)
        for l in self._userChangeListeners:
            l.applicationUserChanged(event)

        for callback, args in self._userChangeCallbacks:
            callback(event, *args)


    def getURL(self):
        """Gets the URL of the application.

        This is the URL what can be entered to a browser window to start the
        application. Navigating to the application URL shows the main window (
        L{getMainWindow}) of the application. Note that the main window
        can also be shown by navigating to the window url (L{Window.getURL}).

        @return: the application's URL.
        """
        return self._applicationUrl


    def close(self):
        """Ends the Application.

        In effect this will cause the application stop returning any windows
        when asked. When the application is closed, its state is removed from
        the session and the browser window is redirected to the application
        logout url set with L{setLogoutURL}. If the logout url has not
        been set, the browser window is reloaded and the application is
        restarted.
        """
        self._applicationIsRunning = False


    def start(self, applicationUrl, applicationProperties, context):
        """Starts the application on the given URL.

        This method is called by Muntjac framework when a user navigates to the
        application. After this call the application corresponds to the given
        URL and it will return windows when asked for them. There is no need to
        call this method directly.

        Application properties are defined by servlet configuration.

        @param applicationUrl:
                   the URL the application should respond to.
        @param applicationProperties:
                   the Application properties as specified by the servlet
                   configuration.
        @param context:
                   the context application will be running in.
        """
        self._applicationUrl = applicationUrl
        self._properties = applicationProperties
        self._context = context
        self.init()
        self._applicationIsRunning = True


    def isRunning(self):
        """Tests if the application is running or if it has been finished.

        Application starts running when its L{start} method has been
        called and stops when the L{close} is called.

        @return: C{True} if the application is running, C{False} if not.
        """
        return self._applicationIsRunning


    def getWindows(self):
        """Gets the set of windows contained by the application.

        Note that the returned set of windows can not be modified.

        @return: the collection of windows.
        """
        return self._windows.values()


    def init(self):
        """Main initializer of the application. The C{init} method is
        called by the framework when the application is started, and it should
        perform whatever initialization operations the application needs, such
        as creating windows and adding components to them.
        """
        raise NotImplementedError


    def getTheme(self):
        """Gets the application's theme. The application's theme is the default
        theme used by all the windows in it that do not explicitly specify a
        theme. If the application theme is not explicitly set, the C{None} is
        returned.

        @return: the name of the application's theme.
        """
        return self.theme


    def setTheme(self, theme):
        """Sets the application's theme.

        Note that this theme can be overridden in the the application level
        windows with L{Window.setTheme}. Setting theme
        to be C{None} selects the default theme. For the available
        theme names, see the contents of the VAADIN/themes directory.

        @param theme:
                   the new theme for this application.
        """
        # Collect list of windows not having the current or future theme
        toBeUpdated = list()
        oldAppTheme = self.getTheme()

        for w in self.getWindows():
            windowTheme = w.getTheme()
            if ((windowTheme is None) or (not (windowTheme == theme) and windowTheme == oldAppTheme)):
                toBeUpdated.append(w)

        # Updates the theme
        self.theme = theme

        # Ask windows to update themselves
        for w in toBeUpdated:
            w.requestRepaint()


    def getMainWindow(self):
        """Gets the mainWindow of the application.

        The main window is the window attached to the application URL
        (L{getURL}) and thus which is show by default to the user.

        Note that each application must have at least one main window.

        @return: the main window.
        """
        return self._mainWindow


    def setMainWindow(self, mainWindow):
        """Sets the mainWindow. If the main window is not explicitly set, the
        main window defaults to first created window. Setting window as a main
        window of this application also adds the window to this application.

        @param mainWindow:
                   the mainWindow to set.
        """
        self.addWindow(mainWindow)
        self._mainWindow = mainWindow


    def getPropertyNames(self):
        """Returns an enumeration of all the names in this application.

        See L{start} how properties are defined.

        @return: an enumeration of all the keys in this property list,
                 including the keys in the default property list.
        """
        return self._properties.keys()


    def getProperty(self, name):
        """Searches for the property with the specified name in this
        application. This method returns C{None} if the property is not found.

        See L{start} how properties are defined.

        @param name:
                   the name of the property.
        @return: the value in this property list with the specified key value.
        """
        return self._properties[name]


    def addResource(self, resource):
        """Adds new resource to the application. The resource can be accessed
        by the user of the application.

        @param resource:
                   the resource to add.
        """
        # Check if the resource is already mapped
        if resource in self._resourceKeyMap:
            return

        # Generate key
        self._lastResourceKeyNumber += 1
        key = str(self._lastResourceKeyNumber)

        # Add the resource to mappings
        self._resourceKeyMap[resource] = key
        self._keyResourceMap[key] = resource


    def removeResource(self, resource):
        """Removes the resource from the application.

        @param resource:
                   the resource to remove.
        """
        key = self._resourceKeyMap.get(resource)
        if key is not None:
            del self._resourceKeyMap[resource]
            if key in self._keyResourceMap:
                del self._keyResourceMap[key]


    def getRelativeLocation(self, resource):
        """Gets the relative uri of the resource. This method is intended to be
        called only be the terminal implementation.

        This method can only be called from within the processing of a UIDL
        request, not from a background thread.

        @param resource:
                   the resource to get relative location.
        @return: the relative uri of the resource or null if called in a
                 background thread

        @deprecated: this method is intended to be used by the terminal only.
                     It may be removed or moved in the future.
        """
        warn(("this method is intended to be used by the "
            "terminal only. It may be removed or moved in the future."),
            DeprecationWarning)

        # Gets the key
        key = self._resourceKeyMap.get(resource)

        # If the resource is not registered, return null
        if key is None:
            return None

        return self._context.generateApplicationResourceURL(resource, key)


    def handleURI(self, context, relativeUri):
        """Application URI handling hub.

        This method gets called by terminal. It has lots of duties like to pass
        uri handler to proper uri handlers registered to windows etc.

        In most situations developers should NOT OVERRIDE this method. Instead
        developers should implement and register uri handlers to windows.

        @deprecated: this method is called be the terminal implementation only
                     and might be removed or moved in the future. Instead of
                     overriding this method, add your L{IUriHandler} to a top
                     level L{Window} (eg.
                     getMainWindow().addUriHanler(handler) instead.
        """
        warn(("this method is called be the terminal "
            "implementation only and might be removed or moved in the future. "
            "Instead of overriding this method, add your L{IUriHandler} to "
            "a top level L{Window} (eg. getMainWindow().addUriHanler(handler) "
            "instead."), DeprecationWarning)

        if self._context.isApplicationResourceURL(context, relativeUri):

            # Handles the resource request
            key = self._context.getURLKey(context, relativeUri)
            resource = self._keyResourceMap.get(key)
            if resource is not None:
                stream = resource.getStream()
                if stream is not None:
                    stream.setCacheTime(resource.getCacheTime())
                    return stream
                else:
                    return None
            else:
                # Resource requests override uri handling
                return None
        else:
            return None


    def getLocale(self):
        """Gets the default locale for this application.

        By default this is the preferred locale of the user using the
        application. In most cases it is read from the browser defaults.

        @return: the locale of this application.
        """
        if self._locale is not None:
            return self._locale

        return defaultLocale()


    def setLocale(self, locale):
        """Sets the default locale for this application.

        By default this is the preferred locale of the user using the
        application. In most cases it is read from the browser defaults.

        @param locale:
                   the Locale object.
        """
        self._locale = locale


    def addListener(self, listener, iface=None):
        """Adds the user change/window attach/window detach listener.

        The user change listener allows one to get notification each time
        L{setUser} is called.  The window attach listener is used to get
        notifications each time a window is attached to the application
        with L{addWindow}.  The window detach listener is used to get
        notifications each time a window is remove from the application
        with L{removeWindow}.
        """
        if (isinstance(listener, IUserChangeListener) and
                (iface is None or issubclass(iface, IUserChangeListener))):
            self._userChangeListeners.append(listener)

        if (isinstance(listener, IWindowAttachListener) and
                (iface is None or issubclass(iface, IWindowAttachListener))):
            self._windowAttachListeners.append(listener)

        if (isinstance(listener, IWindowDetachListener) and
                (iface is None or issubclass(iface, IWindowDetachListener))):
            self._windowDetachListeners.append(listener)

        super(Application, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, UserChangeEvent):
            self._userChangeCallbacks[callback] = args

        elif issubclass(eventType, WindowAttachEvent):
            self._windowAttachCallbacks[callback] = args

        elif issubclass(eventType, WindowDetachEvent):
            self._windowDetachCallbacks[callback] = args

        else:
            super(Application, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        """Removes the user change/window attach/window detach listener.

        @param listener:
                   the listener to remove
        """
        if (isinstance(listener, IUserChangeListener) and
                (iface is None or iface == IUserChangeListener)):
            if listener in self._userChangeListeners:
                self._userChangeListeners.remove(listener)

        if (isinstance(listener, IWindowAttachListener) and
                (iface is None or issubclass(iface, IWindowAttachListener))):
            if listener in self._windowAttachListeners:
                self._windowAttachListeners.remove(listener)

        if (isinstance(listener, IWindowDetachListener) and
                (iface is None or issubclass(iface, IWindowDetachListener))):
            if listener in self._windowDetachListeners:
                self._windowDetachListeners.remove(listener)

        super(Application, self).addListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, UserChangeEvent):
            if callback in self._userChangeCallbacks:
                del self._userChangeCallbacks[callback]

        elif issubclass(eventType, WindowAttachEvent):
            if callback in self._windowAttachCallbacks:
                del self._windowAttachCallbacks[callback]

        elif issubclass(eventType, WindowDetachEvent):
            if callback in self._windowDetachCallbacks:
                del self._windowDetachCallbacks[callback]

        else:
            super(Application, self).removeCallback(callback, eventType)


    def getLogoutURL(self):
        """Returns the URL user is redirected to on application close. If the
        URL is C{None}, the application is closed normally as defined by the
        application running environment.

        Desktop application just closes the application window and
        web-application redirects the browser to application main URL.

        @return: the URL.
        """
        return self._logoutURL


    def setLogoutURL(self, logoutURL):
        """Sets the URL user is redirected to on application close. If the URL
        is C{None}, the application is closed normally as defined by the
        application running environment: Desktop application just closes the
        application window and web-application redirects the browser to
        application main URL.

        @param logoutURL:
                   the logoutURL to set.
        """
        self._logoutURL = logoutURL


    @classmethod
    def getSystemMessages(cls):
        """Gets the SystemMessages for this application. SystemMessages are
        used to notify the user of various critical situations that can occur,
        such as session expiration, client/server out of sync, and internal
        server error.

        You can customize the messages by "overriding" this method and
        returning L{CustomizedSystemMessages}. To "override" this method,
        re-implement this method in your application (the class that extends
        L{Application}). Even though overriding class methods is not
        possible in Python, Muntjac selects to call the static method from the
        subclass instead of the original L{getSystemMessages} if such a
        method exists.

        @return: the SystemMessages for this application
        """
        return cls._DEFAULT_SYSTEM_MESSAGES


    def terminalError(self, event):
        """Invoked by the terminal on any exception that occurs in application
        and is thrown by the C{setVariable} to the terminal. The default
        implementation sets the exceptions as C{ComponentErrors} to the
        component that initiated the exception and prints stack trace to standard
        error stream.

        You can safely override this method in your application in order to
        direct the errors to some other destination (for example log).

        @param event:
                   the change event.
        @see: L{IErrorListener.terminalError}
        """
        t = event.getThrowable()
        if isinstance(t, IOError):  #SocketException
            # Most likely client browser closed socket
            logger.exception('SocketException in CommunicationManager.' \
                              ' Most likely client (browser) closed socket.')
            return

        # Finds the original source of the error/exception
        owner = None
        if isinstance(event, VariableOwnerErrorEvent):
            owner = event.getVariableOwner()
        elif isinstance(event, URIHandlerErrorEvent):
            owner = event.getURIHandler()
        elif isinstance(event, ParameterHandlerErrorEvent):
            owner = event.getParameterHandler()
        elif isinstance(event, ChangeVariablesErrorEvent):
            owner = event.getComponent()

        # Shows the error in AbstractComponent
        if isinstance(owner, AbstractComponent):
            if isinstance(t, IErrorMessage):
                owner.setComponentError(t)
            else:
                owner.setComponentError( SysError(t) )

        # also print the error on console
        logger.exception('ITerminal error: ' + str(t))

        exc_type, _, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, t,
                exc_traceback, file=sys.stdout)


    def getContext(self):
        """Gets the application context.

        The application context is the environment where the application is
        running in. The actual implementation class of may contains quite a lot
        more functionality than defined in the L{ApplicationContext}
        interface.

        By default, when you are deploying your application to a servlet
        container, the implementation class is L{WebApplicationContext} -
        you can safely cast to this class and use the methods from there.

        @return: the application context.
        """
        return self._context


    def getVersion(self):
        """Override this method to return correct version number of your
        Application. Version information is delivered for example to Testing
        Tools test results. By default this returns a string "NONVERSIONED".

        @return: version string
        """
        return 'NONVERSIONED'


    def getErrorHandler(self):
        """Gets the application error handler.

        The default error handler is the application itself.

        @return: Application error handler
        """
        return self._errorHandler


    def setErrorHandler(self, errorHandler):
        """Sets the application error handler.

        The default error handler is the application itself. By overriding
        this, you can redirect the error messages to your selected target
        (log for example).
        """
        self._errorHandler = errorHandler


class UserChangeEvent(EventObject):
    """An event that characterizes a change in the current selection.

    Application user change event sent when the setUser is called to change
    the current user of the application.

    @version: 1.1.0
    """

    def __init__(self, source, newUser, prevUser):
        """Constructor for user change event.

        @param source:
                   the application source.
        @param newUser:
                   the new user.
        @param prevUser:
                   the previous user.
        """
        super(UserChangeEvent, self).__init__(source)

        #: New user of the application.
        self._newUser = newUser

        #: Previous user of the application.
        self._prevUser = prevUser


    def getNewUser(self):
        """Gets the new user of the application.

        @return: the new user.
        """
        return self._newUser


    def getPreviousUser(self):
        """Gets the previous user of the application.

        @return: the previous Muntjac user, if user has not changed ever on
                 application it returns C{None}
        """
        return self._prevUser


    def getApplication(self):
        """Gets the application where the user change occurred.

        @return: the Application.
        """
        return self.getSource()


class IUserChangeListener(IEventListener):
    """The C{UserChangeListener} interface for listening application
    user changes.

    @version: 1.1.0
    """

    def applicationUserChanged(self, event):
        """The C{applicationUserChanged} method Invoked when the
        application user has changed.

        @param event:
                   the change event.
        """
        raise NotImplementedError


class WindowDetachEvent(EventObject):
    """Window detach event.

    This event is sent each time a window is removed from the application
    with L{Application.removeWindow}.
    """

    def __init__(self, window):
        """Creates a event.

        @param window:
                   the detached window.
        """
        super(WindowDetachEvent, self).__init__(self)
        self._window = window


    def getWindow(self):
        """Gets the detached window.

        @return: the detached window.
        """
        return self._window


    def getApplication(self):
        """Gets the application from which the window was detached.

        @return: the application.
        """
        return self.getSource()


class WindowAttachEvent(EventObject):
    """Window attach event.

    This event is sent each time a window is attached to the application with
    L{Application.addWindow}.
    """

    def __init__(self, window):
        """Creates a event.

        @param window:
                   the attached window.
        """
        super(WindowAttachEvent, self).__init__(self)
        self._window = window


    def getWindow(self):
        """Gets the attached window.

        @return: the attached window.
        """
        return self._window


    def getApplication(self):
        """Gets the application to which the window was attached.

        @return: the application.
        """
        return self.getSource()


class IWindowAttachListener(object):
    """Window attach listener interface."""


    def windowAttached(self, event):
        """Window attached

        @param event:
                   the window attach event.
        """
        raise NotImplementedError


class IWindowDetachListener(object):
    """Window detach listener interface."""


    def windowDetached(self, event):
        """Window detached.

        @param event:
                   the window detach event.
        """
        raise NotImplementedError


class ApplicationError(IErrorEvent):
    """Application error is an error message defined on the application level.

    When an error occurs on the application level, this error message type
    should be used. This indicates that the problem is caused by the
    application - not by the user.
    """

    def __init__(self, throwable):
        self._throwable = throwable


    def getThrowable(self):
        return self._throwable


class SingletonApplication(Application):

    _singleton = None

    def __init__(self):
        super(SingletonApplication, self).__init__()
        self.setMainWindow(Window())

    @classmethod
    def get(cls):
        if cls._singleton is None:
            cls._singleton = SingletonApplication()
        return cls._singleton

    def init(self):
        pass
