
from muntjac.api import \
    VerticalLayout, Label, GridLayout, TextField, Select, Link

from muntjac.event.layout_events import ILayoutClickListener
from muntjac.util import fullname


class ClickableLayoutBasicExample(VerticalLayout):

    def __init__(self):
        super(ClickableLayoutBasicExample, self).__init__()

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
        layout.addComponent(Label('<b>This is a vertical layout with a '
                'click listener attached. Try clicking anywhere inside '
                'this layout.</b>', Label.CONTENT_RAW))

        clickX = Label('X-coordinate: <i>Not available.</i>',
                Label.CONTENT_RAW)
        layout.addComponent(clickX)

        clickY = Label('Y-coordinate: <i>Not available.</i>',
                Label.CONTENT_RAW)
        layout.addComponent(clickY)

        clickRelativeX = Label('X-coordinate relative to the layout: '
                '<i>Not available.</i>', Label.CONTENT_RAW)
        layout.addComponent(clickRelativeX)

        clickRelativeY = Label('Y-coordinate relative to the layout: '
                '<i>Not available.</i>', Label.CONTENT_RAW)

        layout.addComponent(clickRelativeY)
        button = Label('Mouse button: <i>Not available.</i>',
                Label.CONTENT_RAW)
        layout.addComponent(button)

        # Listen for layout click events
        layout.addListener(LayoutListener(self, button,
                clickX, clickY, clickRelativeX, clickRelativeY),
                ILayoutClickListener)
        return layout


    def createChildComponentClickableLayout(self):
        # Create a grid layout with click events
        layout = GridLayout(5, 2)
        layout.addStyleName('border')
        layout.setSpacing(True)
        layout.setWidth('90%')
        layout.setMargin(True)

        # Add some components to the layout
        layout.addComponent(Label('<b>Clickable layout events include a '
                'reference to the child component beneath the click. '
                'Try clicking anywhere in this layout.</b>',
                Label.CONTENT_RAW), 0, 0, 4, 0)
        layout.addComponent(TextField(None, 'Click here'))
        layout.addComponent(Link('Click here', None))
        select = Select(None, ['Click here'])
        select.select('Click here')
        layout.addComponent(select)

        # Listen for layout click event
        layout.addListener(GridListener(self), ILayoutClickListener)
        return layout


    def createKeyRegisterClickableLayout(self):
        # Create a vertical layout with click events
        layout = VerticalLayout()
        layout.setWidth('90%')
        layout.setSpacing(True)
        layout.addStyleName('border')
        layout.setMargin(True)

        # Add some components inside the layout
        layout.addComponent(Label('<b>Layout click events register if '
                'control keys are pressed during the click and double '
                'clicks. Try clicking anywhere inside this layout while '
                'holding CTRL, ALT, SHIFT or META key down.</b>',
                Label.CONTENT_RAW))

        # Listen for layout click events
        layout.addListener(VerticalListener(self), ILayoutClickListener)
        return layout


class LayoutListener(ILayoutClickListener):

    def __init__(self, c, button, clickX, clickY,
                clickRelativeX, clickRelativeY):
        self._button = button
        self._c = c
        self._clickX = clickX
        self._clickY = clickY
        self._clickRelativeX = clickRelativeX
        self._clickRelativeY = clickRelativeY


    def layoutClick(self, event):
        # Update components values
        self._clickX.setValue('X-coordinate: %d' % event.getClientX())
        self._clickY.setValue('Y-coordinate: %d' % event.getClientY())

        self._clickRelativeX.setValue('X-coordinate relative to '
                'the layout: %d' % event.getRelativeX())

        self._clickRelativeY.setValue('Y-coordinate relative to '
                'the layout: %d' % event.getRelativeY())

        self._button.setValue('Mouse button: ' + event.getButtonName())
        # Show a notification
        self._c.getWindow().showNotification('Layout clicked!')


class GridListener(ILayoutClickListener):

    def __init__(self, c):
        self._c = c

    def layoutClick(self, event):
        # Get the child component which was clicked
        child = event.getChildComponent()
        if child is None:
            # Not over any child component
            self._c.getWindow().showNotification('The click '
                    'was not over any component.')
        else:
            # Over a child component
            self._c.getWindow().showNotification(
                    'The click was over a ' + fullname(child))


class VerticalListener(ILayoutClickListener):

    def __init__(self, c):
        self._c = c

    def layoutClick(self, event):
        message = ""
        if event.isCtrlKey():
            message += 'CTRL+'
        if event.isAltKey():
            message += 'ALT+'
        if event.isShiftKey():
            message += 'SHIFT+'
        if event.isMetaKey():
            message += 'META+'
        if event.isDoubleClick():
            message += 'DOUBLE CLICK'
        else:
            message += 'CLICK'
        self._c.getWindow().showNotification(message)
