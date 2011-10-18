# Copyright (C) 2010 IT Mill Ltd.
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

import logging
import locale

from warnings import warn

from muntjac.util import EventObject, IEventListener
from muntjac.terminal.uri_handler import IUriHandler
from muntjac.terminal.system_error import SystemErr
from muntjac.terminal.terminal import IErrorListener, ITerminal
from muntjac.terminal.parameter_handler import IErrorEvent
from muntjac.terminal.error_message import IErrorMessage
from muntjac.terminal.variable_owner import IErrorEvent as VariableOwnerErrorEvent
from muntjac.terminal.uri_handler import IErrorEvent as URIHandlerErrorEvent
from muntjac.terminal.parameter_handler import IErrorEvent as ParameterHandlerErrorEvent
from muntjac.terminal.gwt.server.change_variables_error_event import ChangeVariablesErrorEvent
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.util import Locale


logger = logging.getLogger(__name__)


class SystemMessages(object):
    """Contains the system messages used to notify the user about various
    critical situations that can occur.
    <p>
    Customize by overriding the static
    {@link Application#getSystemMessages()} and returning
    {@link CustomizedSystemMessages}.
    </p>
    <p>
    The defaults defined in this class are:
    <ul>
    <li><b>sessionExpiredURL</b> = null</li>
    <li><b>sessionExpiredNotificationEnabled</b> = true</li>
    <li><b>sessionExpiredCaption</b> = ""</li>
    <li><b>sessionExpiredMessage</b> =
    "Take note of any unsaved data, and <u>click here</u> to continue."</li>
    <li><b>communicationErrorURL</b> = null</li>
    <li><b>communicationErrorNotificationEnabled</b> = true</li>
    <li><b>communicationErrorCaption</b> = "Communication problem"</li>
    <li><b>communicationErrorMessage</b> =
    "Take note of any unsaved data, and <u>click here</u> to continue."</li>
    <li><b>internalErrorURL</b> = null</li>
    <li><b>internalErrorNotificationEnabled</b> = true</li>
    <li><b>internalErrorCaption</b> = "Internal error"</li>
    <li><b>internalErrorMessage</b> = "Please notify the administrator.<br/>
    Take note of any unsaved data, and <u>click here</u> to continue."</li>
    <li><b>outOfSyncURL</b> = null</li>
    <li><b>outOfSyncNotificationEnabled</b> = true</li>
    <li><b>outOfSyncCaption</b> = "Out of sync"</li>
    <li><b>outOfSyncMessage</b> = "Something has caused us to be out of sync
    with the server.<br/>
    Take note of any unsaved data, and <u>click here</u> to re-sync."</li>
    <li><b>cookiesDisabledURL</b> = null</li>
    <li><b>cookiesDisabledNotificationEnabled</b> = true</li>
    <li><b>cookiesDisabledCaption</b> = "Cookies disabled"</li>
    <li><b>cookiesDisabledMessage</b> = "This application requires cookies to
    function.<br/>
    Please enable cookies in your browser and <u>click here</u> to try again.
    </li>
    </ul>
    </p>
    """

    def __init__(self):
        """Use {@link CustomizedSystemMessages} to customize"""

        self.sessionExpiredURL = None
        self.sessionExpiredNotificationEnabled = True
        self.sessionExpiredCaption = 'Session Expired'
        self.sessionExpiredMessage = 'Take note of any unsaved data, and <u>click here</u> to continue.'
        self.communicationErrorURL = None
        self.communicationErrorNotificationEnabled = True
        self.communicationErrorCaption = 'Communication problem'
        self.communicationErrorMessage = 'Take note of any unsaved data, and <u>click here</u> to continue.'
        self.authenticationErrorURL = None
        self.authenticationErrorNotificationEnabled = True
        self.authenticationErrorCaption = 'Authentication problem'
        self.authenticationErrorMessage = 'Take note of any unsaved data, and <u>click here</u> to continue.'
        self.internalErrorURL = None
        self.internalErrorNotificationEnabled = True
        self.internalErrorCaption = 'Internal error'
        self.internalErrorMessage = 'Please notify the administrator.<br/>Take note of any unsaved data, and <u>click here</u> to continue.'
        self.outOfSyncURL = None
        self.outOfSyncNotificationEnabled = True
        self.outOfSyncCaption = 'Out of sync'
        self.outOfSyncMessage = 'Something has caused us to be out of sync with the server.<br/>Take note of any unsaved data, and <u>click here</u> to re-sync.'
        self.cookiesDisabledURL = None
        self.cookiesDisabledNotificationEnabled = True
        self.cookiesDisabledCaption = 'Cookies disabled'
        self.cookiesDisabledMessage = 'This application requires cookies to function.<br/>Please enable cookies in your browser and <u>click here</u> to try again.'


    def getSessionExpiredURL(self):
        """@return null to indicate that the application will be restarted after
                session expired message has been shown.
        """
        return self.sessionExpiredURL


    def isSessionExpiredNotificationEnabled(self):
        """@return true to show session expiration message."""
        return self.sessionExpiredNotificationEnabled


    def getSessionExpiredCaption(self):
        """@return "" to show no caption."""
        return self.sessionExpiredCaption if self.sessionExpiredNotificationEnabled else None


    def getSessionExpiredMessage(self):
        """@return
                "Take note of any unsaved data, and <u>click here</u> to continue."
        """
        return self.sessionExpiredMessage if self.sessionExpiredNotificationEnabled else None


    def getCommunicationErrorURL(self):
        """@return null to reload the application after communication error
                message.
        """
        return self.communicationErrorURL


    def isCommunicationErrorNotificationEnabled(self):
        """@return true to show the communication error message."""
        return self.communicationErrorNotificationEnabled


    def getCommunicationErrorCaption(self):
        """@return "Communication problem\""""
        return self.communicationErrorCaption if self.communicationErrorNotificationEnabled else None


    def getCommunicationErrorMessage(self):
        """@return
                "Take note of any unsaved data, and <u>click here</u> to continue."
        """
        return self.communicationErrorMessage if self.communicationErrorNotificationEnabled else None


    def getAuthenticationErrorURL(self):
        """@return null to reload the application after authentication error
                message.
        """
        return self.authenticationErrorURL


    def isAuthenticationErrorNotificationEnabled(self):
        """@return true to show the authentication error message."""
        return self.authenticationErrorNotificationEnabled


    def getAuthenticationErrorCaption(self):
        """@return "Authentication problem\""""
        return self.authenticationErrorCaption if self.authenticationErrorNotificationEnabled else None


    def getAuthenticationErrorMessage(self):
        """@return
                "Take note of any unsaved data, and <u>click here</u> to continue."
        """
        return self.authenticationErrorMessage if self.authenticationErrorNotificationEnabled else None


    def getInternalErrorURL(self):
        """@return null to reload the current URL after internal error message
                has been shown.
        """
        return self.internalErrorURL


    def isInternalErrorNotificationEnabled(self):
        """@return true to enable showing of internal error message."""
        return self.internalErrorNotificationEnabled


    def getInternalErrorCaption(self):
        """@return "Internal error\""""
        return self.internalErrorCaption if self.internalErrorNotificationEnabled else None


    def getInternalErrorMessage(self):
        """@return "Please notify the administrator.<br/>
                Take note of any unsaved data, and <u>click here</u> to
                continue."
        """
        return self.internalErrorMessage if self.internalErrorNotificationEnabled else None


    def getOutOfSyncURL(self):
        """@return null to reload the application after out of sync message."""
        return self.outOfSyncURL


    def isOutOfSyncNotificationEnabled(self):
        """@return true to enable showing out of sync message"""
        return self.outOfSyncNotificationEnabled


    def getOutOfSyncCaption(self):
        """@return "Out of sync\""""
        return self.outOfSyncCaption if self.outOfSyncNotificationEnabled else None


    def getOutOfSyncMessage(self):
        """@return "Something has caused us to be out of sync with the server.<br/>
                Take note of any unsaved data, and <u>click here</u> to
                re-sync."
        """
        return self.outOfSyncMessage if self.outOfSyncNotificationEnabled else None


    def getCookiesDisabledURL(self):
        """Returns the URL the user should be redirected to after dismissing the
        "you have to enable your cookies" message. Typically null.

        @return A URL the user should be redirected to after dismissing the
                message or null to reload the current URL.
        """
        return self.cookiesDisabledURL


    def isCookiesDisabledNotificationEnabled(self):
        """Determines if "cookies disabled" messages should be shown to the end
        user or not. If the notification is disabled the user will be
        immediately redirected to the URL returned by
        {@link #getCookiesDisabledURL()}.

        @return true to show "cookies disabled" messages to the end user,
                false to redirect to the given URL directly
        """
        return self.cookiesDisabledNotificationEnabled


    def getCookiesDisabledCaption(self):
        """Returns the caption of the message shown to the user when cookies are
        disabled in the browser.

        @return The caption of the "cookies disabled" message
        """
        return self.cookiesDisabledCaption if self.cookiesDisabledNotificationEnabled else None


    def getCookiesDisabledMessage(self):
        """Returns the message shown to the user when cookies are disabled in
        the browser.

        @return The "cookies disabled" message
        """
        return self.cookiesDisabledMessage if self.cookiesDisabledNotificationEnabled else None


