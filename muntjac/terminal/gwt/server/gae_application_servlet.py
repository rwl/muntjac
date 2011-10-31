
from gaesessions import get_current_session

from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet

import logging

class GaeApplicationServlet(ApplicationServlet):

    SID = '0ce25c442d1f4fad8fb6eb44f24ff4a5e0df89e07ae97a3f'

    def getSession(self, request, allowSessionCreation=True):
        if allowSessionCreation:
            return get_current_session()
        else:
            s = get_current_session()
            if s.is_active():
                return s
            else:
                return None


    def invalidateSession(self, request):
        session = request.session()
        session.terminate()


    def getSessionId(self, request):
        sid = request.cookies().get('DgU00')
        #sid = get_current_session().sid
        logging.getLogger(__name__).info("COOKIE: " + sid )
        return sid


    def getSessionAttribute(self, session, name, default=None):
        return session.get(name, default)


    def setSessionAttribute(self, session, name, value):
        session[name] = value


    def getMaxInactiveInterval(self, session):
        if session.lifetime is not None:
            return int( session.lifetime.total_seconds() )
        else:
            return self._timeout


    def isSessionNew(self, session):
        raise NotImplementedError
