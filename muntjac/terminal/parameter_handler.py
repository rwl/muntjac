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

from muntjac.terminal.terminal import IErrorEvent as ITerminalErrorEvent


class IParameterHandler(object):
    """{@code IParameterHandler} is implemented by classes capable of handling
    external parameters.

    What parameters are provided depend on what the {@link Terminal} provides
    and if the application is deployed as a servlet or portlet. URL GET
    parameters are typically provided to the {@link #handleParameters(Map)}
    method.

    A {@code IParameterHandler} must be registered to a {@code Window} using
    {@link Window#addParameterHandler(IParameterHandler)} to be called when
    parameters are available.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def handleParameters(self, parameters):
        """Handles the given parameters. All parameters names are of type
        {@link String} and the values are {@link String} arrays.

        @param parameters
                   an unmodifiable map which contains the parameter names
                   and values
        """
        raise NotImplementedError


class IErrorEvent(ITerminalErrorEvent):
    """An IErrorEvent implementation for IParameterHandler."""

    def getParameterHandler(self):
        """Gets the IParameterHandler that caused the error.

        @return the IParameterHandler that caused the error
        """
        raise NotImplementedError
