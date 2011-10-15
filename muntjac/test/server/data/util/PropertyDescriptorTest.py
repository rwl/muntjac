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

from com.vaadin.data.util.NestedMethodPropertyTest import (NestedMethodPropertyTest,)
from com.vaadin.data.util.AbstractBeanContainerTest import (AbstractBeanContainerTest,)
# from com.vaadin.data.Property import (Property,)
# from com.vaadin.data.util.NestedPropertyDescriptor import (NestedPropertyDescriptor,)
# from java.beans.Introspector import (Introspector,)
# from java.beans.PropertyDescriptor import (PropertyDescriptor,)
# from junit.framework.Assert import (Assert,)
# from junit.framework.TestCase import (TestCase,)
Person = NestedMethodPropertyTest.Person


class PropertyDescriptorTest(TestCase):

    def testMethodPropertyDescriptorSerialization(self):
        pds = Introspector.getBeanInfo(Person).getPropertyDescriptors()
        descriptor = None
        for pd in pds:
            if 'name' == pd.getName():
                descriptor = MethodPropertyDescriptor(pd.getName(), str, pd.getReadMethod(), pd.getWriteMethod())
                break
        baos = ByteArrayOutputStream()
        ObjectOutputStream(baos).writeObject(descriptor)
        descriptor2 = ObjectInputStream(ByteArrayInputStream(baos.toByteArray())).readObject()
        property = descriptor2.createProperty(Person('John', None))
        Assert.assertEquals('John', property.getValue())

    def testNestedPropertyDescriptorSerialization(self):
        pd = NestedPropertyDescriptor('name', Person)
        baos = ByteArrayOutputStream()
        ObjectOutputStream(baos).writeObject(pd)
        pd2 = ObjectInputStream(ByteArrayInputStream(baos.toByteArray())).readObject()
        property = pd2.createProperty(Person('John', None))
        Assert.assertEquals('John', property.getValue())
