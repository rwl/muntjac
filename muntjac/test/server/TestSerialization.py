# -*- coding: utf-8 -*-
# from com.vaadin.data.Item import (Item,)
# from com.vaadin.data.util.MethodProperty import (MethodProperty,)
# from com.vaadin.data.validator.RegexpValidator import (RegexpValidator,)
# from com.vaadin.ui.Form import (Form,)
# from java.io.ByteArrayInputStream import (ByteArrayInputStream,)
# from java.io.ByteArrayOutputStream import (ByteArrayOutputStream,)
# from java.io.ObjectInputStream import (ObjectInputStream,)
# from java.io.ObjectOutputStream import (ObjectOutputStream,)
# from junit.framework.TestCase import (TestCase,)


class TestSerialization(TestCase):

    def testValidators(self):
        validator = RegexpValidator('.*', 'Error')
        validator.isValid('aaa')
        validator2 = self.serializeAndDeserialize(validator)
        validator2.isValid('aaa')

    def testForm(self):
        f = Form()
        propertyId = 'My property'
        f.addItemProperty(propertyId, MethodProperty(self.Data(), 'dummyGetterAndSetter'))
        f.replaceWithSelect(propertyId, ['a', 'b', None], ['Item a', 'ITem b', 'Null item'])
        self.serializeAndDeserialize(f)

    def testIndedexContainerItemIds(self):
        ic = IndexedContainer()
        ic.addContainerProperty('prop1', str, None)
        id = ic.addItem()
        ic.getItem(id).getItemProperty('prop1').setValue('1')
        item2 = ic.addItem('item2')
        item2.getItemProperty('prop1').setValue('2')
        self.serializeAndDeserialize(ic)

    def testMethodPropertyGetter(self):
        mp = MethodProperty(self.Data(), 'dummyGetter')
        self.serializeAndDeserialize(mp)

    def testMethodPropertyGetterAndSetter(self):
        mp = MethodProperty(self.Data(), 'dummyGetterAndSetter')
        self.serializeAndDeserialize(mp)

    def testMethodPropertyInt(self):
        mp = MethodProperty(self.Data(), 'dummyInt')
        self.serializeAndDeserialize(mp)

    @classmethod
    def serializeAndDeserialize(cls, s):
        # Serialize and deserialize
        bs = ByteArrayOutputStream()
        out = ObjectOutputStream(bs)
        out.writeObject(s)
        data = bs.toByteArray()
        in_ = ObjectInputStream(ByteArrayInputStream(data))
        s2 = in_.readObject()
        if s == s2:
            print s + ' equals ' + s2
        else:
            print s + ' does NOT equal ' + s2
        return s2

    class Data(Serializable):
        _dummyGetter = None
        _dummyGetterAndSetter = None
        _dummyInt = None

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
