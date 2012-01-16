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

"""Defines an interface to be implemented by components wishing to display
some object that may be dynamically resized."""


class ISizeable(object):
    """Interface to be implemented by components wishing to display some
    object that may be dynamically resized during runtime.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
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
