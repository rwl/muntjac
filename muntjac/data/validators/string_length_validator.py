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

"""Used to validate the length of strings."""

from muntjac.data.validators.abstract_validator import AbstractValidator


class StringLengthValidator(AbstractValidator):
    """This StringLengthValidator is used to validate the length of strings.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.3
    """

    def __init__(self, errorMessage, minLength=None, maxLength=None,
                allowNull=None):
        """Creates a new StringLengthValidator with a given error message,
        permissable lengths and null-string allowance.

        @param errorMessage:
                   the message to display in case the value does not validate.
        @param minLength:
                   the minimum permissible length of the string.
        @param maxLength:
                   the maximum permissible length of the string.
        @param allowNull:
                   Are null strings permissible? This can be handled better by
                   setting a field as required or not.
        """
        self._minLength = -1
        self._maxLength = -1
        self._allowNull = True

        if minLength is None:
            super(StringLengthValidator, self).__init__(errorMessage)
        else:
            StringLengthValidator.__init__(self, errorMessage)
            self.setMinLength(minLength)
            self.setMaxLength(maxLength)
            self.setNullAllowed(allowNull)


    def isValid(self, value):
        """Checks if the given value is valid.

        @param value:
                   the value to validate.
        @return: C{True} for valid value, otherwise C{False}.
        """
        if value is None:
            return self._allowNull

        s = str(value)
        if s is None:
            return self._allowNull

        length = len(s)
        if (self._minLength >= 0 and length < self._minLength) \
                or (self._maxLength >= 0 and length > self._maxLength):
            return False

        return True


    def isNullAllowed(self):
        """Returns C{True} if null strings are allowed.

        @return: C{True} if allows null string, otherwise C{False}.
        """
        return self._allowNull


    def getMaxLength(self):
        """Gets the maximum permissible length of the string.

        @return: the maximum length of the string.
        """
        return self._maxLength


    def getMinLength(self):
        """Gets the minimum permissible length of the string.

        @return: the minimum length of the string.
        """
        return self._minLength


    def setNullAllowed(self, allowNull):
        """Sets whether null-strings are to be allowed. This can be better
        handled by setting a field as required or not.
        """
        self._allowNull = allowNull


    def setMaxLength(self, maxLength):
        """Sets the maximum permissible length of the string.

        @param maxLength:
                   the length to set.
        """
        if maxLength < -1:
            maxLength = -1

        self._maxLength = maxLength


    def setMinLength(self, minLength):
        """Sets the minimum permissible length.

        @param minLength:
                   the length to set.
        """
        if minLength < -1:
            minLength = -1

        self._minLength = minLength
