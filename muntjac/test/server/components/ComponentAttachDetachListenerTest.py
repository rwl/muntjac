# -*- coding: utf-8 -*-
# from com.vaadin.ui.AbsoluteLayout import (AbsoluteLayout,)
# from com.vaadin.ui.AbsoluteLayout.ComponentPosition import (ComponentPosition,)
# from com.vaadin.ui.AbstractOrderedLayout import (AbstractOrderedLayout,)
# from com.vaadin.ui.Component import (Component,)
# from com.vaadin.ui.ComponentContainer import (ComponentContainer,)
# from com.vaadin.ui.ComponentContainer.ComponentAttachEvent import (ComponentAttachEvent,)
# from com.vaadin.ui.ComponentContainer.ComponentAttachListener import (ComponentAttachListener,)
# from com.vaadin.ui.ComponentContainer.ComponentDetachEvent import (ComponentDetachEvent,)
# from com.vaadin.ui.ComponentContainer.ComponentDetachListener import (ComponentDetachListener,)
# from com.vaadin.ui.CssLayout import (CssLayout,)
# from com.vaadin.ui.GridLayout.Area import (Area,)
# from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
# from java.util.Iterator import (Iterator,)
# from junit.framework.TestCase import (TestCase,)


class ComponentAttachDetachListenerTest(TestCase):
    _olayout = None
    _gridlayout = None
    _absolutelayout = None
    _csslayout = None
    # General variables
    _attachCounter = 0
    _attachedComponent = None
    _attachTarget = None
    _foundInContainer = False
    _detachCounter = 0
    _detachedComponent = None
    _detachedTarget = None
    # Ordered layout specific variables
    _indexOfComponent = -1
    # Grid layout specific variables
    _componentArea = None
    # Absolute layout specific variables
    _componentPosition = None

    def MyAttachListener(ComponentAttachDetachListenerTest_this, *args, **kwargs):

        class MyAttachListener(ComponentAttachListener):

            def componentAttachedToContainer(self, event):
                ComponentAttachDetachListenerTest_this._attachCounter += 1
                ComponentAttachDetachListenerTest_this._attachedComponent = event.getAttachedComponent()
                ComponentAttachDetachListenerTest_this._attachTarget = event.getContainer()
                # Search for component in container (should be found)
                iter = ComponentAttachDetachListenerTest_this._attachTarget.getComponentIterator()
                while iter.hasNext():
                    if iter.next() == ComponentAttachDetachListenerTest_this._attachedComponent:
                        ComponentAttachDetachListenerTest_this._foundInContainer = True
                        break
                # Get layout specific variables
                if (
                    isinstance(ComponentAttachDetachListenerTest_this._attachTarget, AbstractOrderedLayout)
                ):
                    ComponentAttachDetachListenerTest_this._indexOfComponent = ComponentAttachDetachListenerTest_this._attachTarget.getComponentIndex(ComponentAttachDetachListenerTest_this._attachedComponent)
                elif (
                    isinstance(ComponentAttachDetachListenerTest_this._attachTarget, GridLayout)
                ):
                    ComponentAttachDetachListenerTest_this._componentArea = ComponentAttachDetachListenerTest_this._attachTarget.getComponentArea(ComponentAttachDetachListenerTest_this._attachedComponent)
                elif (
                    isinstance(ComponentAttachDetachListenerTest_this._attachTarget, AbsoluteLayout)
                ):
                    ComponentAttachDetachListenerTest_this._componentPosition = ComponentAttachDetachListenerTest_this._attachTarget.getPosition(ComponentAttachDetachListenerTest_this._attachedComponent)

        return MyAttachListener(*args, **kwargs)

    def MyDetachListener(ComponentAttachDetachListenerTest_this, *args, **kwargs):

        class MyDetachListener(ComponentDetachListener):

            def componentDetachedFromContainer(self, event):
                ComponentAttachDetachListenerTest_this._detachCounter += 1
                ComponentAttachDetachListenerTest_this._detachedComponent = event.getDetachedComponent()
                ComponentAttachDetachListenerTest_this._detachedTarget = event.getContainer()
                # Search for component in container (should NOT be found)
                iter = ComponentAttachDetachListenerTest_this._detachedTarget.getComponentIterator()
                while iter.hasNext():
                    if iter.next() == ComponentAttachDetachListenerTest_this._detachedComponent:
                        ComponentAttachDetachListenerTest_this._foundInContainer = True
                        break
                # Get layout specific variables
                if (
                    isinstance(ComponentAttachDetachListenerTest_this._detachedTarget, AbstractOrderedLayout)
                ):
                    ComponentAttachDetachListenerTest_this._indexOfComponent = ComponentAttachDetachListenerTest_this._detachedTarget.getComponentIndex(ComponentAttachDetachListenerTest_this._detachedComponent)
                elif (
                    isinstance(ComponentAttachDetachListenerTest_this._detachedTarget, GridLayout)
                ):
                    ComponentAttachDetachListenerTest_this._componentArea = ComponentAttachDetachListenerTest_this._detachedTarget.getComponentArea(ComponentAttachDetachListenerTest_this._detachedComponent)
                elif (
                    isinstance(ComponentAttachDetachListenerTest_this._detachedTarget, AbsoluteLayout)
                ):
                    ComponentAttachDetachListenerTest_this._componentPosition = ComponentAttachDetachListenerTest_this._detachedTarget.getPosition(ComponentAttachDetachListenerTest_this._detachedComponent)

        return MyDetachListener(*args, **kwargs)

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
        self._olayout = HorizontalLayout()
        self._olayout.addListener(self.MyAttachListener())
        self._olayout.addListener(self.MyDetachListener())
        self._gridlayout = GridLayout()
        self._gridlayout.addListener(self.MyAttachListener())
        self._gridlayout.addListener(self.MyDetachListener())
        self._absolutelayout = AbsoluteLayout()
        self._absolutelayout.addListener(self.MyAttachListener())
        self._absolutelayout.addListener(self.MyDetachListener())
        self._csslayout = CssLayout()
        self._csslayout.addListener(self.MyAttachListener())
        self._csslayout.addListener(self.MyDetachListener())

    def testOrderedLayoutAttachListener(self):
        # Reset state variables
        self.resetVariables()
        # Add component -> Should trigger attach listener
        comp = Label()
        self._olayout.addComponent(comp)
        # Attach counter should get incremented
        self.assertEquals(1, self._attachCounter)
        # The attached component should be the label
        self.assertSame(comp, self._attachedComponent)
        # The attached target should be the layout
        self.assertSame(self._olayout, self._attachTarget)
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
        self.assertSame(comp, self._detachedComponent)
        # The detached target should be the layout
        self.assertSame(self._olayout, self._detachedTarget)
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
        self.assertSame(comp, self._attachedComponent)
        # The attached target should be the layout
        self.assertSame(self._gridlayout, self._attachTarget)
        # The attached component should be found in the container
        self.assertTrue(self._foundInContainer)
        # The grid area should not be null
        self.assertNotNull(self._componentArea)

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
        self.assertSame(comp, self._detachedComponent)
        # The detached target should be the layout
        self.assertSame(self._gridlayout, self._detachedTarget)
        # The detached component should not be found in the container
        self.assertFalse(self._foundInContainer)
        # The grid area should be null
        self.assertNull(self._componentArea)

    def testAbsoluteLayoutAttachListener(self):
        # Reset state variables
        self.resetVariables()
        # Add component -> Should trigger attach listener
        comp = Label()
        self._absolutelayout.addComponent(comp)
        # Attach counter should get incremented
        self.assertEquals(1, self._attachCounter)
        # The attached component should be the label
        self.assertSame(comp, self._attachedComponent)
        # The attached target should be the layout
        self.assertSame(self._absolutelayout, self._attachTarget)
        # The attached component should be found in the container
        self.assertTrue(self._foundInContainer)
        # The component position should not be null
        self.assertNotNull(self._componentPosition)

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
        self.assertSame(comp, self._detachedComponent)
        # The detached target should be the layout
        self.assertSame(self._absolutelayout, self._detachedTarget)
        # The detached component should not be found in the container
        self.assertFalse(self._foundInContainer)
        # The component position should be null
        self.assertNull(self._componentPosition)

    def testCSSLayoutAttachListener(self):
        # Reset state variables
        self.resetVariables()
        # Add component -> Should trigger attach listener
        comp = Label()
        self._csslayout.addComponent(comp)
        # Attach counter should get incremented
        self.assertEquals(1, self._attachCounter)
        # The attached component should be the label
        self.assertSame(comp, self._attachedComponent)
        # The attached target should be the layout
        self.assertSame(self._csslayout, self._attachTarget)
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
        self.assertSame(comp, self._detachedComponent)
        # The detached target should be the layout
        self.assertSame(self._csslayout, self._detachedTarget)
        # The detached component should not be found in the container
        self.assertFalse(self._foundInContainer)
