
from warnings import warn

from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet


class GaeApplicationServlet(ApplicationServlet):

    SID = '0ce25c442d1f4fad8fb6eb44f24ff4a5e0df89e07ae97a3f'

    def getSession(self, request, allowSessionCreation=True):
        return super(GaeApplicationServlet, self).getSession(request, True)


    def invalidateSession(self, request):
        session = request.session()
        session.terminate()


    def getSessionId(self, request):
#        return request.value(self.SID, None
        return request.environ().get('HTTP_COOKIE')
