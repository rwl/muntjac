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

"""Used to validate the length of strings."""

from muntjac.data.validators.abstract_validator import AbstractValidator


class StringLengthValidator(AbstractValidator):
    """This StringLengthValidator is used to validate the length of strings.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
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
