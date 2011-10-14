# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
# from com.vaadin.tests.VaadinClasses import (VaadinClasses,)
# from com.vaadin.ui.Component import (Component,)
# from java.lang.reflect.InvocationTargetException import (InvocationTargetException,)
# from java.lang.reflect.Method import (Method,)
# from java.util.Collection import (Collection,)
# from java.util.HashSet import (HashSet,)
# from java.util.Set import (Set,)
# from junit.framework.TestCase import (TestCase,)
# from org.easymock.EasyMock import (EasyMock,)
# from org.junit.Assert import (Assert,)


class AbstractListenerMethodsTest(TestCase):

    @classmethod
    def main(cls, args):
        cls.findAllListenerMethods()

    @classmethod
    def findAllListenerMethods(cls):
        classes = set()
        for c in VaadinClasses.getAllServerSideClasses():
            while c is not None and c.getName().startswith('com.vaadin.'):
                classes.add(c)
                c = c.getSuperclass()
        for c in classes:
            found = False
            for m in c.getDeclaredMethods():
                if m.getName() == 'addListener':
                    if m.getParameterTypes().length != 1:
                        continue
                    packageName = 'com.vaadin.tests.server'
                    if Component.isAssignableFrom(c):
                        packageName += '.component.' + c.__name__.toLowerCase()
                        continue
                    if not found:
                        found = True
                        print 'package ' + packageName + ';'
                        print 'import ' + AbstractListenerMethodsTest.getName() + ';'
                        print 'import ' + c.getName() + ';'
                        print 'public class ' + c.__name__ + 'Listeners extends ' + AbstractListenerMethodsTest.getSimpleName() + ' {'
                    listenerClassName = m.getParameterTypes()[0].getSimpleName()
                    eventClassName = listenerClassName.replaceFirst('Listener$', 'Event')
                    print 'public void test' + listenerClassName + '() throws Exception {'
                    print '    testListener(' + c.__name__ + '.class, ' + eventClassName + '.class, ' + listenerClassName + '.class);'
                    print '}'
            if found:
                print '}'
                print 

    def testListenerAddGetRemove(self, *args):
        # Create a component for testing
        _0 = args
        _1 = len(args)
        if _1 == 3:
            testClass, eventClass, listenerClass = _0
            c = testClass()
            self.testListenerAddGetRemove(testClass, eventClass, listenerClass, c)
        elif _1 == 4:
            cls, eventClass, listenerClass, c = _0
            mockListener1 = EasyMock.createMock(listenerClass)
            mockListener2 = EasyMock.createMock(listenerClass)
            # Verify we start from no listeners
            self.verifyListeners(c, eventClass)
            # Add one listener and verify
            self.addListener(c, mockListener1, listenerClass)
            self.verifyListeners(c, eventClass, mockListener1)
            # Add another listener and verify
            self.addListener(c, mockListener2, listenerClass)
            self.verifyListeners(c, eventClass, mockListener1, mockListener2)
            # Ensure we can fetch using parent class also
            if eventClass.getSuperclass() is not None:
                self.verifyListeners(c, eventClass.getSuperclass(), mockListener1, mockListener2)
            # Remove the first and verify
            self.removeListener(c, mockListener1, listenerClass)
            self.verifyListeners(c, eventClass, mockListener2)
            # Remove the remaining and verify
            self.removeListener(c, mockListener2, listenerClass)
            self.verifyListeners(c, eventClass)
        else:
            raise ARGERROR(3, 4)

    def removeListener(self, c, listener, listenerClass):
        method = self.getRemoveListenerMethod(c.getClass(), listenerClass)
        method.invoke(c, listener)

    def addListener(self, c, listener1, listenerClass):
        method = self.getAddListenerMethod(c.getClass(), listenerClass)
        method.invoke(c, listener1)

    def getListeners(self, c, eventType):
        method = self.getGetListenersMethod(c.getClass())
        return method.invoke(c, eventType)

    def getGetListenersMethod(self, cls):
        return cls.getMethod('getListeners', self.Class)

    def getAddListenerMethod(self, cls, listenerClass):
        return cls.getMethod('addListener', listenerClass)

    def getRemoveListenerMethod(self, cls, listenerClass):
        return cls.getMethod('removeListener', listenerClass)

    def verifyListeners(self, c, eventClass, *expectedListeners):
        registeredListeners = self.getListeners(c, eventClass)
        self.assertEquals('Number of listeners', expectedListeners.length, len(registeredListeners))
        Assert.assertArrayEquals(expectedListeners, list(registeredListeners))


if __name__ == '__main__':
    import sys
    AbstractListenerMethodsTest().main(sys.argv)
