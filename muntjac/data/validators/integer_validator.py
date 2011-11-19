# Copyright (C) 2011 Vaadin Ltd.
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

"""String validator for integers."""

from muntjac.data.validators.abstract_string_validator import \
    AbstractStringValidator


class IntegerValidator(AbstractStringValidator):
    """String validator for integers. See L{AbstractStringValidator} for more
    information.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.0
    """

    def __init__(self, errorMessage):
        """Creates a validator for checking that a string can be parsed as an
        integer.

        @param errorMessage:
                   the message to display in case the value does not validate.
        """
        super(IntegerValidator, self).__init__(errorMessage)


    def isValidString(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False
