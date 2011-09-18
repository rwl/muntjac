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

from com.vaadin.terminal.gwt.widgetsetutils.WidgetMapGenerator import (WidgetMapGenerator,)
# from com.vaadin.ui.ClientWidget.LoadStyle import (LoadStyle,)


class EagerWidgetMapGenerator(WidgetMapGenerator):
    """WidgetMap generator that builds a widgetset that packs all included widgets
    into a single JavaScript file loaded at application initialization. Initially
    loaded data will be relatively large, but minimal amount of server requests
    will be done.
    <p>
    This is the default generator in version 6.4 and produces similar type of
    widgetset as in previous versions of Vaadin. To activate "code splitting",
    use the {@link WidgetMapGenerator} instead, that loads most components
    deferred.

    @see WidgetMapGenerator
    """

    def getLoadStyle(self, paintableType):
        return LoadStyle.EAGER
