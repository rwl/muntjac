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

from muntjac.terminal.Terminal import ErrorEvent


class ParameterHandler(object):
    """{@code ParameterHandler} is implemented by classes capable of handling
    external parameters.

    <p>
    What parameters are provided depend on what the {@link Terminal} provides and
    if the application is deployed as a servlet or portlet. URL GET parameters
    are typically provided to the {@link #handleParameters(Map)} method.
    </p>
    <p>
    A {@code ParameterHandler} must be registered to a {@code Window} using
    {@link Window#addParameterHandler(ParameterHandler)} to be called when
    parameters are available.
    </p>

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def handleParameters(self, parameters):
        """Handles the given parameters. All parameters names are of type
        {@link String} and the values are {@link String} arrays.

        @param parameters
                   an unmodifiable map which contains the parameter names and
                   values
        """
        pass


class ErrorEvent(ErrorEvent):
    """An ErrorEvent implementation for ParameterHandler."""

    def getParameterHandler(self):
        """Gets the ParameterHandler that caused the error.

        @return the ParameterHandler that caused the error
        """
        pass
