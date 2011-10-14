# -*- coding: utf-8 -*-
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
