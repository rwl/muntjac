
from warnings import warn

from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet

from muntjac.terminal.gwt.server.communication_manager import \
    CommunicationManager

from muntjac.terminal.gwt.server.web_application_context import \
    WebApplicationContext


class GaeApplicationServlet(ApplicationServlet):

    SID = '0ce25c442d1f4fad8fb6eb44f24ff4a5e0df89e07ae97a3f'

    def getSession(self, request, allowSessionCreation=True):
        return super(GaeApplicationServlet, self).getSession(request, True)


    def invalidateSession(self, request):
        session = request.session()
        session.terminate()


    def getSessionId(self, request):
        return request.value(self.SID, None)


    def getApplicationContext(self, session):
        return GaeWebApplicationContext.getApplicationContext(session)


#    def createCommunicationManager(self, application):
#        warn("deprecated", DeprecationWarning)
#
#        return GaeCommunicationManager(application)


class GaeWebApplicationContext(WebApplicationContext):

    def getApplicationManager(self, application, servlet):
        mgr = self.applicationToAjaxAppMgrMap.get(application)

        if mgr is None:
            mgr = GaeCommunicationManager(application)
            self.applicationToAjaxAppMgrMap[application] = mgr

        return mgr


class GaeCommunicationManager(CommunicationManager):

    def _getMonths(self, l=None):
        return super(GaeCommunicationManager, self)._getMonths()


    def _getWeekdays(self, l=None):
        return super(GaeCommunicationManager, self)._getWeekdays()


    def _getDateFormat(self, l=None):
        return super(GaeCommunicationManager, self)._getDateFormat()


    def _getAmPmStrings(self, l=None):
        return super(GaeCommunicationManager, self)._getAmPmStrings()
