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
from com.vaadin.data.Validator import (Validator,)
# from java.util.Collection import (Collection,)
# from java.util.HashSet import (HashSet,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.List import (List,)


class CompositeValidator(AbstractValidator):
    """The <code>CompositeValidator</code> allows you to chain (compose) many
    validators to validate one field. The contained validators may be required to
    all validate the value to validate or it may be enough that one contained
    validator validates the value. This behaviour is controlled by the modes
    <code>AND</code> and <code>OR</code>.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # The validators are combined with <code>AND</code> clause: validity of the
    # composite implies validity of the all validators it is composed of must
    # be valid.

    MODE_AND = 0
    # The validators are combined with <code>OR</code> clause: validity of the
    # composite implies that some of validators it is composed of must be
    # valid.

    MODE_OR = 1
    # The validators are combined with and clause: validity of the composite
    # implies validity of the all validators it is composed of

    MODE_DEFAULT = MODE_AND
    # Operation mode.
    _mode = MODE_DEFAULT
    # List of contained validators.
    _validators = LinkedList()

    def __init__(self, *args):
        """Construct a composite validator in <code>AND</code> mode without error
        message.
        ---
        Constructs a composite validator in given mode.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(CompositeValidator, self)('')
        elif _1 == 2:
            mode, errorMessage = _0
            super(CompositeValidator, self)(errorMessage)
            self.setMode(mode)
        else:
            raise ARGERROR(0, 2)

    def validate(self, value):
        """Validates the given value.
        <p>
        The value is valid, if:
        <ul>
        <li><code>MODE_AND</code>: All of the sub-validators are valid
        <li><code>MODE_OR</code>: Any of the sub-validators are valid
        </ul>

        If the value is invalid, validation error is thrown. If the error message
        is set (non-null), it is used. If the error message has not been set, the
        first error occurred is thrown.
        </p>

        @param value
                   the value to check.
        @throws Validator.InvalidValueException
                    if the value is not valid.
        """
        _0 = self._mode
        _1 = False
        while True:
            if _0 == self.MODE_AND:
                _1 = True
                for validator in self._validators:
                    validator.validate(value)
                return
            if (_1 is True) or (_0 == self.MODE_OR):
                _1 = True
                first = None
                for v in self._validators:
                    try:
                        v.validate(value)
                        return
                    except Validator.InvalidValueException, e:
                        if first is None:
                            first = e
                if first is None:
                    return
                em = self.getErrorMessage()
                if em is not None:
                    raise Validator.InvalidValueException(em)
                else:
                    raise first
            break
        raise self.IllegalStateException('The validator is in unsupported operation mode')

    def isValid(self, value):
        """Checks the validity of the the given value. The value is valid, if:
        <ul>
        <li><code>MODE_AND</code>: All of the sub-validators are valid
        <li><code>MODE_OR</code>: Any of the sub-validators are valid
        </ul>

        @param value
                   the value to check.
        """
        _0 = self._mode
        _1 = False
        while True:
            if _0 == self.MODE_AND:
                _1 = True
                for v in self._validators:
                    if not v.isValid(value):
                        return False
                return True
            if (_1 is True) or (_0 == self.MODE_OR):
                _1 = True
                for v in self._validators:
                    if v.isValid(value):
                        return True
                return False
            break
        raise self.IllegalStateException('The valitor is in unsupported operation mode')

    def getMode(self):
        """Gets the mode of the validator.

        @return Operation mode of the validator: <code>MODE_AND</code> or
                <code>MODE_OR</code>.
        """
        return self._mode

    def setMode(self, mode):
        """Sets the mode of the validator. The valid modes are:
        <ul>
        <li><code>MODE_AND</code> (default)
        <li><code>MODE_OR</code>
        </ul>

        @param mode
                   the mode to set.
        """
        if mode != self.MODE_AND and mode != self.MODE_OR:
            raise self.IllegalArgumentException('Mode ' + mode + ' unsupported')
        self._mode = mode

    def getErrorMessage(self):
        """Gets the error message for the composite validator. If the error message
        is null, original error messages of the sub-validators are used instead.
        """
        if super(CompositeValidator, self).getErrorMessage() is not None:
            return super(CompositeValidator, self).getErrorMessage()
        # TODO Return composite error message
        return None

    def addValidator(self, validator):
        """Adds validator to the interface.

        @param validator
                   the Validator object which performs validation checks on this
                   set of data field values.
        """
        if validator is None:
            return
        self._validators.add(validator)

    def removeValidator(self, validator):
        """Removes a validator from the composite.

        @param validator
                   the Validator object which performs validation checks on this
                   set of data field values.
        """
        self._validators.remove(validator)

    def getSubValidators(self, validatorType):
        """Gets sub-validators by class.

        <p>
        If the component contains directly or recursively (it contains another
        composite containing the validator) validators compatible with given type
        they are returned. This only applies to <code>AND</code> mode composite
        validators.
        </p>

        <p>
        If the validator is in <code>OR</code> mode or does not contain any
        validators of given type null is returned.
        </p>

        @return Collection<Validator> of validators compatible with given type
                that must apply or null if none fould.
        """
        if self._mode != self.MODE_AND:
            return None
        found = set()
        for v in self._validators:
            if validatorType.isAssignableFrom(v.getClass()):
                found.add(v)
            if isinstance(v, CompositeValidator) and v.getMode() == self.MODE_AND:
                c = v.getSubValidators(validatorType)
                if c is not None:
                    found.addAll(c)
        return None if found.isEmpty() else found
