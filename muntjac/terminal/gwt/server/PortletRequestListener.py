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

# from java.io.Serializable import (Serializable,)
# from javax.portlet.PortletRequest import (PortletRequest,)
# from javax.portlet.PortletResponse import (PortletResponse,)
# from javax.servlet.Filter import (Filter,)


class PortletRequestListener(Serializable):
    """An {@link Application} that implements this interface gets notified of
    request start and end by the terminal. It is quite similar to the
    {@link HttpServletRequestListener}, but the parameters are Portlet specific.
    If an Application is deployed as both a Servlet and a Portlet, one most
    likely needs to implement both.
    <p>
    Only JSR 286 style Portlets are supported.
    <p>
    The interface can be used for several helper tasks including:
    <ul>
    <li>Opening and closing database connections
    <li>Implementing {@link ThreadLocal}
    <li>Inter-portlet communication
    </ul>
    <p>
    Alternatives for implementing similar features are are Servlet {@link Filter}
    s and {@link TransactionListener}s in Vaadin.

    @since 6.2
    @see HttpServletRequestListener
    """

    def onRequestStart(self, request, response):
        """This method is called before {@link Terminal} applies the request to
        Application.

        @param requestData
                   the {@link PortletRequest} about to change Application state
        """
        pass

    def onRequestEnd(self, request, response):
        """This method is called at the end of each request.

        @param requestData
                   the {@link PortletRequest}
        """
        pass
