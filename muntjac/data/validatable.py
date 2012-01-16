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

"""Interface for validatable objects."""


class IValidatable(object):
    """Interface for validatable objects. Defines methods to verify if the
    object's value is valid or not, and to add, remove and list registered
    validators of the object.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    @see: L{IValidator}
    """

    def addValidator(self, validator):
        """Adds a new validator for this object. The validator's
        L{Validator.validate} method is activated every time the
        object's value needs to be verified, that is, when the L{isValid}
        method is called. This usually happens when the object's value changes.

        @param validator:
                   the new validator
        """
        raise NotImplementedError


    def removeValidator(self, validator):
        """Removes a previously registered validator from the object. The
        specified validator is removed from the object and its C{validate}
        method is no longer called in L{isValid}.

        @param validator:
                   the validator to remove
        """
        raise NotImplementedError


    def getValidators(self):
        """Lists all validators currently registered for the object. If no
        validators are registered, returns C{None}.

        @return: collection of validators or C{None}
        """
        raise NotImplementedError


    def isValid(self):
        """Tests the current value of the object against all registered
        validators. The registered validators are iterated and for each the
        L{Validator.validate} method is called. If any validator
        throws the L{InvalidValueException} this method returns
        C{False}.

        @return: C{True} if the registered validators concur that the
                value is valid, C{False} otherwise
        """
        raise NotImplementedError


    def validate(self):
        """Checks the validity of the validatable. If the validatable is valid
        this method should do nothing, and if it's not valid, it should throw
        C{InvalidValueException}

        @raise InvalidValueException:
                    if the value is not valid
        """
        raise NotImplementedError


    def isInvalidAllowed(self):
        """Checks the validabtable object accept invalid values.The default
        value is C{True}.
        """
        raise NotImplementedError


    def setInvalidAllowed(self, invalidValueAllowed):
        """Should the validabtable object accept invalid values. Supporting
        this configuration possibility is optional. By default invalid values
        are allowed.

        @raise NotImplementedError:
                    if the setInvalidAllowed is not supported.
        """
        raise NotImplementedError
