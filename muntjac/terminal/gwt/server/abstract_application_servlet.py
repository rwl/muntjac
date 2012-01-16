# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
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

"""Defines a servlet that handles all communication between the client and
the server."""

import re
import logging
import mimetypes

from time import time
from warnings import warn

from urlparse import urljoin
from os.path import exists, getmtime

try:
    from StringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from muntjac.util import clsname
from muntjac.application import Application

from muntjac.terminal.gwt.server.constants import Constants
from muntjac.terminal.gwt.server.json_paint_target import JsonPaintTarget
from muntjac.terminal.gwt.server.exceptions import ServletException

from muntjac.terminal.uri_handler import IErrorEvent as URIHandlerErrorEvent
from muntjac.terminal.terminal import IErrorEvent as TerminalErrorEvent

from muntjac.terminal.gwt.server.paste_wsgi_servlet import PasteWsgiServlet

from muntjac.terminal.gwt.server.exceptions import \
    SessionExpiredException, SystemMessageException

from muntjac.terminal.gwt.client.application_connection import \
    ApplicationConnection

from muntjac.terminal.gwt.server.web_application_context import \
    WebApplicationContext

from muntjac.terminal.gwt.server.http_servlet_request_listener import \
    IHttpServletRequestListener

from muntjac.terminal.parameter_handler import \
    IErrorEvent as ParameterHandlerErrorEvent


logger = logging.getLogger(__name__)


class RequestType(object):

    FILE_UPLOAD = 'FILE_UPLOAD'
    UIDL = 'UIDL'
    OTHER = 'OTHER'
    STATIC_FILE = 'STATIC_FILE'
    APPLICATION_RESOURCE = 'APPLICATION_RESOURCE'

    _values = [FILE_UPLOAD, UIDL, OTHER, STATIC_FILE, APPLICATION_RESOURCE]

    @classmethod
    def values(cls):
        return cls._values[:]


