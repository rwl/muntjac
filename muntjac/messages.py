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


class SystemMessages(object):
    """Contains the system messages used to notify the user about various
    critical situations that can occur.

    Customize by overriding the static L{Application.getSystemMessages()} and
    returning L{CustomizedSystemMessages}.

    The defaults defined in this class are:

      - B{sessionExpiredURL} = None
      - B{sessionExpiredNotificationEnabled} = True
      - B{sessionExpiredCaption} = ""
      - B{sessionExpiredMessage} = "Take note of any unsaved data, and <u>click here</u> to continue."
      - B{communicationErrorURL} = None
      - B{communicationErrorNotificationEnabled} = True
      - B{communicationErrorCaption} = "Communication problem"
      - B{communicationErrorMessage} = "Take note of any unsaved data, and <u>click here</u> to continue."
      - B{internalErrorURL} = None
      - B{internalErrorNotificationEnabled} = True
      - B{internalErrorCaption} = "Internal error"
      - B{internalErrorMessage} = "Please notify the administrator.<br/>Take note of any unsaved data, and <u>click here</u> to continue."
      - B{outOfSyncURL} = None
      - B{outOfSyncNotificationEnabled} = True
      - B{outOfSyncCaption} = "Out of sync"
      - B{outOfSyncMessage} = "Something has caused us to be out of sync with the server.<br/>Take note of any unsaved data, and <u>click here</u> to re-sync."
      - B{cookiesDisabledURL} = None
      - B{cookiesDisabledNotificationEnabled} = True
      - B{cookiesDisabledCaption} = "Cookies disabled"
      - B{cookiesDisabledMessage} = "This application requires cookies to function.<br/>Please enable cookies in your browser and <u>click here</u> to try again."

    """

    def __init__(self):
        """Use L{CustomizedSystemMessages} to customize"""

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
        """@return: null to indicate that the application will be restarted after
                    session expired message has been shown.
        """
        return self.sessionExpiredURL


    def isSessionExpiredNotificationEnabled(self):
        """@return: true to show session expiration message."""
        return self.sessionExpiredNotificationEnabled


    def getSessionExpiredCaption(self):
        """@return: "" to show no caption."""
        return self.sessionExpiredCaption if self.sessionExpiredNotificationEnabled else None


    def getSessionExpiredMessage(self):
        """@return: "Take note of any unsaved data, and <u>click here</u> to continue."
        """
        return self.sessionExpiredMessage if self.sessionExpiredNotificationEnabled else None


    def getCommunicationErrorURL(self):
        """@return: null to reload the application after communication error
                    message.
        """
        return self.communicationErrorURL


    def isCommunicationErrorNotificationEnabled(self):
        """@return: true to show the communication error message."""
        return self.communicationErrorNotificationEnabled


    def getCommunicationErrorCaption(self):
        """@return: "Communication problem\""""
        return self.communicationErrorCaption if self.communicationErrorNotificationEnabled else None


    def getCommunicationErrorMessage(self):
        """@return: "Take note of any unsaved data, and <u>click here</u> to continue."
        """
        return self.communicationErrorMessage if self.communicationErrorNotificationEnabled else None


    def getAuthenticationErrorURL(self):
        """@return: null to reload the application after authentication error
                    message.
        """
        return self.authenticationErrorURL


    def isAuthenticationErrorNotificationEnabled(self):
        """@return: true to show the authentication error message."""
        return self.authenticationErrorNotificationEnabled


    def getAuthenticationErrorCaption(self):
        """@return: "Authentication problem\""""
        return self.authenticationErrorCaption if self.authenticationErrorNotificationEnabled else None


    def getAuthenticationErrorMessage(self):
        """@return:
                "Take note of any unsaved data, and <u>click here</u> to continue."
        """
        return self.authenticationErrorMessage if self.authenticationErrorNotificationEnabled else None


    def getInternalErrorURL(self):
        """@return: null to reload the current URL after internal error message
                    has been shown.
        """
        return self.internalErrorURL


    def isInternalErrorNotificationEnabled(self):
        """@return: true to enable showing of internal error message."""
        return self.internalErrorNotificationEnabled


    def getInternalErrorCaption(self):
        """@return: "Internal error\""""
        return self.internalErrorCaption if self.internalErrorNotificationEnabled else None


    def getInternalErrorMessage(self):
        """@return: "Please notify the administrator.<br/>
                Take note of any unsaved data, and <u>click here</u> to
                continue."
        """
        return self.internalErrorMessage if self.internalErrorNotificationEnabled else None


    def getOutOfSyncURL(self):
        """@return: null to reload the application after out of sync message."""
        return self.outOfSyncURL


    def isOutOfSyncNotificationEnabled(self):
        """@return: true to enable showing out of sync message"""
        return self.outOfSyncNotificationEnabled


    def getOutOfSyncCaption(self):
        """@return: "Out of sync\""""
        return self.outOfSyncCaption if self.outOfSyncNotificationEnabled else None


    def getOutOfSyncMessage(self):
        """@return: "Something has caused us to be out of sync with the server.<br/>
                Take note of any unsaved data, and <u>click here</u> to
                re-sync."
        """
        return self.outOfSyncMessage if self.outOfSyncNotificationEnabled else None


    def getCookiesDisabledURL(self):
        """Returns the URL the user should be redirected to after dismissing the
        "you have to enable your cookies" message. Typically null.

        @return: A URL the user should be redirected to after dismissing the
                 message or null to reload the current URL.
        """
        return self.cookiesDisabledURL


    def isCookiesDisabledNotificationEnabled(self):
        """Determines if "cookies disabled" messages should be shown to the end
        user or not. If the notification is disabled the user will be
        immediately redirected to the URL returned by L{getCookiesDisabledURL}.

        @return: true to show "cookies disabled" messages to the end user,
                 false to redirect to the given URL directly
        """
        return self.cookiesDisabledNotificationEnabled


    def getCookiesDisabledCaption(self):
        """Returns the caption of the message shown to the user when cookies are
        disabled in the browser.

        @return: The caption of the "cookies disabled" message
        """
        return self.cookiesDisabledCaption if self.cookiesDisabledNotificationEnabled else None


    def getCookiesDisabledMessage(self):
        """Returns the message shown to the user when cookies are disabled in
        the browser.

        @return: The "cookies disabled" message
        """
        return self.cookiesDisabledMessage if self.cookiesDisabledNotificationEnabled else None


