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

"""String validator comparing the string against a regular expression."""

import re

from muntjac.data.validators.abstract_string_validator import \
    AbstractStringValidator


class RegexpValidator(AbstractStringValidator):
    """String validator comparing the string against a regular expression. Both
    complete matches and substring matches are supported.

    See L{AbstractStringValidator} for more information.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.0
    """

    def __init__(self, *args):
        """Creates a validator for checking that the regular expression matches
        the string to validate.

        @param args: tuple of the form
          - (regexp, errorMessage)
            1. a regular expression
            2. the message to display in case the value does not validate.
          - (regexp, complete, errorMessage)
            1. a regular expression
            2. true to use check for a complete match, false to look for a
               matching substring
            3. the message to display in case the value does not validate.
        """
        self._pattern = None
        self._complete = None
        self._matcher = None

        nargs = len(args)
        if nargs == 2:
            regexp, errorMessage = args
            RegexpValidator.__init__(self, regexp, True, errorMessage)
        elif nargs == 3:
            regexp, complete, errorMessage = args
            super(RegexpValidator, self).__init__(errorMessage)
            self._pattern = re.compile(regexp)  # FIXME: check re use
            self._complete = complete
        else:
            raise ValueError, 'invalid number of arguments'


    def isValidString(self, value):
        if self._complete:
            return self._pattern.match(value)
        else:
            return self._pattern.search(value)  # FIXME: check re use
