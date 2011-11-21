# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

"""Request start and end listener"""


class IHttpServletRequestListener(object):
    """L{Application} that implements this interface gets notified
    of request start and end by terminal.

    Interface can be used for several helper tasks including:

      - Opening and closing database connections
      - Implementing L{ThreadLocal}
      - Setting/Getting L{Cookie}

    Alternatives for implementing similar features are are Servlet
    L{Filter}s and L{TransactionListener}s in Muntjac.
    """

    def onRequestStart(self, request, response):
        """This method is called before L{Terminal} applies the
        request to Application.
        """
        raise NotImplementedError


    def onRequestEnd(self, request, response):
        """This method is called at the end of each request.
        """
        raise NotImplementedError
