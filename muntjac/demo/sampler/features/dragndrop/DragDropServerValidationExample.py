
from muntjac.demo.sampler.ExampleUtil import ExampleUtil

from muntjac.event.dd.acceptcriteria.server_side_criterion import \
    ServerSideCriterion

from muntjac.terminal.gwt.client.ui.dd.vertical_drop_location import \
    VerticalDropLocation

from muntjac.api import HorizontalLayout, Table
from muntjac.ui.table import TableDragMode
from muntjac.event.dd.drop_handler import IDropHandler
from muntjac.event.data_bound_transferable import DataBoundTransferable


class DragDropServerValidationExample(HorizontalLayout):

    def __init__(self):
        super(DragDropServerValidationExample, self).__init__()

        self.setSpacing(True)

        # First create the components to be able to refer to them as allowed
        # drag sources
        self._table = Table('Drag persons onto their relatives')
        self._table.setWidth('100%')

        self._container = ExampleUtil.getPersonContainer()
        self._table.setContainerDataSource(self._container)

        # Drag and drop support
        self._table.setDragMode(TableDragMode.ROW)

        self._table.setDropHandler( TableDropHandler(self) )
        self.addComponent(self._table)


    def getFullName(self, itemId):
        item = self._container.getItem(itemId)
        if item is None:
            # should not happen in this example
            return None
        fn = item.getItemProperty(
                ExampleUtil.PERSON_PROPERTY_FIRSTNAME).getValue()
        ln = item.getItemProperty(
                ExampleUtil.PERSON_PROPERTY_LASTNAME).getValue()
        return fn + ' ' + ln


    def getLastName(self, itemId):
        item = self._container.getItem(itemId)

        if item is None:
            # should not happen in this example
            return None

        return item.getItemProperty(
                ExampleUtil.PERSON_PROPERTY_LASTNAME).getValue()


class TableDropHandler(IDropHandler):

    def __init__(self, example):
        self._example = example

    def drop(self, dropEvent):
        # criteria verify that this is safe
        t = dropEvent.getTransferable()

        sourceItemId = t.getItemId()

        dropData = dropEvent.getTargetDetails()
        targetItemId = dropData.getItemIdOver()

        # tell that the persons are related
        self.getWindow().showNotification(
                self.getFullName(sourceItemId)
                + ' is related to '
                + self.getFullName(targetItemId))

    def getAcceptCriterion(self):
        # during the drag and on drop, check that two different
        # persons with the same last name
        return RelativeCriterion(self._example)


class RelativeCriterion(ServerSideCriterion):

    def __init__(self, example):
        super(RelativeCriterion, self).__init__()

        self._example = example


    def accept(self, dragEvent):
        # only accept drags within the table
        if ((dragEvent.getTransferable().getSourceComponent() != \
             self._example._table)
                or (not isinstance(dragEvent.getTransferable(),
                        DataBoundTransferable))):
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

        sourceLastName = self._example.getLastName(sourceItemId)
        targetLastName = self._example.getLastName(targetItemId)

        if (sourceLastName is not None) and sourceLastName == targetLastName:
            return True

        return False
