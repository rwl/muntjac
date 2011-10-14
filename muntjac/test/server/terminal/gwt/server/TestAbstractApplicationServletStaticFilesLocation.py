# -*- coding: utf-8 -*-
# from com.vaadin.terminal.gwt.server.AbstractApplicationServlet import (AbstractApplicationServlet,)
# from com.vaadin.terminal.gwt.server.ApplicationServlet import (ApplicationServlet,)
# from java.lang.reflect.Field import (Field,)
# from java.lang.reflect.Method import (Method,)
# from java.net.MalformedURLException import (MalformedURLException,)
# from java.net.URL import (URL,)
# from java.util.Enumeration import (Enumeration,)
# from java.util.Properties import (Properties,)
# from javax.servlet.ServletConfig import (ServletConfig,)
# from javax.servlet.ServletContext import (ServletContext,)
# from javax.servlet.http.HttpServletRequest import (HttpServletRequest,)
# from junit.framework.TestCase import (TestCase,)
# from org.easymock.EasyMock.createMock import (createMock,)
# from org.easymock.EasyMock.expect import (expect,)
# from org.easymock.EasyMock.replay import (replay,)


class TestAbstractApplicationServletStaticFilesLocation(TestCase):
    _servlet = None
    _getStaticFilesLocationMethod = None

    def setUp(self):
        super(TestAbstractApplicationServletStaticFilesLocation, self).setUp()
        self._servlet = ApplicationServlet()
        # Workaround to avoid calling init and creating servlet config
        f = AbstractApplicationServlet.getDeclaredField('applicationProperties')
        f.setAccessible(True)
        setattr(self._servlet, f, Properties())
        self._getStaticFilesLocationMethod = AbstractApplicationServlet.getDeclaredMethod('getStaticFilesLocation', [self.javax.servlet.http.HttpServletRequest])
        self._getStaticFilesLocationMethod.setAccessible(True)

    class DummyServletConfig(ServletConfig):
        # public DummyServletConfig(Map<String,String> initParameters, )

        def getInitParameter(self, name):
            # TODO Auto-generated method stub
            return None

        def getInitParameterNames(self):

            class _0_(Enumeration):

                def hasMoreElements(self):
                    return False

                def nextElement(self):
                    return None

            _0_ = _0_()
            return _0_

        def getServletContext(self):
            # TODO Auto-generated method stub
            return None

        def getServletName(self):
            # TODO Auto-generated method stub
            return None

    def testWidgetSetLocation(self):
        # SERVLETS
        # http://dummy.host:8080/contextpath/servlet
        # should return /contextpath
        location = self.testLocation('http://dummy.host:8080', '/contextpath', '/servlet', '')
        self.assertEquals('/contextpath', location)
        # http://dummy.host:8080/servlet
        # should return ""
        location = self.testLocation('http://dummy.host:8080', '', '/servlet', '')
        self.assertEquals('', location)
        # http://dummy.host/contextpath/servlet/extra/stuff
        # should return /contextpath
        location = self.testLocation('http://dummy.host', '/contextpath', '/servlet', '/extra/stuff')
        self.assertEquals('/contextpath', location)
        # http://dummy.host/context/path/servlet/extra/stuff
        # should return /context/path
        location = self.testLocation('http://dummy.host', '/context/path', '/servlet', '/extra/stuff')
        self.assertEquals('/context/path', location)
        # Include requests
        location = self.testIncludedLocation('http://my.portlet.server', '/user', '/tmpservletlocation1', '')
        self.assertEquals('Wrong widgetset location', '/user', location)

    def testLocation(self, base, contextPath, servletPath, pathInfo):
        request = self.createNonIncludeRequest(base, contextPath, servletPath, pathInfo)
        # Set request into replay mode
        replay(request)
        location = self._getStaticFilesLocationMethod.invoke(self._servlet, request)
        return location

    def testIncludedLocation(self, base, portletContextPath, servletPath, pathInfo):
        request = self.createIncludeRequest(base, portletContextPath, servletPath, pathInfo)
        # Set request into replay mode
        replay(request)
        location = self._getStaticFilesLocationMethod.invoke(self._servlet, request)
        return location

    def createIncludeRequest(self, base, realContextPath, realServletPath, pathInfo):
        request = self.createRequest(base, '', '', pathInfo)
        expect(request.getAttribute('javax.servlet.include.context_path')).andReturn(realContextPath).anyTimes()
        expect(request.getAttribute('javax.servlet.include.servlet_path')).andReturn(realServletPath).anyTimes()
        expect(request.getAttribute(AbstractApplicationServlet.REQUEST_VAADIN_STATIC_FILE_PATH)).andReturn(None).anyTimes()
        return request

    def createNonIncludeRequest(self, base, realContextPath, realServletPath, pathInfo):
        request = self.createRequest(base, realContextPath, realServletPath, pathInfo)
        expect(request.getAttribute('javax.servlet.include.context_path')).andReturn(None).anyTimes()
        expect(request.getAttribute('javax.servlet.include.servlet_path')).andReturn(None).anyTimes()
        expect(request.getAttribute(ApplicationServlet.REQUEST_VAADIN_STATIC_FILE_PATH)).andReturn(None).anyTimes()
        return request

    def createRequest(self, base, contextPath, servletPath, pathInfo):
        """Creates a HttpServletRequest mock using the supplied parameters.

        @param base
                   The base url, e.g. http://localhost:8080
        @param contextPath
                   The context path where the application is deployed, e.g.
                   /mycontext
        @param servletPath
                   The servlet path to the servlet we are testing, e.g. /myapp
        @param pathInfo
                   Any text following the servlet path in the request, not
                   including query parameters, e.g. /UIDL/
        @return A mock HttpServletRequest object useful for testing
        @throws MalformedURLException
        """
        url = URL(base + contextPath + pathInfo)
        request = createMock(HttpServletRequest)
        expect(request.isSecure()).andReturn(url.getProtocol().equalsIgnoreCase('https')).anyTimes()
        expect(request.getServerName()).andReturn(url.getHost()).anyTimes()
        expect(request.getServerPort()).andReturn(url.getPort()).anyTimes()
        expect(request.getRequestURI()).andReturn(url.getPath()).anyTimes()
        expect(request.getContextPath()).andReturn(contextPath).anyTimes()
        expect(request.getPathInfo()).andReturn(pathInfo).anyTimes()
        expect(request.getServletPath()).andReturn(servletPath).anyTimes()
        return request
