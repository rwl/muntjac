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
    @version
    @VERSION@
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
    @version
    @VERSION@
    @since 3.0
    """
    # Array of one or more validation errors that are causing this
    # validation error.

    _causes = None

    def __init__(self, *args):
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
        _0 = args
        _1 = len(args)
        if _1 == 1:
            message, = _0
            self.__init__(message, [])
        elif _1 == 2:
            message, causes = _0
            super(InvalidValueException, self)(message)
            if causes is None:
                raise self.NullPointerException('Possible causes array must not be null')
            self._causes = causes
        else:
            raise ARGERROR(1, 2)

    def isInvisible(self):
        """Check if the error message should be hidden.

        An empty (null or "") message is invisible unless it contains nested
        exceptions that are visible.

        @return true if the error message should be hidden, false otherwise
        """
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.ErrorMessage#getErrorLevel()

        msg = self.getMessage()
        if msg is not None and len(msg) > 0:
            return False
        if self._causes is not None:
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(self._causes)):
                    break
                if not self._causes[i].isInvisible():
                    return False
        return True

    def getErrorLevel(self):
        # (non-Javadoc)
        #
        # @see
        # com.vaadin.terminal.Paintable#paint(com.vaadin.terminal.PaintTarget)

        return ErrorMessage.ERROR

    def paint(self, target):
        # (non-Javadoc)
        #
        # @see
        # com.vaadin.terminal.ErrorMessage#addListener(com.vaadin.terminal.
        # Paintable.RepaintRequestListener)

        target.startTag('error')
        target.addAttribute('level', 'error')
        # Error message
        message = self.getLocalizedMessage()
        if message is not None:
            target.addText(message)
        # Paint all the causes
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._causes)):
                break
            self._causes[i].paint(target)
        target.endTag('error')

    def addListener(self, listener):
        # (non-Javadoc)
        #
        # @see
        # com.vaadin.terminal.ErrorMessage#removeListener(com.vaadin.terminal
        # .Paintable.RepaintRequestListener)

        pass

    def removeListener(self, listener):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.ErrorMessage#requestRepaint()

        pass

    def requestRepaint(self):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Paintable#requestRepaintRequests()

        pass

    def requestRepaintRequests(self):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Paintable#getDebugId()

        pass

    def getDebugId(self):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Paintable#setDebugId(java.lang.String)

        return None

    def setDebugId(self, id):
        raise self.UnsupportedOperationException('InvalidValueException cannot have a debug id')

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
    @version
    @VERSION@
    @since 5.3.0
    """

    def __init__(self, message):
        super(EmptyValueException, self)(message)