class CustomizedSystemMessages(SystemMessages):
    """Contains the system messages used to notify the user about various
    critical situations that can occur.
    <p>
    Vaadin gets the SystemMessages from your application by calling a static
    getSystemMessages() method. By default the
    Application.getSystemMessages() is used. You can customize this by
    defining a static MyApplication.getSystemMessages() and returning
    CustomizedSystemMessages. Note that getSystemMessages() is static -
    changing the system messages will by default change the message for all
    users of the application.
    </p>
    <p>
    The default behavior is to show a notification, and restart the
    application the the user clicks the message. <br/>
    Instead of restarting the application, you can set a specific URL that
    the user is taken to.<br/>
    Setting both caption and message to null will restart the application (or
    go to the specified URL) without displaying a notification.
    set*NotificationEnabled(false) will achieve the same thing.
    </p>
    <p>
    The situations are:
    <li>Session expired: the user session has expired, usually due to
    inactivity.</li>
    <li>Communication error: the client failed to contact the server, or the
    server returned and invalid response.</li>
    <li>Internal error: unhandled critical server error (e.g out of memory,
    database crash)
    <li>Out of sync: the client is not in sync with the server. E.g the user
    opens two windows showing the same application, but the application does
    not support this and uses the same Window instance. When the user makes
    changes in one of the windows - the other window is no longer in sync,
    and (for instance) pressing a button that is no longer present in the UI
    will cause a out-of-sync -situation.
    </p>
    """

    def setSessionExpiredURL(self, sessionExpiredURL):
        """Sets the URL to go to when the session has expired.

        @param sessionExpiredURL
                   the URL to go to, or null to reload current
        """
        self.sessionExpiredURL = sessionExpiredURL


    def setSessionExpiredNotificationEnabled(self, sessionExpiredNotificationEnabled):
        """Enables or disables the notification. If disabled, the set URL (or
        current) is loaded directly when next transaction between server and
        client happens.

        @param sessionExpiredNotificationEnabled
                   true = enabled, false = disabled
        """
        self.sessionExpiredNotificationEnabled = sessionExpiredNotificationEnabled


    def setSessionExpiredCaption(self, sessionExpiredCaption):
        """Sets the caption of the notification. Set to null for no caption. If
        both caption and message are null, client automatically forwards to
        sessionExpiredUrl after timeout timer expires. Timer uses value read
        from HTTPSession.getMaxInactiveInterval()

        @param sessionExpiredCaption
                   the caption
        """
        self.sessionExpiredCaption = sessionExpiredCaption


    def setSessionExpiredMessage(self, sessionExpiredMessage):
        """Sets the message of the notification. Set to null for no message. If
        both caption and message are null, client automatically forwards to
        sessionExpiredUrl after timeout timer expires. Timer uses value read
        from HTTPSession.getMaxInactiveInterval()

        @param sessionExpiredMessage
                   the message
        """
        self.sessionExpiredMessage = sessionExpiredMessage


    def setAuthenticationErrorURL(self, authenticationErrorURL):
        """Sets the URL to go to when there is a authentication error.

        @param authenticationErrorURL
                   the URL to go to, or null to reload current
        """
        self.authenticationErrorURL = authenticationErrorURL


    def setAuthenticationErrorNotificationEnabled(self, authenticationErrorNotificationEnabled):
        """Enables or disables the notification. If disabled, the set URL (or
        current) is loaded directly.

        @param authenticationErrorNotificationEnabled
                   true = enabled, false = disabled
        """
        self.authenticationErrorNotificationEnabled = authenticationErrorNotificationEnabled


    def setAuthenticationErrorCaption(self, authenticationErrorCaption):
        """Sets the caption of the notification. Set to null for no caption. If
        both caption and message is null, the notification is disabled;

        @param authenticationErrorCaption
                   the caption
        """
        self.authenticationErrorCaption = authenticationErrorCaption


    def setAuthenticationErrorMessage(self, authenticationErrorMessage):
        """Sets the message of the notification. Set to null for no message. If
        both caption and message is null, the notification is disabled;

        @param authenticationErrorMessage
                   the message
        """
        self.authenticationErrorMessage = authenticationErrorMessage


    def setCommunicationErrorURL(self, communicationErrorURL):
        """Sets the URL to go to when there is a communication error.

        @param communicationErrorURL
                   the URL to go to, or null to reload current
        """
        self.communicationErrorURL = communicationErrorURL


    def setCommunicationErrorNotificationEnabled(self, communicationErrorNotificationEnabled):
        """Enables or disables the notification. If disabled, the set URL (or
        current) is loaded directly.

        @param communicationErrorNotificationEnabled
                   true = enabled, false = disabled
        """
        self.communicationErrorNotificationEnabled = communicationErrorNotificationEnabled


    def setCommunicationErrorCaption(self, communicationErrorCaption):
        """Sets the caption of the notification. Set to null for no caption. If
        both caption and message is null, the notification is disabled;

        @param communicationErrorCaption
                   the caption
        """
        self.communicationErrorCaption = communicationErrorCaption


    def setCommunicationErrorMessage(self, communicationErrorMessage):
        """Sets the message of the notification. Set to null for no message. If
        both caption and message is null, the notification is disabled;

        @param communicationErrorMessage
                   the message
        """
        self.communicationErrorMessage = communicationErrorMessage


    def setInternalErrorURL(self, internalErrorURL):
        """Sets the URL to go to when an internal error occurs.

        @param internalErrorURL
                   the URL to go to, or null to reload current
        """
        self.internalErrorURL = internalErrorURL


    def setInternalErrorNotificationEnabled(self, internalErrorNotificationEnabled):
        """Enables or disables the notification. If disabled, the set URL (or
        current) is loaded directly.

        @param internalErrorNotificationEnabled
                   true = enabled, false = disabled
        """
        self.internalErrorNotificationEnabled = internalErrorNotificationEnabled


    def setInternalErrorCaption(self, internalErrorCaption):
        """Sets the caption of the notification. Set to null for no caption. If
        both caption and message is null, the notification is disabled;

        @param internalErrorCaption
                   the caption
        """
        self.internalErrorCaption = internalErrorCaption


    def setInternalErrorMessage(self, internalErrorMessage):
        """Sets the message of the notification. Set to null for no message. If
        both caption and message is null, the notification is disabled;

        @param internalErrorMessage
                   the message
        """
        self.internalErrorMessage = internalErrorMessage


    def setOutOfSyncURL(self, outOfSyncURL):
        """Sets the URL to go to when the client is out-of-sync.

        @param outOfSyncURL
                   the URL to go to, or null to reload current
        """
        self.outOfSyncURL = outOfSyncURL


    def setOutOfSyncNotificationEnabled(self, outOfSyncNotificationEnabled):
        """Enables or disables the notification. If disabled, the set URL (or
        current) is loaded directly.

        @param outOfSyncNotificationEnabled
                   true = enabled, false = disabled
        """
        self.outOfSyncNotificationEnabled = outOfSyncNotificationEnabled


    def setOutOfSyncCaption(self, outOfSyncCaption):
        """Sets the caption of the notification. Set to null for no caption. If
        both caption and message is null, the notification is disabled;

        @param outOfSyncCaption
                   the caption
        """
        self.outOfSyncCaption = outOfSyncCaption


    def setOutOfSyncMessage(self, outOfSyncMessage):
        """Sets the message of the notification. Set to null for no message. If
        both caption and message is null, the notification is disabled;

        @param outOfSyncMessage
                   the message
        """
        self.outOfSyncMessage = outOfSyncMessage


    def setCookiesDisabledURL(self, cookiesDisabledURL):
        """Sets the URL to redirect to when the browser has cookies disabled.

        @param cookiesDisabledURL
                   the URL to redirect to, or null to reload the current URL
        """
        self.cookiesDisabledURL = cookiesDisabledURL


    def setCookiesDisabledNotificationEnabled(self, cookiesDisabledNotificationEnabled):
        """Enables or disables the notification for "cookies disabled" messages.
        If disabled, the URL returned by {@link #getCookiesDisabledURL()} is
        loaded directly.

        @param cookiesDisabledNotificationEnabled
                   true to enable "cookies disabled" messages, false
                   otherwise
        """
        self.cookiesDisabledNotificationEnabled = cookiesDisabledNotificationEnabled


    def setCookiesDisabledCaption(self, cookiesDisabledCaption):
        """Sets the caption of the "cookies disabled" notification. Set to null
        for no caption. If both caption and message is null, the notification
        is disabled.

        @param cookiesDisabledCaption
                   the caption for the "cookies disabled" notification
        """
        self.cookiesDisabledCaption = cookiesDisabledCaption


    def setCookiesDisabledMessage(self, cookiesDisabledMessage):
        """Sets the message of the "cookies disabled" notification. Set to null
        for no message. If both caption and message is null, the notification
        is disabled.

        @param cookiesDisabledMessage
                   the message for the "cookies disabled" notification
        """
        self.cookiesDisabledMessage = cookiesDisabledMessage


