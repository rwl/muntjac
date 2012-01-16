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

import logging

from muntjac.ui.tree \
    import ExpandEvent, IExpandListener, CollapseEvent, ICollapseListener, \
    COLLAPSE_METHOD, EXPAND_METHOD

from muntjac.ui.treetable.hierarchical_container_ordered_wrapper \
    import HierarchicalContainerOrderedWrapper

from muntjac.data.container import IOrdered, IHierarchical
from muntjac.terminal.gwt.client.ui.v_tree_table import VTreeTable
from muntjac.ui.table import Table

from muntjac.data.util.container_hierarchical_wrapper \
    import ContainerHierarchicalWrapper

from muntjac.ui.treetable.collapsible import ICollapsible
from muntjac.data.util.hierarchical_container import HierarchicalContainer


logger = logging.getLogger(__name__)


class TreeTable(Table, IHierarchical):
    """TreeTable extends the L{Table} component so that it can also visualize
    a hierarchy of its Items in a similar manner that {@link Tree} does. The
    tree hierarchy is always displayed in the first actual column of the
    TreeTable.

    The TreeTable supports the usual {@link Table} features like lazy loading,
    so it should be no problem to display lots of items at once. Only required
    rows and some cache rows are sent to the client.

    TreeTable supports standard L{IHierarchical} container interfaces, but
    also a more fine tuned version - L{ICollapsible}. A container
    implementing the L{ICollapsible} interface stores the collapsed/expanded
    state internally and can this way scale better on the server side than with
    standard Hierarchical implementations. Developer must however note that
    L{ICollapsible} containers can not be shared among several users as they
    share UI state in the container.
    """

    def __init__(self, caption=None, dataSource=None):
        """Creates a TreeTable instance with optional captions and data source.

        @param caption:
                   the caption for the component
        @param dataSource:
                   the dataSource that is used to list items in the component
        """
        if dataSource is None:
            dataSource = HierarchicalContainer()

        super(TreeTable, self).__init__(caption, dataSource)


        self._cStrategy = None
        self._focusedRowId = None
        self._hierarchyColumnId = None

        # The item id that was expanded or collapsed during this request. Reset
        # at the end of paint and only used for determining if a partial or
        # full paint should be done.
        #
        # Can safely be reset to null whenever a change occurs that would
        # prevent a partial update from rendering the correct result, e.g. rows
        # added or removed during an expand operation.
        self._toggledItemId = None
        self._animationsEnabled = None
        self._clearFocusedRowPending = None


    def getContainerStrategy(self):
        if self._cStrategy is None:
            if isinstance(self.getContainerDataSource(), ICollapsible):
                self._cStrategy = CollapsibleStrategy(self)
            else:
                self._cStrategy = HierarchicalStrategy(self)
        return self._cStrategy


    def paintRowAttributes(self, target, itemId):
        super(TreeTable, self).paintRowAttributes(target, itemId)
        depth = self.getContainerStrategy().getDepth(itemId)
        target.addAttribute('depth', depth)
        if self.getContainerDataSource().areChildrenAllowed(itemId):
            target.addAttribute('ca', True)
            isOpen = self.getContainerStrategy().isNodeOpen(itemId)
            target.addAttribute('open', isOpen)


    def paintRowIcon(self, target, cells, indexInRowbuffer):
        # always paint if present (in parent only if row headers visible)
        if self.getRowHeaderMode() == self.ROW_HEADER_MODE_HIDDEN:
            cell = cells[self.CELL_ITEMID][indexInRowbuffer]
            itemIcon = self.getItemIcon(cell)
            if itemIcon is not None:
                target.addAttribute('icon', itemIcon)
        elif cells[self.CELL_ICON][indexInRowbuffer] is not None:
            cell = cells[self.CELL_ICON][indexInRowbuffer]
            target.addAttribute('icon', cell)


    def changeVariables(self, source, variables):
        super(TreeTable, self).changeVariables(source, variables)
        if 'toggleCollapsed' in variables:
            obj = variables.get('toggleCollapsed')
            itemId = self.itemIdMapper.get(obj)
            self._toggledItemId = itemId
            self.toggleChildVisibility(itemId)
            if 'selectCollapsed' in variables:
                # ensure collapsed is selected unless opened with selection
                # head
                if self.isSelectable():
                    self.select(itemId)
        elif 'focusParent' in variables:
            key = variables.get('focusParent')
            refId = self.itemIdMapper.get(key)
            itemId = self.getParent(refId)
            self.focusParent(itemId)


    def focusParent(self, itemId):
        inView = False
        inPageId = self.getCurrentPageFirstItemId()

        i = 0
        while inPageId is not None and i < self.getPageLength():
            if inPageId == itemId:
                inView = True
                break
            inPageId = self.nextItemId(inPageId)
            i += 1  # TODO: check increment

        if not inView:
            self.setCurrentPageFirstItemId(itemId)

        # Select the row if it is selectable.
        if self.isSelectable():
            if self.isMultiSelect():
                self.setValue([itemId])
            else:
                self.setValue(itemId)

        self.setFocusedRow(itemId)


    def setFocusedRow(self, itemId):
        self._focusedRowId = itemId
        if self._focusedRowId is None:
            # Must still inform the client that the focusParent request has
            # been processed
            self._clearFocusedRowPending = True
        self.requestRepaint()


    def paintContent(self, target):
        # Override methods for partial row updates and additions when
        # expanding / collapsing nodes.

        if self._focusedRowId is not None:
            row = self.itemIdMapper.key(self._focusedRowId)
            target.addAttribute('focusedRow', row)
            self._focusedRowId = None
        elif self._clearFocusedRowPending:
            # Must still inform the client that the focusParent request has
            # been processed
            target.addAttribute('clearFocusPending', True)
            self._clearFocusedRowPending = False

        target.addAttribute('animate', self._animationsEnabled)
        if self._hierarchyColumnId is not None:
            visibleColumns2 = self.getVisibleColumns()
            for i in range(len(visibleColumns2)):
                obj = visibleColumns2[i]
                if self._hierarchyColumnId == obj:
                    ahci = VTreeTable.ATTRIBUTE_HIERARCHY_COLUMN_INDEX
                    target.addAttribute(ahci, i)
                    break

        super(TreeTable, self).paintContent(target)
        self._toggledItemId = None


    def isPartialRowUpdate(self):
        return self._toggledItemId is not None


    def getFirstAddedItemIndex(self):
        return self.indexOfId(self._toggledItemId) + 1


    def getAddedRowCount(self):
        ds = self.getContainerDataSource()
        return self.countSubNodesRecursively(ds, self._toggledItemId)


    def countSubNodesRecursively(self, hc, itemId):
        count = 0
        # we need the number of children for toggledItemId no matter if its
        # collapsed or expanded. Other items' children are only counted if the
        # item is expanded.
        if (self.getContainerStrategy().isNodeOpen(itemId)
                or (itemId == self._toggledItemId)):
            children = hc.getChildren(itemId)
            if children is not None:
                count += len(children) if children is not None else 0
                for idd in children:
                    count += self.countSubNodesRecursively(hc, idd)
        return count


    def getFirstUpdatedItemIndex(self):
        return self.indexOfId(self._toggledItemId)


    def getUpdatedRowCount(self):
        return 1


    def shouldHideAddedRows(self):
        return not self.getContainerStrategy().isNodeOpen(self._toggledItemId)


    def toggleChildVisibility(self, itemId):
        self.getContainerStrategy().toggleChildVisibility(itemId)
        # ensure that page still has first item in page, DON'T clear the
        # caches.
        idx = self.getCurrentPageFirstItemIndex()
        self.setCurrentPageFirstItemIndex(idx, False)
        self.requestRepaint()
        if self.isCollapsed(itemId):
            self.fireCollapseEvent(itemId)
        else:
            self.fireExpandEvent(itemId)


    def size(self):
        return len(self.getContainerStrategy())


    def __len__(self):
        return self.size()


    def getContainerDataSource(self):
        return super(TreeTable, self).getContainerDataSource()


    def setContainerDataSource(self, newDataSource):
        self._cStrategy = None
        if not isinstance(newDataSource, IHierarchical):
            newDataSource = ContainerHierarchicalWrapper(newDataSource)
        if not isinstance(newDataSource, IOrdered):
            newDataSource = HierarchicalContainerOrderedWrapper(newDataSource)
        super(TreeTable, self).setContainerDataSource(newDataSource)


    def containerItemSetChange(self, event):
        # Can't do partial repaints if items are added or removed during the
        # expand/collapse request
        self._toggledItemId = None
        self.getContainerStrategy().containerItemSetChange(event)
        super(TreeTable, self).containerItemSetChange(event)


    def getIdByIndex(self, index):
        return self.getContainerStrategy().getIdByIndex(index)


    def indexOfId(self, itemId):
        return self.getContainerStrategy().indexOfId(itemId)


    def nextItemId(self, itemId):
        return self.getContainerStrategy().nextItemId(itemId)


    def lastItemId(self):
        return self.getContainerStrategy().lastItemId()


    def prevItemId(self, itemId):
        return self.getContainerStrategy().prevItemId(itemId)


    def isLastId(self, itemId):
        return self.getContainerStrategy().isLastId(itemId)


    def getItemIds(self):
        return self.getContainerStrategy().getItemIds()


    def areChildrenAllowed(self, itemId):
        return self.getContainerDataSource().areChildrenAllowed(itemId)


    def getChildren(self, itemId):
        return self.getContainerDataSource().getChildren(itemId)


    def getParent(self, itemId=None):
        if itemId is not None:
            return self.getContainerDataSource().getParent(itemId)
        else:
            super(TreeTable, self).getParent()


    def hasChildren(self, itemId):
        return self.getContainerDataSource().hasChildren(itemId)


    def isRoot(self, itemId):
        return self.getContainerDataSource().isRoot(itemId)


    def rootItemIds(self):
        return self.getContainerDataSource().rootItemIds()


    def setChildrenAllowed(self, itemId, areChildrenAllowed):
        return self.getContainerDataSource().setChildrenAllowed(itemId,
                areChildrenAllowed)


    def setParent(self, itemId, newParentId):
        return self.getContainerDataSource().setParent(itemId, newParentId)


    def setCollapsed(self, itemId, collapsed):
        """Sets the Item specified by given identifier collapsed or expanded.
        If the Item is collapsed, its children is not displayed in for the
        user.

        @param itemId:
                   the identifier of the Item
        @param collapsed:
                   true if the Item should be collapsed, false if expanded
        """
        if self.isCollapsed(itemId) != collapsed:
            self.toggleChildVisibility(itemId)


    def isCollapsed(self, itemId):
        """Checks if Item with given identifier is collapsed in the UI.

        @param itemId:
                   the identifier of the checked Item
        @return: true if the Item with given id is collapsed
        @see: L{ICollapsible.isCollapsed}
        """
        return not self.getContainerStrategy().isNodeOpen(itemId)


    def setHierarchyColumn(self, hierarchyColumnId):
        """Explicitly sets the column in which the TreeTable visualizes the
        hierarchy. If hierarchyColumnId is not set, the hierarchy is visualized
        in the first visible column.
        """
        self._hierarchyColumnId = hierarchyColumnId


    def getHierarchyColumnId(self):
        """@return: the identifier of column into which the hierarchy will be
        visualized or null if the column is not explicitly defined.
        """
        return self._hierarchyColumnId


    def addListener(self, listener, iface=None):
        """Adds an expand/collapse listener.

        @param listener:
                   the Listener to be added.
        """
        if (isinstance(listener, ICollapseListener) and
                (iface is None or issubclass(iface, ICollapseListener))):
            self.registerListener(CollapseEvent,
                    listener, COLLAPSE_METHOD)

        if (isinstance(listener, IExpandListener) and
                (iface is None or issubclass(iface, IExpandListener))):
            self.registerListener(ExpandEvent,
                    listener, EXPAND_METHOD)

        super(TreeTable, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, CollapseEvent):
            self.registerCallback(CollapseEvent, callback, None, *args)

        elif issubclass(eventType, ExpandEvent):
            self.registerCallback(ExpandEvent, callback, None, *args)

        else:
            super(TreeTable, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        """Removes an expand or collapselistener.

        @param listener:
                   the Listener to be removed.
        """
        if (isinstance(listener, ICollapseListener) and
                (iface is None or issubclass(iface, ICollapseListener))):
            self.withdrawListener(CollapseEvent,
                    listener, COLLAPSE_METHOD)

        if (isinstance(listener, IExpandListener) and
                (iface is None or issubclass(iface, IExpandListener))):
            self.withdrawListener(ExpandEvent,
                    listener, EXPAND_METHOD)

        super(TreeTable, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, CollapseEvent):
            self.withdrawCallback(CollapseEvent, callback)

        elif issubclass(eventType, ExpandEvent):
            self.withdrawCallback(ExpandEvent, callback)

        else:
            super(TreeTable, self).removeCallback(callback, eventType)


    def fireExpandEvent(self, itemId):
        """Emits an expand event.

        @param itemId:
                   the item id.
        """
        evt = ExpandEvent(self, itemId)
        self.fireEvent(evt)


    def fireCollapseEvent(self, itemId):
        """Emits a collapse event.

        @param itemId:
                   the item id.
        """
        evt = CollapseEvent(self, itemId)
        self.fireEvent(evt)


    def isAnimationsEnabled(self):
        """@return true if animations are enabled"""
        return self._animationsEnabled


    def setAnimationsEnabled(self, animationsEnabled):
        """Animations can be enabled by passing true to this method. Currently
        expanding rows slide in from the top and collapsing rows slide out the
        same way. NOTE! not supported in Internet Explorer 6 or 7.

        @param animationsEnabled
                   true or false whether to enable animations or not.
        """
        self._animationsEnabled = animationsEnabled
        self.requestRepaint()


class IContainerStrategy(object):

    def size(self):
        raise NotImplementedError

    def __len__(self):
        return self.size()

    def isNodeOpen(self, itemId):
        raise NotImplementedError

    def getDepth(self, itemId):
        raise NotImplementedError

    def toggleChildVisibility(self, itemId):
        raise NotImplementedError

    def getIdByIndex(self, index):
        raise NotImplementedError

    def indexOfId(self, idd):
        raise NotImplementedError

    def nextItemId(self, itemId):
        raise NotImplementedError

    def lastItemId(self):
        raise NotImplementedError

    def prevItemId(self, itemId):
        raise NotImplementedError

    def isLastId(self, itemId):
        raise NotImplementedError

    def getItemIds(self):
        raise NotImplementedError

    def containerItemSetChange(self, event):
        raise NotImplementedError


class AbstractStrategy(IContainerStrategy):

    def __init__(self, treetable):
        self._treetable = treetable


    def getDepth(self, itemId):
        """Consider adding getDepth to L{ICollapsible}, might help
        scalability with some container implementations.
        """
        depth = 0
        hierarchicalContainer = self._treetable.getContainerDataSource()
        while not hierarchicalContainer.isRoot(itemId):
            depth += 1
            itemId = hierarchicalContainer.getParent(itemId)
        return depth


    def containerItemSetChange(self, event):
        pass


class CollapsibleStrategy(AbstractStrategy):
    """This strategy is used if current container implements L{Collapsible}.

    Open-collapsed logic diverted to container, otherwise use default
    implementations.
    """

    def c(self):
        return self._treetable.getContainerDataSource()


    def toggleChildVisibility(self, itemId):
        self.c().setCollapsed(itemId, not self.c().isCollapsed(itemId))


    def isNodeOpen(self, itemId):
        return not self.c().isCollapsed(itemId)


    def size(self):
        super(TreeTable, self._treetable).size()


    def getIdByIndex(self, index):
        super(TreeTable, self._treetable).getIdByIndex(index)


    def indexOfId(self, idd):
        super(TreeTable, self._treetable).indexOfId(idd)


    def isLastId(self, itemId):
        # using the default impl
        super(TreeTable, self._treetable).isLastId(itemId)


    def lastItemId(self):
        # using the default impl
        super(TreeTable, self._treetable).lastItemId()


    def nextItemId(self, itemId):
        super(TreeTable, self._treetable).nextItemId(itemId)


    def prevItemId(self, itemId):
        super(TreeTable, self._treetable).prevItemId(itemId)


    def getItemIds(self):
        super(TreeTable, self._treetable).getItemIds()


class HierarchicalStrategy(AbstractStrategy):
    """Strategy for Hierarchical but not Collapsible container like
    L{HierarchicalContainer}.

    Store collapsed/open states internally, fool Table to use preorder when
    accessing items from container via Ordered/Indexed methods.
    """

    def __init__(self, treetable):
        self._openItems = set()
        self._preOrder = None

        super(HierarchicalStrategy, self).__init__(treetable)


    def isNodeOpen(self, itemId):
        return itemId in self._openItems


    def size(self):
        return len(self.getPreOrder())


    def getItemIds(self):
        return list(self.getPreOrder())


    def isLastId(self, itemId):
        if itemId is None:
            return False
        return itemId == self.lastItemId()


    def lastItemId(self):
        if len(self.getPreOrder()) > 0:
            return self.getPreOrder().get(len(self.getPreOrder()) - 1)
        else:
            return None


    def nextItemId(self, itemId):
        try:
            indexOf = self.getPreOrder().index(itemId)
        except ValueError:
            return None

        indexOf += 1

        if indexOf == len(self.getPreOrder()):
            return None
        else:
            return self.getPreOrder().get(indexOf)


    def prevItemId(self, itemId):
        try:
            indexOf = self.getPreOrder().index(itemId)
        except ValueError:
            indexOf = -1
        indexOf -= 1
        if indexOf < 0:
            return None
        else:
            return self.getPreOrder().get(indexOf)


    def toggleChildVisibility(self, itemId):
        if itemId in self._openItems:
            self._openItems.remove(itemId)
            removed = True
        else:
            removed = False

        if not removed:
            self._openItems.add(itemId)
            logger.debug('Item ' + itemId + ' is now expanded')
        else:
            logger.debug('Item ' + itemId + ' is now collapsed')

        self.clearPreorderCache()


    def clearPreorderCache(self):
        self._preOrder = None  # clear preorder cache


    def getPreOrder(self):
        """Preorder of ids currently visible.
        """
        if self._preOrder is None:
            self._preOrder = list()
            dataSource = self._treetable.getContainerDataSource()
            rootItemIds = dataSource.rootItemIds()
            for idd in rootItemIds:
                self._preOrder.add(idd)
                self.addVisibleChildTree(idd)
        return self._preOrder


    def addVisibleChildTree(self, idd):
        if self.isNodeOpen(idd):
            dataSource = self._treetable.getContainerDataSource()
            children = dataSource.getChildren(idd)
            if children is not None:
                for childId in children:
                    self._preOrder.add(childId)
                    self.addVisibleChildTree(childId)


    def indexOfId(self, idd):
        try:
            return self.getPreOrder().index(idd)
        except ValueError:
            return -1


    def getIdByIndex(self, index):
        return self.getPreOrder().get(index)


    def containerItemSetChange(self, event):
        # preorder becomes invalid on sort, item additions etc.
        self.clearPreorderCache()
        super(HierarchicalStrategy, self).containerItemSetChange(event)
