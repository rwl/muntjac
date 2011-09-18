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



class Focusable(object):
    """GWT's HasFocus is way too overkill for just receiving focus in simple
    components. Vaadin uses this interface in addition to GWT's HasFocus to pass
    focus requests from server to actual ui widgets in browsers.

    So in to make your server side focusable component receive focus on client
    side it must either implement this or HasFocus interface.
    """

    def focus(self):
        """Sets focus to this widget."""
        pass
