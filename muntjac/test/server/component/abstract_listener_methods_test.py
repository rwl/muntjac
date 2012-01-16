# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

import inspect
import mox

from unittest import TestCase
from muntjac.util import clsname, getSuperClass
from muntjac.ui.component import IComponent

#from muntjac.test.MuntjacClasses import MuntjacClasses


class AbstractListenerMethodsTest(TestCase):

#    @classmethod
#    def main(cls, args):
#        cls.findAllListenerMethods()
#
#
#    @classmethod
#    def findAllListenerMethods(cls):
#        classes = set()
#        for c in MuntjacClasses.getAllServerSideClasses():
#            while c is not None and clsname(c).startswith('com.vaadin.'):
#                classes.add(c)
#                c = getSuperClass(c)
#
#        for c in classes:
#            found = False
#            for name, m in inspect.getmembers(c, inspect.ismethod):
#                if name == 'addListener':
#                    if len(inspect.getargspec(m).args) != 1:
#                        continue
#                    packageName = 'muntjac.test.server'
#                    if issubclass(c, IComponent):
#                        packageName += '.component.' + c.__name__.lower()
#                        continue
#                    if not found:
#                        found = True
#                        print 'package ' + packageName + ';'
#                        print 'import ' + AbstractListenerMethodsTest.getName() + ';'
#                        print 'import ' + c.getName() + ';'
#                        print 'public class ' + c.__name__ + 'Listeners extends ' + AbstractListenerMethodsTest.getSimpleName() + ' {'
#                    listenerClassName = m.getParameterTypes()[0].getSimpleName()
#                    eventClassName = listenerClassName.replaceFirst('Listener$', 'Event')
#                    print 'public void test' + listenerClassName + '() throws Exception {'
#                    print '    testListener(' + c.__name__ + '.class, ' + eventClassName + '.class, ' + listenerClassName + '.class);'
#                    print '}'
#            if found:
#                print '}'
#                print


    def _testListenerAddGetRemove(self, testClass, eventClass,
                listenerClass, c=None):
        # Create a component for testing
        if c is None:
            c = testClass()

#        mockListener1 = mox.CreateMock(listenerClass)
#        mockListener2 = mox.CreateMock(listenerClass)
        mockListener1 = listenerClass()
        mockListener2 = listenerClass()

        # Verify we start from no listeners
        self.verifyListeners(c, eventClass)

        # Add one listener and verify
        self.addListener(c, mockListener1, listenerClass)
        self.verifyListeners(c, eventClass, mockListener1)

        # Add another listener and verify
        self.addListener(c, mockListener2, listenerClass)
        self.verifyListeners(c, eventClass, mockListener1, mockListener2)

        # Ensure we can fetch using parent class also
        if getSuperClass(eventClass) != object:
            self.verifyListeners(c, getSuperClass(eventClass),
                    mockListener1, mockListener2)

        # Remove the first and verify
        self.removeListener(c, mockListener1, listenerClass)
        self.verifyListeners(c, eventClass, mockListener2)

        # Remove the remaining and verify
        self.removeListener(c, mockListener2, listenerClass)
        self.verifyListeners(c, eventClass)


    def removeListener(self, c, listener, listenerClass):
        method = self.getRemoveListenerMethod(c.__class__, listenerClass)
        method(c, listener, listenerClass)


    def addListener(self, c, listener1, listenerClass):
        method = self.getAddListenerMethod(c.__class__, listenerClass)
        method(c, listener1, listenerClass)


    def getListeners(self, c, eventType):
        method = self.getGetListenersMethod(c.__class__)
        return method(c, eventType)


    def getGetListenersMethod(self, cls):
        return getattr(cls, 'getListeners')


    def getAddListenerMethod(self, cls, listenerClass):
        return getattr(cls, 'addListener')


    def getRemoveListenerMethod(self, cls, listenerClass):
        return getattr(cls, 'removeListener')


    def verifyListeners(self, c, eventClass, *expectedListeners):
        registeredListeners = self.getListeners(c, eventClass)
        self.assertEquals(len(expectedListeners), len(registeredListeners))
        self.assertEquals(sorted(expectedListeners),
                sorted(registeredListeners))


if __name__ == '__main__':
    import sys
    AbstractListenerMethodsTest().main(sys.argv)
