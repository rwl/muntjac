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

"""Used for validating properties that do or do not allow null values."""

from muntjac.data.validator import IValidator, InvalidValueException


class NullValidator(IValidator):
    """This validator is used for validating properties that do or do not
    allow null values. By default, nulls are not allowed.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, errorMessage, onlyNullAllowed):
        """Creates a new NullValidator.

        @param errorMessage:
                   the error message to display on invalidation.
        @param onlyNullAllowed:
                   Are only nulls allowed?
        """
        self._onlyNullAllowed = None
        self._errorMessage = None

        self.setErrorMessage(errorMessage)
        self.setNullAllowed(onlyNullAllowed)


    def validate(self, value):
        """Validates the data given in value.

        @param value:
                   the value to validate.
        @raise InvalidValueException:
                    if the value was invalid.
        """
        if (self._onlyNullAllowed and value is not None) \
                or (not self._onlyNullAllowed and value is None):
            raise InvalidValueException(self._errorMessage)


    def isValid(self, value):
        """Tests if the given value is valid.

        @param value:
                   the value to validate.
        @return: C{True} for valid value, otherwise C{False}.
        """
        return value is None if self._onlyNullAllowed else value is not None


    def isNullAllowed(self):
        """Returns C{True} if nulls are allowed otherwise C{False}.
        """
        return self._onlyNullAllowed


    def setNullAllowed(self, onlyNullAllowed):
        """Sets if nulls (and only nulls) are to be allowed.

        @param onlyNullAllowed:
                   If true, only nulls are allowed. If false only non-nulls are
                   allowed. Do we allow nulls?
        """
        self._onlyNullAllowed = onlyNullAllowed


    def getErrorMessage(self):
        """Gets the error message that is displayed in case the value is
        invalid.

        @return: the Error Message.
        """
        return self._errorMessage


    def setErrorMessage(self, errorMessage):
        """Sets the error message to be displayed on invalid value.

        @param errorMessage:
                   the Error Message to set.
        """
        self._errorMessage = errorMessage
