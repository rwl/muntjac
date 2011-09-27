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

from muntjac.data.Container import Filter


class Operation(object):
    EQUAL = 'EQUAL'
    GREATER = 'GREATER'
    LESS = 'LESS'
    GREATER_OR_EQUAL = 'GREATER_OR_EQUAL'
    LESS_OR_EQUAL = 'LESS_OR_EQUAL'
    _values = [EQUAL, GREATER, LESS, GREATER_OR_EQUAL, LESS_OR_EQUAL]

    @classmethod
    def values(cls):
        return cls._values[:]


class Compare(Filter):
    """Simple container filter comparing an item property value against a given
    constant value. Use the nested classes {@link Equal}, {@link Greater},
    {@link Less}, {@link GreaterOrEqual} and {@link LessOrEqual} instead of this
    class directly.

    This filter also directly supports in-memory filtering.

    The reference and actual values must implement {@link Comparable} and the
    class of the actual property value must be assignable from the class of the
    reference value.

    @since 6.6
    """

    def __init__(self, propertyId, value, operation):
        """Constructor for a {@link Compare} filter that compares the value of an
        item property with the given constant <code>value</code>.

        This constructor is intended to be used by the nested static classes only
        ({@link Equal}, {@link Greater}, {@link Less}, {@link GreaterOrEqual},
        {@link LessOrEqual}).

        For in-memory filtering, comparisons except EQUAL require that the values
        implement {@link Comparable} and {@link Comparable#compareTo(Object)} is
        used for the comparison. The equality comparison is performed using
        {@link Object#equals(Object)}.

        For other containers, the comparison implementation is container
        dependent and may use e.g. database comparison operations. Therefore, the
        behavior of comparisons might differ in some cases between in-memory and
        other containers.

        @param propertyId
                   the identifier of the property whose value to compare against
                   value, not null
        @param value
                   the value to compare against - null values may or may not be
                   supported depending on the container
        @param operation
                   the comparison {@link Operation} to use
        """
        self._propertyId = propertyId
        self._value = value
        self._operation = operation


    def passesFilter(self, itemId, item):
        p = item.getItemProperty(self.getPropertyId())
        if None is p:
            return False
        value = p.getValue()
        _0 = self.getOperation()
        _1 = False
        while True:
            if _0 == self.EQUAL:
                _1 = True
                return None is value if None is self._value else self._value == value
            if (_1 is True) or (_0 == self.GREATER):
                _1 = True
                return self.compareValue(value) > 0
            if (_1 is True) or (_0 == self.LESS):
                _1 = True
                return self.compareValue(value) < 0
            if (_1 is True) or (_0 == self.GREATER_OR_EQUAL):
                _1 = True
                return self.compareValue(value) >= 0
            if (_1 is True) or (_0 == self.LESS_OR_EQUAL):
                _1 = True
                return self.compareValue(value) <= 0
            break
        # all cases should have been processed above
        return False


    def compareValue(self, value1):
        if None is self._value:
            return 0 if None is value1 else -1
        elif None is value1:
            return 1
#        elif (
#            isinstance(self.getValue(), Comparable) and value1.getClass().isAssignableFrom(self.getValue().getClass())
#        ):
#            return -self.getValue().compareTo(value1)
        raise self.IllegalArgumentException('Could not compare the arguments: ' + value1 + ', ' + self.getValue())


    def appliesToProperty(self, propertyId):
        return self.getPropertyId() == propertyId


    def equals(self, obj):
        # Only objects of the same class can be equal
        if not (self.getClass() == obj.getClass()):
            return False
        o = obj
        # Checks the properties one by one
        if (
            self.getPropertyId() != o.getPropertyId() and None is not o.getPropertyId() and not (o.getPropertyId() == self.getPropertyId())
        ):
            return False
        if self.getOperation() != o.getOperation():
            return False
        return None is o.getValue() if None is self.getValue() else self.getValue() == o.getValue()


    def hashCode(self):
        return (self.getPropertyId().hashCode() if None is not self.getPropertyId() else 0) ^ (self.getValue().hashCode() if None is not self.getValue() else 0)


    def getPropertyId(self):
        """Returns the property id of the property to compare against the fixed
        value.

        @return property id (not null)
        """
        return self._propertyId


    def getOperation(self):
        """Returns the comparison operation.

        @return {@link Operation}
        """
        return self._operation


    def getValue(self):
        """Returns the value to compare the property against.

        @return comparison reference value
        """
        return self._value


