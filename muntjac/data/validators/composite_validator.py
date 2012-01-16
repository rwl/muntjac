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

"""Allows you to chain (compose) many validators to validate one field."""

from muntjac.data.validators.abstract_validator import AbstractValidator
from muntjac.data.validator import InvalidValueException


class CompositeValidator(AbstractValidator):
    """The C{CompositeValidator} allows you to chain (compose) many
    validators to validate one field. The contained validators may be required
    to all validate the value to validate or it may be enough that one
    contained validator validates the value. This behaviour is controlled by
    the modes C{AND} and C{OR}.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    #: The validators are combined with C{AND} clause: validity of
    #  the composite implies validity of the all validators it is composed of
    #  must be valid.
    MODE_AND = 0

    #: The validators are combined with C{OR} clause: validity of the
    #  composite implies that some of validators it is composed of must be
    #  valid.
    MODE_OR = 1

    #: The validators are combined with and clause: validity of the composite
    #  implies validity of the all validators it is composed of
    MODE_DEFAULT = MODE_AND

    def __init__(self, mode=None, errorMessage=None):
        """Constructs a composite validator in given mode.
        """
        #: Operation mode.
        self._mode = self.MODE_DEFAULT

        #: List of contained validators.
        self._validators = list()

        if mode is None:
            super(CompositeValidator, self).__init__('')
        else:
            super(CompositeValidator, self).__init__(errorMessage)
            self.setMode(mode)


    def validate(self, value):
        """Validates the given value.

        The value is valid, if:
          - C{MODE_AND}: All of the sub-validators are valid
          - C{MODE_OR}: Any of the sub-validators are valid

        If the value is invalid, validation error is thrown. If the error
        message is set (non-null), it is used. If the error message has not
        been set, the first error occurred is thrown.

        @param value:
                   the value to check.
        @raise InvalidValueException:
                    if the value is not valid.
        """
        if self._mode == self.MODE_AND:
            for validator in self._validators:
                validator.validate(value)
            return
        elif self._mode == self.MODE_OR:
            first = None
            for v in self._validators:
                try:
                    v.validate(value)
                    return
                except InvalidValueException, e:
                    if first is None:
                        first = e
            if first is None:
                return
            em = self.getErrorMessage()
            if em is not None:
                raise InvalidValueException(em)
            else:
                raise first

        raise ValueError, 'The validator is in unsupported operation mode'


    def isValid(self, value):
        """Checks the validity of the the given value. The value is valid, if:
          - C{MODE_AND}: All of the sub-validators are valid
          - C{MODE_OR}: Any of the sub-validators are valid

        @param value:
                   the value to check.
        """
        if self._mode == self.MODE_AND:
            for v in self._validators:
                if not v.isValid(value):
                    return False
            return True

        elif self._mode == self.MODE_OR:
            for v in self._validators:
                if v.isValid(value):
                    return True
            return False

        raise ValueError, 'The valitor is in unsupported operation mode'


    def getMode(self):
        """Gets the mode of the validator.

        @return: Operation mode of the validator: C{MODE_AND} or C{MODE_OR}.
        """
        return self._mode


    def setMode(self, mode):
        """Sets the mode of the validator. The valid modes are:
          - C{MODE_AND} (default)
          - C{MODE_OR}

        @param mode:
                   the mode to set.
        """
        if mode != self.MODE_AND and mode != self.MODE_OR:
            raise ValueError, 'Mode ' + mode + ' unsupported'

        self._mode = mode


    def getErrorMessage(self):
        """Gets the error message for the composite validator. If the error
        message is C{None}, original error messages of the sub-validators are
        used instead.
        """
        if super(CompositeValidator, self).getErrorMessage() is not None:
            return super(CompositeValidator, self).getErrorMessage()

        # TODO: return composite error message

        return None


    def addValidator(self, validator):
        """Adds validator to the interface.

        @param validator:
                   the Validator object which performs validation checks on
                   this set of data field values.
        """
        if validator is None:
            return

        self._validators.append(validator)


    def removeValidator(self, validator):
        """Removes a validator from the composite.

        @param validator:
                   the Validator object which performs validation checks on
                   this set of data field values.
        """
        self._validators.remove(validator)


    def getSubValidators(self, validatorType):
        """Gets sub-validators by class.

        If the component contains directly or recursively (it contains another
        composite containing the validator) validators compatible with given
        type they are returned. This only applies to C{AND} mode composite
        validators.

        If the validator is in C{OR} mode or does not contain any validators
        of given type null is returned.

        @return: iterable of validators compatible with given type
                that must apply or null if none found.
        """
        if self._mode != self.MODE_AND:
            return None

        found = set()
        for v in self._validators:
            if issubclass(v.__class__, validatorType):
                found.add(v)

            if (isinstance(v, CompositeValidator)
                    and v.getMode() == self.MODE_AND):
                c = v.getSubValidators(validatorType)
                if c is not None:
                    for cc in c:
                        found.add(cc)

        return None if len(found) == 0 else found
