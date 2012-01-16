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

from unittest import TestCase
from muntjac.terminal.sizeable import ISizeable
from muntjac.ui.absolute_layout import AbsoluteLayout
from muntjac.ui.button import Button


class ComponentPosition(TestCase):

    _CSS = 'top:7.0px;right:7.0%;bottom:7.0pc;left:7.0em;z-index:7;'
    _PARTIAL_CSS = 'top:7.0px;left:7.0em;'
    _CSS_VALUE = float(7)

    _UNIT_UNSET = ISizeable.UNITS_PIXELS

    def testNoPosition(self):
        """Add component w/o giving positions, assert that everything
        is unset"""
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b)

        self.assertEquals(layout.getPosition(b).getTopValue(), None)
        self.assertEquals(layout.getPosition(b).getBottomValue(), None)
        self.assertEquals(layout.getPosition(b).getLeftValue(), None)
        self.assertEquals(layout.getPosition(b).getRightValue(), None)

        self.assertEquals(self._UNIT_UNSET,
                layout.getPosition(b).getTopUnits())
        self.assertEquals(self._UNIT_UNSET,
                layout.getPosition(b).getBottomUnits())
        self.assertEquals(self._UNIT_UNSET,
                layout.getPosition(b).getLeftUnits())
        self.assertEquals(self._UNIT_UNSET,
                layout.getPosition(b).getRightUnits())

        self.assertEquals(-1, layout.getPosition(b).getZIndex())
        self.assertEquals('', layout.getPosition(b).getCSSString())


    def testFullCss(self):
        """Add component, setting all attributes using CSS, assert
        getter agree"""
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b, self._CSS)

        self.assertEquals(self._CSS_VALUE,
                layout.getPosition(b).getTopValue())
        self.assertEquals(self._CSS_VALUE,
                layout.getPosition(b).getBottomValue())
        self.assertEquals(self._CSS_VALUE,
                layout.getPosition(b).getLeftValue())
        self.assertEquals(self._CSS_VALUE,
                layout.getPosition(b).getRightValue())

        self.assertEquals(ISizeable.UNITS_PIXELS,
                layout.getPosition(b).getTopUnits())
        self.assertEquals(ISizeable.UNITS_PICAS,
                layout.getPosition(b).getBottomUnits())
        self.assertEquals(ISizeable.UNITS_EM,
                layout.getPosition(b).getLeftUnits())
        self.assertEquals(ISizeable.UNITS_PERCENTAGE,
                layout.getPosition(b).getRightUnits())

        self.assertEquals(7, layout.getPosition(b).getZIndex())
        self.assertEquals(self._CSS, layout.getPosition(b).getCSSString())


    def testPartialCss(self):
        """Add component, setting some attributes using CSS, assert
        getters agree"""
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b, self._PARTIAL_CSS)

        self.assertEquals(self._CSS_VALUE,
                layout.getPosition(b).getTopValue())
        self.assertEquals(layout.getPosition(b).getBottomValue(), None)
        self.assertEquals(self._CSS_VALUE,
                layout.getPosition(b).getLeftValue())
        self.assertEquals(layout.getPosition(b).getRightValue(), None)

        self.assertEquals(ISizeable.UNITS_PIXELS,
                layout.getPosition(b).getTopUnits())
        self.assertEquals(self._UNIT_UNSET,
                layout.getPosition(b).getBottomUnits())
        self.assertEquals(ISizeable.UNITS_EM,
                layout.getPosition(b).getLeftUnits())
        self.assertEquals(self._UNIT_UNSET,
                layout.getPosition(b).getRightUnits())
        self.assertEquals(-1,
                layout.getPosition(b).getZIndex())
        self.assertEquals(self._PARTIAL_CSS,
                layout.getPosition(b).getCSSString())


    def testPartialCssReset(self):
        """Add component setting all attributes using CSS, then reset
        using partial CSS; assert getters agree and the appropriate
        attributes are unset.
        """
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b, self._CSS)
        layout.getPosition(b).setCSSString(self._PARTIAL_CSS)

        self.assertEquals(self._CSS_VALUE,
                layout.getPosition(b).getTopValue())
        self.assertIsNone(layout.getPosition(b).getBottomValue(), None)
        self.assertEquals(self._CSS_VALUE,
                layout.getPosition(b).getLeftValue())
        self.assertIsNone(layout.getPosition(b).getRightValue())

        self.assertEquals(ISizeable.UNITS_PIXELS,
                layout.getPosition(b).getTopUnits())
        self.assertEquals(self._UNIT_UNSET,
                layout.getPosition(b).getBottomUnits())
        self.assertEquals(ISizeable.UNITS_EM,
                layout.getPosition(b).getLeftUnits())
        self.assertEquals(self._UNIT_UNSET,
                layout.getPosition(b).getRightUnits())
        self.assertEquals(-1,
                layout.getPosition(b).getZIndex())
        self.assertEquals(self._PARTIAL_CSS,
                layout.getPosition(b).getCSSString())


    def testSetPosition(self):
        """Add component, then set all position attributes with individual
        setters for value and units; assert getters agree.
        """
        SIZE = float(12)
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b)

        layout.getPosition(b).setTopValue(SIZE)
        layout.getPosition(b).setRightValue(SIZE)
        layout.getPosition(b).setBottomValue(SIZE)
        layout.getPosition(b).setLeftValue(SIZE)
        layout.getPosition(b).setTopUnits(ISizeable.UNITS_CM)
        layout.getPosition(b).setRightUnits(ISizeable.UNITS_EX)
        layout.getPosition(b).setBottomUnits(ISizeable.UNITS_INCH)
        layout.getPosition(b).setLeftUnits(ISizeable.UNITS_MM)

        self.assertEquals(SIZE, layout.getPosition(b).getTopValue())
        self.assertEquals(SIZE, layout.getPosition(b).getRightValue())
        self.assertEquals(SIZE, layout.getPosition(b).getBottomValue())
        self.assertEquals(SIZE, layout.getPosition(b).getLeftValue())

        self.assertEquals(ISizeable.UNITS_CM,
                layout.getPosition(b).getTopUnits())
        self.assertEquals(ISizeable.UNITS_EX,
                layout.getPosition(b).getRightUnits())
        self.assertEquals(ISizeable.UNITS_INCH,
                layout.getPosition(b).getBottomUnits())
        self.assertEquals(ISizeable.UNITS_MM,
                layout.getPosition(b).getLeftUnits())


    def testSetPosition2(self):
        """Add component, then set all position attributes with combined
        setters for value and units; assert getters agree.
        """
        SIZE = float(12)
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b)

        layout.getPosition(b).setTop(SIZE, ISizeable.UNITS_CM)
        layout.getPosition(b).setRight(SIZE, ISizeable.UNITS_EX)
        layout.getPosition(b).setBottom(SIZE, ISizeable.UNITS_INCH)
        layout.getPosition(b).setLeft(SIZE, ISizeable.UNITS_MM)

        self.assertEquals(SIZE, layout.getPosition(b).getTopValue())
        self.assertEquals(SIZE, layout.getPosition(b).getRightValue())
        self.assertEquals(SIZE, layout.getPosition(b).getBottomValue())
        self.assertEquals(SIZE, layout.getPosition(b).getLeftValue())

        self.assertEquals(ISizeable.UNITS_CM,
                layout.getPosition(b).getTopUnits())
        self.assertEquals(ISizeable.UNITS_EX,
                layout.getPosition(b).getRightUnits())
        self.assertEquals(ISizeable.UNITS_INCH,
                layout.getPosition(b).getBottomUnits())
        self.assertEquals(ISizeable.UNITS_MM,
                layout.getPosition(b).getLeftUnits())


    def testUnsetPosition(self):
        """Add component, set all attributes using CSS, unset some using
        method calls, assert getters agree.
        """
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b, self._CSS)

        layout.getPosition(b).setTopValue(None)
        layout.getPosition(b).setRightValue(None)
        layout.getPosition(b).setBottomValue(None)
        layout.getPosition(b).setLeftValue(None)
        layout.getPosition(b).setZIndex(-1)

        self.assertEquals(layout.getPosition(b).getTopValue(), None)
        self.assertEquals(layout.getPosition(b).getBottomValue(), None)
        self.assertEquals(layout.getPosition(b).getLeftValue(), None)
        self.assertEquals(layout.getPosition(b).getRightValue(), None)

        self.assertEquals('', layout.getPosition(b).getCSSString())
