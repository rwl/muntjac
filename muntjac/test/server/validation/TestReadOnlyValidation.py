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

# from com.vaadin.data.validator.IntegerValidator import (IntegerValidator,)
# from org.junit.Test import (Test,)


class TestReadOnlyValidation(object):

    def testIntegerValidation(self):
        field = TextField()
        field.addValidator(IntegerValidator('Enter a Valid Number'))
        field.setValue(Integer.valueOf.valueOf(10))
        field.validate()
