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

import pickle

from unittest import TestCase

from muntjac.data.validators.regexp_validator import RegexpValidator
from muntjac.ui.form import Form

from com.vaadin.data.util.method_property import MethodProperty
from muntjac.data.util.indexed_container import IndexedContainer


class TestSerialization(TestCase):

    def testValidators(self):
        validator = RegexpValidator('.*', 'Error')
        validator.isValid('aaa')
        validator2 = self.serializeAndDeserialize(validator)
        validator2.isValid('aaa')


    def testForm(self):
        f = Form()
        propertyId = 'My property'
        f.addItemProperty(propertyId, MethodProperty(Data(),
                'dummyGetterAndSetter'))
        f.replaceWithSelect(propertyId, ['a', 'b', None],
                ['Item a', 'ITem b', 'Null item'])
        self.serializeAndDeserialize(f)


    def testIndedexContainerItemIds(self):
        ic = IndexedContainer()
        ic.addContainerProperty('prop1', str, None)
        idd = ic.addItem()
        ic.getItem(idd).getItemProperty('prop1').setValue('1')
        item2 = ic.addItem('item2')
        item2.getItemProperty('prop1').setValue('2')
        self.serializeAndDeserialize(ic)


    def testMethodPropertyGetter(self):
        mp = MethodProperty(Data(), 'dummyGetter')
        self.serializeAndDeserialize(mp)


    def testMethodPropertyGetterAndSetter(self):
        mp = MethodProperty(Data(), 'dummyGetterAndSetter')
        self.serializeAndDeserialize(mp)


    def testMethodPropertyInt(self):
        mp = MethodProperty(Data(), 'dummyInt')
        self.serializeAndDeserialize(mp)


    @classmethod
    def serializeAndDeserialize(cls, s):
        # Serialize and deserialize

        bs = pickle.dumps(s)
        s2 = pickle.loads(bs)
        if s == s2:
            print s + ' equals ' + s2
        else:
            print s + ' does NOT equal ' + s2
        return s2


class Data(object):

    def __init__(self):
        self._dummyGetter = ''
        self._dummyGetterAndSetter = ''
        self._dummyInt = 0

    def getDummyGetterAndSetter(self):
        return self._dummyGetterAndSetter

    def setDummyGetterAndSetter(self, dummyGetterAndSetter):
        self._dummyGetterAndSetter = dummyGetterAndSetter

    def getDummyInt(self):
        return self._dummyInt

    def setDummyInt(self, dummyInt):
        self._dummyInt = dummyInt

    def getDummyGetter(self):
        return self._dummyGetter
