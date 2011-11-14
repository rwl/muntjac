
from paste.deploy import CONFIG

from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet
from muntjac.terminal.gwt.server.exceptions import ServletException
from muntjac.util import loadClass


class app(ApplicationServlet):
    """Servlet for use with Paste Deploy."""

    SERVLET_PARAMETER_APPLICATION = 'application'

    def __init__(self):
        # Gets the application class name using Paste Deploy config
        appClassName = CONFIG.get(self.SERVLET_PARAMETER_APPLICATION)

        if appClassName is None:
            raise ServletException, ('Application not specified '
                    'in servlet parameters')

        try:
            applicationClass = loadClass(appClassName)
        except ImportError:
            raise ServletException, ('Failed to import module: '
                    + appClassName)
        except AttributeError:
            raise ServletException, ('Failed to load application class: '
                    + appClassName)

        super(app, self).__init__(applicationClass)

        self._applicationProperties.update(CONFIG)
