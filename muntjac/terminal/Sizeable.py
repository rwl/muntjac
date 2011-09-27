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


class Sizeable(object):
    """Interface to be implemented by components wishing to display some object that
    may be dynamically resized during runtime.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Unit code representing pixels.
    UNITS_PIXELS = 0

    # Unit code representing points (1/72nd of an inch).
    UNITS_POINTS = 1

    # Unit code representing picas (12 points).
    UNITS_PICAS = 2

    # Unit code representing the font-size of the relevant font.
    UNITS_EM = 3

    # Unit code representing the x-height of the relevant font.
    UNITS_EX = 4

    # Unit code representing millimeters.
    UNITS_MM = 5

    # Unit code representing centimeters.
    UNITS_CM = 6

    # Unit code representing inches.
    UNITS_INCH = 7

    # Unit code representing in percentage of the containing element defined by
    # terminal.
    UNITS_PERCENTAGE = 8

    SIZE_UNDEFINED = -1

    # Textual representations of units symbols. Supported units and their
    # symbols are:
    # <ul>
    # <li>{@link #UNITS_PIXELS}: "px"</li>
    # <li>{@link #UNITS_POINTS}: "pt"</li>
    # <li>{@link #UNITS_PICAS}: "pc"</li>
    # <li>{@link #UNITS_EM}: "em"</li>
    # <li>{@link #UNITS_EX}: "ex"</li>
    # <li>{@link #UNITS_MM}: "mm"</li>
    # <li>{@link #UNITS_CM}. "cm"</li>
    # <li>{@link #UNITS_INCH}: "in"</li>
    # <li>{@link #UNITS_PERCENTAGE}: "%"</li>
    # </ul>
    # These can be used like <code>Sizeable.UNIT_SYMBOLS[UNITS_PIXELS]</code>.
    UNIT_SYMBOLS = ['px', 'pt', 'pc', 'em', 'ex', 'mm', 'cm', 'in', '%']

    def getWidth(self):
        """Gets the width of the object. Negative number implies unspecified size
        (terminal is free to set the size).

        @return width of the object in units specified by widthUnits property.
        """
        pass


    def setWidth(self, *args):
        """Sets the width of the object. Negative number implies unspecified size
        (terminal is free to set the size).

        @param width
                   the width of the object in units specified by widthUnits
                   property.
        @deprecated Consider using {@link #setWidth(String)} instead. This method
                    works, but is error-prone since the unit must be set
                    separately (and components might have different default
                    unit).
        ---
        Sets the width of the object. Negative number implies unspecified size
        (terminal is free to set the size).

        @param width
                   the width of the object.
        @param unit
                   the unit used for the width. Possible values include
                   {@link #UNITS_PIXELS}, {@link #UNITS_POINTS},
                   {@link #UNITS_PICAS}, {@link #UNITS_EM}, {@link #UNITS_EX},
                   {@link #UNITS_MM}, {@link #UNITS_CM}, {@link #UNITS_INCH},
                   {@link #UNITS_PERCENTAGE}.
        ---
        Sets the width of the component using String presentation.

        String presentation is similar to what is used in Cascading Style Sheets.
        Size can be length or percentage of available size.

        The empty string ("") or null will unset the width and set the units to
        pixels.

        See <a
        href="http://www.w3.org/TR/REC-CSS2/syndata.html#value-def-length">CSS
        specification</a> for more details.

        @param width
                   in CSS style string representation, null or empty string to
                   reset
        """
        pass


    def getHeight(self):
        """Gets the height of the object. Negative number implies unspecified size
        (terminal is free to set the size).

        @return height of the object in units specified by heightUnits property.
        """
        pass


    def setHeight(self, *args):
        """Sets the height of the object. Negative number implies unspecified size
        (terminal is free to set the size).

        @param height
                   the height of the object in units specified by heightUnits
                   property.
        @deprecated Consider using {@link #setHeight(String)} or
                    {@link #setHeight(float, int)} instead. This method works,
                    but is error-prone since the unit must be set separately (and
                    components might have different default unit).
        ---
        Sets the height of the component using String presentation.

        String presentation is similar to what is used in Cascading Style Sheets.
        Size can be length or percentage of available size.

        The empty string ("") or null will unset the height and set the units to
        pixels.

        See <a
        href="http://www.w3.org/TR/REC-CSS2/syndata.html#value-def-length">CSS
        specification</a> for more details.

        @param height
                   in CSS style string representation
        ---
        Sets the height of the object. Negative number implies unspecified size
        (terminal is free to set the size).

        @param height
                   the height of the object.
        @param unit
                   the unit used for the width. Possible values include
                   {@link #UNITS_PIXELS}, {@link #UNITS_POINTS},
                   {@link #UNITS_PICAS}, {@link #UNITS_EM}, {@link #UNITS_EX},
                   {@link #UNITS_MM}, {@link #UNITS_CM}, {@link #UNITS_INCH},
                   {@link #UNITS_PERCENTAGE}.
        """
        pass


    def getWidthUnits(self):
        """Gets the width property units.

        @return units used in width property.
        """
        pass


    def setWidthUnits(self, units):
        """Sets the width property units.

        @param units
                   the units used in width property.
        @deprecated Consider setting width and unit simultaneously using
                    {@link #setWidth(String)} or {@link #setWidth(float, int)},
                    which is less error-prone.
        """
        pass


    def getHeightUnits(self):
        """Gets the height property units.

        @return units used in height property.
        """
        pass


    def setHeightUnits(self, units):
        """Sets the height property units.

        @param units
                   the units used in height property.
        @deprecated Consider setting height and unit simultaneously using
                    {@link #setHeight(String)} or {@link #setHeight(float, int)},
                    which is less error-prone.
        """
        pass


    def setSizeFull(self):
        """Sets the size to 100% x 100%."""
        pass


    def setSizeUndefined(self):
        """Clears any size settings."""
        pass
