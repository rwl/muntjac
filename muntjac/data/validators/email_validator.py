# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""String validator for e-mail addresses."""

from muntjac.data.validators.regexp_validator import RegexpValidator


class EmailValidator(RegexpValidator):
    """String validator for e-mail addresses. The e-mail address syntax is not
    complete according to RFC 822 but handles the vast majority of valid e-mail
    addresses correctly.

    See L{AbstractStringValidator} for more information.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    def __init__(self, errorMessage):
        """Creates a validator for checking that a string is a syntactically
        valid e-mail address.

        @param errorMessage:
                   the message to display in case the value does not validate.
        """
        super(EmailValidator, self).__init__(('^([a-zA-Z0-9_\\.\\-+])+'
            '@(([a-zA-Z0-9-])+\\.)+([a-zA-Z0-9]{2,4})+$'), True, errorMessage)
