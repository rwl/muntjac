# -*- coding: utf-8 -*-
# from com.vaadin.event.LayoutEvents.LayoutClickEvent import (LayoutClickEvent,)
# from com.vaadin.event.LayoutEvents.LayoutClickListener import (LayoutClickListener,)
# from com.vaadin.ui.Layout import (Layout,)
# from com.vaadin.ui.Link import (Link,)
# from com.vaadin.ui.Select import (Select,)


class ClickableLayoutBasicExample(VerticalLayout):

    def __init__(self):
        self.setMargin(True)
        self.setSpacing(True)
        # Add a clickable vertical layout
        self.addComponent(self.createVerticalClickableLayout())
        # Add a clickable grid layout
        self.addComponent(self.createChildComponentClickableLayout())
        # Add a clickable vertical layout
        self.addComponent(self.createKeyRegisterClickableLayout())

    def createVerticalClickableLayout(self):
        # Create a vertical layout with click events
        layout = VerticalLayout()
        layout.setWidth('90%')
        layout.setSpacing(True)
        layout.addStyleName('border')
        layout.setMargin(True)
        # Add some components inside the layout
        layout.addComponent(ALabel('<b>This is a vertical layout with a click listener attached. ' + 'Try clicking anywhere inside this layout.</b>', ALabel.CONTENT_RAW))
        clickX = ALabel('X-coordinate: <i>Not available.</i>', ALabel.CONTENT_RAW)
        layout.addComponent(clickX)
        clickY = ALabel('Y-coordinate: <i>Not available.</i>', ALabel.CONTENT_RAW)
        layout.addComponent(clickY)
        clickRelativeX = ALabel('X-coordinate relative to the layout: <i>Not available.</i>', ALabel.CONTENT_RAW)
        layout.addComponent(clickRelativeX)
        clickRelativeY = ALabel('Y-coordinate relative to the layout: <i>Not available.</i>', ALabel.CONTENT_RAW)
        layout.addComponent(clickRelativeY)
        button = ALabel('Mouse button: <i>Not available.</i>', ALabel.CONTENT_RAW)
        layout.addComponent(button)
        # Listen for layout click events

        class _0_(LayoutClickListener):

            def layoutClick(self, event):
                # Update components values
                self.clickX.setValue('X-coordinate: ' + event.getClientX())
                self.clickY.setValue('Y-coordinate: ' + event.getClientY())
                self.clickRelativeX.setValue('X-coordinate relative to the layout: ' + event.getRelativeX())
                self.clickRelativeY.setValue('Y-coordinate relative to the layout: ' + event.getRelativeY())
                self.button.setValue('Mouse button: ' + event.getButtonName())
                # Show a notification
                self.getWindow().showNotification('Layout clicked!')

        _0_ = _0_()
        layout.addListener(_0_)
        return layout

    def createChildComponentClickableLayout(self):
        # Create a grid layout with click events
        layout = GridLayout(5, 2)
        layout.addStyleName('border')
        layout.setSpacing(True)
        layout.setWidth('90%')
        layout.setMargin(True)
        # Add some components to the layout
        layout.addComponent(ALabel('<b>Clickable layout events include a reference to the ' + 'child component beneath the click. ' + 'Try clicking anywhere in this layout.</b>', ALabel.CONTENT_RAW), 0, 0, 4, 0)
        layout.addComponent(TextField(None, 'Click here'))
        layout.addComponent(Link('Click here', None))
        select = Select(None, Arrays.asList('Click here'))
        select.select('Click here')
        layout.addComponent(select)
        # Listen for layout click events

        class _1_(LayoutClickListener):

            def layoutClick(self, event):
                # Get the child component which was clicked
                child = event.getChildComponent()
                if child is None:
                    # Not over any child component
                    self.getWindow().showNotification('The click was not over any component.')
                else:
                    # Over a child component
                    self.getWindow().showNotification('The click was over a ' + child.getClass().getCanonicalName())

        _1_ = _1_()
        layout.addListener(_1_)
        return layout

    def createKeyRegisterClickableLayout(self):
        # Create a vertical layout with click events
        layout = VerticalLayout()
        layout.setWidth('90%')
        layout.setSpacing(True)
        layout.addStyleName('border')
        layout.setMargin(True)
        # Add some components inside the layout
        layout.addComponent(ALabel('<b>Layout click events register if control keys are pressed during the click and double clicks. ' + 'Try clicking anywhere inside this layout while holding CTRL, ALT, SHIFT or META key down.</b>', ALabel.CONTENT_RAW))
        # Listen for layout click events

        class _2_(LayoutClickListener):

            def layoutClick(self, event):
                message = self.StringBuilder()
                if event.isCtrlKey():
                    message.append('CTRL+')
                if event.isAltKey():
                    message.append('ALT+')
                if event.isShiftKey():
                    message.append('SHIFT+')
                if event.isMetaKey():
                    message.append('META+')
                if event.isDoubleClick():
                    message.append('DOUBLE CLICK')
                else:
                    message.append('CLICK')
                self.getWindow().showNotification(str(message))

        _2_ = _2_()
        layout.addListener(_2_)
        return layout