class CustomizedSystemMessages(SystemMessages):
    """Contains the system messages used to notify the user about various
    critical situations that can occur.

    Muntjac gets the SystemMessages from your application by calling a static
    getSystemMessages() method. By default the
    Application.getSystemMessages() is used. You can customize this by
    defining a static MyApplication.getSystemMessages() and returning
    CustomizedSystemMessages. Note that getSystemMessages() is static -
    changing the system messages will by default change the message for all
    users of the application.

    The default behavior is to show a notification, and restart the
    application the the user clicks the message.

    Instead of restarting the application, you can set a specific URL that
    the user is taken to.

    Setting both caption and message to null will restart the application (or
    go to the specified URL) without displaying a notification.
    set*NotificationEnabled(false) will achieve the same thing.

    The situations are:
      - Session expired: the user session has expired, usually due to
        inactivity.
      - Communication error: the client failed to contact the server, or the
        server returned and invalid response.
      - Internal error: unhandled critical server error (e.g out of memory,
        database crash)
      - Out of sync: the client is not in sync with the server. E.g the user
        opens two windows showing the same application, but the application does
        not support this and uses the same Window instance. When the user makes
        changes in one of the windows - the other window is no longer in sync,
        and (for instance) pressing a button that is no longer present in the UI
        will cause a out-of-sync -situation.
    """

    def setSessionExpiredURL(self, sessionExpiredURL):
        """Sets the URL to go to when the session has expired.

        @param sessionExpiredURL:
                   the URL to go to, or null to reload current
        """
        self.sessionExpiredURL = sessionExpiredURL


    def setSessionExpiredNotificationEnabled(self, sessionExpiredNotificationEnabled):
        """Enables or disables the notification. If disabled, the set URL (or
        current) is loaded directly when next transaction between server and
        client happens.

        @param sessionExpiredNotificationEnabled:
                   true = enabled, false = disabled
        """
        self.sessionExpiredNotificationEnabled = sessionExpiredNotificationEnabled


    def setSessionExpiredCaption(self, sessionExpiredCaption):
        """Sets the caption of the notification. Set to null for no caption. If
        both caption and message are null, client automatically forwards to
        sessionExpiredUrl after timeout timer expires. Timer uses value read
        from HTTPSession.getMaxInactiveInterval()

        @param sessionExpiredCaption: the caption
        """
        self.sessionExpiredCaption = sessionExpiredCaption


    def setSessionExpiredMessage(self, sessionExpiredMessage):
        """Sets the message of the notification. Set to null for no message. If
        both caption and message are null, client automatically forwards to
        sessionExpiredUrl after timeout timer expires. Timer uses value read
        from HTTPSession.getMaxInactiveInterval()

        @param sessionExpiredMessage: the message
        """
        self.sessionExpiredMessage = sessionExpiredMessage


    def setAuthenticationErrorURL(self, authenticationErrorURL):
        """Sets the URL to go to when there is a authentication error.

        @param authenticationErrorURL:
                   the URL to go to, or null to reload current
        """
        self.authenticationErrorURL = authenticationErrorURL


    def setAuthenticationErrorNotificationEnabled(self, authenticationErrorNotificationEnabled):
        """Enables or disables the notification. If disabled, the set URL (or
        current) is loaded directly.

        @param authenticationErrorNotificationEnabled:
                   true = enabled, false = disabled
        """
        self.authenticationErrorNotificationEnabled = authenticationErrorNotificationEnabled


    def setAuthenticationErrorCaption(self, authenticationErrorCaption):
        """Sets the caption of the notification. Set to null for no caption. If
        both caption and message is null, the notification is disabled;

        @param authenticationErrorCaption:
                   the caption
        """
        self.authenticationErrorCaption = authenticationErrorCaption


    def setAuthenticationErrorMessage(self, authenticationErrorMessage):
        """Sets the message of the notification. Set to null for no message. If
        both caption and message is null, the notification is disabled;

        @param authenticationErrorMessage:
                   the message
        """
        self.authenticationErrorMessage = authenticationErrorMessage


    def setCommunicationErrorURL(self, communicationErrorURL):
        """Sets the URL to go to when there is a communication error.

        @param communicationErrorURL:
                   the URL to go to, or null to reload current
        """
        self.communicationErrorURL = communicationErrorURL


    def setCommunicationErrorNotificationEnabled(self, communicationErrorNotificationEnabled):
        """Enables or disables the notification. If disabled, the set URL (or
        current) is loaded directly.

        @param communicationErrorNotificationEnabled:
                   true = enabled, false = disabled
        """
        self.communicationErrorNotificationEnabled = communicationErrorNotificationEnabled


    def setCommunicationErrorCaption(self, communicationErrorCaption):
        """Sets the caption of the notification. Set to null for no caption. If
        both caption and message is null, the notification is disabled;

        @param communicationErrorCaption:
                   the caption
        """
        self.communicationErrorCaption = communicationErrorCaption


    def setCommunicationErrorMessage(self, communicationErrorMessage):
        """Sets the message of the notification. Set to null for no message. If
        both caption and message is null, the notification is disabled;

        @param communicationErrorMessage:
                   the message
        """
        self.communicationErrorMessage = communicationErrorMessage


    def setInternalErrorURL(self, internalErrorURL):
        """Sets the URL to go to when an internal error occurs.

        @param internalErrorURL:
                   the URL to go to, or null to reload current
        """
        self.internalErrorURL = internalErrorURL


    def setInternalErrorNotificationEnabled(self, internalErrorNotificationEnabled):
        """Enables or disables the notification. If disabled, the set URL (or
        current) is loaded directly.

        @param internalErrorNotificationEnabled:
                   true = enabled, false = disabled
        """
        self.internalErrorNotificationEnabled = internalErrorNotificationEnabled


    def setInternalErrorCaption(self, internalErrorCaption):
        """Sets the caption of the notification. Set to null for no caption. If
        both caption and message is null, the notification is disabled;

        @param internalErrorCaption:
                   the caption
        """
        self.internalErrorCaption = internalErrorCaption


    def setInternalErrorMessage(self, internalErrorMessage):
        """Sets the message of the notification. Set to null for no message. If
        both caption and message is null, the notification is disabled;

        @param internalErrorMessage:
                   the message
        """
        self.internalErrorMessage = internalErrorMessage


    def setOutOfSyncURL(self, outOfSyncURL):
        """Sets the URL to go to when the client is out-of-sync.

        @param outOfSyncURL:
                   the URL to go to, or null to reload current
        """
        self.outOfSyncURL = outOfSyncURL


    def setOutOfSyncNotificationEnabled(self, outOfSyncNotificationEnabled):
        """Enables or disables the notification. If disabled, the set URL (or
        current) is loaded directly.

        @param outOfSyncNotificationEnabled:
                   true = enabled, false = disabled
        """
        self.outOfSyncNotificationEnabled = outOfSyncNotificationEnabled


    def setOutOfSyncCaption(self, outOfSyncCaption):
        """Sets the caption of the notification. Set to null for no caption. If
        both caption and message is null, the notification is disabled;

        @param outOfSyncCaption:
                   the caption
        """
        self.outOfSyncCaption = outOfSyncCaption


    def setOutOfSyncMessage(self, outOfSyncMessage):
        """Sets the message of the notification. Set to null for no message. If
        both caption and message is null, the notification is disabled;

        @param outOfSyncMessage:
                   the message
        """
        self.outOfSyncMessage = outOfSyncMessage


    def setCookiesDisabledURL(self, cookiesDisabledURL):
        """Sets the URL to redirect to when the browser has cookies disabled.

        @param cookiesDisabledURL:
                   the URL to redirect to, or null to reload the current URL
        """
        self.cookiesDisabledURL = cookiesDisabledURL


    def setCookiesDisabledNotificationEnabled(self, cookiesDisabledNotificationEnabled):
        """Enables or disables the notification for "cookies disabled" messages.
        If disabled, the URL returned by L{getCookiesDisabledURL} is
        loaded directly.

        @param cookiesDisabledNotificationEnabled:
                   true to enable "cookies disabled" messages, false
                   otherwise
        """
        self.cookiesDisabledNotificationEnabled = cookiesDisabledNotificationEnabled


    def setCookiesDisabledCaption(self, cookiesDisabledCaption):
        """Sets the caption of the "cookies disabled" notification. Set to null
        for no caption. If both caption and message is null, the notification
        is disabled.

        @param cookiesDisabledCaption:
                   the caption for the "cookies disabled" notification
        """
        self.cookiesDisabledCaption = cookiesDisabledCaption


    def setCookiesDisabledMessage(self, cookiesDisabledMessage):
        """Sets the message of the "cookies disabled" notification. Set to null
        for no message. If both caption and message is null, the notification
        is disabled.

        @param cookiesDisabledMessage:
                   the message for the "cookies disabled" notification
        """
        self.cookiesDisabledMessage = cookiesDisabledMessage
