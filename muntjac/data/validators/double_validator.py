# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""String validator for a double precision floating point number."""

from muntjac.data.validators.abstract_string_validator import \
    AbstractStringValidator


class DoubleValidator(AbstractStringValidator):
    """String validator for a double precision floating point number. See
    L{AbstractStringValidator} for more information.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    def __init__(self, errorMessage):
        """Creates a validator for checking that a string can be parsed as an
        double.

        @param errorMessage:
                   the message to display in case the value does not validate.
        """
        super(DoubleValidator, self).__init__(errorMessage)


    def isValidString(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
