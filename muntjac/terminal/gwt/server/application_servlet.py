# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Defines a servlet that connects a Muntjac Application to Web."""

from muntjac.terminal.gwt.server.exceptions import ServletException

from muntjac.terminal.gwt.server.abstract_application_servlet import \
    AbstractApplicationServlet


class ApplicationServlet(AbstractApplicationServlet):
    """This servlet connects a Muntjac Application to Web.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    def __init__(self, applicationClass, *args, **kw_args):
        super(ApplicationServlet, self).__init__(*args, **kw_args)

        self._applicationClass = applicationClass


#    def awake(self, transaction):
#        """Called by the servlet container to indicate to a servlet that
#        the servlet is being placed into service.
#
#        @param servletConfig
#                   the object containing the servlet's configuration and
#                   initialization parameters
#        @raise javax.servlet.ServletException
#                    if an exception has occurred that interferes with the
#                    servlet's normal operation.
#        """
#        super(ApplicationServlet, self).awake(transaction)
#
#
#        # Loads the application class using the same class loader
#        # as the servlet itself
#
#        # Gets the application class name
#        applicationClassName = CONFIG.get('application')
#        if applicationClassName is None:
#            raise ServletException, ('Application not specified '
#                    'in servlet parameters')
#
#        try:
#            self._applicationClass = loadClass(applicationClassName)
#        except ImportError:
#            raise ServletException, ('Failed to import module: '
#                    + applicationClassName)
#        except AttributeError:
#            raise ServletException, ('Failed to load application class: '
#                    + applicationClassName)


    def getNewApplication(self, request):
        # Creates a new application instance
        try:
            applicationClass = self.getApplicationClass()
            application = applicationClass()
        except TypeError:
            raise ServletException, "getNewApplication failed"

        return application


    def getApplicationClass(self):
        return self._applicationClass


class SingletonApplicationServlet(AbstractApplicationServlet):

    def __init__(self, applicationObject, *args, **kw_args):
        super(SingletonApplicationServlet, self).__init__(*args, **kw_args)
        self._applicationObject = applicationObject


    def getNewApplication(self, request):
        if self._applicationObject is not None:
            return self._applicationObject
        else:
            raise ServletException, "getNewApplication failed"


    def getApplicationClass(self):
        return self._applicationObject.__class__
