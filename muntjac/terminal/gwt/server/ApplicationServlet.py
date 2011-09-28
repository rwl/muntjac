# Copyright (C) 2010 IT Mill Ltd.
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

from paste.deploy import CONFIG

from muntjac.terminal.gwt.server.Exceptions import ServletException
from muntjac.terminal.gwt.server.util import loadClass

from muntjac.terminal.gwt.server.AbstractApplicationServlet import \
    AbstractApplicationServlet


class ApplicationServlet(AbstractApplicationServlet):
    """This servlet connects a Muntjac Application to Web.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 5.0
    """

    def awake(self, transaction):
        """Called by the servlet container to indicate to a servlet that
        the servlet is being placed into service.

        @param servletConfig
                   the object containing the servlet's configuration and
                   initialization parameters
        @throws javax.servlet.ServletException
                    if an exception has occurred that interferes with the
                    servlet's normal operation.
        """
        super(ApplicationServlet, self).awake(transaction)

        self._applicationClass = None

        # Loads the application class using the same class loader
        # as the servlet itself

        # Gets the application class name
        applicationClassName = CONFIG.get('application')
        if applicationClassName is None:
            raise ServletException, ('Application not specified '
                    'in servlet parameters')

        try:
            self._applicationClass = loadClass(applicationClassName)
        except ImportError:
            raise ServletException, ('Failed to import module: '
                    + applicationClassName)
        except AttributeError:
            raise ServletException, ('Failed to load application class: '
                    + applicationClassName)


    def getNewApplication(self, request):
        # Creates a new application instance
        try:
            application = self.getApplicationClass()()
        except TypeError:
            raise ServletException, "getNewApplication failed"
        return application


    def getApplicationClass(self):
        return self._applicationClass
