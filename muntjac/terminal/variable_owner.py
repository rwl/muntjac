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

"""Defines a listener interface for UI variable changes."""

from muntjac.terminal.terminal import IErrorEvent as ITerminalErrorEvent


class IVariableOwner(object):
    """Listener interface for UI variable changes. The user communicates
    with the application using the so-called I{variables}. When the
    user makes a change using the UI the terminal trasmits the changed
    variables to the application, and the components owning those variables
    may then process those changes.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def changeVariables(self, source, variables):
        """Called when one or more variables handled by the implementing
        class are changed.

        @param source:
                   the Source of the variable change. This is the origin
                   of the event. For example in Web Adapter this is the
                   request.
        @param variables:
                   the Mapping from variable names to new variable values.
        """
        raise NotImplementedError


    def isEnabled(self):
        """Tests if the variable owner is enabled or not. The terminal
        should not send any variable changes to disabled variable owners.

        @return: C{True} if the variable owner is enabled, C{False} if not
        """
        raise NotImplementedError


    def isImmediate(self):
        """Tests if the variable owner is in immediate mode or not. Being
        in immediate mode means that all variable changes are required to
        be sent back from the terminal immediately when they occur.

        B{Note:} C{IVariableOwner} does not include
        a set-method for the immediateness property. This is because not all
        VariableOwners wish to offer the functionality. Such VariableOwners
        are never in the immediate mode, thus they always return
        C{False} in L{isImmediate}.

        @return: C{True} if the component is in immediate mode, C{False} if not
        """
        raise NotImplementedError


class IErrorEvent(ITerminalErrorEvent):
    """IVariableOwner error event."""

    def getVariableOwner(self):
        """Gets the source IVariableOwner.

        @return: the variable owner.
        """
        raise NotImplementedError
