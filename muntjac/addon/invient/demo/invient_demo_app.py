# @INVIENT_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.application \
    import Application

from muntjac.addon.invient.demo.invient_demo_win \
    import InvientChartsDemoWin

from muntjac.terminal.gwt.server.http_servlet_request_listener \
    import IHttpServletRequestListener


class InvientChartsDemoApp(Application, IHttpServletRequestListener):

    def __init__(self):
        super(InvientChartsDemoApp, self).__init__()
        self._isAppRunningOnGAE = None


    def isAppRunningOnGAE(self):
        if self._isAppRunningOnGAE is None:
            return False
        return self._isAppRunningOnGAE


    def init(self):
        self.setMainWindow(InvientChartsDemoWin())
        self.getMainWindow().showNotification(
                'To hide a series, click on its legend label.')


    def onRequestStart(self, request, response):
        if self._isAppRunningOnGAE is None:
            self._isAppRunningOnGAE = False
#            serverInfo = request.getSession().getServletContext().getServerInfo()  FIXME
#            if serverInfo is not None and 'Google' in serverInfo:
#                self._isAppRunningOnGAE = True


    def onRequestEnd(self, request, response):
        pass


if __name__ == '__main__':
    from muntjac.main import muntjac
    from invient_demo_app_servlet import InvientChartsDemoAppServlet

    muntjac(InvientChartsDemoApp, nogui=True, forever=True, debug=True,
#            servletClass=InvientChartsDemoAppServlet,
            contextRoot='.')