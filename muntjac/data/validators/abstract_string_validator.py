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

"""Validator base class for validating strings."""

from muntjac.data.validators.abstract_validator import AbstractValidator


class AbstractStringValidator(AbstractValidator):
    """Validator base class for validating strings. See L{AbstractValidator}
    for more information.

    To include the value that failed validation in the exception message you
    can use "{0}" in the error message. This will be replaced with the failed
    value (converted to string using L{__str__}) or "None" if the value is
    C{None}.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, errorMessage):
        """Constructs a validator for strings.

        None and empty string values are always accepted. To reject empty
        values, set the field being validated as required.

        @param errorMessage:
                   the message to be included in an L{InvalidValueException}
                   (with "{0}" replaced by the value that failed validation).
        """
        super(AbstractStringValidator, self).__init__(errorMessage)


    def isValid(self, value):
        """Tests if the given value is a valid string.

        None values are always accepted. Values that are not strings are
        converted using L{__str__}. Then L{isValidString} is used to validate
        the value.

        @param value:
                   the value to check
        @return: true if the value (or its __str__) is a valid string, false
                otherwise
        """
        if value is None:
            return True

        if not isinstance(value, str):
            value = str(value)

        return self.isValidString(value)


    def isValidString(self, value):
        """Checks if the given string is valid.

        @param value:
                   String to check. Can never be None.
        @return: true if the string is valid, false otherwise
        """
        pass
