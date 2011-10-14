# -*- coding: utf-8 -*-
# from com.vaadin.data.validator.IntegerValidator import (IntegerValidator,)
# from org.junit.Test import (Test,)


class TestReadOnlyValidation(object):

    def testIntegerValidation(self):
        field = TextField()
        field.addValidator(IntegerValidator('Enter a Valid Number'))
        field.setValue(Integer.valueOf.valueOf(10))
        field.validate()
