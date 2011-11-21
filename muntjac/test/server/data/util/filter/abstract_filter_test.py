# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from unittest import TestCase

from muntjac.data.container import IFilter
from muntjac.data.property import IProperty, ReadOnlyException
from muntjac.data.util.object_property import ObjectProperty
from muntjac.data.util.propertyset_item import PropertysetItem


class AbstractFilterTest(TestCase):

    PROPERTY1 = 'property1'
    PROPERTY2 = 'property2'


class TestItem(PropertysetItem):

    def __init__(self, value1, value2):
        super(TestItem, self).__init__()

        self.addItemProperty(AbstractFilterTest.PROPERTY1,
                ObjectProperty(value1))
        self.addItemProperty(AbstractFilterTest.PROPERTY2,
                ObjectProperty(value2))


class NullProperty(IProperty):

    def getValue(self):
        return None


    def setValue(self, newValue):
        raise ReadOnlyException()


    def getType(self):
        return str


    def isReadOnly(self):
        return True


    def setReadOnly(self, newStatus):
        pass  # do nothing


    def __str__(self):
        return ""


class SameItemFilter(IFilter):

    def __init__(self, item, propertyId=''):
        self._item = item
        self._propertyId = propertyId


    def passesFilter(self, itemId, item):
        return self._item == item


    def appliesToProperty(self, propertyId):
        if self._propertyId is not None:
            return self._propertyId == propertyId
        else:
            return True


    def __eq__(self, obj):
        if (obj is None) or (self.__class__ != obj.__class__):
            return False

        other = obj

        if self._propertyId is None:
            return self._item == other.item and other.propertyId is None
        else:
            return self._propertyId == other.propertyId


    def __hash__(self):
        return hash(self._item)
