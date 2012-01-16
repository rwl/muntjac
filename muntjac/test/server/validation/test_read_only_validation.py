# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from unittest import TestCase

from muntjac.data.validators.integer_validator import IntegerValidator
from muntjac.ui.text_field import TextField


class TestReadOnlyValidation(TestCase):

    def testIntegerValidation(self):
        field = TextField()
        field.addValidator(IntegerValidator('Enter a Valid Number'))
        field.setValue(int(10))
        field.validate()
