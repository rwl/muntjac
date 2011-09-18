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

from com.vaadin.terminal.gwt.server.Constants import (Constants,)
from com.vaadin.terminal.gwt.server.SessionExpiredException import (SessionExpiredException,)
from com.vaadin.Application import (Application,)
from com.vaadin.terminal.gwt.server.AbstractApplicationServlet import (AbstractApplicationServlet, RequestError,)
from com.vaadin.terminal.gwt.server.PortletApplicationContext2 import (PortletApplicationContext2,)
from com.vaadin.terminal.Terminal import (ErrorEvent, Terminal,)
from com.vaadin.terminal.gwt.server.SystemMessageException import (SystemMessageException,)
# from com.liferay.portal.kernel.util.PortalClassInvoker import (PortalClassInvoker,)
# from com.liferay.portal.kernel.util.PropsUtil import (PropsUtil,)
# from com.vaadin.Application.SystemMessages import (SystemMessages,)
# from java.io.BufferedWriter import (BufferedWriter,)
# from java.io.IOException import (IOException,)
# from java.io.InputStream import (InputStream,)
# from java.io.OutputStream import (OutputStream,)
# from java.io.OutputStreamWriter import (OutputStreamWriter,)
# from java.io.PrintWriter import (PrintWriter,)
# from java.io.Serializable import (Serializable,)
# from java.lang.reflect.InvocationTargetException import (InvocationTargetException,)
# from java.lang.reflect.Method import (Method,)
# from java.net.MalformedURLException import (MalformedURLException,)
# from java.security.GeneralSecurityException import (GeneralSecurityException,)
# from java.util.Date import (Date,)
# from java.util.Enumeration import (Enumeration,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedHashMap import (LinkedHashMap,)
# from java.util.Locale import (Locale,)
# from java.util.Map import (Map,)
# from java.util.Properties import (Properties,)
# from java.util.logging.Level import (Level,)
# from java.util.logging.Logger import (Logger,)
# from javax.portlet.ActionRequest import (ActionRequest,)
# from javax.portlet.ActionResponse import (ActionResponse,)
# from javax.portlet.EventRequest import (EventRequest,)
# from javax.portlet.EventResponse import (EventResponse,)
# from javax.portlet.GenericPortlet import (GenericPortlet,)
# from javax.portlet.MimeResponse import (MimeResponse,)
# from javax.portlet.PortalContext import (PortalContext,)
# from javax.portlet.PortletConfig import (PortletConfig,)
# from javax.portlet.PortletContext import (PortletContext,)
# from javax.portlet.PortletException import (PortletException,)
# from javax.portlet.PortletRequest import (PortletRequest,)
# from javax.portlet.PortletResponse import (PortletResponse,)
# from javax.portlet.PortletSession import (PortletSession,)
# from javax.portlet.PortletURL import (PortletURL,)
# from javax.portlet.RenderRequest import (RenderRequest,)
# from javax.portlet.RenderResponse import (RenderResponse,)
# from javax.portlet.ResourceRequest import (ResourceRequest,)
# from javax.portlet.ResourceResponse import (ResourceResponse,)
# from javax.portlet.ResourceURL import (ResourceURL,)
# from javax.servlet.http.HttpServletRequest import (HttpServletRequest,)
# from javax.servlet.http.HttpServletRequestWrapper import (HttpServletRequestWrapper,)
# from javax.servlet.http.HttpServletResponse import (HttpServletResponse,)
import time


