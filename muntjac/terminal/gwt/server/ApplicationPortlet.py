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

from com.vaadin.terminal.gwt.server.ApplicationServlet import (ApplicationServlet,)
from com.vaadin.Application import (Application,)
from com.vaadin.terminal.gwt.server.Constants import (Constants,)
from com.vaadin.terminal.gwt.server.AbstractApplicationPortlet import (AbstractApplicationPortlet,)
from com.vaadin.terminal.gwt.server.PortletApplicationContext import (PortletApplicationContext,)
from com.vaadin.terminal.gwt.server.AbstractApplicationServlet import (AbstractApplicationServlet,)
# from java.io.IOException import (IOException,)
# from java.io.OutputStream import (OutputStream,)
# from java.io.PrintWriter import (PrintWriter,)
# from java.io.Serializable import (Serializable,)
# from java.util.logging.Level import (Level,)
# from java.util.logging.Logger import (Logger,)
# from javax.portlet.ActionRequest import (ActionRequest,)
# from javax.portlet.ActionResponse import (ActionResponse,)
# from javax.portlet.PortalContext import (PortalContext,)
# from javax.portlet.Portlet import (Portlet,)
# from javax.portlet.PortletConfig import (PortletConfig,)
# from javax.portlet.PortletException import (PortletException,)
# from javax.portlet.PortletRequestDispatcher import (PortletRequestDispatcher,)
# from javax.portlet.PortletSession import (PortletSession,)
# from javax.portlet.RenderRequest import (RenderRequest,)
# from javax.portlet.RenderResponse import (RenderResponse,)