class Application(IUriHandler, ITerminal, IErrorListener):
    """<p>
    Base class required for all Vaadin applications. This class provides all the
    basic services required by Vaadin. These services allow external discovery
    and manipulation of the user, {@link com.vaadin.ui.Window windows} and
    themes, and starting and stopping the application.
    </p>

    <p>
    As mentioned, all Vaadin applications must inherit this class. However, this
    is almost all of what one needs to do to create a fully functional
    application. The only thing a class inheriting the <code>Application</code>
    needs to do is implement the <code>init</code> method where it creates the
    windows it needs to perform its function. Note that all applications must
    have at least one window: the main window. The first unnamed window
    constructed by an application automatically becomes the main window which
    behaves just like other windows with one exception: when accessing windows
    using URLs the main window corresponds to the application URL whereas other
    windows correspond to a URL gotten by catenating the window's name to the
    application URL.
    </p>

    <p>
    See the class <code>com.vaadin.demo.HelloWorld</code> for a simple example of
    a fully working application.
    </p>

    <p>
    <strong>Window access.</strong> <code>Application</code> provides methods to
    list, add and remove the windows it contains.
    </p>

    <p>
    <strong>Execution control.</strong> This class includes method to start and
    finish the execution of the application. Being finished means basically that
    no windows will be available from the application anymore.
    </p>

    <p>
    <strong>Theme selection.</strong> The theme selection process allows a theme
    to be specified at three different levels. When a window's theme needs to be
    found out, the window itself is queried for a preferred theme. If the window
    does not prefer a specific theme, the application containing the window is
    queried. If neither the application prefers a theme, the default theme for
    the {@link com.vaadin.terminal.ITerminal terminal} is used. The terminal
    always defines a default theme.
    </p>

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    # The default SystemMessages (read-only). Change by overriding
    # getSystemMessages() and returning CustomizedSystemMessages
    _DEFAULT_SYSTEM_MESSAGES = SystemMessages()


    def __init__(self):

        # Id use for the next window that is opened. Access to this must be
        # synchronized.
        self._nextWindowId = 1

        # Application context the application is running in.
        self._context = None

        # The current user or <code>null</code> if no user has logged in.
        self._user = None

        # Mapping from window name to window instance.
        self._windows = dict()

        # Main window of the application.
        self._mainWindow = None

        # The application's URL.
        self._applicationUrl = None

        # Name of the theme currently used by the application.
        self._theme = None

        # Application status.
        self._applicationIsRunning = False

        # Application properties.
        self._properties = dict

        # Default locale of the application.
        self._locale = None

        # List of listeners listening user changes.
        self._userChangeListeners = None

        # Window attach listeners.
        self._windowAttachListeners = None

        # Window detach listeners.
        self._windowDetachListeners = None

        # Application resource mapping: key <-> resource.
        self._resourceKeyMap = dict()
        self._keyResourceMap = dict()
        self._lastResourceKeyNumber = 0

        # URL where the user is redirected to on application close, or null if
        # application is just closed without redirection.
        self._logoutURL = None

        # Application wide error handler which is used by default if an error is
        # left unhandled.
        self._errorHandler = self


    def getWindow(self, name):
        """<p>
        Gets a window by name. Returns <code>null</code> if the application is
        not running or it does not contain a window corresponding to the name.
        </p>

        <p>
        All windows can be referenced by their names in url
        <code>http://host:port/foo/bar/</code> where
        <code>http://host:port/foo/</code> is the application url as returned by
        getURL() and <code>bar</code> is the name of the window.
        </p>

        <p>
        One should note that this method can, as a side effect create new windows
        if needed by the application. This can be achieved by overriding the
        default implementation.
        </p>

        <p>
        If for some reason user opens another window with same url that is
        already open, name is modified by adding "_12345678" postfix to the name,
        where 12345678 is a random number. One can decide to create another
        window-object for those windows (recommended) or to discard the postfix.
        If the user has two browser windows pointing to the same window-object on
        server, synchronization errors are likely to occur.
        </p>

        <p>
        If no browser-level windowing is used, all defaults are fine and this
        method can be left as is. In case browser-level windows are needed, it is
        recommended to create new window-objects on this method from their names
        if the super.getWindow() does not find existing windows. See below for
        implementation example: <code><pre>
                // If we already have the requested window, use it
                Window w = super.getWindow(name);
                if (w == null) {
                    // If no window found, create it
                    w = new Window(name);
                    // set windows name to the one requested
                    w.setName(name);
                    // add it to this application
                    addWindow(w);
                    // ensure use of window specific url
                    w.open(new ExternalResource(w.getURL().toString()));
                    // add some content
                    w.addComponent(new Label("Test window"));
                }
                return w;</pre></code>
        </p>

        <p>
        <strong>Note</strong> that all returned Window objects must be added to
        this application instance.

        <p>
        The method should return null if the window does not exists (and is not
        created as a side-effect) or if the application is not running anymore.
        </p>

        @param name
                   the name of the window.
        @return the window associated with the given URI or <code>null</code>
        """
        # For closed app, do not give any windows
        if not self.isRunning():
            return None

        # Gets the window by name
        return self._windows[name]


    def addWindow(self, window):
        """Adds a new window to the application.

        <p>
        This implicitly invokes the
        {@link com.vaadin.ui.Window#setApplication(Application)} method.
        </p>

        <p>
        Note that all application-level windows can be accessed by their names in
        url <code>http://host:port/foo/bar/</code> where
        <code>http://host:port/foo/</code> is the application url as returned by
        getURL() and <code>bar</code> is the name of the window. Also note that
        not all windows should be added to application - one can also add windows
        inside other windows - these windows show as smaller windows inside those
        windows.
        </p>

        @param window
                   the new <code>Window</code> to add. If the name of the window
                   is <code>null</code>, an unique name is automatically given
                   for the window.
        @raise ValueError
                    if a window with the same name as the new window already
                    exists in the application.
        @raise ValueError
                    if the given <code>Window</code> is <code>null</code>.
        """
        # Nulls can not be added to application
        if window is None:
            return

        # Check that one is not adding a sub-window to application
        if window.getParent() is not None:
            raise ValueError('Window was already added inside another window' + ' - it can not be added to application also.')

        # Gets the naming proposal from window
        name = window.getName()

        # Checks that the application does not already contain
        # window having the same name
        if name is not None and name in self._windows:

            # If the window is already added
            if window == self._windows[name]:
                return

            # Otherwise complain
            raise ValueError('Window with name \'' + window.getName() + '\' is already present in the application')

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
        """Send information to all listeners about new Windows associated with this
        application.

        @param window
        """
        # Fires the window attach event
        if self._windowAttachListeners is not None:
            listeners = list(self._windowAttachListeners)
            event = WindowAttachEvent(window)
            for l in listeners:
                l.windowAttached(event)


    def removeWindow(self, window):
        """Removes the specified window from the application.

        <p>
        Removing the main window of the Application also sets the main window to
        null. One must another window to be the main window after this with
        {@link #setMainWindow(Window)}.
        </p>

        <p>
        Note that removing window from the application does not close the browser
        window - the window is only removed from the server-side.
        </p>

        @param window
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
        if self._windowDetachListeners is not None:
            listeners = list(self._windowDetachListeners)
            event = WindowDetachEvent(window)
            for l in listeners:
                l.windowDetached(event)


    def getUser(self):
        """Gets the user of the application.

        <p>
        Vaadin doesn't define of use user object in any way - it only provides
        this getter and setter methods for convenience. The user is any object
        that has been stored to the application with {@link #setUser(Object)}.
        </p>

        @return the User of the application.
        """
        return self._user


    def setUser(self, user):
        """<p>
        Sets the user of the application instance. An application instance may
        have a user associated to it. This can be set in login procedure or
        application initialization.
        </p>
        <p>
        A component performing the user login procedure can assign the user
        property of the application and make the user object available to other
        components of the application.
        </p>
        <p>
        Vaadin doesn't define of use user object in any way - it only provides
        getter and setter methods for convenience. The user reference stored to
        the application can be read with {@link #getUser()}.
        </p>

        @param user
                   the new user.
        """
        prevUser = self._user
        if (user == prevUser) or (user is not None and user == prevUser):
            return

        self._user = user
        if self._userChangeListeners is not None:
            listeners = list(self._userChangeListeners)
            event = UserChangeEvent(self, user, prevUser)
            for l in listeners:
                l.applicationUserChanged(event)


    def getURL(self):
        """Gets the URL of the application.

        <p>
        This is the URL what can be entered to a browser window to start the
        application. Navigating to the application URL shows the main window (
        {@link #getMainWindow()}) of the application. Note that the main window
        can also be shown by navigating to the window url (
        {@link com.vaadin.ui.Window#getURL()}).
        </p>

        @return the application's URL.
        """
        return self._applicationUrl


    def close(self):
        """Ends the Application.

        <p>
        In effect this will cause the application stop returning any windows when
        asked. When the application is closed, its state is removed from the
        session and the browser window is redirected to the application logout
        url set with {@link #setLogoutURL(String)}. If the logout url has not
        been set, the browser window is reloaded and the application is
        restarted.
        </p>
        .
        """
        self._applicationIsRunning = False


    def start(self, applicationUrl, applicationProperties, context):
        """Starts the application on the given URL.

        <p>
        This method is called by Vaadin framework when a user navigates to the
        application. After this call the application corresponds to the given URL
        and it will return windows when asked for them. There is no need to call
        this method directly.
        </p>

        <p>
        Application properties are defined by servlet configuration object
        {@link javax.servlet.ServletConfig} and they are overridden by
        context-wide initialization parameters
        {@link javax.servlet.ServletContext}.
        </p>

        @param applicationUrl
                   the URL the application should respond to.
        @param applicationProperties
                   the Application properties as specified by the servlet
                   configuration.
        @param context
                   the context application will be running in.
        """
        self._applicationUrl = applicationUrl
        self._properties = applicationProperties
        self._context = context
        self.init()
        self._applicationIsRunning = True


    def isRunning(self):
        """Tests if the application is running or if it has been finished.

        <p>
        Application starts running when its
        {@link #start(URL, Properties, ApplicationContext)} method has been
        called and stops when the {@link #close()} is called.
        </p>

        @return <code>true</code> if the application is running,
                <code>false</code> if not.
        """
        return self._applicationIsRunning


    def getWindows(self):
        """Gets the set of windows contained by the application.

        <p>
        Note that the returned set of windows can not be modified.
        </p>

        @return the Unmodifiable collection of windows.
        """
        return self._windows.values()


    def init(self):
        """<p>
        Main initializer of the application. The <code>init</code> method is
        called by the framework when the application is started, and it should
        perform whatever initialization operations the application needs, such as
        creating windows and adding components to them.
        </p>
        """
        raise NotImplementedError


    def getTheme(self):
        """Gets the application's theme. The application's theme is the default
        theme used by all the windows in it that do not explicitly specify a
        theme. If the application theme is not explicitly set, the
        <code>null</code> is returned.

        @return the name of the application's theme.
        """
        return self._theme


    def setTheme(self, theme):
        """Sets the application's theme.
        <p>
        Note that this theme can be overridden in the the application level
        windows with {@link com.vaadin.ui.Window#setTheme(String)}. Setting theme
        to be <code>null</code> selects the default theme. For the available
        theme names, see the contents of the VAADIN/themes directory.
        </p>

        @param theme
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
        self._theme = theme

        # Ask windows to update themselves
        for w in toBeUpdated:
            w.requestRepaint()


    def getMainWindow(self):
        """Gets the mainWindow of the application.

        <p>
        The main window is the window attached to the application URL (
        {@link #getURL()}) and thus which is show by default to the user.
        </p>
        <p>
        Note that each application must have at least one main window.
        </p>

        @return the main window.
        """
        return self._mainWindow


    def setMainWindow(self, mainWindow):
        """<p>
        Sets the mainWindow. If the main window is not explicitly set, the main
        window defaults to first created window. Setting window as a main window
        of this application also adds the window to this application.
        </p>

        @param mainWindow
                   the mainWindow to set.
        """
        self.addWindow(mainWindow)
        self._mainWindow = mainWindow


    def getPropertyNames(self):
        """Returns an enumeration of all the names in this application.

        <p>
        See {@link #start(URL, Properties, ApplicationContext)} how properties
        are defined.
        </p>

        @return an enumeration of all the keys in this property list, including
                the keys in the default property list.
        """
        return self._properties.keys()


    def getProperty(self, name):
        """Searches for the property with the specified name in this application.
        This method returns <code>null</code> if the property is not found.

        See {@link #start(URL, Properties, ApplicationContext)} how properties
        are defined.

        @param name
                   the name of the property.
        @return the value in this property list with the specified key value.
        """
        return self._properties[name]


    def addResource(self, resource):
        """Adds new resource to the application. The resource can be accessed by the
        user of the application.

        @param resource
                   the resource to add.
        """
        # Check if the resource is already mapped
        if resource in self._resourceKeyMap:
            return

        # Generate key
        key = str(++self._lastResourceKeyNumber)

        # Add the resource to mappings
        self._resourceKeyMap[resource] = key
        self._keyResourceMap[key] = resource


    def removeResource(self, resource):
        """Removes the resource from the application.

        @param resource
                   the resource to remove.
        """
        key = self._resourceKeyMap.get(resource)
        if key is not None:
            del self._resourceKeyMap[resource]
            del self._keyResourceMap[key]


    def getRelativeLocation(self, resource):
        """Gets the relative uri of the resource. This method is intended to be
        called only be the terminal implementation.

        This method can only be called from within the processing of a UIDL
        request, not from a background thread.

        @param resource
                   the resource to get relative location.
        @return the relative uri of the resource or null if called in a
                background thread

        @deprecated: this method is intended to be used by the terminal only. It
                    may be removed or moved in the future.
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

        <p>
        This method gets called by terminal. It has lots of duties like to pass
        uri handler to proper uri handlers registered to windows etc.
        </p>

        <p>
        In most situations developers should NOT OVERRIDE this method. Instead
        developers should implement and register uri handlers to windows.
        </p>

        @deprecated this method is called be the terminal implementation only and
                    might be removed or moved in the future. Instead of
                    overriding this method, add your {@link IUriHandler} to a top
                    level {@link Window} (eg.
                    getMainWindow().addUriHanler(handler) instead.
        """
        warn(("this method is called be the terminal "
            "implementation only and might be removed or moved in the future. "
            "Instead of overriding this method, add your {@link IUriHandler} to "
            "a top level {@link Window} (eg. getMainWindow().addUriHanler(handler) "
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

        @return the locale of this application.
        """
        if self._locale is not None:
            return self._locale

        return Locale.getDefault()


    def setLocale(self, locale):
        """Sets the default locale for this application.

        By default this is the preferred locale of the user using the
        application. In most cases it is read from the browser defaults.

        @param locale
                   the Locale object.
        """
        self._locale = locale


    def addListener(self, listener):
        """Adds the user change listener.

        This allows one to get notification each time {@link #setUser(Object)} is
        called.

        @param listener
                   the user change listener to add.
        ---
        Adds the window attach listener.

        Use this to get notifications each time a window is attached to the
        application with {@link #addWindow(Window)}.

        @param listener
                   the window attach listener to add.
        ---
        Adds the window detach listener.

        Use this to get notifications each time a window is remove from the
        application with {@link #removeWindow(Window)}.

        @param listener
                   the window detach listener to add.
        """
        if isinstance(listener, UserChangeListener):
            if self._userChangeListeners is None:
                self._userChangeListeners = list()

            self._userChangeListeners.append(listener)
        elif isinstance(listener, WindowAttachListener):
            if self._windowAttachListeners is None:
                self._windowAttachListeners = list()

            self._windowAttachListeners.append(listener)
        elif isinstance(listener, WindowDetachListener):
            if self._windowDetachListeners is None:
                self._windowDetachListeners = list()

            self._windowDetachListeners.append(listener)
        else:
            super(Application, self).addListener(listener)


    def removeListener(self, listener):
        """Removes the user change listener.

        @param listener
                   the user change listener to remove.
        ---
        Removes the window attach listener.

        @param listener
                   the window attach listener to remove.
        ---
        Removes the window detach listener.

        @param listener
                   the window detach listener to remove.
        """
        if isinstance(listener, UserChangeListener):
            if self._userChangeListeners is None:
                return
            self._userChangeListeners.remove(listener)
            if len(self._userChangeListeners) == 0:
                self._userChangeListeners = None

        elif isinstance(listener, WindowAttachListener):
            if self._windowAttachListeners is not None:
                self._windowAttachListeners.remove(listener)
                if len(self._windowAttachListeners) == 0:
                    self._windowAttachListeners = None

        elif isinstance(listener, WindowDetachListener):
            if self._windowDetachListeners is not None:
                self._windowDetachListeners.remove(listener)
                if len(self._windowDetachListeners) == 0:
                    self._windowDetachListeners = None
        else:
            super(Application, self).addListener(listener)


    def getLogoutURL(self):
        """Returns the URL user is redirected to on application close. If the URL is
        <code>null</code>, the application is closed normally as defined by the
        application running environment.
        <p>
        Desktop application just closes the application window and
        web-application redirects the browser to application main URL.
        </p>

        @return the URL.
        """
        return self._logoutURL


    def setLogoutURL(self, logoutURL):
        """Sets the URL user is redirected to on application close. If the URL is
        <code>null</code>, the application is closed normally as defined by the
        application running environment: Desktop application just closes the
        application window and web-application redirects the browser to
        application main URL.

        @param logoutURL
                   the logoutURL to set.
        """
        self._logoutURL = logoutURL


    @classmethod
    def getSystemMessages(cls):
        """Gets the SystemMessages for this application. SystemMessages are used to
        notify the user of various critical situations that can occur, such as
        session expiration, client/server out of sync, and internal server error.

        You can customize the messages by "overriding" this method and returning
        {@link CustomizedSystemMessages}. To "override" this method, re-implement
        this method in your application (the class that extends
        {@link Application}). Even though overriding static methods is not
        possible in Java, Vaadin selects to call the static method from the
        subclass instead of the original {@link #getSystemMessages()} if such a
        method exists.

        @return the SystemMessages for this application
        """
        return cls._DEFAULT_SYSTEM_MESSAGES


    def terminalError(self, event):
        """<p>
        Invoked by the terminal on any exception that occurs in application and
        is thrown by the <code>setVariable</code> to the terminal. The default
        implementation sets the exceptions as <code>ComponentErrors</code> to the
        component that initiated the exception and prints stack trace to standard
        error stream.
        </p>
        <p>
        You can safely override this method in your application in order to
        direct the errors to some other destination (for example log).
        </p>

        @param event
                   the change event.
        @see com.vaadin.terminal.ITerminal.IErrorListener#terminalError(com.vaadin.terminal.ITerminal.IErrorEvent)
        """
        t = event.getThrowable()
        if isinstance(t, IOError):  #SocketException
            # Most likely client browser closed socket
            logger.info('SocketException in CommunicationManager.' \
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
                owner.setComponentError( SystemErr(t) )
        # also print the error on console
        logger.critical('ITerminal error: ' + str(t))


    def getContext(self):
        """Gets the application context.
        <p>
        The application context is the environment where the application is
        running in. The actual implementation class of may contains quite a lot
        more functionality than defined in the {@link ApplicationContext}
        interface.
        </p>
        <p>
        By default, when you are deploying your application to a servlet
        container, the implementation class is {@link WebApplicationContext} -
        you can safely cast to this class and use the methods from there. When
        you are deploying your application as a portlet, context implementation
        is {@link PortletApplicationContext}.
        </p>

        @return the application context.
        """
        return self._context


    def getVersion(self):
        """Override this method to return correct version number of your
        Application. Version information is delivered for example to Testing
        Tools test results. By default this returns a string "NONVERSIONED".

        @return version string
        """
        return 'NONVERSIONED'


    def getErrorHandler(self):
        """Gets the application error handler.

        The default error handler is the application itself.

        @return Application error handler
        """
        return self._errorHandler


    def setErrorHandler(self, errorHandler):
        """Sets the application error handler.

        The default error handler is the application itself. By overriding this,
        you can redirect the error messages to your selected target (log for
        example).

        @param errorHandler
        """
        self._errorHandler = errorHandler


class UserChangeEvent(EventObject):
    """<p>
    An event that characterizes a change in the current selection.
    </p>
    Application user change event sent when the setUser is called to change
    the current user of the application.

    @version @VERSION@
    @since 3.0
    """

    def __init__(self, source, newUser, prevUser):
        """Constructor for user change event.

        @param source
                   the application source.
        @param newUser
                   the new User.
        @param prevUser
                   the previous User.
        """
        super(UserChangeEvent, self).__init__(source)

        # New user of the application.
        self._newUser = newUser

        # Previous user of the application.
        self._prevUser = prevUser


    def getNewUser(self):
        """Gets the new user of the application.

        @return the new User.
        """
        return self._newUser


    def getPreviousUser(self):
        """Gets the previous user of the application.

        @return the previous Vaadin user, if user has not changed ever on
                application it returns <code>null</code>
        """
        return self._prevUser


    def getApplication(self):
        """Gets the application where the user change occurred.

        @return the Application.
        """
        return self.getSource()


class UserChangeListener(IEventListener):
    """The <code>UserChangeListener</code> interface for listening application
    user changes.

    @version @VERSION@
    @since 3.0
    """

    def applicationUserChanged(self, event):
        """The <code>applicationUserChanged</code> method Invoked when the
        application user has changed.

        @param event
                   the change event.
        """
        pass


class WindowDetachEvent(EventObject):
    """Window detach event.

    This event is sent each time a window is removed from the application
    with {@link com.vaadin.Application#removeWindow(Window)}.
    """

    def __init__(self, window):
        """Creates a event.

        @param window
                   the Detached window.
        """
        super(WindowDetachEvent, self).__init__(self)
        self._window = window


    def getWindow(self):
        """Gets the detached window.

        @return the detached window.
        """
        return self._window


    def getApplication(self):
        """Gets the application from which the window was detached.

        @return the Application.
        """
        return self.getSource()


class WindowAttachEvent(EventObject):
    """Window attach event.

    This event is sent each time a window is attached tothe application with
    {@link com.vaadin.Application#addWindow(Window)}.
    """

    def __init__(self, window):
        """Creates a event.

        @param window
                   the Attached window.
        """
        super(WindowAttachEvent, self).__init__(self)
        self._window = window


    def getWindow(self):
        """Gets the attached window.

        @return the attached window.
        """
        return self._window


    def getApplication(self):
        """Gets the application to which the window was attached.

        @return the Application.
        """
        return self.getSource()


class WindowAttachListener(object):
    """Window attach listener interface."""


    def windowAttached(self, event):
        """Window attached

        @param event
                   the window attach event.
        """
        pass


class WindowDetachListener(object):
    """Window detach listener interface."""


    def windowDetached(self, event):
        """Window detached.

        @param event
                   the window detach event.
        """
        pass


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
