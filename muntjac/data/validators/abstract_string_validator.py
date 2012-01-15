# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Validator base class for validating strings."""

from muntjac.data.validators.abstract_validator import AbstractValidator


class AbstractStringValidator(AbstractValidator):
    """Validator base class for validating strings. See L{AbstractValidator}
    for more information.

    To include the value that failed validation in the exception message you
    can use "{0}" in the error message. This will be replaced with the failed
    value (converted to string using L{__str__}) or "None" if the value is
    C{None}.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    def __init__(self, errorMessage):
        """Constructs a validator for strings.

        None and empty string values are always accepted. To reject empty
        values, set the field being validated as required.

        @param errorMessage:
                   the message to be included in an L{InvalidValueException}
                   (with "{0}" replaced by the value that failed validation).
        """
        super(AbstractStringValidator, self).__init__(errorMessage)


    def isValid(self, value):
        """Tests if the given value is a valid string.

        None values are always accepted. Values that are not strings are
        converted using L{__str__}. Then L{isValidString} is used to validate
        the value.

        @param value:
                   the value to check
        @return: true if the value (or its __str__) is a valid string, false
                otherwise
        """
        if value is None:
            return True

        if not isinstance(value, str):
            value = str(value)

        return self.isValidString(value)


    def isValidString(self, value):
        """Checks if the given string is valid.

        @param value:
                   String to check. Can never be None.
        @return: true if the string is valid, false otherwise
        """
        pass
