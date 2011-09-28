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

from muntjac.terminal.ErrorMessage import ErrorMessage


class Validator(object):
    """Interface that implements a method for validating if an {@link Object} is
    valid or not.
    <p>
    Implementors of this class can be added to any
    {@link com.vaadin.data.Validatable Validatable} implementor to verify its
    value.
    </p>
    <p>
    {@link #isValid(Object)} and {@link #validate(Object)} can be used to check
    if a value is valid. {@link #isValid(Object)} and {@link #validate(Object)}
    must use the same validation logic so that iff {@link #isValid(Object)}
    returns false, {@link #validate(Object)} throws an
    {@link InvalidValueException}.
    </p>
    <p>
    Validators must not have any side effects.
    </p>

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def validate(self, value):
        """Checks the given value against this validator. If the value is valid the
        method does nothing. If the value is invalid, an
        {@link InvalidValueException} is thrown.

        @param value
                   the value to check
        @throws Validator.InvalidValueException
                    if the value is invalid
        """
        pass


    def isValid(self, value):
        """Tests if the given value is valid. This method must be symmetric with
        {@link #validate(Object)} so that {@link #validate(Object)} throws an
        error iff this method returns false.

        @param value
                   the value to check
        @return <code>true</code> if the value is valid, <code>false</code>
                otherwise.
        """
        pass


class InvalidValueException(RuntimeError, ErrorMessage):
    """Exception that is thrown by a {@link Validator} when a value is invalid.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, message, causes=None):
        """Constructs a new {@code InvalidValueException} with the specified
        message.

        @param message
                   The detail message of the problem.
        ---
        Constructs a new {@code InvalidValueException} with a set of causing
        validation exceptions. The causing validation exceptions are included
        when the exception is painted to the client.

        @param message
                   The detail message of the problem.
        @param causes
                   One or more {@code InvalidValueException}s that caused
                   this exception.
        """
        super(InvalidValueException, self)(message)

        # Array of one or more validation errors that are causing this
        # validation error.
        if causes is not None:
            self._causes = causes
        else:
            self._causes = list()


    def isInvisible(self):
        """Check if the error message should be hidden.

        An empty (null or "") message is invisible unless it contains nested
        exceptions that are visible.

        @return true if the error message should be hidden, false otherwise
        """
        msg = self.getMessage()

        if msg is not None and len(msg) > 0:
            return False

        if self._causes is not None:
            for i in range(len(self._causes)):
                if not self._causes[i].isInvisible():
                    return False

        return True


    def getErrorLevel(self):
        return ErrorMessage.ERROR


    def paint(self, target):
        target.startTag('error')
        target.addAttribute('level', 'error')

        # Error message
        message = self.getLocalizedMessage()
        if message is not None:
            target.addText(message)

        # Paint all the causes
        for i in range(len(self._causes)):
            self._causes[i].paint(target)

        target.endTag('error')


    def addListener(self, listener):
        pass


    def removeListener(self, listener):
        pass


    def requestRepaint(self):
        pass


    def requestRepaintRequests(self):
        pass


    def getDebugId(self):
        return None


    def setDebugId(self, idd):
        raise NotImplementedError, 'InvalidValueException cannot have a debug id'


    def getCauses(self):
        """Returns the {@code InvalidValueExceptions} that caused this
        exception.

        @return An array containing the {@code InvalidValueExceptions} that
                caused this exception. Returns an empty array if this
                exception was not caused by other exceptions.
        """
        return self._causes


class EmptyValueException(Validator.InvalidValueException):
    """A specific type of {@link InvalidValueException} that indicates that
    validation failed because the value was empty. What empty means is up to
    the thrower.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 5.3.0
    """

    def __init__(self, message):
        super(EmptyValueException, self)(message)
