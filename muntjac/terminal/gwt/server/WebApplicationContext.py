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

from muntjac.terminal.gwt.server.AbstractWebApplicationContext import AbstractWebApplicationContext
from muntjac.terminal.gwt.server.ApplicationServlet import ApplicationServlet


class WebApplicationContext(AbstractWebApplicationContext):
    """Web application context for Vaadin applications.

    This is automatically added as a {@link HttpSessionBindingListener} when
    added to a {@link HttpSession}.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.1
    """

    def __init__(self):
        """Creates a new Web Application Context."""
        self.session = None
        self._reinitializingSession = False
        # Stores a reference to the currentRequest. Null it not inside a request.
        self._currentRequest = None


    def startTransaction(self, application, request):
        self._currentRequest = request
        super(WebApplicationContext, self).startTransaction(application, request)


    def endTransaction(self, application, request):
        super(WebApplicationContext, self).endTransaction(application, request)
        self._currentRequest = None


    def valueUnbound(self, event):
        if not self._reinitializingSession:
            # Avoid closing the application if we are only reinitializing the
            # session. Closing the application would cause the state to be lost
            # and a new application to be created, which is not what we want.
            super(WebApplicationContext, self).valueUnbound(event)


    def reinitializeSession(self):
        """Discards the current session and creates a new session with the same
        contents. The purpose of this is to introduce a new session key in order
        to avoid session fixation attacks.
        """
        oldSession = self.getHttpSession()
        # Stores all attributes (security key, reference to this context
        # instance) so they can be added to the new session
        attrs = dict()
        attrs.update(oldSession.values)

        # Invalidate the current session, set flag to avoid call to
        # valueUnbound
        self._reinitializingSession = True
        oldSession.invalidate()
        self._reinitializingSession = False

        # Create a new session
        newSession = self._currentRequest.getSession()

        # Restores all attributes (security key, reference to this context
        # instance)
        for name in attrs.keys():
            newSession.setAttribute(name, attrs.get(name))

        # Update the "current session" variable
        self.session = newSession


    def getBaseDirectory(self):
        """Gets the application context base directory.

        @see com.vaadin.service.ApplicationContext#getBaseDirectory()
        """
        realPath = ApplicationServlet.getResourcePath(self.session.getServletContext(), '/')
        if realPath is None:
            return None
        return realPath


    def getHttpSession(self):
        """Gets the http-session application is running in.

        @return HttpSession this application context resides in.
        """
        return self.session


    @classmethod
    def getApplicationContext(cls, session):
        """Gets the application context for an HttpSession.

        @param session
                   the HTTP session.
        @return the application context for HttpSession.
        """
        cx = session.value(WebApplicationContext.__class__.__name__)
        if cx is None:
            cx = WebApplicationContext()
            session.setValue(WebApplicationContext.__class__.__name__, cx)
        if cx.session is None:
            cx.session = session
        return cx


    def addApplication(self, application):
        self.applications.add(application)


    def getApplicationManager(self, application, servlet):
        """Gets communication manager for an application.

        If this application has not been running before, a new manager is
        created.

        @param application
        @return CommunicationManager
        """
        mgr = self.applicationToAjaxAppMgrMap.get(application)
        if mgr is None:
            # Creates new manager
            mgr = servlet.createCommunicationManager(application)
            self.applicationToAjaxAppMgrMap.put(application, mgr)

        return mgr
