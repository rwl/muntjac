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

"""Defines an interface to be implemented by components wishing to display
some object that may be dynamically resized."""


class ISizeable(object):
    """Interface to be implemented by components wishing to display some
    object that may be dynamically resized during runtime.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.3
    """

    #: Unit code representing pixels.
    UNITS_PIXELS = 0

    #: Unit code representing points (1/72nd of an inch).
    UNITS_POINTS = 1

    #: Unit code representing picas (12 points).
    UNITS_PICAS = 2

    #: Unit code representing the font-size of the relevant font.
    UNITS_EM = 3

    #: Unit code representing the x-height of the relevant font.
    UNITS_EX = 4

    #: Unit code representing millimeters.
    UNITS_MM = 5

    #: Unit code representing centimeters.
    UNITS_CM = 6

    #: Unit code representing inches.
    UNITS_INCH = 7

    #: Unit code representing in percentage of the containing element
    #  defined by terminal.
    UNITS_PERCENTAGE = 8

    SIZE_UNDEFINED = -1

    # Textual representations of units symbols. Supported units and
    # their symbols are:
    #
    #   - L{#UNITS_PIXELS}: "px"
    #   - L{#UNITS_POINTS}: "pt"
    #   - L{#UNITS_PICAS}: "pc"
    #   - L{#UNITS_EM}: "em"
    #   - L{#UNITS_EX}: "ex"
    #   - L{#UNITS_MM}: "mm"
    #   - L{#UNITS_CM}. "cm"
    #   - L{#UNITS_INCH}: "in"
    #   - L{#UNITS_PERCENTAGE}: "%"
    #
    # These can be used like C{ISizeable.UNIT_SYMBOLS[UNITS_PIXELS]}.
    UNIT_SYMBOLS = ['px', 'pt', 'pc', 'em', 'ex', 'mm', 'cm', 'in', '%']


    def getWidth(self):
        """Gets the width of the object. Negative number implies unspecified
        size (terminal is free to set the size).

        @return: width of the object in units specified by widthUnits property.
        """
        raise NotImplementedError


    def setWidth(self, *args):
        """Sets the width of the object. Negative number implies unspecified
        size (terminal is free to set the size).

        @param args: tuple of the form
                - (width)
                  1. the width of the object in units specified by widthUnits
                     propertyor in CSS style string representation, null or
                     empty string to reset
                - (width, unit)
                  1. the width of the object.
                  2. the unit used for the width. Possible values include
                     L{UNITS_PIXELS}, L{UNITS_POINTS},
                     L{UNITS_PICAS}, L{UNITS_EM}, L{UNITS_EX},
                     L{UNITS_MM}, L{UNITS_CM}, L{UNITS_INCH},
                     L{UNITS_PERCENTAGE}.

        See U{CSS specification
        <http://www.w3.org/TR/REC-CSS2/syndata.html#value-def-length>} for
        more details.
        """
        raise NotImplementedError


    def getHeight(self):
        """Gets the height of the object. Negative number implies unspecified
        size (terminal is free to set the size).

        @return: height of the object in units specified by heightUnits
                property.
        """
        raise NotImplementedError


    def setHeight(self, *args):
        """Sets the height of the object. Negative number implies unspecified
        size (terminal is free to set the size).

        @param args: tuple of the form
                - (height)
                   1. the height of the object in units specified by
                      heightUnits property or the height of the component using
                      string presentation. String presentation is similar to
                      what is used in Cascading Style Sheets. Size can be
                      length or percentage of available size.
                - (height, unit)
                  1. the height of the object.
                  2. the unit used for the width. Possible values include
                     L{UNITS_PIXELS}, L{UNITS_POINTS},
                     L{UNITS_PICAS}, L{UNITS_EM}, L{UNITS_EX},
                     L{UNITS_MM}, L{UNITS_CM}, L{UNITS_INCH},
                     L{UNITS_PERCENTAGE}.
        """
        raise NotImplementedError


    def getWidthUnits(self):
        """Gets the width property units.

        @return: units used in width property.
        """
        raise NotImplementedError


    def setWidthUnits(self, units):
        """Sets the width property units.

        @param units:
                   the units used in width property.
        @deprecated: Consider setting width and unit simultaneously using
                    L{setWidth}, which is less error-prone.
        """
        raise NotImplementedError


    def getHeightUnits(self):
        """Gets the height property units.

        @return: units used in height property.
        """
        raise NotImplementedError


    def setHeightUnits(self, units):
        """Sets the height property units.

        @param units:
                   the units used in height property.
        @deprecated: Consider setting height and unit simultaneously using
                    L{setHeight} or which is less error-prone.
        """
        raise NotImplementedError


    def setSizeFull(self):
        """Sets the size to 100% x 100%."""
        raise NotImplementedError


    def setSizeUndefined(self):
        """Clears any size settings."""
        raise NotImplementedError
