# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.data.validator.AbstractValidator import AbstractValidator


class AbstractStringValidator(AbstractValidator):
    """Validator base class for validating strings. See
    {@link com.vaadin.data.validator.AbstractValidator} for more information.

    <p>
    To include the value that failed validation in the exception message you can
    use "{0}" in the error message. This will be replaced with the failed value
    (converted to string using {@link #toString()}) or "null" if the value is
    null.
    </p>

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 5.4
    """

    def __init__(self, errorMessage):
        """Constructs a validator for strings.

        <p>
        Null and empty string values are always accepted. To reject empty values,
        set the field being validated as required.
        </p>

        @param errorMessage
                   the message to be included in an {@link InvalidValueException}
                   (with "{0}" replaced by the value that failed validation).
             *
        """
        super(AbstractStringValidator, self)(errorMessage)


    def isValid(self, value):
        """Tests if the given value is a valid string.
        <p>
        Null values are always accepted. Values that are not {@link String}s are
        converted using {@link #toString()}. Then {@link #isValidString(String)}
        is used to validate the value.
        </p>

        @param value
                   the value to check
        @return true if the value (or its toString()) is a valid string, false
                otherwise
        """
        if value is None:
            return True
        if not isinstance(value, str):
            value = str(value)
        return self.isValidString(value)


    def isValidString(self, value):
        """Checks if the given string is valid.

        @param value
                   String to check. Can never be null.
        @return true if the string is valid, false otherwise
        """
        pass
