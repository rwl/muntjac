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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.data.validator.AbstractValidator import (AbstractValidator,)


class StringLengthValidator(AbstractValidator):
    """This <code>StringLengthValidator</code> is used to validate the length of
    strings.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    _minLength = -1
    _maxLength = -1
    _allowNull = True

    def __init__(self, *args):
        """Creates a new StringLengthValidator with a given error message.

        @param errorMessage
                   the message to display in case the value does not validate.
        ---
        Creates a new StringLengthValidator with a given error message,
        permissable lengths and null-string allowance.

        @param errorMessage
                   the message to display in case the value does not validate.
        @param minLength
                   the minimum permissible length of the string.
        @param maxLength
                   the maximum permissible length of the string.
        @param allowNull
                   Are null strings permissible? This can be handled better by
                   setting a field as required or not.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            errorMessage, = _0
            super(StringLengthValidator, self)(errorMessage)
        elif _1 == 4:
            errorMessage, minLength, maxLength, allowNull = _0
            self.__init__(errorMessage)
            self.setMinLength(minLength)
            self.setMaxLength(maxLength)
            self.setNullAllowed(allowNull)
        else:
            raise ARGERROR(1, 4)

    def isValid(self, value):
        """Checks if the given value is valid.

        @param value
                   the value to validate.
        @return <code>true</code> for valid value, otherwise <code>false</code>.
        """
        if value is None:
            return self._allowNull
        s = str(value)
        if s is None:
            return self._allowNull
        len = len(s)
        if (
            (self._minLength >= 0 and len < self._minLength) or (self._maxLength >= 0 and len > self._maxLength)
        ):
            return False
        return True

    def isNullAllowed(self):
        """Returns <code>true</code> if null strings are allowed.

        @return <code>true</code> if allows null string, otherwise
                <code>false</code>.
        """
        return self._allowNull

    def getMaxLength(self):
        """Gets the maximum permissible length of the string.

        @return the maximum length of the string.
        """
        return self._maxLength

    def getMinLength(self):
        """Gets the minimum permissible length of the string.

        @return the minimum length of the string.
        """
        return self._minLength

    def setNullAllowed(self, allowNull):
        """Sets whether null-strings are to be allowed. This can be better handled
        by setting a field as required or not.
        """
        self._allowNull = allowNull

    def setMaxLength(self, maxLength):
        """Sets the maximum permissible length of the string.

        @param maxLength
                   the length to set.
        """
        if maxLength < -1:
            maxLength = -1
        self._maxLength = maxLength

    def setMinLength(self, minLength):
        """Sets the minimum permissible length.

        @param minLength
                   the length to set.
        """
        if minLength < -1:
            minLength = -1
        self._minLength = minLength