class AbstractApplicationServlet(PasteWsgiServlet, Constants):
    """Abstract implementation of the ApplicationServlet which handles all
    communication between the client and the server.

    It is possible to extend this class to provide own functionality but in
    most cases this is unnecessary.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    #: The version number of this release. For example "6.2.0". Always in the
    #  format "major.minor.revision[.build]". The build part is optional. All of
    #  major, minor, revision must be integers.
    VERSION = None

    #: Major version number. For example 6 in 6.2.0.
    VERSION_MAJOR = None

    #: Minor version number. For example 2 in 6.2.0.
    VERSION_MINOR = None

    #: Version revision number. For example 0 in 6.2.0.
    VERSION_REVISION = None

    #: Build identifier. For example "nightly-20091123-c9963" in
    #  6.2.0.nightly-20091123-c9963.
    VERSION_BUILD = None

    #: Initialize version numbers from string replaced by build-script.
    if '1.1.0' == '@' + 'VERSION' + '@':
        VERSION = '9.9.9.INTERNAL-DEBUG-BUILD'
    else:
        VERSION = '1.1.0'

    digits = VERSION.split('.', 4)
    VERSION_MAJOR = int(digits[0])
    VERSION_MINOR = int(digits[1])
    VERSION_REVISION = int(digits[2])

    if len(digits) == 4:
        VERSION_BUILD = digits[3]
    else:
        VERSION_BUILD = ''

    #: If the attribute is present in the request, a html fragment will be
    #  written instead of a whole page.
    #
    #  It is set to "true" by the L{ApplicationPortlet} (Portlet 1.0) and
    #  read by L{AbstractApplicationServlet}.
    REQUEST_FRAGMENT = ''#clsname(ApplicationServlet) + '.fragment'

    #: This request attribute forces widgetsets to be loaded from under the
    #  specified base path; e.g shared widgetset for all portlets in a portal.
    #
    #  It is set by the L{ApplicationPortlet} (Portlet 1.0) based on
    #  L{Constants.PORTAL_PARAMETER_VAADIN_RESOURCE_PATH} and read by
    #  L{AbstractApplicationServlet}.
    REQUEST_VAADIN_STATIC_FILE_PATH = ''#clsname(ApplicationServlet) + '.widgetsetPath'

    #: This request attribute forces widgetset used; e.g for portlets that can
    #  not have different widgetsets.
    #
    #  It is set by the L{ApplicationPortlet} (Portlet 1.0) based on
    #  L{ApplicationPortlet.PORTLET_PARAMETER_WIDGETSET} and read by
    #  L{AbstractApplicationServlet}.
    REQUEST_WIDGETSET = ''#clsname(ApplicationServlet) + '.widgetset'

    #: This request attribute indicates the shared widgetset (e.g. portal-wide
    #  default widgetset).
    #
    #  It is set by the L{ApplicationPortlet} (Portlet 1.0) based on
    #  L{Constants.PORTAL_PARAMETER_VAADIN_WIDGETSET} and read by
    #  L{AbstractApplicationServlet}.
    REQUEST_SHARED_WIDGETSET = ''#clsname(ApplicationServlet) + '.sharedWidgetset'

    #: If set, do not load the default theme but assume that loading it is
    #  handled e.g. by ApplicationPortlet.
    #
    #  It is set by the L{ApplicationPortlet} (Portlet 1.0) based on
    #  L{Constants.PORTAL_PARAMETER_VAADIN_THEME} and read by
    #  L{AbstractApplicationServlet}.
    REQUEST_DEFAULT_THEME = ''#clsname(ApplicationServlet) + '.defaultThemeUri'

    #: This request attribute is used to add styles to the main element. E.g
    #  "height:500px" generates a style="height:500px" to the main element,
    #  useful from some embedding situations (e.g portlet include.)
    #
    #  It is typically set by the L{ApplicationPortlet} (Portlet 1.0) based
    #  on L{ApplicationPortlet.PORTLET_PARAMETER_STYLE} and read by
    #  L{AbstractApplicationServlet}.
    REQUEST_APPSTYLE = ''#clsname(ApplicationServlet) + '.style'

    UPLOAD_URL_PREFIX = 'APP/UPLOAD/'


    def __init__(self, productionMode=False, debug=False, widgetset=None,
                 resourceCacheTime=3600, disableXsrfProtection=False,
                 *args, **kw_args):

        super(AbstractApplicationServlet, self).__init__(*args, **kw_args)

        self._applicationProperties = dict()
        self._productionMode = False
        self._resourcePath = None
        self._resourceCacheTime = 3600
        self._firstTransaction = True

        self._applicationProperties[
                self.SERVLET_PARAMETER_PRODUCTION_MODE] = \
                        'true' if productionMode else 'false'

        self._applicationProperties[self.SERVLET_PARAMETER_DEBUG] = \
                'true' if debug else 'false'

        self._applicationProperties[self.PARAMETER_WIDGETSET] = \
                self.DEFAULT_WIDGETSET if widgetset is None else widgetset

        self._applicationProperties[
                self.SERVLET_PARAMETER_RESOURCE_CACHE_TIME] = \
                        str(resourceCacheTime)

        self._applicationProperties[
                self.SERVLET_PARAMETER_DISABLE_XSRF_PROTECTION] = \
                        'true' if disableXsrfProtection else 'false'


    def init(self):
        """Called by the servlet container to indicate to a servlet that the
        servlet is being placed into service.
        """
        # Stores the application parameters into Properties object
        #self._applicationProperties = dict()
        #for name in CONFIG:
        #    self._applicationProperties[name] = CONFIG[name]

        ## Overrides with server.xml parameters
        #context = servletConfig.getServletContext()
        #for name in context.getInitParameterNames():
        #    self._applicationProperties[name] = context.getInitParameter(name)

        if self._firstTransaction:
            self._firstTransaction = False
            self.checkProductionMode()
            self.checkCrossSiteProtection()
            self.checkResourceCacheTime()


    def checkCrossSiteProtection(self):
        if self.getApplicationOrSystemProperty(
                self.SERVLET_PARAMETER_DISABLE_XSRF_PROTECTION,
                'false') == 'true':
            # Print an information/warning message about running with xsrf
            # protection disabled
            logger.warning(self.WARNING_XSRF_PROTECTION_DISABLED)


    def checkWidgetsetVersion(self, request):
        """Checks that the version reported by the client (widgetset) matches
        that of the server.
        """
        if not (self.VERSION == self.getParameter(request, 'wsver', '')):
#            logger.warning(self.WIDGETSET_MISMATCH_INFO %
#                    (self.VERSION, self.getParameter(request, 'wsver', '')))
            pass  # FIXME: implement Python client side


    def checkProductionMode(self):
        """Check if the application is in production mode."""
        # We are in production mode if debug=false or productionMode=true
        if self.getApplicationOrSystemProperty(
                self.SERVLET_PARAMETER_DEBUG,
                'true') == 'false':
            # "dDebug=true" is the old way and should no longer be used
            self._productionMode = True
        elif self.getApplicationOrSystemProperty(
                self.SERVLET_PARAMETER_PRODUCTION_MODE,
                'false') == 'true':
            # "productionMode=true" is the real way to do it
            self._productionMode = True

        if not self._productionMode:
            # Print an information/warning message about running in debug mode
            logger.warning(self.NOT_PRODUCTION_MODE_INFO)


    def checkResourceCacheTime(self):
        # Check if the browser caching time has been set in INI
        # Default is 1h
        try:
            rct = self.getApplicationOrSystemProperty(
                    self.SERVLET_PARAMETER_RESOURCE_CACHE_TIME, '3600')
            self._resourceCacheTime = int(rct)
        except ValueError:
            self._resourceCacheTime = 3600
            logger.warning(self.WARNING_RESOURCE_CACHING_TIME_NOT_NUMERIC)


    def getApplicationProperty(self, parameterName):
        """Gets an application property value.

        @param parameterName:
                   the Name or the parameter.
        @return: String value or C{None} if not found
        """
        val = self._applicationProperties.get(parameterName)
        if val is not None:
            return val

        # Try lower case application properties for backward compatibility
        val = self._applicationProperties.get(parameterName.lower())
        return val


    def getSystemProperty(self, parameterName):
        """Gets an system property value.

        @param parameterName:
                   the Name or the parameter.
        @return: String value or C{None} if not found
        """
        raise NotImplementedError


    def getApplicationOrSystemProperty(self, parameterName, defaultValue):
        """Gets an application or system property value.

        @param parameterName:
                   the Name or the parameter.
        @param defaultValue:
                   the Default to be used.
        @return: String value or default if not found
        """
        # Try application properties
        val = self.getApplicationProperty(parameterName)
        if val is not None:
            return val

        # Try system properties
        #val = self.getSystemProperty(parameterName)
        #if val is not None:
        #    return val

        return defaultValue


    def isProductionMode(self):
        """Returns true if the servlet is running in production mode.
        Production mode disables all debug facilities.

        @return: true if in production mode, false if in debug mode
        """
        return self._productionMode


    def getResourceCacheTime(self):
        """Returns the amount of milliseconds the browser should cache a file.
        Default is 1 hour (3600 ms).

        @return: The amount of milliseconds files are cached in the browser
        """
        return self._resourceCacheTime


    def service(self, request, response):
        """Receives standard HTTP requests from the public service method and
        dispatches them.
        """
        requestType = self.getRequestType(request)
        if not self.ensureCookiesEnabled(requestType, request, response):
            return

        if requestType == RequestType.STATIC_FILE:
            self.serveStaticResources(request, response)
            return

        if self.isRepaintAll(request):
            # warn if versions do not match
            self.checkWidgetsetVersion(request)

        application = None
        transactionStarted = False
        requestStarted = False

        try:
            # If a duplicate "close application" URL is received for an
            # application that is not open, redirect to the application's main
            # page.
            # This is needed as e.g. Spring Security remembers the last
            # URL from the application, which is the logout URL, and repeats
            # it.
            # We can tell apart a real onunload request from a repeated one
            # based on the real one having content (at least the UIDL security
            # key).
            if (requestType == RequestType.UIDL
                    and ApplicationConnection.PARAM_UNLOADBURST
                        in self.getParameters(request)
                    and self.getContentLength(request) < 1
                    and self.getExistingApplication(request, False) is None):
                self.redirectToApplication(request, response)
                return

            # Find out which application this request is related to
            application = self.findApplicationInstance(request, requestType)
            if application is None:
                return

            # Get or create a WebApplicationContext and an ApplicationManager
            # for the session
            webApplicationContext = \
                    self.getApplicationContext(self.getSession(request))
            applicationManager = \
                    webApplicationContext.getApplicationManager(
                            application, self)

            # Update browser information from the request
            self.updateBrowserProperties(
                    webApplicationContext.getBrowser(), request)

            # Call application requestStart before Application.init()
            # (bypasses the limitation in TransactionListener)
            if isinstance(application, IHttpServletRequestListener):
                application.onRequestStart(request, response)
                requestStarted = True

            # Start the newly created application
            self.startApplication(request, application, webApplicationContext)

            # Transaction starts. Call transaction listeners. Transaction end
            # is called in the finally block below.
            webApplicationContext.startTransaction(application, request)
            transactionStarted = True

            # Handle the request
            if requestType == RequestType.FILE_UPLOAD:
                applicationManager.handleFileUpload(request, response, self)
                return
            elif requestType == RequestType.UIDL:
                # Handles AJAX UIDL requests
                window = applicationManager.getApplicationWindow(request,
                        self, application, None)
                applicationManager.handleUidlRequest(request, response,
                        self, window)
                return

            # Removes application if it has stopped (mayby by thread or
            # transactionlistener)
            if not application.isRunning():
                self.endApplication(request, response, application)
                return

            # Finds the window within the application
            window = self.getApplicationWindow(request, applicationManager,
                    application)
            if window is None:
                raise ServletException(self.ERROR_NO_WINDOW_FOUND)

            # Sets terminal type for the window, if not already set
            if window.getTerminal() is None:
                window.setTerminal(webApplicationContext.getBrowser())

            # Handle parameters
            parameters = request.fields()
            if window is not None and parameters is not None:
                window.handleParameters(parameters)

            # Call the URI handlers and if this turns out to be a download
            # request, send the file to the client
            if self.handleURI(applicationManager, window, request, response):
                return

            # Send initial AJAX page that kickstarts a Muntjac application
            self.writeAjaxPage(request, response, window, application)

        except SessionExpiredException, e:
            # Session has expired, notify user
            self.handleServiceSessionExpired(request, response)
        #except GeneralSecurityException, e:
        #    self._handleServiceSecurityException(request, response)
#        except Exception, e:
#            self.handleServiceException(request, response, application, e)
        finally:
            # Notifies transaction end
            try:
                if transactionStarted:
                    application.getContext().endTransaction(application,
                            request)
            finally:
                if requestStarted:
                    application.onRequestEnd(request, response)


    def ensureCookiesEnabled(self, requestType, request, response):
        """Check that cookie support is enabled in the browser. Only checks
        UIDL requests.

        @param requestType:
                   Type of the request as returned by L{getRequestType}
        @param request:
                   The request from the browser
        @param response:
                   The response to which an error can be written
        @return: false if cookies are disabled, true otherwise
        @raise IOException:
        """
        if requestType == RequestType.UIDL and not self.isRepaintAll(request):
            # In all other but the first UIDL request a cookie should be
            # returned by the browser.
            # This can be removed if cookieless mode (#3228) is supported
            if self.getSessionId(request) is None:
                # User has cookies disabled
                self.criticalNotification(request, response,
                        self.getSystemMessages().getCookiesDisabledCaption(),
                        self.getSystemMessages().getCookiesDisabledMessage(),
                        None,
                        self.getSystemMessages().getCookiesDisabledURL())
                return False

        return True


    def updateBrowserProperties(self, browser, request):
        # request based details updated always
        browser.updateRequestDetails(self.getLocale(request),
                self.getHeader(request, 'REMOTE_ADDR'),
                self.isSecure(request),
                self.getUserAgent(request))

        if request.field('repaintAll', None) is not None:
            browser.updateClientSideDetails(
                    self.getParameter(request, 'sw', None),
                    self.getParameter(request, 'sh', None),
                    self.getParameter(request, 'tzo', None),
                    self.getParameter(request, 'rtzo', None),
                    self.getParameter(request, 'dstd', None),
                    self.getParameter(request, 'dston', None),
                    self.getParameter(request, 'curdate', None),
                    self.getParameter(request, 'td', None) is not None)


    def criticalNotification(self, request, response, caption, message,
                             details, url):
        """Send a notification to client's application. Used to notify
        client of critical errors, session expiration and more. Server
        has no knowledge of what application client refers to.

        @param request:
                   the HTTP request instance.
        @param response:
                   the HTTP response to write to.
        @param caption:
                   the notification caption
        @param message:
                   to notification body
        @param details:
                   a detail message to show in addition to the message.
                   Currently shown directly below the message but could be
                   hidden behind a details drop down in the future. Mainly
                   used to give additional information not necessarily
                   useful to the end user.
        @param url:
                   url to load when the message is dismissed. Null will
                   reload the current page.
        @raise IOException:
                    if the writing failed due to input/output error.
        """
        if self.isUIDLRequest(request):

            if caption is not None:
                caption = '\"' + JsonPaintTarget.escapeJSON(caption) + '\"'

            if details is not None:
                if message is None:
                    message = details
                else:
                    message += '<br/><br/>' + details

            if message is not None:
                message = '\"' + JsonPaintTarget.escapeJSON(message) + '\"'
            else:
                message = 'null'

            if url is not None:
                url = '\"' + JsonPaintTarget.escapeJSON(url) + '\"'
            else:
                url = 'null'

            output = ('for(;;);[{\"changes\":[], \"meta\" : {'
                '\"appError\": {' + '\"caption\":' + caption + ','
                '\"message\" : ' + message + ',' + '\"url\" : ' + url +
                '}}, \"resources\": {}, \"locales\":[]}]')

            self.writeResponse(
                    response, 'application/json; charset=UTF-8', output)
        else:
            # Create an HTML response with the error
            output = ''

            if url is not None:
                output += '<a href=\"' + url + '\">'

            if caption is not None:
                output += '<b>' + caption + '</b><br/>'

            if message is not None:
                output += message
                output += '<br/><br/>'

            if details is not None:
                output += details
                output += '<br/><br/>'

            if url is not None:
                output += '</a>'

            self.writeResponse(response, 'text/html; charset=UTF-8', output)


    def writeResponse(self, response, contentType, output):
        """Writes the response in C{output} using the contentType given
        in C{contentType} to the provided L{HttpServletResponse}

        @param response:
        @param contentType:
        @param output:
                   Output to write (UTF-8 encoded)
        @raise IOException:
        """
        self.setHeader(response, 'Content-Type', contentType)
        self.write(response, output)


    def findApplicationInstance(self, request, requestType):
        """Returns the application instance to be used for the request. If
        an existing instance is not found a new one is created or null is
        returned to indicate that the application is not available.

        @raise ServletException:
        @raise SessionExpiredException:
        """
        requestCanCreateApplication = \
                self.requestCanCreateApplication(request, requestType)

        # Find an existing application for this request.
        application = self.getExistingApplication(request,
                requestCanCreateApplication)

        if application is not None:
            # There is an existing application. We can use this as long as the
            # user not specifically requested to close or restart it.
            restartApplication = self.getParameter(request,
                    self.URL_PARAMETER_RESTART_APPLICATION, None) is not None

            closeApplication = self.getParameter(request,
                    self.URL_PARAMETER_CLOSE_APPLICATION, None) is not None

            if restartApplication:
                session = self.getSession(request, False)
                self.closeApplication(application, session)
                return self.createApplication(request)

            elif closeApplication:
                session = self.getSession(request, False)
                self.closeApplication(application, session)
                return None

            else:
                return application

        # No existing application was found
        if requestCanCreateApplication:
            # If the request is such that it should create a new application
            # if one as not found, we do that.
            return self.createApplication(request)

        else:
            # The application was not found and a new one should not be
            # created. Assume the session has expired.
            raise SessionExpiredException()


    def requestCanCreateApplication(self, request, requestType):
        """Check if the request should create an application if an existing
        application is not found.

        @return: true if an application should be created, false otherwise
        """
        if (requestType == RequestType.UIDL) and self.isRepaintAll(request):
            # UIDL request contains valid repaintAll=1 event, the user
            # probably wants to initiate a new application through a custom
            # index.html without using writeAjaxPage.
            return True

        elif requestType == RequestType.OTHER:
            # I.e URIs that are not application resources or static (theme)
            # files.
            return True

        return False


    def handleDownload(self, stream, request, response):
        """Handles the requested URI. An application can add handlers to do
        special processing, when a certain URI is requested. The handlers
        are invoked before any windows URIs are processed and if a
        DownloadStream is returned it is sent to the client.

        @param stream:
                   the download stream.
        @param request:
                   the HTTP request instance.
        @param response:
                   the HTTP response to write to.
        @raise IOException:

        @see: L{URIHandler}
        """
        if stream.getParameter('Location') is not None:
            self.setStatus(response, 302, 'Found')
            self.setHeader(response, 'Location',
                    stream.getParameter('Location'))
            return

        # Download from given stream
        data = stream.getStream()
        if data is not None:
            # Sets content type
            self.setHeader(response, 'Content-Type', stream.getContentType())

            # Sets cache headers
            cacheTime = stream.getCacheTime()
            if cacheTime <= 0:
                self.setHeader(response, 'Cache-Control', 'no-cache')
                self.setHeader(response, 'Pragma', 'no-cache')
                self.setHeader(response, 'Expires', '0')
            else:
                self.setHeader(response, 'Cache-Control',
                        'max-age=' + str(cacheTime / 1000))
                self.setHeader(response, 'Expires',
                        str(1000 * time.time() + cacheTime))
                # Required to apply caching in some Tomcats
                self.setHeader(response, 'Pragma', 'cache')

            # Copy download stream parameters directly
            # to HTTP headers.
            names = stream.getParameterNames()
            if names is not None:
                for param in names:
                    self.setHeader(response, param, stream.getParameter(param))

            # suggest local filename from DownloadStream if
            # Content-Disposition not explicitly set
            contentDispositionValue = \
                    stream.getParameter('Content-Disposition')
            if contentDispositionValue is None:
                contentDispositionValue = ('filename=\"'
                        + stream.getFileName() + '\"')
                self.setHeader(response, 'Content-Disposition',
                        contentDispositionValue)

            self.write(response, data.getvalue())
            data.close()


    def createApplication(self, request):
        """Creates a new application and registers it into
        WebApplicationContext (aka session). This is not meant to be
        overridden. Override getNewApplication to create the application
        instance in a custom way.

        @raise ServletException:
        @raise MalformedURLException:
        """
        newApplication = self.getNewApplication(request)

        context = self.getApplicationContext(self.getSession(request))
        context.addApplication(newApplication)

        return newApplication


    def handleServiceException(self, request, response, application, e):
        # if this was an UIDL request, response UIDL back to client
        if self.getRequestType(request) == RequestType.UIDL:
            ci = self.getSystemMessages()

            self.criticalNotification(request, response,
                    ci.getInternalErrorCaption(),
                    ci.getInternalErrorMessage(),
                    None, ci.getInternalErrorURL())

            if application is not None:
                application.getErrorHandler().terminalError(RequestError(e))
            else:
                raise ServletException(e)
        else:
            # Re-throw other exceptions
            raise ServletException, str(e)


    def getThemeForWindow(self, request, window):
        """Returns the theme for given request/window
        """
        # Finds theme name
        if self.getParameter(request, self.URL_PARAMETER_THEME,
                None) is not None:
            themeName = self.getParameter(request, self.URL_PARAMETER_THEME)
        else:
            themeName = window.getTheme()

        if themeName is None:
            # no explicit theme for window defined
            if self.getParameter(request, self.REQUEST_DEFAULT_THEME,
                    None) is not None:
                # the default theme is defined in request (by portal)
                themeName = self.getParameter(request,
                        self.REQUEST_DEFAULT_THEME)
            else:
                # using the default theme defined by Muntjac
                themeName = self.getDefaultTheme()

        # XSS prevention, theme names shouldn't contain special chars anyway.
        # The servlet denies them via url parameter.
        themeName = self.stripSpecialChars(themeName)

        return themeName


    @classmethod
    def stripSpecialChars(cls, themeName):
        """A helper method to strip away characters that might somehow be
        used for XSS attacks. Leaves at least alphanumeric characters intact.
        Also removes eg. ( and ), so values should be safe in javascript too.
        """
        sb = StringIO()
        for c in themeName:
            if c not in cls._CHAR_BLACKLIST:
                sb.write(c)
        result = sb.getvalue()
        sb.close()
        return result


    _CHAR_BLACKLIST = ['&', '"', '\'', '<', '>', '(', ')', ';']


    @classmethod
    def getDefaultTheme(cls):
        """Returns the default theme. Must never return C{None}.
        """
        return cls.DEFAULT_THEME_NAME


    def handleURI(self, applicationManager, window, request, response):
        """Calls URI handlers for the request. If an URI handler returns a
        DownloadStream the stream is passed to the client for downloading.

        @return: true if an DownloadStream was sent to the client
        @raise IOException
        """
        # Handles the URI
        download = applicationManager.handleURI(window, request, response,
                self)

        # A download request
        if download is not None:
            # Client downloads an resource
            self.handleDownload(download, request, response)
            return True

        return False


    def handleServiceSessionExpired(self, request, response):
        if self.isOnUnloadRequest(request):
            # Request was an unload request (e.g. window close event) and
            # the client expects no response if it fails.
            return

        try:
            ci = self.getSystemMessages()
            if self.getRequestType(request) != RequestType.UIDL:
                # 'plain' http req - e.g. browser reload;
                # just go ahead redirect the browser
                response.sendRedirect(ci.getSessionExpiredURL())
            else:
                # Invalidate session (weird to have session if we're saying
                # that it's expired, and worse: portal integration will fail
                # since the session is not created by the portal.
                #
                # Session must be invalidated before criticalNotification
                # as it commits the response.
                self.invalidateSession(request)

                # send uidl redirect
                self.criticalNotification(request, response,
                        ci.getSessionExpiredCaption(),
                        ci.getSessionExpiredMessage(),
                        None, ci.getSessionExpiredURL())
        except SystemMessageException, ee:
            raise ServletException(ee)


    def handleServiceSecurityException(self, request, response):
        if self.isOnUnloadRequest(request):
            # Request was an unload request (e.g. window close event) and the
            # client expects no response if it fails.
            return

        try:
            ci = self.getSystemMessages()
            if self.getRequestType(request) != RequestType.UIDL:
                # 'plain' http req - e.g. browser reload;
                # just go ahead redirect the browser
                self.redirect(response, ci.getCommunicationErrorURL())
            else:
                # send uidl redirect
                self.criticalNotification(request, response,
                        ci.getCommunicationErrorCaption(),
                        ci.getCommunicationErrorMessage(),
                        self.INVALID_SECURITY_KEY_MSG,
                        ci.getCommunicationErrorURL())
                # Invalidate session. Portal integration will fail otherwise
                # since the session is not created by the portal.
                self.invalidateSession(request)
        except SystemMessageException, ee:
            raise ServletException(ee)

        logger.error('Invalid security key received from '
                     + request.getRemoteHost())


    def getNewApplication(self, request):
        """Creates a new application for the given request.

        @param request:
                   the HTTP request.
        @return: A new Application instance.
        @raise ServletException:
        """
        raise NotImplementedError


    def startApplication(self, request, application, webApplicationContext):
        """Starts the application if it is not already running.

        @raise ServletException:
        @raise MalformedURLException:
        """
        if not application.isRunning():
            # Create application
            applicationUrl = self.getApplicationUrl(request)

            # Initial locale comes from the request
            lc = self.getLocale(request)
            application.setLocale(lc)
            application.start(applicationUrl, self._applicationProperties,
                    webApplicationContext)


    def serveStaticResources(self, request, response):
        """Check if this is a request for a static resource and, if it is,
        serve the resource to the client.

        @return: true if a file was served and the request has been handled,
                 false otherwise.
        @raise IOException:
        @raise ServletException:
        """
        pathInfo = self.getPathInfo(request)
        # FIXME: What does 10 refer to?
        if (pathInfo is None) or (len(pathInfo) <= 10):
            return False

        contextPath = self.getContextPath(request)
        if (contextPath is not None
                and self.getRequestUri(request).startswith('/VAADIN/')):

            self.serveStaticResourcesInVAADIN(self.getRequestUri(request),
                    request, response)
            return True

        elif self.getRequestUri(request).startswith(contextPath + '/VAADIN/'):

            self.serveStaticResourcesInVAADIN(
                    self.getRequestUri(request)[len(contextPath):],
                    request, response)
            return True

        return False


    def serveStaticResourcesInVAADIN(self, filename, request, response):
        """Serve resources from VAADIN directory.

        @param filename:
                   The filename to serve. Should always start with /VAADIN/.
        @param request:
        @param response:
        @raise IOException:
        @raise ServletException:
        """
        #sc = self.getServletContext()  # FIXME: ServletContext
        resourceUrl = self.getResource(filename)

        if not exists(resourceUrl):
            # cannot serve requested file
            msg = 'Requested resource [' + filename + '] not found'
            logger.info(msg)
            self.setStatus(response, 404, msg)
            return

        # security check: do not permit navigation out of the VAADIN
        # directory
        if not self.isAllowedVAADINResourceUrl(request, resourceUrl):
            msg = ('Requested resource [%s] not accessible in the VAADIN '
                   'directory or access to it is forbidden.' % filename)
            logger.info(msg)
            self.setStatus(response, 403, msg)
            return

        # Find the modification timestamp
        lastModifiedTime = 0
        try:
            lastModifiedTime = int(getmtime(resourceUrl) * 1000)
            # Remove milliseconds to avoid comparison problems (milliseconds
            # are not returned by the browser in the "If-Modified-Since"
            # header).
            lastModifiedTime = lastModifiedTime - (lastModifiedTime % 1000)

            if self.browserHasNewestVersion(request, lastModifiedTime):
                self.setStatus(response, 304, 'Not Modified')
                return
        except Exception:
            # Failed to find out last modified timestamp. Continue without it.
            # Set type mime type if we can determine it based on the filename
            logger.info('Failed to find out last modified timestamp. '
                        + 'Continuing without it.')

        mimetype, _ = mimetypes.guess_type(filename)
        if mimetype is not None:
            self.setHeader(response, 'Content-Type', mimetype)

        # Provide modification timestamp to the browser if it is known.
        if lastModifiedTime > 0:
            self.setHeader(response, 'Last-Modified', str(lastModifiedTime))

            # The browser is allowed to cache for 1 hour without checking if
            # the file has changed. This forces browsers to fetch a new version
            # when the Muntjac version is updated. This will cause more requests
            # to the servlet than without this but for high volume sites the
            # static files should never be served through the servlet. The
            # cache timeout can be configured by setting the resourceCacheTime
            # parameter in web.xml
            self.setHeader(response, 'Cache-Control', 'max-age: '
                               + str(self._resourceCacheTime))

        # Write the resource to the client.
        fd = open(resourceUrl, 'rb')
        self.write(response, fd.read())
        fd.close()


    def isAllowedVAADINResourceUrl(self, request, resourceUrl):
        """Check whether a URL obtained from a classloader refers to a valid
        static resource in the directory VAADIN.

        Warning: Overriding of this method is not recommended, but is possible
        to support non-default classloaders or servers that may produce URLs
        different from the normal ones. The method prototype may change in the
        future. Care should be taken not to expose class files or other
        resources outside the VAADIN directory if the method is overridden.
        """
        # Check that the URL is in a VAADIN directory and does not contain
        # "/../"
        if ("/VAADIN/" not in self.getUrlPath(resourceUrl)
                or "/../" in self.getUrlPath(resourceUrl)):
            logger.info("Blocked attempt to access file: " + resourceUrl)
            return False

        #logger.info("Accepted access to a file using a class loader: "
        #        + resourceUrl)
        return True


    def browserHasNewestVersion(self, request, resourceLastModifiedTimestamp):
        """Checks if the browser has an up to date cached version of
        requested resource. Currently the check is performed using the
        "If-Modified-Since" header. Could be expanded if needed.

        @param request:
                   The HttpServletRequest from the browser.
        @param resourceLastModifiedTimestamp:
                   The timestamp when the resource was last modified. 0 if
                   the last modification time is unknown.
        @return: true if the If-Modified-Since header tells the cached version
                    in the browser is up to date, false otherwise
        """
        if resourceLastModifiedTimestamp < 1:
            # We do not know when it was modified so the browser cannot have
            # an up-to-date version
            return False

        # The browser can request the resource conditionally using an
        # If-Modified-Since header. Check this against the last modification
        # time.
        try:
            # If-Modified-Since represents the timestamp of the version cached
            # in the browser
            headerIfModifiedSince = self.getIfModifiedSince(request)
            if headerIfModifiedSince >= resourceLastModifiedTimestamp:
                # Browser has this an up-to-date version of the resource
                return True
        except Exception:
            # Failed to parse header. Fail silently - the browser does not
            # have an up-to-date version in its cache.
            pass

        return False


    def getRequestType(self, request):
        if self.isFileUploadRequest(request):
            return RequestType.FILE_UPLOAD

        elif self.isUIDLRequest(request):
            return RequestType.UIDL

        elif self.isStaticResourceRequest(request):
            return RequestType.STATIC_FILE

        elif self.isApplicationRequest(request):
            return RequestType.APPLICATION_RESOURCE

        elif self.getParameter(request, 'FileId', None) is not None:  # FIXME: getHeader
            return RequestType.FILE_UPLOAD

        return RequestType.OTHER


    def isApplicationRequest(self, request):
        path = self.getRequestPathInfo(request)

        if (path is not None) and path.startswith('/APP/'):
            return True

        return False


    def isStaticResourceRequest(self, request):
        pathInfo = self.getPathInfo(request)

        if (pathInfo is None) or (len(pathInfo) <= 10):
            return False

        contextPath = self.getContextPath(request)
        if ((contextPath is not None)
                and self.getRequestUri(request).startswith('/VAADIN/')):
            return True

        elif self.getRequestUri(request).startswith(contextPath + '/VAADIN/'):
            return True

        return False


    def isUIDLRequest(self, request):
        pathInfo = self.getRequestPathInfo(request)

        if pathInfo is None:
            return False

        compare = self.AJAX_UIDL_URI

        if pathInfo.startswith(compare + '/') or pathInfo.endswith(compare):
            return True

        return False


    def isFileUploadRequest(self, request):
        pathInfo = self.getRequestPathInfo(request)

        if pathInfo is None:
            return False

        if pathInfo.startswith('/' + self.UPLOAD_URL_PREFIX):
            return True

        return False


    def isOnUnloadRequest(self, request):
        param = ApplicationConnection.PARAM_UNLOADBURST
        return self.getParameter(request, param, None) is not None


    def getSystemMessages(self):
        """Get system messages from the current application class
        """
        try:
            appCls = self.getApplicationClass()
            return appCls.getSystemMessages()
        except AttributeError:
            raise SystemMessageException(
                    'Application.getSystemMessage() should be callable')

        return Application.getSystemMessages()


    def getApplicationClass(self):
        raise NotImplementedError


    def getStaticFilesLocation(self, request):
        """Return the URL from where static files, e.g. the widgetset and
        the theme, are served. In a standard configuration the VAADIN folder
        inside the returned folder is what is used for widgetsets and themes.

        The returned folder is usually the same as the context path and
        independent of the application.

        @return: The location of static resources (should contain the VAADIN
                directory). Never ends with a slash (/).
        """
        # request may have an attribute explicitly telling location (portal
        # case)
        param = self.REQUEST_VAADIN_STATIC_FILE_PATH
        staticFileLocation = self.getParameter(request, param)

        if staticFileLocation is not None:
            # TODO remove trailing slash if any?
            return staticFileLocation

        return self.getWebApplicationsStaticFileLocation(request)


    def getWebApplicationsStaticFileLocation(self, request):
        """The default method to fetch static files location (URL). This
        method does not check for request attribute
        C{REQUEST_VAADIN_STATIC_FILE_PATH}.
        """
        # if property is defined in configurations, use that
        staticFileLocation = self.getApplicationOrSystemProperty(
                self.PARAMETER_VAADIN_RESOURCES, None)

        if staticFileLocation is not None:
            return staticFileLocation

        # the last (but most common) option is to generate default location
        # from request

        # if context is specified add it to widgetsetUrl
        ctxPath = self.getContextPath(request)

        # FIXME: ctxPath.length() == 0 condition is probably unnecessary and
        # might even be wrong.
        if ((len(ctxPath) == 0)
                and (self.originalContextPath(request) is not None)):
            # include request (e.g portlet), get context path from
            # attribute
            ctxPath = self.originalContextPath(request)

        # Remove heading and trailing slashes from the context path
        ctxPath = self.removeHeadingOrTrailing(ctxPath, '/')

        if ctxPath == '':
            return ''
        else:
            return '/' + ctxPath


    @classmethod
    def removeHeadingOrTrailing(cls, string, what):
        """Remove any heading or trailing "what" from the "string".
        """
        while string.startswith(what):
            string = string[1:]

        while string.endswith(what):
            string = string[:-1]

        return string


    def redirectToApplication(self, request, response):
        """Write a redirect response to the main page of the application.

        @raise IOException:
                    if sending the redirect fails due to an input/output
                    error or a bad application URL
        """
        applicationUrl = self.getApplicationUrl(request)
        self.sendRedirect(response, applicationUrl)  # encodeRedirectURL


    def writeAjaxPage(self, request, response, window, application):
        """This method writes the html host page (aka kickstart page) that
        starts the actual Muntjac application.

        If one needs to override parts of the host page, it is suggested
        that one overrides on of several submethods which are called by
        this method:

          - L{setAjaxPageHeaders}
          - L{writeAjaxPageHtmlHeadStart}
          - L{writeAjaxPageHtmlHeader}
          - L{writeAjaxPageHtmlBodyStart}
          - L{writeAjaxPageHtmlMuntjacScripts}
          - L{writeAjaxPageHtmlMainDiv}
          - L{writeAjaxPageHtmlBodyEnd}

        @param request:
                   the HTTP request.
        @param response:
                   the HTTP response to write to.
        @param window:
        @param application:
        @raise IOException:
                    if the writing failed due to input/output error.
        @raise MalformedURLException:
                    if the application is denied access the persistent data
                    store represented by the given URL.
        """
        # e.g portlets only want a html fragment
        fragment = self.getParameter(request, self.REQUEST_FRAGMENT,
                None) is not None

        if fragment:
            # if this is a fragment request, the actual application is put to
            # request so ApplicationPortlet can save it for a later use
            self.setParameter(request, clsname(Application), application)

        page = StringIO()

        if window.getCaption() is None:
            title = 'Muntjac 6'
        else:
            title = window.getCaption()

        # Fetch relative url to application
        # don't use server and port in uri. It may cause problems with some
        # virtual server configurations which lose the server name
        appUrl = self.getUrlPath( self.getApplicationUrl(request) )
        if appUrl.endswith('/'):
            appUrl = appUrl[:-1]

        themeName = self.getThemeForWindow(request, window)

        themeUri = self.getThemeUri(themeName, request)

        if not fragment:
            self.setAjaxPageHeaders(response)
            self.writeAjaxPageHtmlHeadStart(page, request)
            self.writeAjaxPageHtmlHeader(page, title, themeUri, request)
            self.writeAjaxPageHtmlBodyStart(page, request)

        appId = appUrl
        if '' == appUrl:
            appId = 'ROOT'

        appId = re.sub('[^a-zA-Z0-9]', '', appId)

        # Add hashCode to the end, so that it is still (sort of) predictable,
        # but indicates that it should not be used in CSS and such:
        hashCode = hash(appId)
        if hashCode < 0:
            hashCode = -hashCode

        appId = appId + '-' + str(hashCode)

        self.writeAjaxPageHtmlMuntjacScripts(window, themeName, application,
                page, appUrl, themeUri, appId, request)

        # - Add classnames;
        #      .v-app
        #      .v-app-loading
        #      .v-app-<simpleName for app class>
        #      .v-theme-<themeName, remove non-alphanum>

        appClass = 'v-app-' + self.getApplicationCSSClassName()

        themeClass = ''
        if themeName is not None:
            themeClass = 'v-theme-' + re.sub('[^a-zA-Z0-9]', '', themeName)
        else:
            themeClass = ('v-theme-'
                    + re.sub('[^a-zA-Z0-9]', '', self.getDefaultTheme()))

        classNames = 'v-app ' + themeClass + ' ' + appClass

        divStyle = None
        if self.getParameter(request, self.REQUEST_APPSTYLE, None) is not None:
            divStyle = ('style=\"'
                    + self.getParameter(request, self.REQUEST_APPSTYLE) + '\"')

        self.writeAjaxPageHtmlMainDiv(page, appId, classNames, divStyle,
                request)

        if not fragment:
            page.write('</body>\n</html>\n')

        self.write(response, page.getvalue())
        page.close()


    def getApplicationCSSClassName(self):
        """Returns the application class identifier for use in the
        application CSS class name in the root DIV. The application
        CSS class name is of form "v-app-"+getApplicationCSSClassName().

        This method should normally not be overridden.

        @return: The CSS class name to use in combination with "v-app-".
        """
        try:
            return self.getApplicationClass().__name__
        except Exception, e:  # ClassNotFoundException
            logger.warning('getApplicationCSSClassName failed')
            return 'unknown'


    def getThemeUri(self, themeName, request):
        """Get the URI for the application theme.

        A portal-wide default theme is fetched from the portal shared
        resource directory (if any), other themes from the portlet.
        """
        if themeName == self.getParameter(request, self.REQUEST_DEFAULT_THEME,
                None):
            # our window theme is the portal wide default theme, make it load
            # from portals directory is defined
            staticFilePath = self.getStaticFilesLocation(request)
        else:
            # theme is a custom theme, which is not necessarily located in
            # portals VAADIN directory. Let the default servlet conf decide
            # (omitting request parameter) the location. Note that theme can
            # still be placed to portal directory with servlet parameter.

            staticFilePath = self.getWebApplicationsStaticFileLocation(request)

        return staticFilePath + '/' + self.THEME_DIRECTORY_PATH + themeName


    def writeAjaxPageHtmlMainDiv(self, page, appId, classNames, divStyle,
            request):
        """Method to write the div element into which that actual Muntjac
        application is rendered.

        Override this method if you want to add some custom html around around
        the div element into which the actual Muntjac application will be
        rendered.

        @raise IOException:
        """
        page.write('<div id=\"' + appId + '\" class=\"' + classNames + '\" ' \
                + (divStyle if divStyle is not None else '') + '>')
        page.write('<div class=\"v-app-loading\"></div>')
        page.write('</div>\n')
        page.write('<noscript>' + self.getNoScriptMessage() + '</noscript>')


    def writeAjaxPageHtmlMuntjacScripts(self, window, themeName, application,
                page, appUrl, themeUri, appId, request):
        """Method to write the script part of the page which loads needed
        Muntjac scripts and themes.

        Override this method if you want to add some custom html around
        scripts.

        @raise ServletException:
        @raise IOException:
        """
        # request widgetset takes precedence (e.g portlet include)
        requestWidgetset = self.getParameter(request, self.REQUEST_WIDGETSET,
                None)
        sharedWidgetset = self.getParameter(request,
                self.REQUEST_SHARED_WIDGETSET, None)

        if requestWidgetset is None and sharedWidgetset is None:
            # Use the value from configuration or DEFAULT_WIDGETSET.
            # If no shared widgetset is specified, the default widgetset is
            # assumed to be in the servlet/portlet itself.
            requestWidgetset = self.getApplicationOrSystemProperty(
                    self.PARAMETER_WIDGETSET, self.DEFAULT_WIDGETSET)

        if requestWidgetset is not None:
            widgetset = requestWidgetset
            widgetsetBasePath = \
                self.getWebApplicationsStaticFileLocation(request)
        else:
            widgetset = sharedWidgetset
            widgetsetBasePath = self.getStaticFilesLocation(request)

        widgetset = self.stripSpecialChars(widgetset)
        widgetsetFilePath = (widgetsetBasePath
                + '/' + self.WIDGETSET_DIRECTORY_PATH + widgetset
                + '/' + widgetset + '.nocache.js?'
                + str( int(time() * 1000) ))  # ms since epoch

        # Get system messages
        systemMessages = None
        # failing to get the system messages is always a problem
        try:
            systemMessages = self.getSystemMessages()
        except SystemMessageException, e:
            raise ServletException('CommunicationError!', e)

        page.write('<script type=\"text/javascript\">\n')
        page.write('//<![CDATA[\n')
        page.write(('if(!vaadin || !vaadin.vaadinConfigurations) {\n '
                + 'if(!vaadin) { var vaadin = {}} \n'
                + 'vaadin.vaadinConfigurations = {};\n'
                + 'if (!vaadin.themesLoaded) '
                + '{ vaadin.themesLoaded = {}; }\n'))

        if not self.isProductionMode():
            page.write('vaadin.debug = true;\n')

        page.write(('document.write(\'<iframe tabIndex=\"-1\" '
                + 'id=\"__gwt_historyFrame\" '
                + 'style=\"position:absolute;width:0;height:0;border:0;'
                + 'overflow:hidden;\" '
                + 'src=\"javascript:false\"></iframe>\');\n'))

        page.write('document.write(\"<script language=\'javascript\' '
                + 'src=\''
                + widgetsetFilePath + '\'><\\/script>\");\n}\n')

        page.write('vaadin.vaadinConfigurations[\"'
                + appId + '\"] = {')

        page.write('appUri:\'' + appUrl + '\', ')

        if window != application.getMainWindow():
            page.write('windowName: \"' \
                    + JsonPaintTarget.escapeJSON(window.getName()) + '\", ')

        if self.isStandalone():
            page.write('standalone: true, ')

        page.write('themeUri:')
        page.write('\"' + themeUri + '\"' if themeUri is not None else 'null')
        page.write(', versionInfo : {vaadinVersion:\"')
        page.write(self.VERSION)
        page.write('\",applicationVersion:\"')
        page.write(JsonPaintTarget.escapeJSON(application.getVersion()))
        page.write('\"}')

        if systemMessages is not None:
            # Write the CommunicationError -message to client
            caption = systemMessages.getCommunicationErrorCaption()
            if caption is not None:
                caption = '\"' + JsonPaintTarget.escapeJSON(caption) + '\"'

            message = systemMessages.getCommunicationErrorMessage()
            if message is not None:
                message = '\"' + JsonPaintTarget.escapeJSON(message) + '\"'

            url = systemMessages.getCommunicationErrorURL()
            if url is not None:
                url = '\"' + JsonPaintTarget.escapeJSON(url) + '\"'
            else:
                url = 'null'

            page.write(',\"comErrMsg\": {' + '\"caption\":'
                    + caption + ',' + '\"message\" : ' + message + ','
                    + '\"url\" : ' + url + '}')

            # Write the AuthenticationError -message to client
            caption = systemMessages.getAuthenticationErrorCaption()
            if caption is not None:
                caption = '\"' + JsonPaintTarget.escapeJSON(caption) + '\"'

            message = systemMessages.getAuthenticationErrorMessage()
            if message is not None:
                message = '\"' + JsonPaintTarget.escapeJSON(message) + '\"'

            url = systemMessages.getAuthenticationErrorURL()
            if url is not None:
                url = '\"' + JsonPaintTarget.escapeJSON(url) + '\"'
            else:
                url = 'null'

            page.write(',\"authErrMsg\": {' + '\"caption\":'
                    + caption + ',' + '\"message\" : ' + message
                    + ',' + '\"url\" : ' + url + '}')

        page.write('};\n//]]>\n</script>\n')

        if themeName is not None:
            # Custom theme's stylesheet, load only once, in different
            # script
            # tag to be dominate styles injected by widget set
            page.write('<script type=\"text/javascript\">\n')
            page.write('//<![CDATA[\n')
            page.write('if(!vaadin.themesLoaded[\'' + themeName + '\']) {\n')
            page.write('var stylesheet = document.createElement(\'link\');\n')
            page.write('stylesheet.setAttribute(\'rel\', \'stylesheet\');\n')
            page.write('stylesheet.setAttribute(\'type\', \'text/css\');\n')
            page.write('stylesheet.setAttribute(\'href\', \'' \
                    + themeUri + '/styles.css\');\n')
            page.write('document.getElementsByTagName(\'head\')[0]'
                    '.appendChild(stylesheet);\n')
            page.write('vaadin.themesLoaded[\'' \
                    + themeName + '\'] = true;\n}\n')
            page.write('//]]>\n</script>\n')

        # Warn if the widgetset has not been loaded after 15 seconds on
        # inactivity
        page.write('<script type=\"text/javascript\">\n')
        page.write('//<![CDATA[\n')
        page.write('setTimeout(\'if (typeof '
                + widgetset.replace('.', '_')
                + ' == \"undefined\") {alert(\"Failed to load the widgetset: '
                + widgetsetFilePath
                + '\")};\',15000);\n'
                + '//]]>\n</script>\n')


    def isStandalone(self):
        """@return: true if the served application is considered to be the
                only or main content of the host page. E.g. various embedding
                solutions should override this to false.
        """
        return True


    def writeAjaxPageHtmlBodyStart(self, page, request):
        """Method to open the body tag of the html kickstart page.

        This method is responsible for closing the head tag and opening
        the body tag.

        Override this method if you want to add some custom html to the page.

        @raise IOException:
        """
        page.write('\n</head>\n<body scroll=\"auto\" class=\"'
                + ApplicationConnection.GENERATED_BODY_CLASSNAME
                + '\">\n')


    def writeAjaxPageHtmlHeader(self, page, title, themeUri, request):
        """Method to write the contents of head element in html kickstart page.

        Override this method if you want to add some custom html to the header
        of the page.

        @raise IOException:
        """
        page.write('<meta http-equiv=\"Content-Type\" '
                + 'content=\"text/html; charset=utf-8\"/>\n')

        context = self.getApplicationContext(self.getSession(request))
        browser = context.getBrowser()
        if browser.isIE():
            # Chrome frame in all versions of IE (only if Chrome frame is
            # installed)
            page.write('<meta http-equiv=\"X-UA-Compatible\" '
                    + 'content=\"chrome=1\"/>\n')

        page.write('<style type=\"text/css\">'
                + 'html, body {height:100%;margin:0;}</style>')

        # Add favicon links
        page.write('<link rel=\"shortcut icon\" '
                + 'type=\"image/vnd.microsoft.icon\" href=\"'
                + themeUri
                + '/favicon.ico\" />')
        page.write('<link rel=\"icon\" type=\"image/vnd.microsoft.icon\" '
                + 'href=\"' + themeUri + '/favicon.ico\" />')
        page.write('<title>'
                + self.safeEscapeForHtml(title)
                + '</title>')


    def writeAjaxPageHtmlHeadStart(self, page, request):
        """Method to write the beginning of the html page.

        This method is responsible for writing appropriate doc type
        declarations and to open html and head tags.

        Override this method if you want to add some custom html to the
        very beginning of the page.

        @raise IOException:
        """
        # write html header
        page.write('<!DOCTYPE html PUBLIC \"-//W3C//DTD '
                + 'XHTML 1.0 Transitional//EN\" '
                + '\"http://www.w3.org/TR/xhtml1/'
                + 'DTD/xhtml1-transitional.dtd\">\n')
        page.write('<html xmlns=\"http://www.w3.org/1999/xhtml\"'
                + '>\n<head>\n')


    def setAjaxPageHeaders(self, response):
        """Method to set http request headers for the Muntjac kickstart page.

        Override this method if you need to customize http headers of the page.
        """
        # Window renders are not cacheable
        self.setHeader(response, 'Cache-Control', 'no-cache')
        self.setHeader(response, 'Pragma', 'no-cache')
        self.setHeader(response, 'Expires', '0')
        self.setHeader(response, 'Content-Type', 'text/html; charset=UTF-8')


    def getNoScriptMessage(self):
        """Returns a message printed for browsers without scripting support
        or if browsers scripting support is disabled.
        """
        return ('You have to enable javascript in your browser to use an '
            'application built with Muntjac.')


    def getApplicationUrl(self, request):
        """Gets the current application URL from request.

        @param request:
                   the HTTP request.
        @raise MalformedURLException:
                    if the application is denied access to the persistent
                    data store represented by the given URL.
        """
        reqURL = 'https://' if self.isSecure(request) else 'http://'
        reqURL += self.getServerName(request)
        if (self.isSecure(request) and self.getServerPort(request) == 443
                or (not self.isSecure(request)
                        and self.getServerPort(request) == 80)):
            reqURL += ''
        else:
            reqURL += ':%d' % self.getServerPort(request)
        reqURL += self.getRequestUri(request)

        # FIXME: implement include requests
        if self.getParameter(request, 'javax.servlet.include.servlet_path',
                    None) is not None:
            # this is an include request
            servletPath = (self.getParameter(request,
                        'javax.servlet.include.context_path', None)
                    + self.getParameter(request,
                        'javax.servlet.include.servlet_path', None))
            #servletPath = (request.originalContextPath
            #        + request.originalServletPath())
        else:
            servletPath = (self.getContextPath(request)  # FIXME: context path
                    + self.getServletPath(request))

        if len(servletPath) == 0 or servletPath[len(servletPath) - 1] != '/':
            servletPath = servletPath + '/'

        return urljoin(reqURL, servletPath)  # FIXME: urljoin


    def getExistingApplication(self, request, allowSessionCreation):
        """Gets the existing application for given request. Looks for
        application instance for given request based on the requested URL.

        @param request:
                   the HTTP request.
        @param allowSessionCreation:
                   true if a session should be created if no session
                   exists, false if no session should be created
        @return: Application instance, or null if the URL does not map to
                    valid application.
        @raise MalformedURLException:
                    if the application is denied access to the persistent
                    data store represented by the given URL.
        @raise SessionExpiredException:
        """
        # Ensures that the session is still valid
        session = self.getSession(request, allowSessionCreation)

        if session is None:
            raise SessionExpiredException()

        context = self.getApplicationContext(session)

        # Gets application list for the session.
        applications = context.getApplications()

        # Search for the application (using the application URI) from the list
        for sessionApplication in applications:
            sessionApplicationPath = \
                    self.getUrlPath(sessionApplication.getURL())
            requestApplicationPath = \
                    self.getUrlPath(self.getApplicationUrl(request))

            if requestApplicationPath == sessionApplicationPath:
                # Found a running application
                if sessionApplication.isRunning():
                    return sessionApplication

                # Application has stopped, so remove it before creating a new
                # application
                self.getApplicationContext(
                        session).removeApplication(sessionApplication)
                break

        # Existing application not found
        return None


    def endApplication(self, request, response, application):
        """Ends the application.

        @param request:
                   the HTTP request.
        @param response:
                   the HTTP response to write to.
        @param application:
                   the application to end.
        @raise IOException:
                    if the writing failed due to input/output error.
        """
        logoutUrl = application.getLogoutURL()

        if logoutUrl is None:
            logoutUrl = application.getURL()

        session = self.getSession(request)
        if session is not None:
            self.getApplicationContext(session).removeApplication(application)

        response.sendRedirect(logoutUrl)  # FIXME: encodeRedirectURL


    def getApplicationWindow(self, request, applicationManager, application):
        """Gets the existing application or create a new one. Get a
        window within an application based on the requested URI.

        @param request:
                   the HTTP Request.
        @param application:
                   the Application to query for window.
        @return: Window matching the given URI or null if not found.
        @raise ServletException:
                    if an exception has occurred that interferes with the
                    servlet's normal operation.
        """
        # Finds the window where the request is handled
        assumedWindow = None
        path = self.getRequestPathInfo(request)

        # Main window as the URI is empty
        if not (path is None or len(path) == 0 or path == '/'):
            if path.startswith('/APP/'):
                # Use main window for application resources
                return application.getMainWindow()

            windowName = None
            if path[0] == '/':
                path = path[1:]

            index = path.find('/')

            if index < 0:
                windowName = path
                path = ''
            else:
                windowName = path[:index]

            assumedWindow = application.getWindow(windowName)

        return applicationManager.getApplicationWindow(request, self,
                application, assumedWindow)


    def getRequestPathInfo(self, request):
        """Returns the path info; note that this _can_ be different than
        request.getPathInfo(). Examples where this might be useful:

          - An application runner servlet that runs different Muntjac
            applications based on an identifier.
          - Providing a REST interface in the context root, while serving a
            Muntjac UI on a sub-URI using only one servlet (e.g. REST on
            http://example.com/foo, UI on http://example.com/foo/vaadin)
        """
        return self.getPathInfo(request)


    def getResourceLocation(self, theme, resource):
        """Gets relative location of a theme resource.

        @param theme:
                   the Theme name.
        @param resource:
                   the Theme resource.
        @return: External URI specifying the resource
        """
        if self._resourcePath is None:
            return resource.getResourceId()

        return self._resourcePath + theme + '/' + resource.getResourceId()


    def isRepaintAll(self, request):
        return ((self.getParameter(request, self.URL_PARAMETER_REPAINT_ALL,
                    None) is not None)
                and (self.getParameter(request, self.URL_PARAMETER_REPAINT_ALL,
                    '') == '1'))


    def closeApplication(self, application, session):
        if application is None:
            return
        application.close()
        if session is not None:
            context = self.getApplicationContext(session)
            context.removeApplication(application)


    def getApplicationContext(self, session):
        """Gets the application context from an HttpSession. If no context
        is currently stored in a session a new context is created and stored
        in the session.

        @param session:
                   the HTTP session.
        @return: the application context for HttpSession.
        """
        # TODO the ApplicationContext.getApplicationContext() should be
        # removed and logic moved here. Now overriding context type is
        # possible, but the whole creation logic should be here. MT 1101

        return WebApplicationContext.getApplicationContext(session, self)


    def createCommunicationManager(self, application):
        """Override this method if you need to use a specialized
        communication mananger implementation.

        @deprecated: Instead of overriding this method, override
                    L{WebApplicationContext} implementation via
                    L{getApplicationContext} method and in that customized
                    implementation return your CommunicationManager in
                    L{WebApplicationContext.getApplicationManager}
                    method.
        """
        warn("deprecated", DeprecationWarning)

        from muntjac.terminal.gwt.server.communication_manager import \
            CommunicationManager

        return CommunicationManager(application)


    @classmethod
    def safeEscapeForHtml(cls, unsafe):
        """Escapes characters to html entities. An exception is made for some
        "safe characters" to keep the text somewhat readable.

        @return: a safe string to be added inside an html tag
        """
        if unsafe is None:
            return None

        safe = StringIO()
        for c in unsafe:
            if cls.isSafe(ord(c)):
                safe.write(c)
            else:
                safe.write('&#')
                safe.write(ord(c))
                safe.write(';')

        result = safe.getvalue()
        safe.close()

        return result


    @classmethod
    def isSafe(cls, c):
        # alphanum or A-Z or a-z
        return ((c > 47 and c < 58)
                or (c > 64 and c < 91)
                or (c > 96 and c < 123))


class ParameterHandlerErrorImpl(ParameterHandlerErrorEvent):
    """Implementation of IErrorEvent interface."""

    def __init__(self, owner, throwable):
        self._owner = owner
        self._throwable = throwable


    def getThrowable(self):
        """Gets the contained throwable.

        @see: L{muntjac.terminal.terminal.IErrorEvent.getThrowable()}
        """
        return self._throwable


    def getParameterHandler(self):
        """Gets the source ParameterHandler.

        @see: L{IErrorEvent.getParameterHandler}
        """
        return self._owner


class URIHandlerErrorImpl(URIHandlerErrorEvent):
    """Implementation of URIHandler.IErrorEvent interface."""

    def __init__(self, owner, throwable):
        self._owner = owner
        self._throwable = throwable


    def getThrowable(self):
        """Gets the contained throwable.

        @see: L{muntjac.terminal.terminal.IErrorEvent.getThrowable()}
        """
        return self._throwable


    def getURIHandler(self):
        """Gets the source URIHandler.

        @see: L{muntjac.terminal.uri_handler.IErrorEvent.getURIHandler}
        """
        return self._owner


class RequestError(TerminalErrorEvent):

    def __init__(self, throwable):
        self._throwable = throwable


    def getThrowable(self):
        return self._throwable
