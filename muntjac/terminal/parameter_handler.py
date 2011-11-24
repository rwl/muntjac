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

"""Defines an interface implemented by classes capable of handling
external parameters."""

from muntjac.terminal.terminal import IErrorEvent as ITerminalErrorEvent


class IParameterHandler(object):
    """C{IParameterHandler} is implemented by classes capable of handling
    external parameters.

    What parameters are provided depend on what the L{Terminal} provides
    and if the application is deployed as a servlet. URL GET
    parameters are typically provided to the L{handleParameters}
    method.

    A C{IParameterHandler} must be registered to a C{Window} using
    L{Window.addParameterHandler} to be called when parameters are available.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.3
    """

    def handleParameters(self, parameters):
        """Handles the given parameters. All parameters names are of type
        string and the values are string arrays.

        @param parameters:
                   an unmodifiable map which contains the parameter names
                   and values
        """
        raise NotImplementedError


class IErrorEvent(ITerminalErrorEvent):
    """An IErrorEvent implementation for IParameterHandler."""

    def getParameterHandler(self):
        """Gets the IParameterHandler that caused the error.

        @return: the IParameterHandler that caused the error
        """
        raise NotImplementedError
