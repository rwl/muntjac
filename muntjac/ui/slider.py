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

"""Defines a component for selecting a numerical value within a range."""

from muntjac.ui.abstract_field import AbstractField


class Slider(AbstractField):
    """A component for selecting a numerical value within a range.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    """

    CLIENT_WIDGET = None #ClientWidget(VSlider, LoadStyle.LAZY)

    ORIENTATION_HORIZONTAL = 0

    ORIENTATION_VERTICAL = 1

    #: Style constant representing a scrollbar styled slider. Use this with
    #  L{#addStyleName(String)}. Default styling usually represents a
    #  common slider found e.g. in Adobe Photoshop. The client side
    #  implementation dictates how different styles will look.
    STYLE_SCROLLBAR = 'scrollbar'


    def __init__(self, *args):
        """Slider constructor.

        @param args: tuple of the form
            - ()
            - (caption)
              1. The caption for this Slider (e.g. "Volume").
            - (min, max, resolution)
            - (min, max)
            - (caption, min, max)
        """
        #: Minimum value of slider
        self._min = 0

        #: Maximum value of slider
        self._max = 100

        #: Resolution, how many digits are considered relevant after the
        #  decimal point. Must be a non-negative value
        self._resolution = 0

        #: Slider orientation (horizontal/vertical), defaults .
        self._orientation = self.ORIENTATION_HORIZONTAL

        #: Slider size in pixels. In horizontal mode, if set to -1, allow
        #  100% width of container. In vertical mode, if set to -1, default
        #  height is determined by the client-side implementation.
        #
        # @deprecated
        self._size = -1

        #: Handle (draggable control element) size in percents relative to
        #  base size. Must be a value between 1-99. Other values are converted
        #  to nearest bound. A negative value sets the width to auto
        #  (client-side implementation calculates).
        #
        # @deprecated: The size is dictated by the current theme.
        self._handleSize = -1

        #: Show arrows that can be pressed to slide the handle in some
        #  increments (client-side implementation decides the increment,
        #  usually somewhere between 5-10% of slide range).
        self._arrows = False

        args = args
        nargs = len(args)
        if nargs == 0:
            super(Slider, self).__init__()
            super(Slider, self).setValue(float(self._min))
        elif nargs == 1:
            caption, = args
            Slider.__init__(self)
            self.setCaption(caption)
        elif nargs == 2:
            minn, maxx = args
            Slider.__init__(self)
            self.setMin(minn)
            self.setMax(maxx)
            self.setResolution(0)
        elif nargs == 3:
            if isinstance(args[0], float):
                minn, maxx, resolution = args
                Slider.__init__(self)
                self.setMin(minn)
                self.setMax(maxx)
                self.setResolution(resolution)
            else:
                caption, minn, maxx = args
                Slider.__init__(self, minn, maxx)
                self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'


    def getMax(self):
        """Gets the biggest possible value in Sliders range.

        @return: the biggest value slider can have
        """
        return self._max


    def setMax(self, maximum):
        """Set the maximum value of the Slider. If the current value of
        the Slider is out of new bounds, the value is set to new minimum.

        @param maximum: new maximum value of the Slider
        """
        self._max = maximum

        try:
            if float(str( self.getValue() )) > maximum:
                super(Slider, self).setValue( float(maximum) )
        except ValueError:  # ClassCastException
            # FIXME: Handle exception
            # Where does ClassCastException come from? Can't see any casts
            # above
            super(Slider, self).setValue( float(maximum) )

        self.requestRepaint()


    def getMin(self):
        """Gets the minimum value in Sliders range.

        @return: the smallest value slider can have
        """
        return self._min


    def setMin(self, minimum):
        """Set the minimum value of the Slider. If the current value of
        the Slider is out of new bounds, the value is set to new minimum.

        @param minimum:
                   New minimum value of the Slider.
        """
        self._min = minimum

        try:
            if float( str(self.getValue()) ) < minimum:
                super(Slider, self).setValue(float(minimum))
        except ValueError:  # ClassCastException
            # FIXME: Handle exception
            # Where does ClassCastException come from? Can't see any casts
            # above
            super(Slider, self).setValue(float(minimum))

        self.requestRepaint()


    def getOrientation(self):
        """Get the current orientation of the Slider (horizontal or vertical).

        @return: orientation
        """
        return self._orientation


    def setOrientation(self, orientation):
        """Set the orientation of the Slider.
        """
        self._orientation = orientation
        self.requestRepaint()


    def getResolution(self):
        """Get the current resolution of the Slider.

        @return: resolution
        """
        return self._resolution


    def setResolution(self, resolution):
        """Set a new resolution for the Slider.
        """
        if resolution < 0:
            return
        self._resolution = resolution
        self.requestRepaint()


    def setValue(self, value, repaintIsNotNeeded=False):
        """Set the value of this Slider.

        @param value:
                   New value of Slider. Must be within Sliders range
                   (min - max), otherwise throws an exception.
        @param repaintIsNotNeeded:
                   If true, client-side is not requested to repaint itself.
        @raise ValueOutOfBoundsException:
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

        @return: size in pixels or -1 for auto sizing.
        @deprecated: use standard getWidth/getHeight instead
        """
        return self._size


    def setSize(self, size):
        """Set the size for this Slider.

        @param size:
                   in pixels, or -1 auto sizing.
        @deprecated: use standard setWidth/setHeight instead
        """
        self._size = size

        if self._orientation == self.ORIENTATION_HORIZONTAL:
            self.setWidth(size, self.UNITS_PIXELS)
        else:
            self.setHeight(size, self.UNITS_PIXELS)

        self.requestRepaint()


    def getHandleSize(self):
        """Get the handle size of this Slider.

        @return: handle size in percentages.
        @deprecated: The size is dictated by the current theme.
        """
        return self._handleSize


    def setHandleSize(self, handleSize):
        """Set the handle size of this Slider.

        @param handleSize:
                   in percentages relative to slider base size.
        @deprecated: The size is dictated by the current theme.
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

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    """

    def __init__(self, valueOutOfBounds):
        """Constructs an C{ValueOutOfBoundsException} with
        the specified detail message.
        """
        self._value = valueOutOfBounds


    def getValue(self):
        return self._value
