# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""String validator for integers."""

from muntjac.data.validators.abstract_string_validator import \
    AbstractStringValidator


class IntegerValidator(AbstractStringValidator):
    """String validator for integers. See L{AbstractStringValidator} for more
    information.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
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
