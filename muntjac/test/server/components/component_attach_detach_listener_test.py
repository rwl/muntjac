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

from muntjac.ui.label import Label
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.grid_layout import GridLayout
from muntjac.ui.absolute_layout import AbsoluteLayout
from muntjac.ui.css_layout import CssLayout
from muntjac.ui.abstract_ordered_layout import AbstractOrderedLayout

from muntjac.ui.component_container import \
    IComponentAttachListener, IComponentDetachListener


class ComponentAttachDetachListenerTest(TestCase):

    def resetVariables(self):
        # Attach
        self._attachCounter = 0
        self._attachedComponent = None
        self._attachTarget = None
        self._foundInContainer = False

        # Detach
        self._detachCounter = 0
        self._detachedComponent = None
        self._detachedTarget = None

        # Common
        self._indexOfComponent = -1
        self._componentArea = None
        self._componentPosition = None


    def setUp(self):
        super(ComponentAttachDetachListenerTest, self).setUp()

        # General variables
        self._attachCounter = 0
        self._attachedComponent = None
        self._attachTarget = None
        self._foundInContainer = False
        self._detachCounter = 0
        self._detachedComponent = None
        self._detachedTarget = None

        # Ordered layout specific variables
        self._indexOfComponent = -1

        # Grid layout specific variables
        self._componentArea = None

        # Absolute layout specific variables
        self._componentPosition = None

        self._olayout = HorizontalLayout()
        listener = MyAttachListener(self)
        self._olayout.addListener(listener, IComponentAttachListener)
        listener = MyDetachListener(self)
        self._olayout.addListener(listener, IComponentDetachListener)

        self._gridlayout = GridLayout()
        listener = MyAttachListener(self)
        self._gridlayout.addListener(listener, IComponentAttachListener)
        listener = MyDetachListener(self)
        self._gridlayout.addListener(listener, IComponentDetachListener)

        self._absolutelayout = AbsoluteLayout()
        listener = MyAttachListener(self)
        self._absolutelayout.addListener(listener, IComponentAttachListener)
        listener = MyDetachListener(self)
        self._absolutelayout.addListener(listener, IComponentDetachListener)

        self._csslayout = CssLayout()
        listener = MyAttachListener(self)
        self._csslayout.addListener(listener, IComponentAttachListener)
        listener = MyDetachListener(self)
        self._csslayout.addListener(listener, IComponentDetachListener)


    def testOrderedLayoutAttachListener(self):
        # Reset state variables
        self.resetVariables()

        # Add component -> Should trigger attach listener
        comp = Label()
        self._olayout.addComponent(comp)

        # Attach counter should get incremented
        self.assertEquals(1, self._attachCounter)

        # The attached component should be the label
        self.assertEquals(comp, self._attachedComponent)

        # The attached target should be the layout
        self.assertEquals(self._olayout, self._attachTarget)

        # The attached component should be found in the container
        self.assertTrue(self._foundInContainer)

        # The index of the component should not be -1
        self.assertFalse(self._indexOfComponent == -1)


    def testOrderedLayoutDetachListener(self):
        # Add a component to detach
        comp = Label()
        self._olayout.addComponent(comp)

        # Reset state variables (since they are set by the attach listener)
        self.resetVariables()

        # Detach the component -> triggers the detach listener
        self._olayout.removeComponent(comp)

        # Detach counter should get incremented
        self.assertEquals(1, self._detachCounter)

        # The detached component should be the label
        self.assertEquals(comp, self._detachedComponent)

        # The detached target should be the layout
        self.assertEquals(self._olayout, self._detachedTarget)

        # The detached component should not be found in the container
        self.assertFalse(self._foundInContainer)

        # The index of the component should be -1
        self.assertEquals(-1, self._indexOfComponent)


    def testGridLayoutAttachListener(self):
        # Reset state variables
        self.resetVariables()

        # Add component -> Should trigger attach listener
        comp = Label()
        self._gridlayout.addComponent(comp)

        # Attach counter should get incremented
        self.assertEquals(1, self._attachCounter)

        # The attached component should be the label
        self.assertEquals(comp, self._attachedComponent)

        # The attached target should be the layout
        self.assertEquals(self._gridlayout, self._attachTarget)

        # The attached component should be found in the container
        self.assertTrue(self._foundInContainer)

        # The grid area should not be null
        self.assertIsNotNone(self._componentArea)


    def testGridLayoutDetachListener(self):
        # Add a component to detach
        comp = Label()
        self._gridlayout.addComponent(comp)

        # Reset state variables (since they are set by the attach listener)
        self.resetVariables()

        # Detach the component -> triggers the detach listener
        self._gridlayout.removeComponent(comp)

        # Detach counter should get incremented
        self.assertEquals(1, self._detachCounter)

        # The detached component should be the label
        self.assertEquals(comp, self._detachedComponent)

        # The detached target should be the layout
        self.assertEquals(self._gridlayout, self._detachedTarget)

        # The detached component should not be found in the container
        self.assertFalse(self._foundInContainer)

        # The grid area should be null
        self.assertIsNone(self._componentArea)


    def testAbsoluteLayoutAttachListener(self):
        # Reset state variables
        self.resetVariables()

        # Add component -> Should trigger attach listener
        comp = Label()
        self._absolutelayout.addComponent(comp)

        # Attach counter should get incremented
        self.assertEquals(1, self._attachCounter)

        # The attached component should be the label
        self.assertEquals(comp, self._attachedComponent)

        # The attached target should be the layout
        self.assertEquals(self._absolutelayout, self._attachTarget)

        # The attached component should be found in the container
        self.assertTrue(self._foundInContainer)

        # The component position should not be null
        self.assertIsNotNone(self._componentPosition)


    def testAbsoluteLayoutDetachListener(self):
        # Add a component to detach
        comp = Label()
        self._absolutelayout.addComponent(comp)

        # Reset state variables (since they are set by the attach listener)
        self.resetVariables()

        # Detach the component -> triggers the detach listener
        self._absolutelayout.removeComponent(comp)

        # Detach counter should get incremented
        self.assertEquals(1, self._detachCounter)

        # The detached component should be the label
        self.assertEquals(comp, self._detachedComponent)

        # The detached target should be the layout
        self.assertEquals(self._absolutelayout, self._detachedTarget)

        # The detached component should not be found in the container
        self.assertFalse(self._foundInContainer)

        # The component position should be null
        self.assertIsNone(self._componentPosition)


    def testCSSLayoutAttachListener(self):
        # Reset state variables
        self.resetVariables()

        # Add component -> Should trigger attach listener
        comp = Label()
        self._csslayout.addComponent(comp)

        # Attach counter should get incremented
        self.assertEquals(1, self._attachCounter)

        # The attached component should be the label
        self.assertEquals(comp, self._attachedComponent)

        # The attached target should be the layout
        self.assertEquals(self._csslayout, self._attachTarget)

        # The attached component should be found in the container
        self.assertTrue(self._foundInContainer)


    def testCSSLayoutDetachListener(self):
        # Add a component to detach
        comp = Label()
        self._csslayout.addComponent(comp)

        # Reset state variables (since they are set by the attach listener)
        self.resetVariables()

        # Detach the component -> triggers the detach listener
        self._csslayout.removeComponent(comp)

        # Detach counter should get incremented
        self.assertEquals(1, self._detachCounter)

        # The detached component should be the label
        self.assertEquals(comp, self._detachedComponent)

        # The detached target should be the layout
        self.assertEquals(self._csslayout, self._detachedTarget)

        # The detached component should not be found in the container
        self.assertFalse(self._foundInContainer)


