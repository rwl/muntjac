# @INVIENT_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet


class InvientChartsDemoAppServlet(ApplicationServlet):

    def writeAjaxPageHtmlMuntjacScripts(self, window, themeName, application, page, appUrl, themeUri, appId, request):
        page.write('<script type=\"text/javascript\">\n')
        page.write('//<![CDATA[\n')
        page.write('document.write(\"<script language=\'javascript\' src=\'./jquery/jquery-1.4.4.min.js\'><\\/script>\");\n')
        page.write('document.write(\"<script language=\'javascript\' src=\'./js/highcharts.js\'><\\/script>\");\n')
        page.write('document.write(\"<script language=\'javascript\' src=\'./js/modules/exporting.js\'><\\/script>\");\n')
        page.write('//]]>\n</script>\n')
        super(InvientChartsDemoAppServlet, self).writeAjaxPageHtmlMuntjacScripts(window, themeName, application, page, appUrl, themeUri, appId, request)