class AbstractApplicationPortlet(GenericPortlet, Constants):
    """Portlet 2.0 base class. This replaces the servlet in servlet/portlet 1.0
    deployments and handles various portlet requests from the browser.

    TODO Document me!

    @author peholmst
    """
    _logger = Logger.getLogger(AbstractApplicationPortlet.getName())
    # This portlet parameter is used to add styles to the main element. E.g
    # "height:500px" generates a style="height:500px" to the main element.

    PORTLET_PARAMETER_STYLE = 'style'
    _PORTAL_PARAMETER_VAADIN_THEME = 'vaadin.theme'
    # TODO some parts could be shared with AbstractApplicationServlet
    # TODO Can we close the application when the portlet is removed? Do we know
    # when the portlet is removed?
    # TODO What happens when the portlet window is resized? Do we know when the
    # window is resized?
    _applicationProperties = None
    _productionMode = False

    def init(self, config):
        super(AbstractApplicationPortlet, self).init(config)
        # Stores the application parameters into Properties object
        self._applicationProperties = Properties()
        _0 = True
        e = config.getInitParameterNames()
        while True:
            if _0 is True:
                _0 = False
            if not e.hasMoreElements():
                break
            name = e.nextElement()
            self._applicationProperties.setProperty(name, config.getInitParameter(name))
        # Overrides with server.xml parameters
        context = config.getPortletContext()
        _1 = True
        e = context.getInitParameterNames()
        while True:
            if _1 is True:
                _1 = False
            if not e.hasMoreElements():
                break
            name = e.nextElement()
            self._applicationProperties.setProperty(name, context.getInitParameter(name))
        self.checkProductionMode()
        self.checkCrossSiteProtection()

    def checkCrossSiteProtection(self):
        if (
            self.getApplicationOrSystemProperty(self.SERVLET_PARAMETER_DISABLE_XSRF_PROTECTION, 'false') == 'true'
        ):
            # Print an information/warning message about running with xsrf
            # protection disabled

            self._logger.warning(self.WARNING_XSRF_PROTECTION_DISABLED)

    def checkWidgetsetVersion(self, request):
        """Checks that the version reported by the client (widgetset) matches that
        of the server.

        @param request
        """
        if (
            not (AbstractApplicationServlet.VERSION == self.getHTTPRequestParameter(request, 'wsver'))
        ):
            self._logger.warning(String.format.format(self.WIDGETSET_MISMATCH_INFO, AbstractApplicationServlet.VERSION, self.getHTTPRequestParameter(request, 'wsver')))

    def checkProductionMode(self):
        # Check if the application is in production mode.
        # We are in production mode if Debug=false or productionMode=true
        if (
            self.getApplicationOrSystemProperty(self.SERVLET_PARAMETER_DEBUG, 'true') == 'false'
        ):
            # "Debug=true" is the old way and should no longer be used
            self._productionMode = True
        elif (
            self.getApplicationOrSystemProperty(self.SERVLET_PARAMETER_PRODUCTION_MODE, 'false') == 'true'
        ):
            # "productionMode=true" is the real way to do it
            self._productionMode = True
        if not self._productionMode:
            # Print an information/warning message about running in debug mode
            # TODO Maybe we need a different message for portlets?
            self._logger.warning(self.NOT_PRODUCTION_MODE_INFO)

    def getApplicationProperty(self, parameterName):
        """Gets an application property value.

        @param parameterName
                   the Name or the parameter.
        @return String value or null if not found
        """
        val = self._applicationProperties.getProperty(parameterName)
        if val is not None:
            return val
        # Try lower case application properties for backward compatibility with
        # 3.0.2 and earlier
        val = self._applicationProperties.getProperty(parameterName.toLowerCase())
        return val

    def getSystemProperty(self, parameterName):
        """Gets an system property value.

        @param parameterName
                   the Name or the parameter.
        @return String value or null if not found
        """
        val = None
        pkg = self.getClass().getPackage()
        if pkg is not None:
            pkgName = pkg.getName()
        else:
            className = self.getClass().getName()
            pkgName = str(className.toCharArray(), 0, className.rfind('.'))
        val = System.getProperty(pkgName + '.' + parameterName)
        if val is not None:
            return val
        # Try lowercased system properties
        val = System.getProperty(pkgName + '.' + parameterName.toLowerCase())
        return val

    def getApplicationOrSystemProperty(self, parameterName, defaultValue):
        """Gets an application or system property value.

        @param parameterName
                   the Name or the parameter.
        @param defaultValue
                   the Default to be used.
        @return String value or default if not found
        """
        val = None
        # Try application properties
        val = self.getApplicationProperty(parameterName)
        if val is not None:
            return val
        # Try system properties
        val = self.getSystemProperty(parameterName)
        if val is not None:
            return val
        return defaultValue

    def getStaticFilesLocation(self, request):
        """Return the URL from where static files, e.g. the widgetset and the theme,
        are served. In a standard configuration the VAADIN folder inside the
        returned folder is what is used for widgetsets and themes.

        @param request
        @return The location of static resources (inside which there should be a
                VAADIN directory). Does not end with a slash (/).
        """
        # TODO allow overriding on portlet level?
        staticFileLocation = self.getPortalProperty(Constants.PORTAL_PARAMETER_VAADIN_RESOURCE_PATH, request.getPortalContext())
        if staticFileLocation is not None:
            # remove trailing slash if any
            while staticFileLocation.endswith('.'):
                staticFileLocation = staticFileLocation[:-1]
            return staticFileLocation
        else:
            # default for Liferay
            return '/html'

    class RequestType(object):
        FILE_UPLOAD = 'FILE_UPLOAD'
        UIDL = 'UIDL'
        RENDER = 'RENDER'
        STATIC_FILE = 'STATIC_FILE'
        APPLICATION_RESOURCE = 'APPLICATION_RESOURCE'
        DUMMY = 'DUMMY'
        EVENT = 'EVENT'
        ACTION = 'ACTION'
        UNKNOWN = 'UNKNOWN'
        _values = [FILE_UPLOAD, UIDL, RENDER, STATIC_FILE, APPLICATION_RESOURCE, DUMMY, EVENT, ACTION, UNKNOWN]

        @classmethod
        def values(cls):
            return cls._enum_values[:]

    def getRequestType(self, request):
        if isinstance(request, RenderRequest):
            return self.RequestType.RENDER
        elif isinstance(request, ResourceRequest):
            if self.isUIDLRequest(request):
                return self.RequestType.UIDL
            elif self.isFileUploadRequest(request):
                return self.RequestType.FILE_UPLOAD
            elif self.isApplicationResourceRequest(request):
                return self.RequestType.APPLICATION_RESOURCE
            elif self.isDummyRequest(request):
                return self.RequestType.DUMMY
            else:
                return self.RequestType.STATIC_FILE
        elif isinstance(request, ActionRequest):
            return self.RequestType.ACTION
        elif isinstance(request, EventRequest):
            return self.RequestType.EVENT
        return self.RequestType.UNKNOWN

    def isApplicationResourceRequest(self, request):
        return request.getResourceID() is not None and request.getResourceID().startswith('APP')

    def isUIDLRequest(self, request):
        return request.getResourceID() is not None and request.getResourceID() == 'UIDL'

    def isDummyRequest(self, request):
        return request.getResourceID() is not None and request.getResourceID() == 'DUMMY'

    def isFileUploadRequest(self, request):
        return 'UPLOAD' == request.getResourceID()

    def isProductionMode(self):
        """Returns true if the servlet is running in production mode. Production
        mode disables all debug facilities.

        @return true if in production mode, false if in debug mode
        """
        return self._productionMode

    def handleRequest(self, request, response):
        requestType = self.getRequestType(request)
        if requestType == self.RequestType.UNKNOWN:
            self.handleUnknownRequest(request, response)
        elif requestType == self.RequestType.DUMMY:
            # This dummy page is used by action responses to redirect to, in
            # order to prevent the boot strap code from being rendered into
            # strange places such as iframes.

            response.setContentType('text/html')
            out = response.getPortletOutputStream()
            outWriter = PrintWriter(BufferedWriter(OutputStreamWriter(out, 'UTF-8')))
            outWriter.print_('<html><body>dummy page</body></html>')
            outWriter.close()
        elif requestType == self.RequestType.STATIC_FILE:
            self.serveStaticResources(request, response)
        else:
            application = None
            transactionStarted = False
            requestStarted = False
            try:
                application = self.findApplicationInstance(request, requestType)
                if application is None:
                    return
                # Get or create an application context and an application
                # manager for the session

                applicationContext = self.getApplicationContext(request.getPortletSession())
                applicationContext.setResponse(response)
                applicationContext.setPortletConfig(self.getPortletConfig())
                applicationManager = applicationContext.getApplicationManager(application)
                # Update browser information from request
                self.updateBrowserProperties(applicationContext.getBrowser(), request)
                # Call application requestStart before Application.init() is
                # called (bypasses the limitation in TransactionListener)

                if isinstance(application, PortletRequestListener):
                    application.onRequestStart(request, response)
                    requestStarted = True
                # Start the newly created application
                self.startApplication(request, application, applicationContext)
                # Transaction starts. Call transaction listeners. Transaction
                # end is called in the finally block below.

                applicationContext.startTransaction(application, request)
                transactionStarted = True
                # Notify listeners
                # Finds the window within the application
                window = None
                if application.isRunning():
                    _0 = requestType
                    _1 = False
                    while True:
                        if _0 == self.FILE_UPLOAD:
                            _1 = True
                            break
                        if (_1 is True) or (_0 == self.APPLICATION_RESOURCE):
                            _1 = True
                            window = application.getMainWindow()
                            break
                        if True:
                            _1 = True
                            window = applicationManager.getApplicationWindow(request, self, application, None)
                        break
                    # if window not found, not a problem - use null
                # TODO Should this happen before or after the transaction
                # starts?
                if isinstance(request, RenderRequest):
                    applicationContext.firePortletRenderRequest(application, window, request, response)
                elif isinstance(request, ActionRequest):
                    applicationContext.firePortletActionRequest(application, window, request, response)
                elif isinstance(request, EventRequest):
                    applicationContext.firePortletEventRequest(application, window, request, response)
                elif isinstance(request, ResourceRequest):
                    applicationContext.firePortletResourceRequest(application, window, request, response)
                # Handle the request
                if requestType == self.RequestType.FILE_UPLOAD:
                    applicationManager.handleFileUpload(request, response)
                    return
                elif requestType == self.RequestType.UIDL:
                    # Handles AJAX UIDL requests
                    if self.isRepaintAll(request):
                        # warn if versions do not match
                        self.checkWidgetsetVersion(request)
                    applicationManager.handleUidlRequest(request, response, self, window)
                    return
                else:
                    # Removes the application if it has stopped
                    if not application.isRunning():
                        self.endApplication(request, response, application)
                        return
                    self.handleOtherRequest(request, response, requestType, application, window, applicationContext, applicationManager)
            except SessionExpiredException, e:
                self._logger.finest('A user session has expired')
            except GeneralSecurityException, e:
                self._logger.fine('General security exception, the security key was probably incorrect.')
            except Throwable, e:
                self.handleServiceException(request, response, application, e)
            finally:
                try:
                    if transactionStarted:
                        application.getContext().endTransaction(application, request)
                finally:
                    if requestStarted:
                        application.onRequestEnd(request, response)
            # TODO What about PARAM_UNLOADBURST & redirectToApplication??
            # Find out which application this request is related to
            # TODO Figure out a better way to deal with
            # SessionExpiredExceptions
            # TODO Figure out a better way to deal with
            # GeneralSecurityExceptions
            # Notifies transaction end

    def handleUnknownRequest(self, request, response):
        self._logger.warning('Unknown request type')

    def handleOtherRequest(self, request, response, requestType, application, window, applicationContext, applicationManager):
        """Handle a portlet request that is not for static files, UIDL or upload.
        Also render requests are handled here.

        This method is called after starting the application and calling portlet
        and transaction listeners.

        @param request
        @param response
        @param requestType
        @param application
        @param applicationContext
        @param applicationManager
        @throws PortletException
        @throws IOException
        @throws MalformedURLException
        """
        if window is None:
            raise PortletException(self.ERROR_NO_WINDOW_FOUND)
        # Sets terminal type for the window, if not already set
        if window.getTerminal() is None:
            window.setTerminal(applicationContext.getBrowser())
        # Handle parameters
        parameters = request.getParameterMap()
        if window is not None and parameters is not None:
            window.handleParameters(parameters)
        if requestType == self.RequestType.APPLICATION_RESOURCE:
            self.handleURI(applicationManager, window, request, response)
        elif requestType == self.RequestType.RENDER:
            self.writeAjaxPage(request, response, window, application)
        elif requestType == self.RequestType.EVENT:
            # nothing to do, listeners do all the work
            pass
        elif requestType == self.RequestType.ACTION:
            # nothing to do, listeners do all the work
            pass
        else:
            raise self.IllegalStateException('handleRequest() without anything to do - should never happen!')

    def updateBrowserProperties(self, browser, request):
        userAgent = self.getHTTPHeader(request, 'user-agent')
        browser.updateRequestDetails(request.getLocale(), None, request.isSecure(), userAgent)
        if self.getHTTPRequestParameter(request, 'repaintAll') is not None:
            browser.updateClientSideDetails(self.getHTTPRequestParameter(request, 'sw'), self.getHTTPRequestParameter(request, 'sh'), self.getHTTPRequestParameter(request, 'tzo'), self.getHTTPRequestParameter(request, 'rtzo'), self.getHTTPRequestParameter(request, 'dstd'), self.getHTTPRequestParameter(request, 'dstActive'), self.getHTTPRequestParameter(request, 'curdate'), self.getHTTPRequestParameter(request, 'td') is not None)

    def processEvent(self, request, response):
        self.handleRequest(request, response)

    def handleURI(self, applicationManager, window, request, response):
        # Handles the URI
        download = applicationManager.handleURI(window, request, response, self)
        # A download request
        if download is not None:
            # Client downloads an resource
            self.handleDownload(download, request, response)
            return True
        return False

    def handleDownload(self, stream, request, response):
        if stream.getParameter('Location') is not None:
            response.setProperty(ResourceResponse.HTTP_STATUS_CODE, str(HttpServletResponse.SC_MOVED_TEMPORARILY))
            response.setProperty('Location', stream.getParameter('Location'))
            return
        # Download from given stream
        data = stream.getStream()
        if data is not None:
            # Sets content type
            response.setContentType(stream.getContentType())
            # Sets cache headers
            cacheTime = stream.getCacheTime()
            if cacheTime <= 0:
                response.setProperty('Cache-Control', 'no-cache')
                response.setProperty('Pragma', 'no-cache')
                response.setProperty('Expires', '0')
            else:
                response.setProperty('Cache-Control', 'max-age=' + (cacheTime / 1000))
                response.setProperty('Expires', '' + 1000 * time.time() + cacheTime)
                # Required to apply caching in some Tomcats
                response.setProperty('Pragma', 'cache')
            # Copy download stream parameters directly
            # to HTTP headers.
            i = stream.getParameterNames()
            if i is not None:
                while i.hasNext():
                    param = i.next()
                    response.setProperty(param, stream.getParameter(param))
            # suggest local filename from DownloadStream if Content-Disposition
            # not explicitly set
            contentDispositionValue = stream.getParameter('Content-Disposition')
            if contentDispositionValue is None:
                contentDispositionValue = 'filename=\"' + stream.getFileName() + '\"'
                response.setProperty('Content-Disposition', contentDispositionValue)
            bufferSize = stream.getBufferSize()
            if (bufferSize <= 0) or (bufferSize > self.MAX_BUFFER_SIZE):
                bufferSize = self.DEFAULT_BUFFER_SIZE
            buffer = [None] * bufferSize
            bytesRead = 0
            out = response.getPortletOutputStream()
            while bytesRead = data.read(buffer) > 0:
                out.write(buffer, 0, bytesRead)
                out.flush()
            out.close()

    def serveStaticResources(self, request, response):
        resourceID = request.getResourceID()
        pc = self.getPortletContext()
        is_ = pc.getResourceAsStream(resourceID)
        if is_ is not None:
            mimetype = pc.getMimeType(resourceID)
            if mimetype is not None:
                response.setContentType(mimetype)
            os = response.getPortletOutputStream()
            buffer = [None] * self.DEFAULT_BUFFER_SIZE
            while bytes = is_.read(buffer) >= 0:
                os.write(buffer, 0, bytes)
        else:
            self._logger.info('Requested resource [' + resourceID + '] could not be found')
            response.setProperty(ResourceResponse.HTTP_STATUS_CODE, str(HttpServletResponse.SC_NOT_FOUND))

    def processAction(self, request, response):
        self.handleRequest(request, response)

    def doDispatch(self, request, response):
        # try to let super handle - it'll call methods annotated for
        # handling, the default doXYZ(), or throw if a handler for the mode
        # is not found
        try:
            super(AbstractApplicationPortlet, self).doDispatch(request, response)
        except PortletException, e:
            if e.getCause() is None:
                # No cause interpreted as 'unknown mode' - pass that trough
                # so that the application can handle
                self.handleRequest(request, response)
            else:
                # Something else failed, pass on
                raise e

    def serveResource(self, request, response):
        self.handleRequest(request, response)

    def requestCanCreateApplication(self, request, requestType):
        if requestType == self.RequestType.UIDL and self.isRepaintAll(request):
            return True
        elif requestType == self.RequestType.RENDER:
            # In most cases the first request is a render request that renders
            # the HTML fragment. This should create an application instance.
            return True
        elif requestType == self.RequestType.EVENT:
            # A portlet can also be sent an event even though it has not been
            # rendered, e.g. portlet on one page sends an event to a portlet on
            # another page and then moves the user to that page.
            return True
        return False

    def isRepaintAll(self, request):
        return request.getParameter(self.URL_PARAMETER_REPAINT_ALL) is not None and request.getParameter(self.URL_PARAMETER_REPAINT_ALL) == '1'

    def startApplication(self, request, application, context):
        if not application.isRunning():
            locale = request.getLocale()
            application.setLocale(locale)
            # No application URL when running inside a portlet
            application.start(None, self._applicationProperties, context)

    def endApplication(self, request, response, application):
        session = request.getPortletSession()
        if session is not None:
            self.getApplicationContext(session).removeApplication(application)
        # Do not send any redirects when running inside a portlet.

    def findApplicationInstance(self, request, requestType):
        requestCanCreateApplication = self.requestCanCreateApplication(request, requestType)
        # Find an existing application for this request.
        application = self.getExistingApplication(request, requestCanCreateApplication)
        if application is not None:
            # There is an existing application. We can use this as long as the
            # user not specifically requested to close or restart it.

            restartApplication = self.getHTTPRequestParameter(request, self.URL_PARAMETER_RESTART_APPLICATION) is not None
            closeApplication = self.getHTTPRequestParameter(request, self.URL_PARAMETER_CLOSE_APPLICATION) is not None
            if restartApplication:
                closeApplication(application, request.getPortletSession(False))
                return self.createApplication(request)
            elif closeApplication:
                closeApplication(application, request.getPortletSession(False))
                return None
            else:
                return application
        # No existing application was found
        if requestCanCreateApplication:
            return self.createApplication(request)
        else:
            raise SessionExpiredException()

    def closeApplication(self, application, session):
        if application is None:
            return
        application.close()
        if session is not None:
            context = self.getApplicationContext(session)
            context.removeApplication(application)

    def createApplication(self, request):
        newApplication = self.getNewApplication(request)
        context = self.getApplicationContext(request.getPortletSession())
        context.addApplication(newApplication, request.getWindowID())
        return newApplication

    def getExistingApplication(self, request, allowSessionCreation):
        session = request.getPortletSession(allowSessionCreation)
        if session is None:
            raise SessionExpiredException()
        context = self.getApplicationContext(session)
        application = context.getApplicationForWindowId(request.getWindowID())
        if application is None:
            return None
        if application.isRunning():
            return application
        # application found but not running
        context.removeApplication(application)
        return None

    def getWidgetsetURL(self, widgetset, request):
        """Returns the URL from which the widgetset is served on the portal.

        @param widgetset
        @param request
        @return
        """
        return self.getStaticFilesLocation(request) + '/' + self.WIDGETSET_DIRECTORY_PATH + widgetset + '/' + widgetset + '.nocache.js?' + Date().getTime()

    def getThemeURI(self, themeName, request):
        """Returns the theme URI for the named theme on the portal.

        Note that this is not the only location referring to the theme URI - also
        e.g. PortletCommunicationManager uses its own way to access the portlet
        2.0 theme resources.

        @param themeName
        @param request
        @return
        """
        return self.getStaticFilesLocation(request) + '/' + self.THEME_DIRECTORY_PATH + themeName

    def writeAjaxPage(self, request, response, window, application):
        """Writes the html host page (aka kickstart page) that starts the actual
        Vaadin application.

        If one needs to override parts of the portlet HTML contents creation, it
        is suggested that one overrides one of several submethods including:
        <ul>
        <li>
        {@link #writeAjaxPageHtmlMainDiv(RenderRequest, RenderResponse, BufferedWriter, String)}
        <li>
        {@link #getVaadinConfigurationMap(RenderRequest, RenderResponse, Application, String)}
        <li>
        {@link #writeAjaxPageHtmlVaadinScripts(RenderRequest, RenderResponse, BufferedWriter, Application, String)}
        </ul>

        @param request
                   the portlet request.
        @param response
                   the portlet response to write to.
        @param window
        @param application
        @throws IOException
                    if the writing failed due to input/output error.
        @throws MalformedURLException
                    if the application is denied access the persistent data store
                    represented by the given URL.
        @throws PortletException
        """
        response.setContentType('text/html')
        page = BufferedWriter(OutputStreamWriter(response.getPortletOutputStream(), 'UTF-8'))
        # TODO Currently, we can only load widgetsets and themes from the
        # portal
        themeName = self.getThemeForWindow(request, window)
        self.writeAjaxPageHtmlVaadinScripts(request, response, page, application, themeName)
        # - Add classnames;
        #      .v-app
        #      .v-app-loading
        #      .v-app-<simpleName for app class>
        #      .v-theme-<themeName, remove non-alphanum>

        appClass = 'v-app-'
        try:
            appClass += self.getApplicationClass().getSimpleName()
        except ClassNotFoundException, e:
            appClass += 'unknown'
            self._logger.log(Level.SEVERE, 'Could not find application class', e)
        themeClass = 'v-theme-' + themeName.replaceAll('[^a-zA-Z0-9]', '')
        classNames = 'v-app ' + themeClass + ' ' + appClass
        style = self.getApplicationProperty(self.PORTLET_PARAMETER_STYLE)
        divStyle = ''
        if style is not None:
            divStyle = 'style=\"' + style + '\"'
        self.writeAjaxPageHtmlMainDiv(request, response, page, self.getApplicationDomId(request), classNames, divStyle)
        page.close()

    def getApplicationDomId(self, request):
        """Creates and returns a unique ID for the DIV where the application is to
        be rendered. We need to generate a unique ID because some portals already
        create a DIV with the portlet's Window ID as the DOM ID.

        @param request
                   PortletRequest
        @return the id to use in the DOM
        """
        return 'v-' + request.getWindowID()

    def writeAjaxPageHtmlVaadinScripts(self, request, response, writer, application, themeName):
        """This method writes the scripts to load the widgetset and the themes as
        well as define Vaadin configuration parameters on the HTML fragment that
        starts the actual Vaadin application.

        @param request
        @param response
        @param writer
        @param application
        @param themeName
        @throws IOException
        @throws PortletException
        """
        themeURI = self.getThemeURI(themeName, request)
        # fixed base theme to use - all portal pages with Vaadin
        # applications will load this exactly once
        portalTheme = self.getPortalProperty(self._PORTAL_PARAMETER_VAADIN_THEME, request.getPortalContext())
        writer.write('<script type=\"text/javascript\">\n')
        writer.write('if(!vaadin || !vaadin.vaadinConfigurations) {\n ' + 'if(!vaadin) { var vaadin = {}} \n' + 'vaadin.vaadinConfigurations = {};\n' + 'if (!vaadin.themesLoaded) { vaadin.themesLoaded = {}; }\n')
        if not self.isProductionMode():
            writer.write('vaadin.debug = true;\n')
        self.writeAjaxPageScriptWidgetset(request, response, writer)
        config = self.getVaadinConfigurationMap(request, response, application, themeURI)
        self.writeAjaxPageScriptConfigurations(request, response, writer, config)
        writer.write('</script>\n')
        self.writeAjaxPageHtmlTheme(request, writer, themeName, themeURI, portalTheme)
        # TODO Warn if widgetset has not been loaded after 15 seconds

    def writeAjaxPageScriptWidgetset(self, request, response, writer):
        """Writes the script to load the widgetset on the HTML fragment created by
        the portlet.

        @param request
        @param response
        @param writer
        @throws IOException
        """
        requestWidgetset = self.getApplicationOrSystemProperty(self.PARAMETER_WIDGETSET, None)
        sharedWidgetset = self.getPortalProperty(self.PORTAL_PARAMETER_VAADIN_WIDGETSET, request.getPortalContext())
        if requestWidgetset is not None:
            widgetset = requestWidgetset
        elif sharedWidgetset is not None:
            widgetset = sharedWidgetset
        else:
            widgetset = self.DEFAULT_WIDGETSET
        widgetsetURL = self.getWidgetsetURL(widgetset, request)
        writer.write('document.write(\'<iframe tabIndex=\"-1\" id=\"__gwt_historyFrame\" ' + 'style=\"position:absolute;width:0;height:0;border:0;overflow:' + 'hidden;opacity:0;top:-100px;left:-100px;\" src=\"javascript:false\"></iframe>\');\n')
        writer.write('document.write(\"<script language=\'javascript\' src=\'' + widgetsetURL + '\'><\\/script>\");\n}\n')

    def getVaadinConfigurationMap(self, request, response, application, themeURI):
        """Returns the configuration parameters to pass to the client.

        To add configuration parameters for the client, override, call the super
        method and then modify the map. Overriding this method may also require
        client side changes in {@link ApplicationConnection} and
        {@link ApplicationConfiguration}.

        Note that this method must escape and quote the values when appropriate.

        The map returned is typically a {@link LinkedHashMap} to preserve
        insertion order, but it is not guaranteed to be one.

        @param request
        @param response
        @param application
        @param themeURI
        @return modifiable Map from parameter name to its full value
        @throws PortletException
        """
        config = LinkedHashMap()
        # We need this in order to get uploads to work. TODO this is not needed
        # for uploads anymore, check if this is needed for some other things

        appUri = response.createActionURL()
        config.put('appUri', '\'' + str(appUri) + '\'')
        config.put('usePortletURLs', 'true')
        uidlUrlBase = response.createResourceURL()
        uidlUrlBase.setResourceID('UIDL')
        config.put('portletUidlURLBase', '\'' + str(uidlUrlBase) + '\'')
        config.put('pathInfo', '\'\'')
        config.put('themeUri', '\'' + themeURI + '\'')
        versionInfo = '{vaadinVersion:\"' + AbstractApplicationServlet.VERSION + '\",applicationVersion:\"' + application.getVersion() + '\"}'
        config.put('versionInfo', versionInfo)
        # Get system messages
        systemMessages = None
        # failing to get the system messages is always a problem
        try:
            systemMessages = self.getSystemMessages()
        except SystemMessageException, e:
            raise PortletException('Failed to obtain system messages!', e)
        if systemMessages is not None:
            # Write the CommunicationError -message to client
            caption = systemMessages.getCommunicationErrorCaption()
            if caption is not None:
                caption = '\"' + caption + '\"'
            message = systemMessages.getCommunicationErrorMessage()
            if message is not None:
                message = '\"' + message + '\"'
            url = systemMessages.getCommunicationErrorURL()
            if url is not None:
                url = '\"' + url + '\"'
            config.put('\"comErrMsg\"', '{' + '\"caption\":' + caption + ',' + '\"message\" : ' + message + ',' + '\"url\" : ' + url + '}')
            # Write the AuthenticationError -message to client
            caption = systemMessages.getAuthenticationErrorCaption()
            if caption is not None:
                caption = '\"' + caption + '\"'
            message = systemMessages.getAuthenticationErrorMessage()
            if message is not None:
                message = '\"' + message + '\"'
            url = systemMessages.getAuthenticationErrorURL()
            if url is not None:
                url = '\"' + url + '\"'
            config.put('\"authErrMsg\"', '{' + '\"caption\":' + caption + ',' + '\"message\" : ' + message + ',' + '\"url\" : ' + url + '}')
        return config

    def writeAjaxPageScriptConfigurations(self, request, response, writer, config):
        """Constructs the Vaadin configuration section for
        {@link ApplicationConnection} and {@link ApplicationConfiguration}.

        Typically this method should not be overridden. Instead, modify
        {@link #getVaadinConfigurationMap(RenderRequest, RenderResponse, Application, String)}
        .

        @param request
        @param response
        @param writer
        @param config
        @throws IOException
        @throws PortletException
        """
        writer.write('vaadin.vaadinConfigurations[\"' + self.getApplicationDomId(request) + '\"] = {')
        keyIt = config.keys()
        while keyIt.hasNext():
            key = keyIt.next()
            writer.write(key + ': ' + config[key])
            if keyIt.hasNext():
                writer.write(', ')
        writer.write('};\n')

    def writeAjaxPageHtmlTheme(self, request, writer, themeName, themeURI, portalTheme):
        """Writes the Vaadin theme loading section of the portlet HTML. Loads both
        the portal theme and the portlet theme in this order, skipping loading of
        themes that are already loaded (matched by name).

        @param request
        @param writer
        @param themeName
        @param themeURI
        @param portalTheme
        @throws IOException
        """
        writer.write('<script type=\"text/javascript\">\n')
        if portalTheme is None:
            portalTheme = self.DEFAULT_THEME_NAME
        writer.write('if(!vaadin.themesLoaded[\'' + portalTheme + '\']) {\n')
        writer.write('var defaultStylesheet = document.createElement(\'link\');\n')
        writer.write('defaultStylesheet.setAttribute(\'rel\', \'stylesheet\');\n')
        writer.write('defaultStylesheet.setAttribute(\'type\', \'text/css\');\n')
        writer.write('defaultStylesheet.setAttribute(\'href\', \'' + self.getThemeURI(portalTheme, request) + '/styles.css\');\n')
        writer.write('document.getElementsByTagName(\'head\')[0].appendChild(defaultStylesheet);\n')
        writer.write('vaadin.themesLoaded[\'' + portalTheme + '\'] = true;\n}\n')
        if not (portalTheme == themeName):
            writer.write('if(!vaadin.themesLoaded[\'' + themeName + '\']) {\n')
            writer.write('var stylesheet = document.createElement(\'link\');\n')
            writer.write('stylesheet.setAttribute(\'rel\', \'stylesheet\');\n')
            writer.write('stylesheet.setAttribute(\'type\', \'text/css\');\n')
            writer.write('stylesheet.setAttribute(\'href\', \'' + themeURI + '/styles.css\');\n')
            writer.write('document.getElementsByTagName(\'head\')[0].appendChild(stylesheet);\n')
            writer.write('vaadin.themesLoaded[\'' + themeName + '\'] = true;\n}\n')
        writer.write('</script>\n')

    def writeAjaxPageHtmlMainDiv(self, request, response, writer, id, classNames, divStyle):
        """Method to write the div element into which that actual Vaadin application
        is rendered.
        <p>
        Override this method if you want to add some custom html around around
        the div element into which the actual Vaadin application will be
        rendered.

        @param request
        @param response
        @param writer
        @param id
        @param classNames
        @param divStyle
        @throws IOException
        """
        writer.write('<div id=\"' + id + '\" class=\"' + classNames + '\" ' + divStyle + '>')
        writer.write('<div class=\"v-app-loading\"></div>')
        writer.write('</div>\n')
        writer.write('<noscript>' + self.getNoScriptMessage() + '</noscript>')

    def getNoScriptMessage(self):
        """Returns a message printed for browsers without scripting support or if
        browsers scripting support is disabled.
        """
        return 'You have to enable javascript in your browser to use an application built with Vaadin.'

    def getThemeForWindow(self, request, window):
        """Returns the theme for given request/window

        @param request
        @param window
        @return
        """
        # Finds theme name
        # theme defined for the window?
        themeName = window.getTheme()
        if themeName is None:
            # no, is the default theme defined by the portal?
            themeName = self.getPortalProperty(Constants.PORTAL_PARAMETER_VAADIN_THEME, request.getPortalContext())
        if themeName is None:
            # no, using the default theme defined by Vaadin
            themeName = self.DEFAULT_THEME_NAME
        return themeName

    def getApplicationClass(self):
        pass

    def getNewApplication(self, request):
        try:
            application = self.getApplicationClass()()
            return application
        except IllegalAccessException, e:
            raise PortletException('getNewApplication failed', e)
        except InstantiationException, e:
            raise PortletException('getNewApplication failed', e)
        except ClassNotFoundException, e:
            raise PortletException('getNewApplication failed', e)

    def getClassLoader(self):
        # TODO Add support for custom class loader
        return self.getClass().getClassLoader()

    def getSystemMessages(self):
        """Get system messages from the current application class

        @return
        """
        # This should never happen
        # This is completely ok and should be silently ignored
        # This should never happen
        # This should never happen
        try:
            appCls = self.getApplicationClass()
            m = appCls.getMethod('getSystemMessages', None)
            return m.invoke(None, None)
        except ClassNotFoundException, e:
            raise SystemMessageException(e)
        except SecurityException, e:
            raise SystemMessageException('Application.getSystemMessage() should be static public', e)
        except NoSuchMethodException, e:
            pass # astStmt: [Stmt([]), None]
        except IllegalArgumentException, e:
            raise SystemMessageException(e)
        except IllegalAccessException, e:
            raise SystemMessageException('Application.getSystemMessage() should be static public', e)
        except InvocationTargetException, e:
            raise SystemMessageException(e)
        return Application.getSystemMessages()

    def handleServiceException(self, request, response, application, e):
        # TODO Check that this error handler is working when running inside a
        # portlet
        # if this was an UIDL request, response UIDL back to client
        if self.getRequestType(request) == self.RequestType.UIDL:
            ci = self.getSystemMessages()
            self.criticalNotification(request, response, ci.getInternalErrorCaption(), ci.getInternalErrorMessage(), None, ci.getInternalErrorURL())
            if application is not None:
                application.getErrorHandler().terminalError(RequestError(e))
            else:
                raise PortletException(e)
        else:
            # Re-throw other exceptions
            raise PortletException(e)

    class RequestError(Terminal, ErrorEvent, Serializable):
        _throwable = None

        def __init__(self, throwable):
            self._throwable = throwable

        def getThrowable(self):
            return self._throwable

    def criticalNotification(self, request, response, caption, message, details, url):
        """Send notification to client's application. Used to notify client of
        critical errors and session expiration due to long inactivity. Server has
        no knowledge of what application client refers to.

        @param request
                   the Portlet request instance.
        @param response
                   the Portlet response to write to.
        @param caption
                   for the notification
        @param message
                   for the notification
        @param details
                   a detail message to show in addition to the passed message.
                   Currently shown directly but could be hidden behind a details
                   drop down.
        @param url
                   url to load after message, null for current page
        @throws IOException
                    if the writing failed due to input/output error.
        """
        # clients JS app is still running, but server application either
        # no longer exists or it might fail to perform reasonably.
        # send a notification to client's application and link how
        # to "restart" application.
        if caption is not None:
            caption = '\"' + caption + '\"'
        if details is not None:
            if message is None:
                message = details
            else:
                message += '<br/><br/>' + details
        if message is not None:
            message = '\"' + message + '\"'
        if url is not None:
            url = '\"' + url + '\"'
        # Set the response type
        response.setContentType('application/json; charset=UTF-8')
        out = response.getPortletOutputStream()
        outWriter = PrintWriter(BufferedWriter(OutputStreamWriter(out, 'UTF-8')))
        outWriter.print_('for(;;);[{\"changes\":[], \"meta\" : {' + '\"appError\": {' + '\"caption\":' + caption + ',' + '\"message\" : ' + message + ',' + '\"url\" : ' + url + '}}, \"resources\": {}, \"locales\":[]}]')
        outWriter.close()

    @classmethod
    def getPortalProperty(cls, name, context):
        """Returns a portal configuration property.

        Liferay is handled separately as
        {@link PortalContext#getProperty(String)} does not return portal
        properties from e.g. portal-ext.properties .

        @param name
        @param context
        @return
        """
        isLifeRay = context.getPortalInfo().toLowerCase().contains('liferay')
        # TODO test on non-LifeRay platforms
        if isLifeRay:
            value = cls.getLifeRayPortalProperty(name)
        else:
            value = context.getProperty(name)
        return value

    @classmethod
    def getLifeRayPortalProperty(cls, name):
        try:
            value = PropsUtil.get(name)
        except Exception, e:
            value = None
        return value

    @classmethod
    def getHTTPHeader(cls, request, name):
        """Try to get an HTTP header value from a request using portal specific
        APIs.

        @param name
                   HTTP header name
        @return the value of the header (empty string if defined without a value,
                null if the parameter is not present or retrieving it failed)
        """
        value = None
        portalInfo = request.getPortalContext().getPortalInfo().toLowerCase()
        if portalInfo.contains('liferay'):
            value = cls.getLiferayHTTPHeader(request, name)
        elif portalInfo.contains('gatein'):
            value = cls.getGateInHTTPHeader(request, name)
        return value

    @classmethod
    def getHTTPRequestParameter(cls, request, name):
        """Try to get the value of a HTTP request parameter from a portlet request
        using portal specific APIs. It is not possible to get the HTTP request
        parameters using the official Portlet 2.0 API.

        @param name
                   HTTP request parameter name
        @return the value of the parameter (empty string if parameter defined
                without a value, null if the parameter is not present or
                retrieving it failed)
        """
        value = request.getParameter(name)
        if value is None:
            portalInfo = request.getPortalContext().getPortalInfo().toLowerCase()
            if portalInfo.contains('liferay'):
                value = cls.getLiferayHTTPRequestParameter(request, name)
            elif portalInfo.contains('gatein'):
                value = cls.getGateInHTTPRequestParameter(request, name)
        return value

    @classmethod
    def getGateInHTTPRequestParameter(cls, request, name):
        value = None
        # do nothing - not on GateIn simple-portal
        try:
            getRealReq = request.getClass().getMethod('getRealRequest')
            origRequest = getRealReq.invoke(request)
            value = origRequest.getParameter(name)
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        return value

    @classmethod
    def getLiferayHTTPRequestParameter(cls, request, name):
        # httpRequest = PortalUtil.getHttpServletRequest(request);
        # ignore and return null - unable to get the original request
        try:
            httpRequest = PortalClassInvoker.invoke('com.liferay.portal.util.PortalUtil', 'getHttpServletRequest', request)
            # httpRequest =
            # PortalUtil.getOriginalServletRequest(httpRequest);
            httpRequest = PortalClassInvoker.invoke('com.liferay.portal.util.PortalUtil', 'getOriginalServletRequest', httpRequest)
            if httpRequest is not None:
                return httpRequest.getParameter(name)
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        return None

    @classmethod
    def getGateInHTTPHeader(cls, request, name):
        value = None
        # do nothing - not on GateIn simple-portal
        try:
            getRealReq = request.getClass().getMethod('getRealRequest')
            origRequest = getRealReq.invoke(request)
            value = origRequest.getHeader(name)
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        return value

    @classmethod
    def getLiferayHTTPHeader(cls, request, name):
        # httpRequest = PortalUtil.getHttpServletRequest(request);
        # ignore and return null - unable to get the original request
        try:
            httpRequest = PortalClassInvoker.invoke('com.liferay.portal.util.PortalUtil', 'getHttpServletRequest', request)
            # httpRequest =
            # PortalUtil.getOriginalServletRequest(httpRequest);
            httpRequest = PortalClassInvoker.invoke('com.liferay.portal.util.PortalUtil', 'getOriginalServletRequest', httpRequest)
            if httpRequest is not None:
                return httpRequest.getHeader(name)
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        return None

    def getApplicationContext(self, portletSession):
        """Gets the application context for a PortletSession. If no context is
        currently stored in a session a new context is created and stored in the
        session.

        @param portletSession
                   the portlet session.
        @return the application context for the session.
        """
        return PortletApplicationContext2.getApplicationContext(portletSession)
