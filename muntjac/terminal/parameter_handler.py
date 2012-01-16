# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

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
    @version: 1.1.0
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
