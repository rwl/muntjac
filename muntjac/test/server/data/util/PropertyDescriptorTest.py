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

from muntjac.test.server.data.util.NestedMethodPropertyTest import \
    NestedMethodPropertyTest

from muntjac.test.server.data.util.AbstractBeanContainerTest import Person

from muntjac.data.util.nested_property_descriptor import \
    NestedPropertyDescriptor

from muntjac.data.util.method_property_descriptor import \
    MethodPropertyDescriptor


class PropertyDescriptorTest(TestCase):

    def testMethodPropertyDescriptorSerialization(self):
        pds = Introspector.getBeanInfo(Person).getPropertyDescriptors()
        descriptor = None
        for pd in pds:
            if 'name' == pd.getName():
                descriptor = MethodPropertyDescriptor(pd.getName(), str,
                        pd.getReadMethod(), pd.getWriteMethod())
                break
        baos = pickle.dumps(descriptor)
        descriptor2 = pickle.loads(baos)
        prop = descriptor2.createProperty(Person('John', None))
        self.assertEquals('John', prop.getValue())


    def testNestedPropertyDescriptorSerialization(self):
        pd = NestedPropertyDescriptor('name', Person)
        baos = pickle.dumps(pd)
        pd2 = pickle.loads(baos)
        prop = pd2.createProperty(Person('John', None))
        self.assertEquals('John', prop.getValue())
