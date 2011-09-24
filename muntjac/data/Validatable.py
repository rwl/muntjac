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


class Validatable(object):
    """<p>
    Interface for validatable objects. Defines methods to verify if the object's
    value is valid or not, and to add, remove and list registered validators of
    the object.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    @see com.vaadin.data.Validator
    """

    def addValidator(self, validator):
        """<p>
        Adds a new validator for this object. The validator's
        {@link Validator#validate(Object)} method is activated every time the
        object's value needs to be verified, that is, when the {@link #isValid()}
        method is called. This usually happens when the object's value changes.
        </p>

        @param validator
                   the new validator
        """
        pass


    def removeValidator(self, validator):
        """<p>
        Removes a previously registered validator from the object. The specified
        validator is removed from the object and its <code>validate</code> method
        is no longer called in {@link #isValid()}.
        </p>

        @param validator
                   the validator to remove
        """
        pass


    def getValidators(self):
        """<p>
        Lists all validators currently registered for the object. If no
        validators are registered, returns <code>null</code>.
        </p>

        @return collection of validators or <code>null</code>
        """
        pass


    def isValid(self):
        """<p>
        Tests the current value of the object against all registered validators.
        The registered validators are iterated and for each the
        {@link Validator#validate(Object)} method is called. If any validator
        throws the {@link Validator.InvalidValueException} this method returns
        <code>false</code>.
        </p>

        @return <code>true</code> if the registered validators concur that the
                value is valid, <code>false</code> otherwise
        """
        pass


    def validate(self):
        """<p>
        Checks the validity of the validatable. If the validatable is valid this
        method should do nothing, and if it's not valid, it should throw
        <code>Validator.InvalidValueException</code>
        </p>

        @throws Validator.InvalidValueException
                    if the value is not valid
        """
        pass


    def isInvalidAllowed(self):
        """<p>
        Checks the validabtable object accept invalid values.The default value is
        <code>true</code>.
        </p>
        """
        pass


    def setInvalidAllowed(self, invalidValueAllowed):
        """<p>
        Should the validabtable object accept invalid values. Supporting this
        configuration possibility is optional. By default invalid values are
        allowed.
        </p>

        @param invalidValueAllowed

        @throws UnsupportedOperationException
                    if the setInvalidAllowed is not supported.
        """
        pass
