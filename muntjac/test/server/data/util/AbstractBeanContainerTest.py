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

from com.vaadin.data.util.AbstractContainerTest import (AbstractContainerTest,)
from com.vaadin.data.util.AbstractInMemoryContainerTest import (AbstractInMemoryContainerTest,)
# from com.vaadin.data.util.AbstractBeanContainer import (AbstractBeanContainer,)


class AbstractBeanContainerTest(AbstractInMemoryContainerTest):
    """Automated test for {@link AbstractBeanContainer}.

    Only a limited subset of the functionality is tested here, the rest in tests
    of subclasses including {@link BeanItemContainer} and {@link BeanContainer}.
    """

    class Person(object):
        _name = None

        def __init__(self, name):
            self.setName(name)

        def setName(self, name):
            self._name = name

        def getName(self):
            return self._name

    class ClassName(object):
        # field names match constants in parent test class
        _fullyQualifiedName = None
        _simpleName = None
        _reverseFullyQualifiedName = None
        _idNumber = None

        def __init__(self, fullyQualifiedName, idNumber):
            self._fullyQualifiedName = fullyQualifiedName
            self._simpleName = AbstractContainerTest.getSimpleName(fullyQualifiedName)
            self._reverseFullyQualifiedName = self.reverse(fullyQualifiedName)
            self._idNumber = idNumber

        def getFullyQualifiedName(self):
            return self._fullyQualifiedName

        def setFullyQualifiedName(self, fullyQualifiedName):
            self._fullyQualifiedName = fullyQualifiedName

        def getSimpleName(self):
            return self._simpleName

        def setSimpleName(self, simpleName):
            self._simpleName = simpleName

        def getReverseFullyQualifiedName(self):
            return self._reverseFullyQualifiedName

        def setReverseFullyQualifiedName(self, reverseFullyQualifiedName):
            self._reverseFullyQualifiedName = reverseFullyQualifiedName

        def getIdNumber(self):
            return self._idNumber

        def setIdNumber(self, idNumber):
            self._idNumber = idNumber
