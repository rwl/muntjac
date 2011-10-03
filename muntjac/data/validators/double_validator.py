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

from muntjac.data.validators.abstract_string_validator import \
    AbstractStringValidator


class DoubleValidator(AbstractStringValidator):
    """String validator for a double precision floating point number. See
    {@link com.vaadin.data.validator.AbstractStringValidator} for more
    information.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 5.4
    """

    def __init__(self, errorMessage):
        """Creates a validator for checking that a string can be parsed as an
        double.

        @param errorMessage
                   the message to display in case the value does not validate.
        """
        super(DoubleValidator, self)(errorMessage)


    def isValidString(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