class Equal(Compare):
    """A {@link Compare} filter that accepts items for which the identified
    property value is equal to <code>value</code>.

    For in-memory filters, equals() is used for the comparison. For other
    containers, the comparison implementation is container dependent and may
    use e.g. database comparison operations.

    @since 6.6
    """

    def __init__(self, propertyId, value):
        """Construct a filter that accepts items for which the identified
        property value is equal to <code>value</code>.

        For in-memory filters, equals() is used for the comparison. For other
        containers, the comparison implementation is container dependent and
        may use e.g. database comparison operations.

        @param propertyId
                   the identifier of the property whose value to compare
                   against value, not null
        @param value
                   the value to compare against - null values may or may not
                   be supported depending on the container
        """
        super(Equal, self)(propertyId, value, Operation.EQUAL)


class Greater(Compare):
    """A {@link Compare} filter that accepts items for which the identified
    property value is greater than <code>value</code>.

    For in-memory filters, the values must implement {@link Comparable} and
    {@link Comparable#compareTo(Object)} is used for the comparison. For
    other containers, the comparison implementation is container dependent
    and may use e.g. database comparison operations.

    @since 6.6
    """

    def __init__(self, propertyId, value):
        """Construct a filter that accepts items for which the identified
        property value is greater than <code>value</code>.

        For in-memory filters, the values must implement {@link Comparable}
        and {@link Comparable#compareTo(Object)} is used for the comparison.
        For other containers, the comparison implementation is container
        dependent and may use e.g. database comparison operations.

        @param propertyId
                   the identifier of the property whose value to compare
                   against value, not null
        @param value
                   the value to compare against - null values may or may not
                   be supported depending on the container
        """
        super(Greater, self)(propertyId, value, Operation.GREATER)


class Less(Compare):
    """A {@link Compare} filter that accepts items for which the identified
    property value is less than <code>value</code>.

    For in-memory filters, the values must implement {@link Comparable} and
    {@link Comparable#compareTo(Object)} is used for the comparison. For
    other containers, the comparison implementation is container dependent
    and may use e.g. database comparison operations.

    @since 6.6
    """

    def __init__(self, propertyId, value):
        """Construct a filter that accepts items for which the identified
        property value is less than <code>value</code>.

        For in-memory filters, the values must implement {@link Comparable}
        and {@link Comparable#compareTo(Object)} is used for the comparison.
        For other containers, the comparison implementation is container
        dependent and may use e.g. database comparison operations.

        @param propertyId
                   the identifier of the property whose value to compare
                   against value, not null
        @param value
                   the value to compare against - null values may or may not
                   be supported depending on the container
        """
        super(Less, self)(propertyId, value, Operation.LESS)


class GreaterOrEqual(Compare):
    """A {@link Compare} filter that accepts items for which the identified
    property value is greater than or equal to <code>value</code>.

    For in-memory filters, the values must implement {@link Comparable} and
    {@link Comparable#compareTo(Object)} is used for the comparison. For
    other containers, the comparison implementation is container dependent
    and may use e.g. database comparison operations.

    @since 6.6
    """

    def __init__(self, propertyId, value):
        """Construct a filter that accepts items for which the identified
        property value is greater than or equal to <code>value</code>.

        For in-memory filters, the values must implement {@link Comparable}
        and {@link Comparable#compareTo(Object)} is used for the comparison.
        For other containers, the comparison implementation is container
        dependent and may use e.g. database comparison operations.

        @param propertyId
                   the identifier of the property whose value to compare
                   against value, not null
        @param value
                   the value to compare against - null values may or may not
                   be supported depending on the container
        """
        super(GreaterOrEqual, self)(propertyId, value, Operation.GREATER_OR_EQUAL)


class LessOrEqual(Compare):
    """A {@link Compare} filter that accepts items for which the identified
    property value is less than or equal to <code>value</code>.

    For in-memory filters, the values must implement {@link Comparable} and
    {@link Comparable#compareTo(Object)} is used for the comparison. For
    other containers, the comparison implementation is container dependent
    and may use e.g. database comparison operations.

    @since 6.6
    """

    def __init__(self, propertyId, value):
        """Construct a filter that accepts items for which the identified
        property value is less than or equal to <code>value</code>.

        For in-memory filters, the values must implement {@link Comparable}
        and {@link Comparable#compareTo(Object)} is used for the comparison.
        For other containers, the comparison implementation is container
        dependent and may use e.g. database comparison operations.

        @param propertyId
                   the identifier of the property whose value to compare
                       against value, not null
            @param value
                       the value to compare against - null values may or may not
                       be supported depending on the container
        """
        super(LessOrEqual, self)(propertyId, value, Operation.LESS_OR_EQUAL)
