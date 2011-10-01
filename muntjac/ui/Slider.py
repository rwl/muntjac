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

from muntjac.ui.AbstractField import AbstractField


class Slider(AbstractField):
    """A component for selecting a numerical value within a range.

    @author IT Mill Ltd.
    @author Richard Lincoln
    """

    #CLIENT_WIDGET = ClientWidget(VSlider, LoadStyle.LAZY)

    ORIENTATION_HORIZONTAL = 0

    ORIENTATION_VERTICAL = 1

    # Style constant representing a scrollbar styled slider. Use this with
    # {@link #addStyleName(String)}. Default styling usually represents a
    # common slider found e.g. in Adobe Photoshop. The client side
    # implementation dictates how different styles will look.
    STYLE_SCROLLBAR = 'scrollbar'


    def __init__(self, *args):
        """Default Slider constructor. Sets all values to defaults and the
        slide handle at minimum value.
        ---
        Create a new slider with the caption given as parameter. All slider
        values set to defaults.

        @param caption
                   The caption for this Slider (e.g. "Volume").
        ---
        Create a new slider with given range and resolution

        @param min
        @param max
        @param resolution
        ---
        Create a new slider with given range

        @param min
        @param max
        ---
        Create a new slider with given caption and range

        @param caption
        @param min
        @param max
        """
        # Minimum value of slider
        self._min = 0

        # Maximum value of slider
        self._max = 100

        # Resolution, how many digits are considered relevant after the
        # decimal point. Must be a non-negative value
        self._resolution = 0

        # Slider orientation (horizontal/vertical), defaults .
        self._orientation = self.ORIENTATION_HORIZONTAL

        # Slider size in pixels. In horizontal mode, if set to -1, allow
        # 100% width of container. In vertical mode, if set to -1, default
        # height is determined by the client-side implementation.
        #
        # @deprecated
        self._size = -1

        # Handle (draggable control element) size in percents relative to
        # base size. Must be a value between 1-99. Other values are converted
        # to nearest bound. A negative value sets the width to auto
        # (client-side implementation calculates).
        #
        # @deprecated The size is dictated by the current theme.
        self._handleSize = -1

        # Show arrows that can be pressed to slide the handle in some
        # increments (client-side implementation decides the increment,
        # usually somewhere between 5-10% of slide range).
        self._arrows = False

        args = args
        nargs = len(args)
        if nargs == 0:
            super(Slider, self)()
            super(Slider, self).setValue(float(self._min))
        elif nargs == 1:
            caption, = args
            self.__init__()
            self.setCaption(caption)
        elif nargs == 2:
            minn, maxx = args
            self.__init__()
            self.setMin(minn)
            self.setMax(maxx)
            self.setResolution(0)
        elif nargs == 3:
            if isinstance(args[0], float):
                minn, maxx, resolution = args
                self.__init__()
                self.setMin(minn)
                self.setMax(maxx)
                self.setResolution(resolution)
            else:
                caption, minn, maxx = args
                self.__init__(minn, maxx)
                self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'


    def getMax(self):
        """Gets the biggest possible value in Sliders range.

        @return the biggest value slider can have
        """
        return self._max


    def setMax(self, maxx):
        """Set the maximum value of the Slider. If the current value of
        the Slider is out of new bounds, the value is set to new minimum.

        @param max: new maximum value of the Slider
        """
        self._max = maxx

        try:
            if float(str( self.getValue() )) > maxx:
                super(Slider, self).setValue( float(maxx) )
        except ValueError:  # ClassCastException
            # FIXME: Handle exception
            # Where does ClassCastException come from? Can't see any casts
            # above
            super(Slider, self).setValue( float(maxx) )

        self.requestRepaint()


    def getMin(self):
        """Gets the minimum value in Sliders range.

        @return the smallest value slider can have
        """
        return self._min


    def setMin(self, minn):
        """Set the minimum value of the Slider. If the current value of
        the Slider is out of new bounds, the value is set to new minimum.

        @param min
                   New minimum value of the Slider.
        """
        self._min = minn

        try:
            if float( str(self.getValue()) ) < minn:
                super(Slider, self).setValue(float(minn))
        except ValueError:  # ClassCastException
            # FIXME: Handle exception
            # Where does ClassCastException come from? Can't see any casts
            # above
            super(Slider, self).setValue(float(minn))

        self.requestRepaint()


    def getOrientation(self):
        """Get the current orientation of the Slider (horizontal or vertical).

        @return orientation
        """
        return self._orientation


    def setOrientation(self, orientation):
        """Set the orientation of the Slider.

        @param int new orientation
        """
        self._orientation = orientation
        self.requestRepaint()


    def getResolution(self):
        """Get the current resolution of the Slider.

        @return resolution
        """
        return self._resolution


    def setResolution(self, resolution):
        """Set a new resolution for the Slider.

        @param resolution
        """
        if resolution < 0:
            return
        self._resolution = resolution
        self.requestRepaint()


    def setValue(self, value, repaintIsNotNeeded=False):
        """Set the value of this Slider.

        @param value
                   New value of Slider. Must be within Sliders range
                   (min - max), otherwise throws an exception.
        @param repaintIsNotNeeded
                   If true, client-side is not requested to repaint itself.
        @throws ValueOutOfBoundsException
        ---
        Set the value of this Slider.

        @param value
                   New value of Slider. Must be within Sliders range
                   (min - max), otherwise throws an exception.
        @throws ValueOutOfBoundsException
        ---
        Set the value of this Slider.

        @param value
                   New value of Slider. Must be within Sliders range
                   (min - max), otherwise throws an exception.
        @throws ValueOutOfBoundsException
        """
        v = value

        if self._resolution > 0:
            # Round up to resolution
            newValue = v * 10**self._resolution
            newValue = newValue / 10**self._resolution
            if (self._min > newValue) or (self._max < newValue):
                raise ValueOutOfBoundsException(value)
        else:
            newValue = v
            if (self._min > newValue) or (self._max < newValue):
                raise ValueOutOfBoundsException(value)

        super(Slider, self).setValue(float(newValue), repaintIsNotNeeded)


    def getSize(self):
        """Get the current Slider size.

        @return size in pixels or -1 for auto sizing.
        @deprecated use standard getWidth/getHeight instead
        """
        return self._size


    def setSize(self, size):
        """Set the size for this Slider.

        @param size
                   in pixels, or -1 auto sizing.
        @deprecated use standard setWidth/setHeight instead
        """
        self._size = size

        if self._orientation == self.ORIENTATION_HORIZONTAL:
            self.setWidth(size, self.UNITS_PIXELS)
        else:
            self.setHeight(size, self.UNITS_PIXELS)

        self.requestRepaint()


    def getHandleSize(self):
        """Get the handle size of this Slider.

        @return handle size in percentages.
        @deprecated The size is dictated by the current theme.
        """
        return self._handleSize


    def setHandleSize(self, handleSize):
        """Set the handle size of this Slider.

        @param handleSize
                   in percentages relative to slider base size.
        @deprecated The size is dictated by the current theme.
        """
        if handleSize < 0:
            self._handleSize = -1
        elif handleSize > 99:
            self._handleSize = 99
        elif handleSize < 1:
            self._handleSize = 1
        else:
            self._handleSize = handleSize

        self.requestRepaint()


    def paintContent(self, target):
        super(Slider, self).paintContent(target)

        target.addAttribute('min', self._min)
        if self._max > self._min:
            target.addAttribute('max', self._max)
        else:
            target.addAttribute('max', self._min)

        target.addAttribute('resolution', self._resolution)

        if self._resolution > 0:
            target.addVariable(self, 'value', float( self.getValue() ))
        else:
            target.addVariable(self, 'value', int( self.getValue() ))

        if self._orientation == self.ORIENTATION_VERTICAL:
            target.addAttribute('vertical', True)

        if self._arrows:
            target.addAttribute('arrows', True)

        if self._size > -1:
            target.addAttribute('size', self._size)

        if self._min != self._max and self._min < self._max:
            target.addAttribute('hsize', self._handleSize)
        else:
            target.addAttribute('hsize', 100)


    def changeVariables(self, source, variables):
        """Invoked when the value of a variable has changed. Slider listeners
        are notified if the slider value has changed.

        @param source
        @param variables
        """
        super(Slider, self).changeVariables(source, variables)

        if 'value' in variables:
            value = variables.get('value')
            newValue = float(str(value))
            if (newValue is not None and newValue != self.getValue()
                    and newValue != self.getValue()):
                # Convert to nearest bound
                try:
                    self.setValue(newValue, True)
                except ValueOutOfBoundsException, e:
                    out = float( e.getValue() )
                    if out < self._min:
                        out = self._min
                    if out > self._max:
                        out = self._max
                    super(Slider, self).setValue(float(out), False)


    def getType(self):
        return float


class ValueOutOfBoundsException(Exception):
    """ValueOutOfBoundsException

    @author IT Mill Ltd.
    @author Richard Lincoln
    """

    def __init__(self, valueOutOfBounds):
        """Constructs an <code>ValueOutOfBoundsException</code> with
        the specified detail message.

        @param valueOutOfBounds
        """
        self._value = valueOutOfBounds


    def getValue(self):
        return self._value
