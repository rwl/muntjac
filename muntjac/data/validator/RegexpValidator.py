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

import re

from muntjac.data.validator.AbstractStringValidator import AbstractStringValidator


class RegexpValidator(AbstractStringValidator):
    """String validator comparing the string against a Java regular expression. Both
    complete matches and substring matches are supported.

    For the Java regular expression syntax, see
    {@link java.util.regex.Pattern#sum}

    See {@link com.vaadin.data.validator.AbstractStringValidator} for more
    information.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 5.4
    """

    def __init__(self, *args):
        """Creates a validator for checking that the regular expression matches the
        complete string to validate.

        @param regexp
                   a regular expression
        @param errorMessage
                   the message to display in case the value does not validate.
        ---
        Creates a validator for checking that the regular expression matches the
        string to validate.

        @param regexp
                   a regular expression
        @param complete
                   true to use check for a complete match, false to look for a
                   matching substring
        @param errorMessage
                   the message to display in case the value does not validate.
        """
        self._pattern = None
        self._complete = None
        self._matcher = None

        nargs = len(args)
        if nargs == 2:
            regexp, errorMessage = args
            self.__init__(regexp, True, errorMessage)
        elif nargs == 3:
            regexp, complete, errorMessage = args
            super(RegexpValidator, self)(errorMessage)
            self._pattern = re.compile(regexp)  # FIXME: check re use
            self._complete = complete
        else:
            raise ValueError, 'invalid number of arguments'


    def isValidString(self, value):
        if self._complete:
            return self._pattern.match(value)
        else:
            return self._pattern.search(value)  # FIXME: check re use
