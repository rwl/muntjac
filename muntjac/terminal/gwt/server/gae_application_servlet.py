
from gaesessions import get_current_session

from paste.webkit.wksession import Session

from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet

class GaeApplicationServlet(ApplicationServlet):

    def getSession(self, request, allowSessionCreation=True):
        if allowSessionCreation:
            return Session( get_current_session() )
        else:
            # FIXME: avoid session creation
            return Session( get_current_session() )


    def invalidateSession(self, request):
        session = get_current_session()
        session.terminate()
