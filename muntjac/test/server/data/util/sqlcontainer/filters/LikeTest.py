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

# from com.vaadin.data.util.ObjectProperty import (ObjectProperty,)
# from com.vaadin.data.util.PropertysetItem import (PropertysetItem,)
# from org.junit.Assert import (Assert,)
# from org.junit.Test import (Test,)


class LikeTest(object):

    def passesFilter_valueIsNotStringType_shouldFail(self):
        like = Like('test', '%foo%')
        item = PropertysetItem()
        item.addItemProperty('test', ObjectProperty(5))
        Assert.assertFalse(like.passesFilter('id', item))

    def passesFilter_containsLikeQueryOnStringContainingValue_shouldSucceed(self):
        like = Like('test', '%foo%')
        item = PropertysetItem()
        item.addItemProperty('test', ObjectProperty('asdfooghij'))
        Assert.assertTrue(like.passesFilter('id', item))

    def passesFilter_containsLikeQueryOnStringContainingValueCaseInsensitive_shouldSucceed(self):
        like = Like('test', '%foo%')
        like.setCaseSensitive(False)
        item = PropertysetItem()
        item.addItemProperty('test', ObjectProperty('asdfOOghij'))
        Assert.assertTrue(like.passesFilter('id', item))

    def passesFilter_containsLikeQueryOnStringContainingValueConstructedCaseInsensitive_shouldSucceed(self):
        like = Like('test', '%foo%', False)
        item = PropertysetItem()
        item.addItemProperty('test', ObjectProperty('asdfOOghij'))
        Assert.assertTrue(like.passesFilter('id', item))

    def passesFilter_containsLikeQueryOnStringNotContainingValue_shouldFail(self):
        like = Like('test', '%foo%')
        item = PropertysetItem()
        item.addItemProperty('test', ObjectProperty('asdbarghij'))
        Assert.assertFalse(like.passesFilter('id', item))

    def passesFilter_containsLikeQueryOnStringExactlyEqualToValue_shouldSucceed(self):
        like = Like('test', '%foo%')
        item = PropertysetItem()
        item.addItemProperty('test', ObjectProperty('foo'))
        Assert.assertTrue(like.passesFilter('id', item))

    def passesFilter_containsLikeQueryOnStringEqualToValueMinusOneCharAtTheEnd_shouldFail(self):
        like = Like('test', '%foo%')
        item = PropertysetItem()
        item.addItemProperty('test', ObjectProperty('fo'))
        Assert.assertFalse(like.passesFilter('id', item))

    def passesFilter_beginsWithLikeQueryOnStringBeginningWithValue_shouldSucceed(self):
        like = Like('test', 'foo%')
        item = PropertysetItem()
        item.addItemProperty('test', ObjectProperty('foobar'))
        Assert.assertTrue(like.passesFilter('id', item))

    def passesFilter_beginsWithLikeQueryOnStringNotBeginningWithValue_shouldFail(self):
        like = Like('test', 'foo%')
        item = PropertysetItem()
        item.addItemProperty('test', ObjectProperty('barfoo'))
        Assert.assertFalse(like.passesFilter('id', item))

    def passesFilter_endsWithLikeQueryOnStringEndingWithValue_shouldSucceed(self):
        like = Like('test', '%foo')
        item = PropertysetItem()
        item.addItemProperty('test', ObjectProperty('barfoo'))
        Assert.assertTrue(like.passesFilter('id', item))

    def passesFilter_endsWithLikeQueryOnStringNotEndingWithValue_shouldFail(self):
        like = Like('test', '%foo')
        item = PropertysetItem()
        item.addItemProperty('test', ObjectProperty('foobar'))
        Assert.assertFalse(like.passesFilter('id', item))

    def passesFilter_startsWithAndEndsWithOnMatchingValue_shouldSucceed(self):
        like = Like('test', 'foo%bar')
        item = PropertysetItem()
        item.addItemProperty('test', ObjectProperty('fooASDFbar'))
        Assert.assertTrue(like.passesFilter('id', item))

    def appliesToProperty_valueIsProperty_shouldBeTrue(self):
        like = Like('test', '%foo')
        Assert.assertTrue(like.appliesToProperty('test'))

    def appliesToProperty_valueIsNotProperty_shouldBeFalse(self):
        like = Like('test', '%foo')
        Assert.assertFalse(like.appliesToProperty('bar'))

    def equals_sameInstances_shouldBeTrue(self):
        like1 = Like('test', '%foo')
        like2 = like1
        Assert.assertTrue(like1 == like2)

    def equals_twoEqualInstances_shouldBeTrue(self):
        like1 = Like('test', 'foo')
        like2 = Like('test', 'foo')
        Assert.assertTrue(like1 == like2)

    def equals_differentValues_shouldBeFalse(self):
        like1 = Like('test', 'foo')
        like2 = Like('test', 'bar')
        Assert.assertFalse(like1 == like2)

    def equals_differentProperties_shouldBeFalse(self):
        like1 = Like('foo', 'test')
        like2 = Like('bar', 'test')
        Assert.assertFalse(like1 == like2)

    def equals_differentPropertiesAndValues_shouldBeFalse(self):
        like1 = Like('foo', 'bar')
        like2 = Like('baz', 'zomg')
        Assert.assertFalse(like1 == like2)

    def equals_differentClasses_shouldBeFalse(self):
        like1 = Like('foo', 'bar')
        obj = self.Object()
        Assert.assertFalse(like1 == obj)

    def equals_bothHaveNullProperties_shouldBeTrue(self):
        like1 = Like(None, 'foo')
        like2 = Like(None, 'foo')
        Assert.assertTrue(like1 == like2)

    def equals_bothHaveNullValues_shouldBeTrue(self):
        like1 = Like('foo', None)
        like2 = Like('foo', None)
        Assert.assertTrue(like1 == like2)

    def equals_onePropertyIsNull_shouldBeFalse(self):
        like1 = Like(None, 'bar')
        like2 = Like('foo', 'baz')
        Assert.assertFalse(like1 == like2)

    def equals_oneValueIsNull_shouldBeFalse(self):
        like1 = Like('foo', None)
        like2 = Like('baz', 'bar')
        Assert.assertFalse(like1 == like2)

    def hashCode_equalInstances_shouldBeEqual(self):
        like1 = Like('test', 'foo')
        like2 = Like('test', 'foo')
        Assert.assertEquals(like1.hashCode(), like2.hashCode())

    def hashCode_differentPropertiesAndValues_shouldNotEqual(self):
        like1 = Like('foo', 'bar')
        like2 = Like('baz', 'zomg')
        Assert.assertTrue(like1.hashCode() != like2.hashCode())
