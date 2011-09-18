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

from com.vaadin.terminal.gwt.server.AbstractApplicationPortlet import (AbstractApplicationPortlet,)
# from javax.portlet.PortletConfig import (PortletConfig,)
# from javax.portlet.PortletException import (PortletException,)


class ApplicationPortlet2(AbstractApplicationPortlet):
    """TODO Write documentation, fix JavaDoc tags.

    @author peholmst
    """
    _applicationClass = None

    def init(self, config):
        super(ApplicationPortlet2, self).init(config)
        applicationClassName = config.getInitParameter('application')
        if applicationClassName is None:
            raise PortletException('Application not specified in portlet parameters')
        try:
            self._applicationClass = self.getClassLoader().loadClass(applicationClassName)
        except ClassNotFoundException, e:
            raise PortletException('Failed to load application class: ' + applicationClassName)

    def getApplicationClass(self):
        return self._applicationClass
