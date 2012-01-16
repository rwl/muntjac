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

"""Abstract IValidator implementation that provides a basic IValidator
implementation except the isValid method."""

from muntjac.data.validator import InvalidValueException, IValidator


class AbstractValidator(IValidator):
    """Abstract L{IValidator} implementation that provides a basic IValidator
    implementation except the L{isValid} method. Sub-classes need to implement
    the L{isValid} method.

    To include the value that failed validation in the exception message you
    can use "{0}" in the error message. This will be replaced with the failed
    value (converted to string using L{__str__}) or "null" if the value is
    None.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, errorMessage):
        """Constructs a validator with the given error message.

        @param errorMessage:
                   the message to be included in an L{InvalidValueException}
                   (with "{0}" replaced by the value that failed validation).
        """
        # Error message that is included in an L{InvalidValueException} if
        # such is thrown.
        self._errorMessage = errorMessage


    def validate(self, value):
        if not self.isValid(value):
            message = self._errorMessage.replace('{0}', str(value))
            raise InvalidValueException(message)


    def getErrorMessage(self):
        """Returns the message to be included in the exception in case the
        value does not validate.

        @return: the error message provided in the constructor or using
                L{setErrorMessage}.
        """
        return self._errorMessage


    def setErrorMessage(self, errorMessage):
        """Sets the message to be included in the exception in case the value
        does not validate. The exception message is typically shown to the end
        user.

        @param errorMessage:
                   the error message. "{0}" is automatically replaced by the
                   value that did not validate.
        """
        self._errorMessage = errorMessage
