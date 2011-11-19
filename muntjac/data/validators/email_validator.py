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

"""String validator for e-mail addresses."""

from muntjac.data.validators.regexp_validator import RegexpValidator


class EmailValidator(RegexpValidator):
    """String validator for e-mail addresses. The e-mail address syntax is not
    complete according to RFC 822 but handles the vast majority of valid e-mail
    addresses correctly.

    See L{AbstractStringValidator} for more information.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.0
    """

    def __init__(self, errorMessage):
        """Creates a validator for checking that a string is a syntactically
        valid e-mail address.

        @param errorMessage:
                   the message to display in case the value does not validate.
        """
        super(EmailValidator, self).__init__(('^([a-zA-Z0-9_\\.\\-+])+'
            '@(([a-zA-Z0-9-])+\\.)+([a-zA-Z0-9]{2,4})+$'), True, errorMessage)
