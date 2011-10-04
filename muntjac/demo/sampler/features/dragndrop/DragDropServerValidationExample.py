# -*- coding: utf-8 -*-
from muntjac.demo.sampler.ExampleUtil import (ExampleUtil,)
# from com.vaadin.data.Item import (Item,)
# from com.vaadin.data.util.IndexedContainer import (IndexedContainer,)
# from com.vaadin.event.DataBoundTransferable import (DataBoundTransferable,)
# from com.vaadin.event.dd.DragAndDropEvent import (DragAndDropEvent,)
# from com.vaadin.event.dd.DropHandler import (DropHandler,)
# from com.vaadin.event.dd.acceptcriteria.AcceptCriterion import (AcceptCriterion,)
# from com.vaadin.event.dd.acceptcriteria.ServerSideCriterion import (ServerSideCriterion,)
# from com.vaadin.terminal.gwt.client.ui.dd.VerticalDropLocation import (VerticalDropLocation,)
# from com.vaadin.ui.AbstractSelect.AbstractSelectTargetDetails import (AbstractSelectTargetDetails,)
# from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
# from com.vaadin.ui.Table import (Table,)
# from com.vaadin.ui.Table.TableDragMode import (TableDragMode,)


class DragDropServerValidationExample(HorizontalLayout):
    _table = None
    _container = None

    def RelativeCriterion(DragDropServerValidationExample_this, *args, **kwargs):

        class RelativeCriterion(ServerSideCriterion):

            def accept(self, dragEvent):
                # only accept drags within the table
                if (
                    (dragEvent.getTransferable().getSourceComponent() != DragDropServerValidationExample_this._table) or (not isinstance(dragEvent.getTransferable(), DataBoundTransferable))
                ):
                    return False
                # AbstractSelectDropTargetDetails as in a Table
                dropData = dragEvent.getTargetDetails()
                # only allow drop over a row, not between rows
                if not (VerticalDropLocation.MIDDLE == dropData.getDropLocation()):
                    return False
                t = dragEvent.getTransferable()
                # check that two different persons whose last names match
                sourceItemId = t.getItemId()
                targetItemId = dropData.getItemIdOver()
                if sourceItemId == targetItemId:
                    return False
                sourceLastName = DragDropServerValidationExample_this.getLastName(sourceItemId)
                targetLastName = DragDropServerValidationExample_this.getLastName(targetItemId)
                if sourceLastName is not None and sourceLastName == targetLastName:
                    return True
                return False

        return RelativeCriterion(*args, **kwargs)

    def __init__(self):
        DragDropServerValidationExample_thisBAA = self
        self.setSpacing(True)
        # First create the components to be able to refer to them as allowed
        # drag sources
        self._table = Table('Drag persons onto their relatives')
        self._table.setWidth('100%')
        self._container = ExampleUtil.getPersonContainer()
        self._table.setContainerDataSource(self._container)
        # Drag and drop support
        self._table.setDragMode(TableDragMode.ROW)

        class _0_(DropHandler):

            def drop(self, dropEvent):
                # criteria verify that this is safe
                t = dropEvent.getTransferable()
                sourceItemId = t.getItemId()
                dropData = dropEvent.getTargetDetails()
                targetItemId = dropData.getItemIdOver()
                # tell that the persons are related
                self.getWindow().showNotification(DragDropServerValidationExample_this.getFullName(sourceItemId) + ' is related to ' + DragDropServerValidationExample_this.getFullName(targetItemId))

            def getAcceptCriterion(self):
                # during the drag and on drop, check that two different persons
                # with the same last name
                return DragDropServerValidationExample_this.RelativeCriterion()

        _0_ = _0_()
        self._table.setDropHandler(_0_)
        self.addComponent(self._table)

    def getFullName(self, itemId):
        item = self._container.getItem(itemId)
        if item is None:
            # should not happen in this example
            return None
        fn = item.getItemProperty(ExampleUtil.PERSON_PROPERTY_FIRSTNAME).getValue()
        ln = item.getItemProperty(ExampleUtil.PERSON_PROPERTY_LASTNAME).getValue()
        return fn + ' ' + ln

    def getLastName(self, itemId):
        item = self._container.getItem(itemId)
        if item is None:
            # should not happen in this example
            return None
        return item.getItemProperty(ExampleUtil.PERSON_PROPERTY_LASTNAME).getValue()
