# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

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
    @version: @VERSION@
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
        self._regexp = ''
        self._complete = None
        self._matcher = None

        nargs = len(args)
        if nargs == 2:
            regexp, errorMessage = args
            self._regexp = regexp
            RegexpValidator.__init__(self, regexp, True, errorMessage)
        elif nargs == 3:
            regexp, complete, errorMessage = args
            super(RegexpValidator, self).__init__(errorMessage)
            self._regexp = regexp
            self._pattern = re.compile(regexp)  # FIXME: check re use
            self._complete = complete
        else:
            raise ValueError, 'invalid number of arguments'


    def __getstate__(self):
        result = self.__dict__.copy()
        del result['_pattern']
        return result


    def __setstate__(self, d):
        self.__dict__ = d
        self._pattern = re.compile(d.get('_regexp'))


    def isValidString(self, value):
        if self._complete:
            return self._pattern.match(value)
        else:
            return self._pattern.search(value)  # FIXME: check re use
