# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.ui.Tree import (Tree,)
from com.vaadin.ui.treetable.HierarchicalContainerOrderedWrapper import (HierarchicalContainerOrderedWrapper,)
from com.vaadin.data.Container import (Container,)
from com.vaadin.terminal.gwt.client.ui.VTreeTable import (VTreeTable,)
from com.vaadin.ui.Table import (Table,)
from com.vaadin.data.util.ContainerHierarchicalWrapper import (ContainerHierarchicalWrapper,)
from com.vaadin.ui.treetable.Collapsible import (Collapsible,)
from com.vaadin.data.util.HierarchicalContainer import (HierarchicalContainer,)
# from com.google.gwt.user.client.ui.Tree import (Tree,)
# from java.io.Serializable import (Serializable,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.Collections import (Collections,)
# from java.util.HashSet import (HashSet,)
# from java.util.List import (List,)
# from java.util.Map import (Map,)
# from java.util.logging.Logger import (Logger,)
ExpandEvent = Tree.ExpandEvent
ExpandListener = Tree.ExpandListener
CollapseEvent = Tree.CollapseEvent
CollapseListener = Tree.CollapseListener
Ordered = Container.Ordered
Hierarchical = Container.Hierarchical


class TreeTable(Table, Hierarchical):
    """TreeTable extends the {@link Table} component so that it can also visualize a
    hierarchy of its Items in a similar manner that {@link Tree} does. The tree
    hierarchy is always displayed in the first actual column of the TreeTable.
    <p>
    The TreeTable supports the usual {@link Table} features like lazy loading, so
    it should be no problem to display lots of items at once. Only required rows
    and some cache rows are sent to the client.
    <p>
    TreeTable supports standard {@link Hierarchical} container interfaces, but
    also a more fine tuned version - {@link Collapsible}. A container
    implementing the {@link Collapsible} interface stores the collapsed/expanded
    state internally and can this way scale better on the server side than with
    standard Hierarchical implementations. Developer must however note that
    {@link Collapsible} containers can not be shared among several users as they
    share UI state in the container.
    """
    _logger = Logger.getLogger(TreeTable.getName())

    class ContainerStrategy(Serializable):

        def size(self):
            pass

        def isNodeOpen(self, itemId):
            pass

        def getDepth(self, itemId):
            pass

        def toggleChildVisibility(self, itemId):
            pass

        def getIdByIndex(self, index):
            pass

        def indexOfId(self, id):
            pass

        def nextItemId(self, itemId):
            pass

        def lastItemId(self):
            pass

        def prevItemId(self, itemId):
            pass

        def isLastId(self, itemId):
            pass

        def getItemIds(self):
            pass

        def containerItemSetChange(self, event):
            pass

    def AbstractStrategy(TreeTable_this, *args, **kwargs):

        class AbstractStrategy(ContainerStrategy):

            def getDepth(self, itemId):
                """Consider adding getDepth to {@link Collapsible}, might help
                scalability with some container implementations.
                """
                depth = 0
                hierarchicalContainer = TreeTable_this.getContainerDataSource()
                while not hierarchicalContainer.isRoot(itemId):
                    depth += 1
                    itemId = hierarchicalContainer.getParent(itemId)
                return depth

            def containerItemSetChange(self, event):
                pass

        return AbstractStrategy(*args, **kwargs)

    def CollapsibleStrategy(TreeTable_this, *args, **kwargs):

        class CollapsibleStrategy(AbstractStrategy):
            """This strategy is used if current container implements {@link Collapsible}
            .

            open-collapsed logic diverted to container, otherwise use default
            implementations.
            """

            def c(self):
                return TreeTable_this.getContainerDataSource()

            def toggleChildVisibility(self, itemId):
                self.c().setCollapsed(itemId, not self.c().isCollapsed(itemId))

            def isNodeOpen(self, itemId):
                return not self.c().isCollapsed(itemId)

            def size(self):
                # return TreeTable.super.size();
                pass

            def getIdByIndex(self, index):
                # return TreeTable.super.getIdByIndex(index);
                pass

            def indexOfId(self, id):
                # return TreeTable.super.indexOfId(id);
                pass

            def isLastId(self, itemId):
                # using the default impl
                # return TreeTable.super.isLastId(itemId);
                pass

            def lastItemId(self):
                # using the default impl
                # return TreeTable.super.lastItemId();
                pass

            def nextItemId(self, itemId):
                # return TreeTable.super.nextItemId(itemId);
                pass

            def prevItemId(self, itemId):
                # return TreeTable.super.prevItemId(itemId);
                pass

            def getItemIds(self):
                # return TreeTable.super.getItemIds();
                pass

        return CollapsibleStrategy(*args, **kwargs)

    def HierarchicalStrategy(TreeTable_this, *args, **kwargs):

        class HierarchicalStrategy(AbstractStrategy):
            """Strategy for Hierarchical but not Collapsible container like
            {@link HierarchicalContainer}.

            Store collapsed/open states internally, fool Table to use preorder when
            accessing items from container via Ordered/Indexed methods.
            """
            _openItems = set()

            def isNodeOpen(self, itemId):
                return itemId in self._openItems

            def size(self):
                return len(self.getPreOrder())

            def getItemIds(self):
                return Collections.unmodifiableCollection(self.getPreOrder())

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
                indexOf = self.getPreOrder().index(itemId)
                if indexOf == -1:
                    return None
                indexOf += 1
                if indexOf == len(self.getPreOrder()):
                    return None
                else:
                    return self.getPreOrder().get(indexOf)

            def prevItemId(self, itemId):
                indexOf = self.getPreOrder().index(itemId)
                indexOf -= 1
                if indexOf < 0:
                    return None
                else:
                    return self.getPreOrder().get(indexOf)

            def toggleChildVisibility(self, itemId):
                removed = self._openItems.remove(itemId)
                if not removed:
                    self._openItems.add(itemId)
                    TreeTable_this._logger.finest('Item ' + itemId + ' is now expanded')
                else:
                    TreeTable_this._logger.finest('Item ' + itemId + ' is now collapsed')
                self.clearPreorderCache()

            def clearPreorderCache(self):
                self._preOrder = None
                # clear preorder cache

            _preOrder = None

            def getPreOrder(self):
                """Preorder of ids currently visible

                @return
                """
                if self._preOrder is None:
                    self._preOrder = list()
                    rootItemIds = TreeTable_this.getContainerDataSource().rootItemIds()
                    for id in rootItemIds:
                        self._preOrder.add(id)
                        self.addVisibleChildTree(id)
                return self._preOrder

            def addVisibleChildTree(self, id):
                if self.isNodeOpen(id):
                    children = TreeTable_this.getContainerDataSource().getChildren(id)
                    if children is not None:
                        for childId in children:
                            self._preOrder.add(childId)
                            self.addVisibleChildTree(childId)

            def indexOfId(self, id):
                return self.getPreOrder().index(id)

            def getIdByIndex(self, index):
                return self.getPreOrder().get(index)

            def containerItemSetChange(self, event):
                # preorder becomes invalid on sort, item additions etc.
                self.clearPreorderCache()
                super(HierarchicalStrategy, self).containerItemSetChange(event)

        return HierarchicalStrategy(*args, **kwargs)

    def __init__(self, *args):
        """Creates an empty TreeTable with a default container.
        ---
        Creates an empty TreeTable with a default container.

        @param caption
                   the caption for the TreeTable
        ---
        Creates a TreeTable instance with given captions and data source.

        @param caption
                   the caption for the component
        @param dataSource
                   the dataSource that is used to list items in the component
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(TreeTable, self)(None, HierarchicalContainer())
        elif _1 == 1:
            caption, = _0
            self.__init__()
            self.setCaption(caption)
        elif _1 == 2:
            caption, dataSource = _0
            super(TreeTable, self)(caption, dataSource)
        else:
            raise ARGERROR(0, 2)

    _cStrategy = None
    _focusedRowId = None
    _hierarchyColumnId = None
    # The item id that was expanded or collapsed during this request. Reset at
    # the end of paint and only used for determining if a partial or full paint
    # should be done.
    # 
    # Can safely be reset to null whenever a change occurs that would prevent a
    # partial update from rendering the correct result, e.g. rows added or
    # removed during an expand operation.

    _toggledItemId = None
    _animationsEnabled = None
    _clearFocusedRowPending = None

    def getContainerStrategy(self):
        if self._cStrategy is None:
            if isinstance(self.getContainerDataSource(), Collapsible):
                self._cStrategy = self.CollapsibleStrategy()
            else:
                self._cStrategy = self.HierarchicalStrategy()
        return self._cStrategy

    def paintRowAttributes(self, target, itemId):
        super(TreeTable, self).paintRowAttributes(target, itemId)
        target.addAttribute('depth', self.getContainerStrategy().getDepth(itemId))
        if self.getContainerDataSource().areChildrenAllowed(itemId):
            target.addAttribute('ca', True)
            target.addAttribute('open', self.getContainerStrategy().isNodeOpen(itemId))

    def paintRowIcon(self, target, cells, indexInRowbuffer):
        # always paint if present (in parent only if row headers visible)
        if self.getRowHeaderMode() == self.ROW_HEADER_MODE_HIDDEN:
            itemIcon = self.getItemIcon(cells[self.CELL_ITEMID][indexInRowbuffer])
            if itemIcon is not None:
                target.addAttribute('icon', itemIcon)
        elif cells[self.CELL_ICON][indexInRowbuffer] is not None:
            target.addAttribute('icon', cells[self.CELL_ICON][indexInRowbuffer])

    def changeVariables(self, source, variables):
        super(TreeTable, self).changeVariables(source, variables)
        if 'toggleCollapsed' in variables:
            object = variables['toggleCollapsed']
            itemId = self.itemIdMapper.get(object)
            self._toggledItemId = itemId
            self.toggleChildVisibility(itemId)
            if 'selectCollapsed' in variables:
                # ensure collapsed is selected unless opened with selection
                # head
                if self.isSelectable():
                    self.select(itemId)
        elif 'focusParent' in variables:
            key = variables['focusParent']
            refId = self.itemIdMapper.get(key)
            itemId = self.getParent(refId)
            self.focusParent(itemId)

    def focusParent(self, itemId):
        inView = False
        inPageId = self.getCurrentPageFirstItemId()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (inPageId is not None and i < self.getPageLength()):
                break
            if inPageId == itemId:
                inView = True
                break
            inPageId = self.nextItemId(inPageId)
            i += 1
        if not inView:
            self.setCurrentPageFirstItemId(itemId)
        # Select the row if it is selectable.
        if self.isSelectable():
            if self.isMultiSelect():
                self.setValue(Collections.singleton(itemId))
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
        # Override methods for partial row updates and additions when expanding /
        # collapsing nodes.

        if self._focusedRowId is not None:
            target.addAttribute('focusedRow', self.itemIdMapper.key(self._focusedRowId))
            self._focusedRowId = None
        elif self._clearFocusedRowPending:
            # Must still inform the client that the focusParent request has
            # been processed
            target.addAttribute('clearFocusPending', True)
            self._clearFocusedRowPending = False
        target.addAttribute('animate', self._animationsEnabled)
        if self._hierarchyColumnId is not None:
            visibleColumns2 = self.getVisibleColumns()
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(visibleColumns2)):
                    break
                object = visibleColumns2[i]
                if self._hierarchyColumnId == object:
                    target.addAttribute(VTreeTable.ATTRIBUTE_HIERARCHY_COLUMN_INDEX, i)
                    break
        super(TreeTable, self).paintContent(target)
        self._toggledItemId = None

    def isPartialRowUpdate(self):
        return self._toggledItemId is not None

    def getFirstAddedItemIndex(self):
        return self.indexOfId(self._toggledItemId) + 1

    def getAddedRowCount(self):
        return self.countSubNodesRecursively(self.getContainerDataSource(), self._toggledItemId)

    def countSubNodesRecursively(self, hc, itemId):
        count = 0
        # we need the number of children for toggledItemId no matter if its
        # collapsed or expanded. Other items' children are only counted if the
        # item is expanded.
        if (
            self.getContainerStrategy().isNodeOpen(itemId) or (itemId == self._toggledItemId)
        ):
            children = hc.getChildren(itemId)
            if children is not None:
                count += len(children) if children is not None else 0
                for id in children:
                    count += self.countSubNodesRecursively(hc, id)
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
        self.setCurrentPageFirstItemIndex(self.getCurrentPageFirstItemIndex(), False)
        self.requestRepaint()
        if self.isCollapsed(itemId):
            self.fireCollapseEvent(itemId)
        else:
            self.fireExpandEvent(itemId)

    def size(self):
        return len(self.getContainerStrategy())

    def getContainerDataSource(self):
        return super(TreeTable, self).getContainerDataSource()

    def setContainerDataSource(self, newDataSource):
        self._cStrategy = None
        if not isinstance(newDataSource, Hierarchical):
            newDataSource = ContainerHierarchicalWrapper(newDataSource)
        if not isinstance(newDataSource, Ordered):
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

    def getParent(self, itemId):
        return self.getContainerDataSource().getParent(itemId)

    def hasChildren(self, itemId):
        return self.getContainerDataSource().hasChildren(itemId)

    def isRoot(self, itemId):
        return self.getContainerDataSource().isRoot(itemId)

    def rootItemIds(self):
        return self.getContainerDataSource().rootItemIds()

    def setChildrenAllowed(self, itemId, areChildrenAllowed):
        return self.getContainerDataSource().setChildrenAllowed(itemId, areChildrenAllowed)

    def setParent(self, itemId, newParentId):
        return self.getContainerDataSource().setParent(itemId, newParentId)

    def setCollapsed(self, itemId, collapsed):
        """Sets the Item specified by given identifier collapsed or expanded. If the
        Item is collapsed, its children is not displayed in for the user.

        @param itemId
                   the identifier of the Item
        @param collapsed
                   true if the Item should be collapsed, false if expanded
        """
        if self.isCollapsed(itemId) != collapsed:
            self.toggleChildVisibility(itemId)

    def isCollapsed(self, itemId):
        """Checks if Item with given identifier is collapsed in the UI.

        <p>

        @param itemId
                   the identifier of the checked Item
        @return true if the Item with given id is collapsed
        @see Collapsible#isCollapsed(Object)
        """
        return not self.getContainerStrategy().isNodeOpen(itemId)

    def setHierarchyColumn(self, hierarchyColumnId):
        """Explicitly sets the column in which the TreeTable visualizes the
        hierarchy. If hierarchyColumnId is not set, the hierarchy is visualized
        in the first visible column.

        @param hierarchyColumnId
        """
        self._hierarchyColumnId = hierarchyColumnId

    def getHierarchyColumnId(self):
        """@return the identifier of column into which the hierarchy will be
                visualized or null if the column is not explicitly defined.
        """
        return self._hierarchyColumnId

    def addListener(self, *args):
        """Adds an expand listener.

        @param listener
                   the Listener to be added.
        ---
        Adds a collapse listener.

        @param listener
                   the Listener to be added.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], CollapseListener):
                listener, = _0
                self.addListener(CollapseEvent, listener, CollapseListener.COLLAPSE_METHOD)
            else:
                listener, = _0
                self.addListener(ExpandEvent, listener, ExpandListener.EXPAND_METHOD)
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        """Removes an expand listener.

        @param listener
                   the Listener to be removed.
        ---
        Removes a collapse listener.

        @param listener
                   the Listener to be removed.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], CollapseListener):
                listener, = _0
                self.removeListener(CollapseEvent, listener, CollapseListener.COLLAPSE_METHOD)
            else:
                listener, = _0
                self.removeListener(ExpandEvent, listener, ExpandListener.EXPAND_METHOD)
        else:
            raise ARGERROR(1, 1)

    def fireExpandEvent(self, itemId):
        """Emits an expand event.

        @param itemId
                   the item id.
        """
        self.fireEvent(ExpandEvent(self, itemId))

    def fireCollapseEvent(self, itemId):
        """Emits a collapse event.

        @param itemId
                   the item id.
        """
        self.fireEvent(CollapseEvent(self, itemId))

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