class MyAttachListener(IComponentAttachListener):

    def __init__(self, test):
        self._test = test

    def componentAttachedToContainer(self, event):
        self._test._attachCounter += 1
        self._test._attachedComponent = event.getAttachedComponent()
        self._test._attachTarget = event.getContainer()

        # Search for component in container (should be found)
        it = self._test._attachTarget.getComponentIterator()
        while True:
            try:
                if it.next() == self._test._attachedComponent:
                    self._test._foundInContainer = True
                    break
            except StopIteration:
                break

        # Get layout specific variables
        if isinstance(self._test._attachTarget, AbstractOrderedLayout):
            self._test._indexOfComponent = \
                    self._test._attachTarget.getComponentIndex(
                            self._test._attachedComponent)
        elif isinstance(self._test._attachTarget, GridLayout):
            self._test._componentArea = \
                    self._test._attachTarget.getComponentArea(
                            self._test._attachedComponent)
        elif isinstance(self._test._attachTarget, AbsoluteLayout):
            self._test._componentPosition = \
                    self._test._attachTarget.getPosition(
                            self._test._attachedComponent)



class MyDetachListener(IComponentDetachListener):

    def __init__(self, test):
        self._test = test

    def componentDetachedFromContainer(self, event):
        self._test._detachCounter += 1
        self._test._detachedComponent = event.getDetachedComponent()
        self._test._detachedTarget = event.getContainer()

        # Search for component in container (should NOT be found)
        it = self._test._detachedTarget.getComponentIterator()
        while True:
            try:
                if it.next() == self._test._detachedComponent:
                    self._test._foundInContainer = True
                    break
            except StopIteration:
                break

        # Get layout specific variables
        if isinstance(self._test._detachedTarget, AbstractOrderedLayout):
            self._test._indexOfComponent = \
                    self._test._detachedTarget.getComponentIndex(
                            self._test._detachedComponent)
        elif isinstance(self._test._detachedTarget, GridLayout):
            self._test._componentArea = \
                    self._test._detachedTarget.getComponentArea(
                            self._test._detachedComponent)
        elif isinstance(self._test._detachedTarget, AbsoluteLayout):
            self._test._componentPosition = \
                    self._test._detachedTarget.getPosition(
                            self._test._detachedComponent)
