# -*- coding: utf-8 -*-
# from com.vaadin.event.dd.DropTarget import (DropTarget,)
# from com.vaadin.event.dd.TargetDetails import (TargetDetails,)
# from com.vaadin.event.dd.acceptcriteria.Not import (Not,)
# from com.vaadin.event.dd.acceptcriteria.SourceIsTarget import (SourceIsTarget,)
# from com.vaadin.terminal.ThemeResource import (ThemeResource,)
# from com.vaadin.terminal.gwt.client.ui.dd.HorizontalDropLocation import (HorizontalDropLocation,)
# from com.vaadin.ui.AbstractOrderedLayout import (AbstractOrderedLayout,)
# from com.vaadin.ui.Alignment import (Alignment,)
# from com.vaadin.ui.Button import (Button,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.CustomComponent import (CustomComponent,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.List import (List,)


class DragDropRearrangeComponentsExample(VerticalLayout):

    def __init__(self):
        layout = self.SortableLayout(True)
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
        components.add(label)
        image = Embedded('', ThemeResource('../runo/icons/64/document.png'))
        components.add(image)
        documentLayout = CssLayout()
        documentLayout.setWidth('19px')
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 5):
                break
            e = Embedded(None, ThemeResource('../runo/icons/16/document.png'))
            e.setHeight('16px')
            e.setWidth('16px')
            documentLayout.addComponent(e)
        components.add(documentLayout)
        buttonLayout = VerticalLayout()
        button = Button('Button')

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                self.getWindow().showNotification('Button clicked')

        _0_ = _0_()
        button.addListener(_0_)
        buttonLayout.addComponent(button)
        buttonLayout.setComponentAlignment(button, Alignment.MIDDLE_CENTER)
        components.add(buttonLayout)
        return components

    def SortableLayout(DragDropRearrangeComponentsExample_this, *args, **kwargs):

        class SortableLayout(CustomComponent):
            _layout = None
            _horizontal = None
            _dropHandler = None

            def __init__(self, horizontal):
                self._horizontal = horizontal
                if horizontal:
                    self._layout = HorizontalLayout()
                else:
                    self._layout = VerticalLayout()
                self._dropHandler = DragDropRearrangeComponentsExample_this.ReorderLayoutDropHandler(self._layout)
                pane = DragAndDropWrapper(self._layout)
                self.setCompositionRoot(pane)

            def addComponent(self, component):
                wrapper = DragDropRearrangeComponentsExample_this.WrappedComponent(component, self._dropHandler)
                wrapper.setSizeUndefined()
                if self._horizontal:
                    component.setHeight('100%')
                    wrapper.setHeight('100%')
                else:
                    component.setWidth('100%')
                    wrapper.setWidth('100%')
                self._layout.addComponent(wrapper)

        return SortableLayout(*args, **kwargs)

    class WrappedComponent(DragAndDropWrapper):
        _dropHandler = None

        def __init__(self, content, dropHandler):
            super(WrappedComponent, self)(content)
            self._dropHandler = dropHandler
            self.setDragStartMode(self.DragStartMode.WRAPPER)

        def getDropHandler(self):
            return self._dropHandler

    def ReorderLayoutDropHandler(DragDropRearrangeComponentsExample_this, *args, **kwargs):

        class ReorderLayoutDropHandler(DropHandler):
            _layout = None

            def __init__(self, layout):
                self._layout = layout

            def getAcceptCriterion(self):
                return Not(SourceIsTarget.get())

            def drop(self, dropEvent):
                transferable = dropEvent.getTransferable()
                sourceComponent = transferable.getSourceComponent()
                if (
                    isinstance(sourceComponent, DragDropRearrangeComponentsExample_this.WrappedComponent)
                ):
                    dropTargetData = dropEvent.getTargetDetails()
                    target = dropTargetData.getTarget()
                    # find the location where to move the dragged component
                    sourceWasAfterTarget = True
                    index = 0
                    componentIterator = self._layout.getComponentIterator()
                    next = None
                    while next != target and componentIterator.hasNext():
                        next = componentIterator.next()
                        if next != sourceComponent:
                            index += 1
                        else:
                            sourceWasAfterTarget = False
                    if (next is None) or (next != target):
                        # component not found - if dragging from another layout
                        return
                    # drop on top of target?
                    if (
                        dropTargetData.getData('horizontalLocation') == str(HorizontalDropLocation.CENTER)
                    ):
                        # drop before the target?
                        if sourceWasAfterTarget:
                            index -= 1
                    elif (
                        dropTargetData.getData('horizontalLocation') == str(HorizontalDropLocation.LEFT)
                    ):
                        index -= 1
                        if index < 0:
                            index = 0
                    # move component within the layout
                    self._layout.removeComponent(sourceComponent)
                    self._layout.addComponent(sourceComponent, index)

        return ReorderLayoutDropHandler(*args, **kwargs)