class ApplicationPortlet(Portlet, Serializable):
    """Portlet main class for Portlet 1.0 (JSR-168) portlets which consist of a
    portlet and a servlet. For Portlet 2.0 (JSR-286, no servlet required), use
    {@link ApplicationPortlet2} instead.
    """
    # portlet configuration parameters
    _PORTLET_PARAMETER_APPLICATION = 'application'
    _PORTLET_PARAMETER_STYLE = 'style'
    _PORTLET_PARAMETER_WIDGETSET = 'widgetset'
    # The application to show
    app = None
    # some applications might require forced height (and, more seldom, width)
    style = None
    # e.g "height:500px;"
    # force the portlet to use this widgetset - portlet level setting
    portletWidgetset = None

    def destroy(self):
        pass

    def init(self, config):
        self.app = config.getInitParameter(self._PORTLET_PARAMETER_APPLICATION)
        if self.app is None:
            raise PortletException('No porlet application url defined in portlet.xml. Define the \'' + self._PORTLET_PARAMETER_APPLICATION + '\' init parameter to be the servlet deployment path.')
        self.style = config.getInitParameter(self._PORTLET_PARAMETER_STYLE)
        # enable forcing the selection of the widgetset in portlet
        # configuration for a single portlet (backwards compatibility)
        self.portletWidgetset = config.getInitParameter(self._PORTLET_PARAMETER_WIDGETSET)

    def processAction(self, request, response):
        PortletApplicationContext.dispatchRequest(self, request, response)

    def render(self, request, response):
        # display the Vaadin application
        self.writeAjaxWindow(request, response)

    def writeAjaxWindow(self, request, response):
        response.setContentType('text/html')
        if self.app is not None:
            sess = request.getPortletSession()
            ctx = PortletApplicationContext.getApplicationContext(sess)
            dispatcher = sess.getPortletContext().getRequestDispatcher('/' + self.app)
            # portal-wide settings
            try:
                portalCtx = request.getPortalContext()
                isLifeRay = portalCtx.getPortalInfo().toLowerCase().contains('liferay')
                request.setAttribute(ApplicationServlet.REQUEST_FRAGMENT, 'true')
                # fixed base theme to use - all portal pages with Vaadin
                # applications will load this exactly once
                portalTheme = self.getPortalProperty(Constants.PORTAL_PARAMETER_VAADIN_THEME, portalCtx)
                portalWidgetset = self.getPortalProperty(Constants.PORTAL_PARAMETER_VAADIN_WIDGETSET, portalCtx)
                # location of the widgetset(s) and default theme (to which
                # /VAADIN/widgetsets/...
                # is appended)
                portalResourcePath = self.getPortalProperty(Constants.PORTAL_PARAMETER_VAADIN_RESOURCE_PATH, portalCtx)
                if portalResourcePath is not None:
                    # if portalResourcePath is defined, set it as a request
                    # parameter which will override the default location in
                    # servlet
                    request.setAttribute(ApplicationServlet.REQUEST_VAADIN_STATIC_FILE_PATH, portalResourcePath)
                # - if the user has specified a widgetset for this portlet, use
                # it from the portlet (not fully supported)
                # - otherwise, if specified, use the portal-wide widgetset
                # and widgetset path settings (recommended)
                # - finally, default to use the default widgetset if nothing
                # else is found
                if self.portletWidgetset is not None:
                    request.setAttribute(ApplicationServlet.REQUEST_WIDGETSET, self.portletWidgetset)
                if portalWidgetset is not None:
                    request.setAttribute(ApplicationServlet.REQUEST_SHARED_WIDGETSET, portalWidgetset)
                if self.style is not None:
                    request.setAttribute(ApplicationServlet.REQUEST_APPSTYLE, self.style)
                # portalTheme is only used if the shared portal resource
                # directory is defined
                if portalTheme is not None and portalResourcePath is not None:
                    request.setAttribute(ApplicationServlet.REQUEST_DEFAULT_THEME, portalTheme)
                    defaultThemeUri = None
                    defaultThemeUri = portalResourcePath + '/' + AbstractApplicationServlet.THEME_DIRECTORY_PATH + portalTheme
                    # Make sure portal default Vaadin theme is included in DOM.
                    # Vaadin portlet themes do not "inherit" base theme, so we
                    # need to force loading of the common base theme.

                    out = response.getPortletOutputStream()
                    # Using portal-wide theme
                    loadDefaultTheme = '<script type=\"text/javascript\">\n' + 'if(!vaadin) { var vaadin = {} } \n' + 'if(!vaadin.themesLoaded) { vaadin.themesLoaded = {} } \n' + 'if(!vaadin.themesLoaded[\'' + portalTheme + '\']) {\n' + 'var stylesheet = document.createElement(\'link\');\n' + 'stylesheet.setAttribute(\'rel\', \'stylesheet\');\n' + 'stylesheet.setAttribute(\'type\', \'text/css\');\n' + 'stylesheet.setAttribute(\'href\', \'' + defaultThemeUri + '/styles.css\');\n' + 'document.getElementsByTagName(\'head\')[0].appendChild(stylesheet);\n' + 'vaadin.themesLoaded[\'' + portalTheme + '\'] = true;\n}\n' + '</script>\n'
                    out.write(loadDefaultTheme.getBytes())
                dispatcher.include(request, response)
                if isLifeRay:
                    # Temporary support to heartbeat Liferay session when using
                    # Vaadin based portlet. We hit an extra xhr to liferay
                    # servlet to extend the session lifetime after each Vaadin
                    # request. This hack can be removed when supporting portlet
                    # 2.0 and resourceRequests.
                    # 
                    # TODO make this configurable, this is not necessary with
                    # some custom session configurations.

                    out = response.getPortletOutputStream()
                    lifeRaySessionHearbeatHack = '<script type=\"text/javascript\">' + 'if(!vaadin.postRequestHooks) {' + '    vaadin.postRequestHooks = {};' + '}' + 'vaadin.postRequestHooks.liferaySessionHeartBeat = function() {' + '    if (Liferay && Liferay.Session && Liferay.Session.setCookie) {' + '        Liferay.Session.setCookie();' + '    }' + '};' + '</script>'
                    out.write(lifeRaySessionHearbeatHack.getBytes())
            except PortletException, e:
                out = response.getWriter()
                out.print_('<h1>Servlet include failed!</h1>')
                Logger.getLogger(AbstractApplicationPortlet.getName()).log(Level.WARNING, 'Servlet include failed', e)
                ctx.setPortletApplication(self, None)
                return
            app = request.getAttribute(Application.getName())
            ctx.setPortletApplication(self, app)
            ctx.firePortletRenderRequest(self, request, response)

    def getPortalProperty(self, name, context):
        isLifeRay = context.getPortalInfo().toLowerCase().contains('liferay')
        # TODO test on non-LifeRay platforms
        if isLifeRay:
            value = self.getLifeRayPortalProperty(name)
        else:
            value = context.getProperty(name)
        return value

    def getLifeRayPortalProperty(self, name):
        try:
            value = self.PropsUtil.get(name)
        except Exception, e:
            value = None
        return value
