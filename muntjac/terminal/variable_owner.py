# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

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
    @version: @VERSION@
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
