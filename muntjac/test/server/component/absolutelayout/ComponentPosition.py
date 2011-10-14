# -*- coding: utf-8 -*-
# from com.vaadin.terminal.Sizeable import (Sizeable,)
# from com.vaadin.ui.AbsoluteLayout import (AbsoluteLayout,)
# from com.vaadin.ui.Button import (Button,)
# from junit.framework.TestCase import (TestCase,)


class ComponentPosition(TestCase):
    _CSS = 'top:7.0px;right:7.0%;bottom:7.0pc;left:7.0em;z-index:7;'
    _PARTIAL_CSS = 'top:7.0px;left:7.0em;'
    _CSS_VALUE = Float.valueOf.valueOf(7)
    _UNIT_UNSET = Sizeable.UNITS_PIXELS

    def testNoPosition(self):
        """Add component w/o giving positions, assert that everything is unset"""
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b)
        self.assertNull(layout.getPosition(b).getTopValue())
        self.assertNull(layout.getPosition(b).getBottomValue())
        self.assertNull(layout.getPosition(b).getLeftValue())
        self.assertNull(layout.getPosition(b).getRightValue())
        self.assertEquals(self._UNIT_UNSET, layout.getPosition(b).getTopUnits())
        self.assertEquals(self._UNIT_UNSET, layout.getPosition(b).getBottomUnits())
        self.assertEquals(self._UNIT_UNSET, layout.getPosition(b).getLeftUnits())
        self.assertEquals(self._UNIT_UNSET, layout.getPosition(b).getRightUnits())
        self.assertEquals(-1, layout.getPosition(b).getZIndex())
        self.assertEquals('', layout.getPosition(b).getCSSString())

    def testFullCss(self):
        """Add component, setting all attributes using CSS, assert getter agree"""
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b, self._CSS)
        self.assertEquals(self._CSS_VALUE, layout.getPosition(b).getTopValue())
        self.assertEquals(self._CSS_VALUE, layout.getPosition(b).getBottomValue())
        self.assertEquals(self._CSS_VALUE, layout.getPosition(b).getLeftValue())
        self.assertEquals(self._CSS_VALUE, layout.getPosition(b).getRightValue())
        self.assertEquals(Sizeable.UNITS_PIXELS, layout.getPosition(b).getTopUnits())
        self.assertEquals(Sizeable.UNITS_PICAS, layout.getPosition(b).getBottomUnits())
        self.assertEquals(Sizeable.UNITS_EM, layout.getPosition(b).getLeftUnits())
        self.assertEquals(Sizeable.UNITS_PERCENTAGE, layout.getPosition(b).getRightUnits())
        self.assertEquals(7, layout.getPosition(b).getZIndex())
        self.assertEquals(self._CSS, layout.getPosition(b).getCSSString())

    def testPartialCss(self):
        """Add component, setting some attributes using CSS, assert getters agree"""
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b, self._PARTIAL_CSS)
        self.assertEquals(self._CSS_VALUE, layout.getPosition(b).getTopValue())
        self.assertNull(layout.getPosition(b).getBottomValue())
        self.assertEquals(self._CSS_VALUE, layout.getPosition(b).getLeftValue())
        self.assertNull(layout.getPosition(b).getRightValue())
        self.assertEquals(Sizeable.UNITS_PIXELS, layout.getPosition(b).getTopUnits())
        self.assertEquals(self._UNIT_UNSET, layout.getPosition(b).getBottomUnits())
        self.assertEquals(Sizeable.UNITS_EM, layout.getPosition(b).getLeftUnits())
        self.assertEquals(self._UNIT_UNSET, layout.getPosition(b).getRightUnits())
        self.assertEquals(-1, layout.getPosition(b).getZIndex())
        self.assertEquals(self._PARTIAL_CSS, layout.getPosition(b).getCSSString())

    def testPartialCssReset(self):
        """Add component setting all attributes using CSS, then reset using partial
        CSS; assert getters agree and the appropriate attributes are unset.
        """
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b, self._CSS)
        layout.getPosition(b).setCSSString(self._PARTIAL_CSS)
        self.assertEquals(self._CSS_VALUE, layout.getPosition(b).getTopValue())
        self.assertNull(layout.getPosition(b).getBottomValue())
        self.assertEquals(self._CSS_VALUE, layout.getPosition(b).getLeftValue())
        self.assertNull(layout.getPosition(b).getRightValue())
        self.assertEquals(Sizeable.UNITS_PIXELS, layout.getPosition(b).getTopUnits())
        self.assertEquals(self._UNIT_UNSET, layout.getPosition(b).getBottomUnits())
        self.assertEquals(Sizeable.UNITS_EM, layout.getPosition(b).getLeftUnits())
        self.assertEquals(self._UNIT_UNSET, layout.getPosition(b).getRightUnits())
        self.assertEquals(-1, layout.getPosition(b).getZIndex())
        self.assertEquals(self._PARTIAL_CSS, layout.getPosition(b).getCSSString())

    def testSetPosition(self):
        """Add component, then set all position attributes with individual setters
        for value and units; assert getters agree.
        """
        SIZE = Float.valueOf.valueOf(12)
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b)
        layout.getPosition(b).setTopValue(SIZE)
        layout.getPosition(b).setRightValue(SIZE)
        layout.getPosition(b).setBottomValue(SIZE)
        layout.getPosition(b).setLeftValue(SIZE)
        layout.getPosition(b).setTopUnits(Sizeable.UNITS_CM)
        layout.getPosition(b).setRightUnits(Sizeable.UNITS_EX)
        layout.getPosition(b).setBottomUnits(Sizeable.UNITS_INCH)
        layout.getPosition(b).setLeftUnits(Sizeable.UNITS_MM)
        self.assertEquals(SIZE, layout.getPosition(b).getTopValue())
        self.assertEquals(SIZE, layout.getPosition(b).getRightValue())
        self.assertEquals(SIZE, layout.getPosition(b).getBottomValue())
        self.assertEquals(SIZE, layout.getPosition(b).getLeftValue())
        self.assertEquals(Sizeable.UNITS_CM, layout.getPosition(b).getTopUnits())
        self.assertEquals(Sizeable.UNITS_EX, layout.getPosition(b).getRightUnits())
        self.assertEquals(Sizeable.UNITS_INCH, layout.getPosition(b).getBottomUnits())
        self.assertEquals(Sizeable.UNITS_MM, layout.getPosition(b).getLeftUnits())

    def testSetPosition2(self):
        """Add component, then set all position attributes with combined setters for
        value and units; assert getters agree.
        """
        SIZE = Float.valueOf.valueOf(12)
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b)
        layout.getPosition(b).setTop(SIZE, Sizeable.UNITS_CM)
        layout.getPosition(b).setRight(SIZE, Sizeable.UNITS_EX)
        layout.getPosition(b).setBottom(SIZE, Sizeable.UNITS_INCH)
        layout.getPosition(b).setLeft(SIZE, Sizeable.UNITS_MM)
        self.assertEquals(SIZE, layout.getPosition(b).getTopValue())
        self.assertEquals(SIZE, layout.getPosition(b).getRightValue())
        self.assertEquals(SIZE, layout.getPosition(b).getBottomValue())
        self.assertEquals(SIZE, layout.getPosition(b).getLeftValue())
        self.assertEquals(Sizeable.UNITS_CM, layout.getPosition(b).getTopUnits())
        self.assertEquals(Sizeable.UNITS_EX, layout.getPosition(b).getRightUnits())
        self.assertEquals(Sizeable.UNITS_INCH, layout.getPosition(b).getBottomUnits())
        self.assertEquals(Sizeable.UNITS_MM, layout.getPosition(b).getLeftUnits())

    def testUnsetPosition(self):
        """Add component, set all attributes using CSS, unset some using method
        calls, assert getters agree.
        """
        layout = AbsoluteLayout()
        b = Button()
        layout.addComponent(b, self._CSS)
        layout.getPosition(b).setTopValue(None)
        layout.getPosition(b).setRightValue(None)
        layout.getPosition(b).setBottomValue(None)
        layout.getPosition(b).setLeftValue(None)
        layout.getPosition(b).setZIndex(-1)
        self.assertNull(layout.getPosition(b).getTopValue())
        self.assertNull(layout.getPosition(b).getBottomValue())
        self.assertNull(layout.getPosition(b).getLeftValue())
        self.assertNull(layout.getPosition(b).getRightValue())
        self.assertEquals('', layout.getPosition(b).getCSSString())
