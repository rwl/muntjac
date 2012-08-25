# @INVIENT_COPYRIGHT@
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