
from muntjac.api import VerticalLayout, Label, Embedded, Button, Alignment
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.ui.css_layout import CssLayout
from muntjac.ui.button import IClickListener
from muntjac.ui.custom_component import CustomComponent
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.drag_and_drop_wrapper import DragAndDropWrapper, DragStartMode
from muntjac.event.dd.drop_handler import IDropHandler
from muntjac.event.dd.acceptcriteria.source_is_target import SourceIsTarget
from muntjac.event.dd.acceptcriteria.not_ import Not

from muntjac.terminal.gwt.client.ui.dd.horizontal_drop_location import \
    HorizontalDropLocation


class DragDropRearrangeComponentsExample(VerticalLayout):

    def __init__(self):
        super(DragDropRearrangeComponentsExample, self).__init__()

        layout = SortableLayout(True)
        layout.setSizeUndefined()
        layout.setHeight('100px')

        # Use these styles to hide irrelevant drag hints
        layout.addStyleName('no-vertical-drag-hints')
        # layout.addStyleName("no-horizontal-drag-hints");
        # layout.addStyleName("no-box-drag-hints");

        for component in self.createComponents():
            layout.addComponent(component)

        self.addComponent(layout)


    def createComponents(self):
        components = list()

        label = Label('This is a long text block that will wrap.')
        label.setWidth('120px')
        components.append(label)

        image = Embedded('', ThemeResource('../runo/icons/64/document.png'))
        components.append(image)

        documentLayout = CssLayout()
        documentLayout.setWidth('19px')
        for _ in range(5):
            e = Embedded(None, ThemeResource('../runo/icons/16/document.png'))
            e.setHeight('16px')
            e.setWidth('16px')
            documentLayout.addComponent(e)
        components.append(documentLayout)

        buttonLayout = VerticalLayout()
        button = Button('Button')

        button.addListener(ButtonClickListener(self), IClickListener)
        buttonLayout.addComponent(button)
        buttonLayout.setComponentAlignment(button, Alignment.MIDDLE_CENTER)
        components.append(buttonLayout)

        return components


class ButtonClickListener(IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c.getWindow().showNotification('Button clicked')


class SortableLayout(CustomComponent):

    def __init__(self, horizontal):
        super(SortableLayout, self).__init__()

        self._horizontal = horizontal
        if horizontal:
            self._layout = HorizontalLayout()
        else:
            self._layout = VerticalLayout()

        self._dropHandler = ReorderLayoutDropHandler(self._layout)

        pane = DragAndDropWrapper(self._layout)
        self.setCompositionRoot(pane)


    def addComponent(self, component):
        wrapper = WrappedComponent(component, self._dropHandler)
        wrapper.setSizeUndefined()
        if self._horizontal:
            component.setHeight('100%')
            wrapper.setHeight('100%')
        else:
            component.setWidth('100%')
            wrapper.setWidth('100%')
        self._layout.addComponent(wrapper)


class WrappedComponent(DragAndDropWrapper):

    def __init__(self, content, dropHandler):
        super(WrappedComponent, self).__init__(content)

        self._dropHandler = dropHandler
        self.setDragStartMode(DragStartMode.WRAPPER)


    def getDropHandler(self):
        return self._dropHandler


class ReorderLayoutDropHandler(IDropHandler):

    def __init__(self, layout):
        self._layout = layout


    def getAcceptCriterion(self):
        return Not(SourceIsTarget.get())


    def drop(self, dropEvent):
        transferable = dropEvent.getTransferable()
        sourceComponent = transferable.getSourceComponent()

        if isinstance(sourceComponent, WrappedComponent):
            dropTargetData = dropEvent.getTargetDetails()
            target = dropTargetData.getTarget()

            # find the location where to move the dragged component
            sourceWasAfterTarget = True
            index = 0
            componentIterator = self._layout.getComponentIterator()
            nxt = None
            while nxt != target:
                try:
                    nxt = componentIterator.next()
                    if nxt != sourceComponent:
                        index += 1
                    else:
                        sourceWasAfterTarget = False
                except StopIteration:
                    break

            if (nxt is None) or (nxt != target):
                # component not found - if dragging from another layout
                return

            # drop on top of target?
            if (dropTargetData.getData('horizontalLocation')
                    == str(HorizontalDropLocation.CENTER)):
                # drop before the target?
                if sourceWasAfterTarget:
                    index -= 1
            elif (dropTargetData.getData('horizontalLocation')
                    == str(HorizontalDropLocation.LEFT)):
                index -= 1
                if index < 0:
                    index = 0

            # move component within the layout
            self._layout.removeComponent(sourceComponent)
            self._layout.addComponent(sourceComponent, index)
