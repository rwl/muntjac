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
from com.vaadin.data.validator.AbstractStringValidator import (AbstractStringValidator,)
# from java.util.regex.Matcher import (Matcher,)
# from java.util.regex.Pattern import (Pattern,)


class RegexpValidator(AbstractStringValidator):
    """String validator comparing the string against a Java regular expression. Both
    complete matches and substring matches are supported.

    <p>
    For the Java regular expression syntax, see
    {@link java.util.regex.Pattern#sum}
    </p>
    <p>
    See {@link com.vaadin.data.validator.AbstractStringValidator} for more
    information.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 5.4
    """
    _pattern = None
    _complete = None
    _matcher = None

    def __init__(self, *args):
        """Creates a validator for checking that the regular expression matches the
        complete string to validate.

        @param regexp
                   a Java regular expression
        @param errorMessage
                   the message to display in case the value does not validate.
        ---
        Creates a validator for checking that the regular expression matches the
        string to validate.

        @param regexp
                   a Java regular expression
        @param complete
                   true to use check for a complete match, false to look for a
                   matching substring
        @param errorMessage
                   the message to display in case the value does not validate.
        """
        _0 = args
        _1 = len(args)
        if _1 == 2:
            regexp, errorMessage = _0
            self.__init__(regexp, True, errorMessage)
        elif _1 == 3:
            regexp, complete, errorMessage = _0
            super(RegexpValidator, self)(errorMessage)
            self._pattern = Pattern.compile(regexp)
            self._complete = complete
        else:
            raise ARGERROR(2, 3)

    def isValidString(self, value):
        if self._complete:
            return self.getMatcher(value).matches()
        else:
            return self.getMatcher(value).find()

    def getMatcher(self, value):
        """Get a new or reused matcher for the pattern

        @param value
                   the string to find matches in
        @return Matcher for the string
        """
        if self._matcher is None:
            self._matcher = self._pattern.matcher(value)
        else:
            self._matcher.reset(value)
        return self._matcher
