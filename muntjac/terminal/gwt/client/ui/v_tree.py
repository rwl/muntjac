# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from __pyjamas__ import JS

from pyjamas import DOM, Window

from pyjamas.ui import Event, KeyboardListener

from pyjamas.ui.UIObject import UIObject
from pyjamas.ui.Widget import Widget
from pyjamas.ui.FlowPanel import FlowPanel
from pyjamas.ui.SimplePanel import SimplePanel

from muntjac.terminal.gwt.client.paintable import IPaintable
from muntjac.terminal.gwt.client.tooltip_info import TooltipInfo
from muntjac.terminal.gwt.client.ui.dd.dd_util import DDUtil
from muntjac.terminal.gwt.client.v_tooltip import VTooltip
from muntjac.terminal.gwt.client.ui.dd.vertical_drop_location import VerticalDropLocation
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.ui.dd.v_has_drop_handler import VHasDropHandler
from muntjac.terminal.gwt.client.ui.focus_element_panel import FocusElementPanel
from muntjac.terminal.gwt.client.ui.action_owner import ActionOwner
from muntjac.terminal.gwt.client.ui.tree_action import TreeAction
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails
from muntjac.terminal.gwt.client.ui.sub_part_aware import SubPartAware
from muntjac.terminal.gwt.client.ui.dd.v_accept_callback import VAcceptCallback
from muntjac.terminal.gwt.client.ui.dd.v_transferable import VTransferable
from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.ui.dd.v_drag_and_drop_manager import VDragAndDropManager
from muntjac.terminal.gwt.client.ui.dd.v_abstract_drop_handler import VAbstractDropHandler
from muntjac.terminal.gwt.client.ui.icon import Icon


class VTree(FocusElementPanel, IPaintable, VHasDropHandler, SubPartAware,
            ActionOwner):
#            FocusHandler, BlurHandler, KeyPressHandler, KeyDownHandler):

    CLASSNAME = 'v-tree'

    ITEM_CLICK_EVENT_ID = 'itemClick'

    MULTISELECT_MODE_DEFAULT = 0
    MULTISELECT_MODE_SIMPLE = 1

    _CHARCODE_SPACE = 32

    _SUBPART_NODE_PREFIX = 'n'
    _EXPAND_IDENTIFIER = 'expand'

    def __init__(self):

        self._body = FlowPanel()
        self._selectedIds = set()
        self._client = None
        self._paintableId = None
        self._selectable = None
        self._isMultiselect = None
        self._currentMouseOverKey = None
        self._lastSelection = None
        self._focusedNode = None
        self._multiSelectMode = self.MULTISELECT_MODE_DEFAULT
        self._keyToNode = dict()
        # This map contains captions and icon urls for actions like: * "33_c" ->
        # "Edit" * "33_i" -> "http://dom.com/edit.png"
        self._actionMap = dict()
        self._immediate = None
        self._isNullSelectionAllowed = True
        self._disabled = False
        self._readonly = None
        self._rendering = None
        self._dropHandler = None
        self._dragMode = None
        self._selectionHasChanged = False
        self._bodyActionKeys = None

        # iconLoaded = VLazyExecutor(50,
        # new ScheduledCommand() {
        # public void execute() {
        # Util.notifyParentOfSizeChange(VTree.this, true);
        # }
        # });

        # In webkit, focus may have been requested for this component but not yet
        # gained. Use this to trac if tree has gained the focus on webkit. See
        # FocusImplSafari and #6373
        self._treeHasFocus = None

        super(VTree, self).__init__()
        self.setStyleName(self.CLASSNAME)
        self.add(self._body)

        self.addFocusHandler(self)
        self.addBlurHandler(self)

        # Listen to context menu events on the empty space in the tree
        self.sinkEvents(Event.ONCONTEXTMENU)

        class _1_(ContextMenuHandler):

            def onContextMenu(self, event):
                VTree_this.handleBodyContextMenu(event)

        _1_ = _1_()
        self.addDomHandler(_1_, ContextMenuEvent.getType())

        # Firefox auto-repeat works correctly only if we use a key press
        # handler, other browsers handle it correctly when using a key down
        # handler
        if BrowserInfo.get().isGecko() or BrowserInfo.get().isOpera():
            self.addKeyPressHandler(self)
        else:
            self.addKeyDownHandler(self)

        # We need to use the sinkEvents method to catch the keyUp events so we
        # can cache a single shift. KeyUpHandler cannot do this. At the same
        # time we catch the mouse down and up events so we can apply the text
        # selection patch in IE
        self.sinkEvents(Event.ONMOUSEDOWN | Event.ONMOUSEUP | Event.ONKEYUP)

        # Re-set the tab index to make sure that the FocusElementPanel's
        # (super) focus element gets the tab index and not the element
        # containing the tree.
        self.setTabIndex(0)


    def onBrowserEvent(self, event):
        super(VTree, self).onBrowserEvent(event)
        if event.getTypeInt() == Event.ONMOUSEDOWN:
            # Prevent default text selection in IE
            if BrowserInfo.get().isIE():
                event.getEventTarget().setPropertyJSO('onselectstart',
                        self.applyDisableTextSelectionIEHack())
        elif event.getTypeInt() == Event.ONMOUSEUP:
            # Remove IE text selection hack
            if BrowserInfo.get().isIE():
                event.getEventTarget().setPropertyJSO('onselectstart', None)
        elif event.getTypeInt() == Event.ONKEYUP:
            if self._selectionHasChanged:
                if (event.getKeyCode() == self.getNavigationDownKey()
                        and not event.getShiftKey()):
                    self.sendSelectionToServer()
                    event.preventDefault()
                elif (event.getKeyCode() == self.getNavigationUpKey()
                        and not event.getShiftKey()):
                    self.sendSelectionToServer()
                    event.preventDefault()
                elif event.getKeyCode() == KeyboardListener.KEY_SHIFT:
                    self.sendSelectionToServer()
                    event.preventDefault()
                elif event.getKeyCode() == self.getNavigationSelectKey():
                    self.sendSelectionToServer()
                    event.preventDefault()


    def updateActionMap(self, c):
        it = c.getChildIterator()
        while it.hasNext():
            action = it.next()
            key = action.getStringAttribute('key')
            caption = action.getStringAttribute('caption')
            self._actionMap.put(key + '_c', caption)
            if action.hasAttribute('icon'):
                # TODO need some uri handling ??
                self._actionMap[key + '_i'] = \
                    self._client.translateVaadinUri(
                            action.getStringAttribute('icon'))
            else:
                self._actionMap.remove(key + '_i')


    def getActionCaption(self, actionKey):
        return self._actionMap.get(actionKey + '_c')


    def getActionIcon(self, actionKey):
        return self._actionMap.gfet(actionKey + '_i')


    def updateFromUIDL(self, uidl, client):
        # Ensure correct implementation and let container manage caption
        if client.updateComponent(self, uidl, True):
            return

        self._rendering = True

        self._client = client

        if uidl.hasAttribute('partialUpdate'):
            self.handleUpdate(uidl)
            self._rendering = False
            return

        self._paintableId = uidl.getId()

        self._immediate = uidl.hasAttribute('immediate')

        self._disabled = uidl.getBooleanAttribute('disabled')
        self._readonly = uidl.getBooleanAttribute('readonly')

        self._dragMode = uidl.getIntAttribute('dragMode') if uidl.hasAttribute('dragMode') else 0

        self._isNullSelectionAllowed = uidl.getBooleanAttribute('nullselect')

        if uidl.hasAttribute('alb'):
            self._bodyActionKeys = uidl.getStringArrayAttribute('alb')

        self._body.clear()
        # clear out any references to nodes that no longer are attached
        self._keyToNode.clear()
        childTree = None
        childUidl = None

        i = uidl.getChildIterator()
        while i.hasNext():
            childUidl = i.next()
            if 'actions' == childUidl.getTag():
                self.updateActionMap(childUidl)
                continue
            elif '-ac' == childUidl.getTag():
                self.updateDropHandler(childUidl)
                continue

            childTree = self.TreeNode()
            if childTree.ie6compatnode is not None:
                self._body.add(childTree)

            childTree.updateFromUIDL(childUidl, client)
            if childTree.ie6compatnode is None:
                self._body.add(childTree)

            childTree.addStyleDependentName('root')
            childTree.childNodeContainer.addStyleDependentName('root')

        if childTree is not None and childUidl is not None:
            leaf = not (childUidl.getTag() == 'node')
            childTree.addStyleDependentName('leaf-last' if leaf else 'last')
            childTree.childNodeContainer.addStyleDependentName('last')

        selectMode = uidl.getStringAttribute('selectmode')
        self._selectable = not ('none' == selectMode)
        self._isMultiselect = 'multi' == selectMode

        if self._isMultiselect:
            self._multiSelectMode = uidl.getIntAttribute('multiselectmode')

        self._selectedIds = uidl.getStringArrayVariableAsSet('selected')

        # Update lastSelection and focusedNode to point to *actual* nodes again
        # after the old ones have been cleared from the body. This fixes focus
        # and keyboard navigation issues as described in #7057 and other
        # tickets.
        if self._lastSelection is not None:
            self._lastSelection = self._keyToNode.get(self._lastSelection.key)

        if self._focusedNode is not None:
            self.setFocusedNode(self._keyToNode.get(self._focusedNode.key))

        if (self._lastSelection is None and self._focusedNode is None
                and not self._selectedIds.isEmpty()):
            self.setFocusedNode(self._keyToNode[self._selectedIds.next()])
            self._focusedNode.setFocused(False)

        self._rendering = False


    def getFirstRootNode(self):
        """Returns the first root node of the tree or null if there are no
        root nodes.

        @return: The first root {@link TreeNode}
        """
        if self._body.getWidgetCount() == 0:
            return None

        return self._body.getWidget(0)


    def getLastRootNode(self):
        """Returns the last root node of the tree or null if there are no
        root nodes.

        @return: The last root {@link TreeNode}
        """
        if self._body.getWidgetCount() == 0:
            return None

        return self._body.getWidget(self._body.getWidgetCount() - 1)


    def getRootNodes(self):
        """Returns a list of all root nodes in the Tree in the order they
        appear in the tree.

        @return: A list of all root {@link TreeNode}s.
        """
        rootNodes = list()
        for i in range(self._body.getWidgetCount()):
            rootNodes.add(self._body.getWidget(i))
        return rootNodes


    def updateTreeRelatedDragData(self, drag):
        self._currentMouseOverKey = self.findCurrentMouseOverKey(
                drag.getElementOver())

        drag.getDropDetails()['itemIdOver'] = self._currentMouseOverKey
        if self._currentMouseOverKey is not None:
            treeNode = self._keyToNode[self._currentMouseOverKey]
            detail = treeNode.getDropDetail(drag.getCurrentGwtEvent())
            overTreeNode = None
            if (treeNode is not None and not treeNode.isLeaf()
                    and detail == VerticalDropLocation.MIDDLE):
                overTreeNode = True
            drag.getDropDetails()['itemIdOverIsNode'] = overTreeNode
            drag.getDropDetails()['detail'] = detail
        else:
            drag.getDropDetails()['itemIdOverIsNode'] = None
            drag.getDropDetails()['detail'] = None


    def findCurrentMouseOverKey(self, elementOver):
        treeNode = Util.findWidget(elementOver, TreeNode)
        return None if treeNode is None else treeNode.key


    def updateDropHandler(self, childUidl):
        if self._dropHandler is None:
            VTree_this = self

            class DropHandler(VAbstractDropHandler):

                def dragEnter(self, drag):
                    pass

                def dragAccepted(self, drag):
                    pass

                def dragOver(self, currentDrag):
                    oldIdOver = currentDrag.getDropDetails().get('itemIdOver')
                    oldDetail = currentDrag.getDropDetails().get('detail')
                    VTree_this.updateTreeRelatedDragData(currentDrag)
                    detail = currentDrag.getDropDetails().get('detail')
                    nodeHasChanged = (VTree_this._currentMouseOverKey is not None and VTree_this._currentMouseOverKey != oldIdOver) or (VTree_this._currentMouseOverKey is None and oldIdOver is not None)
                    detailHasChanded = (detail is not None and detail != oldDetail) or (detail is None and oldDetail is not None)
                    if nodeHasChanged or detailHasChanded:
                        newKey = VTree_this._currentMouseOverKey
                        treeNode = VTree_this._keyToNode[oldIdOver]
                        if treeNode is not None:
                            # clear old styles
                            treeNode.emphasis(None)
                        if newKey is not None:

                            class AcceptCallback(VAcceptCallback):

                                def accepted(self, event):
                                    curDetail = event.getDropDetails().get('detail')
                                    if curDetail == self.detail and self.newKey == VTree_this._currentMouseOverKey:
                                        VTree_this._keyToNode[self.newKey].emphasis(self.detail)
                                    # Else drag is already on a different
                                    # node-detail pair, new criteria check is
                                    # going on

                            self.validate(AcceptCallback(), currentDrag)

                def dragLeave(self, drag):
                    self.cleanUp()

                def cleanUp(self):
                    if VTree_this._currentMouseOverKey is not None:
                        VTree_this._keyToNode[VTree_this._currentMouseOverKey].emphasis(None)
                        VTree_this._currentMouseOverKey = None

                def drop(self, drag):
                    self.cleanUp()
                    return super(DropHandler, self).drop(drag)

                def getPaintable(self):
                    return VTree_this

                def getApplicationConnection(self):
                    return VTree_this._client

            self._dropHandler = DropHandler()
        self._dropHandler.updateAcceptRules(childUidl)


    def handleUpdate(self, uidl):
        rootNode = self._keyToNode[uidl.getStringAttribute('rootKey')]
        if rootNode is not None:
            if not rootNode.getState():
                # expanding node happened server side
                rootNode.setState(True, False)
            rootNode.renderChildNodes(uidl.getChildIterator())


    def setSelected(self, treeNode, selected):
        if selected:
            if not self._isMultiselect:
                while len(self._selectedIds) > 0:
                    id = self._selectedIds.next()
                    oldSelection = self._keyToNode[id]
                    if oldSelection is not None:
                        # can be null if the node is not visible (parent
                        # collapsed)
                        oldSelection.setSelected(False)
                    self._selectedIds.remove(id)
            treeNode.setSelected(True)
            self._selectedIds.add(treeNode.key)
        else:
            if not self._isNullSelectionAllowed:
                if (not self._isMultiselect) or (len(self._selectedIds) == 1):
                    return
            self._selectedIds.remove(treeNode.key)
            treeNode.setSelected(False)

        self.sendSelectionToServer()


    def sendSelectionToServer(self):
        """Sends the selection to the server"""

        class command(Command):

            def execute(self):
                VTree_this._client.updateVariable(VTree_this._paintableId, 'selected', list([None] * len(VTree_this._selectedIds)), VTree_this._immediate)
                VTree_this._selectionHasChanged = False

        # Delaying the sending of the selection in webkit to ensure the
        # selection is always sent when the tree has focus and after click
        # events have been processed. This is due to the focusing
        # implementation in FocusImplSafari which uses timeouts when focusing
        # and blurring.
        if BrowserInfo.get().isWebkit():
            Scheduler.get().scheduleDeferred(command)
        else:
            command.execute()


    def isSelected(self, treeNode):
        """Is a node selected in the tree

        @param treeNode:
                   The node to check
        """
        return treeNode.key in self._selectedIds


    def getDropHandler(self):
        return self._dropHandler


    def getNodeByKey(self, key):
        return self._keyToNode.get(key)


    def deselectAll(self):
        """Deselects all items in the tree"""
        for key in self._selectedIds:
            node = self._keyToNode.get(key)
            if node is not None:
                node.setSelected(False)
        self._selectedIds.clear()
        self._selectionHasChanged = True


    def selectNodeRange(self, startNodeKey, endNodeKey):
        """Selects a range of nodes

        @param startNodeKey:
                   The start node key
        @param endNodeKey:
                   The end node key
        """
        startNode = self._keyToNode.get(startNodeKey)
        endNode = self._keyToNode.get(endNodeKey)

        # The nodes have the same parent
        if startNode.getParent() == endNode.getParent():
            self.doSiblingSelection(startNode, endNode)
            # The start node is a grandparent of the end node
        elif startNode.isGrandParentOf(endNode):
            self.doRelationSelection(startNode, endNode)
            # The end node is a grandparent of the start node
        elif endNode.isGrandParentOf(startNode):
            self.doRelationSelection(endNode, startNode)
        else:
            self.doNoRelationSelection(startNode, endNode)


    def selectNode(self, node, deselectPrevious):
        """Selects a node and deselect all other nodes

        @param node:
                   The node to select
        """
        if deselectPrevious:
            self.deselectAll()

        if node is not None:
            node.setSelected(True)
            self._selectedIds.add(node.key)
            self._lastSelection = node

        self._selectionHasChanged = True


    def deselectNode(self, node):
        """Deselects a node

        @param node:
                   The node to deselect
        """
        node.setSelected(False)
        self._selectedIds.remove(node.key)
        self._selectionHasChanged = True


    def selectAllChildren(self, node, includeRootNode):
        """Selects all the open children to a node

        @param node:
                   The parent node
        """
        if includeRootNode:
            node.setSelected(True)
            self._selectedIds.add(node.key)

        for child in node.getChildren():
            if not child.isLeaf() and child.getState():
                self.selectAllChildren(child, True)
            else:
                child.setSelected(True)
                self._selectedIds.add(child.key)

        self._selectionHasChanged = True


    def selectAllChildrenUntil(self, root, stopNode, includeRootNode,
                includeStopNode):
        """Selects all children until a stop child is reached

        @param root:
                   The root not to start from
        @param stopNode:
                   The node to finish with
        @param includeRootNode:
                   Should the root node be selected
        @param includeStopNode:
                   Should the stop node be selected

        @return: Returns false if the stop child was found, else true if all
                 children was selected
        """
        if includeRootNode:
            root.setSelected(True)
            self._selectedIds.add(root.key)

        if root.getState() and root != stopNode:
            for child in root.getChildren():
                if (not child.isLeaf() and child.getState()
                        and child != stopNode):
                    if not self.selectAllChildrenUntil(child, stopNode, True,
                            includeStopNode):
                        return False
                elif child == stopNode:
                    if includeStopNode:
                        child.setSelected(True)
                        self._selectedIds.add(child.key)
                    return False
                elif child.isLeaf():
                    child.setSelected(True)
                    self._selectedIds.add(child.key)

        self._selectionHasChanged = True

        return True


    def doNoRelationSelection(self, startNode, endNode):
        """Select a range between two nodes which have no relation to each
        other.

        @param startNode:
                   The start node to start the selection from
        @param endNode:
                   The end node to end the selection to
        """
        commonParent = self.getCommonGrandParent(startNode, endNode)

        startBranch = None
        endBranch = None

        # Find the children of the common parent
        if commonParent is not None:
            children = commonParent.getChildren()
        else:
            children = self.getRootNodes()

        # Find the start and end branches
        for node in children:
            if self.nodeIsInBranch(startNode, node):
                startBranch = node
            if self.nodeIsInBranch(endNode, node):
                endBranch = node

        # Swap nodes if necessary
        if children.index(startBranch) > children.index(endBranch):
            temp = startBranch
            startBranch = endBranch
            endBranch = temp
            temp = startNode
            startNode = endNode
            endNode = temp

        # Select all children under the start node
        self.selectAllChildren(startNode, True)
        startParent = startNode.getParentNode()
        currentNode = startNode

        while startParent is not None and startParent != commonParent:
            startChildren = startParent.getChildren()
            i = startChildren.index(currentNode) + 1
            while i < len(startChildren):
                self.selectAllChildren(startChildren[i], True)
                i += 1
            currentNode = startParent
            startParent = startParent.getParentNode()

        # Select nodes until the end node is reached
        i = children.index(startBranch) + 1
        while i <= children.index(endBranch):
            self.selectAllChildrenUntil(children[i], endNode, True, True)
            i += 1

        # Ensure end node was selected
        endNode.setSelected(True)
        self._selectedIds.add(endNode.key)
        self._selectionHasChanged = True


    def nodeIsInBranch(self, node, branch):
        """Examines the children of the branch node and returns true if a
        node is in that branch.

        @param node:
                   The node to search for
        @param branch:
                   The branch to search in
        @return: True if found, false if not found
        """
        if node == branch:
            return True

        for child in branch.getChildren():
            if child == node:
                return True
            if not child.isLeaf() and child.getState():
                if self.nodeIsInBranch(node, child):
                    return True

        return False


    def doRelationSelection(self, startNode, endNode):
        """Selects a range of items which are in direct relation with each
        other.

        NOTE: The start node MUST be before the end node!
        """
        currentNode = endNode
        while currentNode != startNode:
            currentNode.setSelected(True)
            self._selectedIds.add(currentNode.key)

            # Traverse children above the selection
            subChildren = currentNode.getParentNode().getChildren()

            if len(subChildren) > 1:
                self.selectNodeRange(subChildren.next().key, currentNode.key)
            elif len(subChildren) == 1:
                n = subChildren[0]
                n.setSelected(True)
                self._selectedIds.add(n.key)

            currentNode = currentNode.getParentNode()

        startNode.setSelected(True)
        self._selectedIds.add(startNode.key)
        self._selectionHasChanged = True


    def doSiblingSelection(self, startNode, endNode):
        """Selects a range of items which have the same parent.

        @param startNode:
                   The start node
        @param endNode:
                   The end node
        """
        parent = startNode.getParentNode()
        if parent is None:
            # Topmost parent
            children = self.getRootNodes()
        else:
            children = parent.getChildren()

        # Swap start and end point if needed
        if children.index(startNode) > children.index(endNode):
            temp = startNode
            startNode = endNode
            endNode = temp

        childIter = children
        startFound = False
        while childIter.hasNext():
            node = childIter.next()
            if node == startNode:
                startFound = True
            if startFound and node != endNode and node.getState():
                self.selectAllChildren(node, True)
            elif startFound and node != endNode:
                node.setSelected(True)
                self._selectedIds.add(node.key)
            if node == endNode:
                node.setSelected(True)
                self._selectedIds.add(node.key)
                break

        self._selectionHasChanged = True


    def getCommonGrandParent(self, node1, node2):
        """Returns the first common parent of two nodes

        @param node1:
                   The first node
        @param node2:
                   The second node
        @return: The common parent or null
        """
        # If either one does not have a grand parent then return null
        if (node1.getParentNode() is None) or (node2.getParentNode() is None):
            return None

        # If the nodes are parents of each other then return null
        if node1.isGrandParentOf(node2) or node2.isGrandParentOf(node1):
            return None

        # Get parents of node1
        parents1 = list()
        parent1 = node1.getParentNode()
        while parent1 is not None:
            parents1.append(parent1)
            parent1 = parent1.getParentNode()

        # Get parents of node2
        parents2 = list()
        parent2 = node2.getParentNode()
        while parent2 is not None:
            parents2.append(parent2)
            parent2 = parent2.getParentNode()

        # Search the parents for the first common parent
        for i in range(len(parents1)):
            parent1 = parents1[i]
            for j in range(len(parents2)):
                parent2 = parents2[j]
                if parent1 == parent2:
                    return parent1

        return None


    def setFocusedNode(self, node, scrollIntoView=True):
        """Sets the node currently in focus

        @param node:
                   The node to focus or null to remove the focus completely
        @param scrollIntoView:
                   Scroll the node into view
        """
        # Unfocus previously focused node
        if self._focusedNode is not None:
            self._focusedNode.setFocused(False)

        if node is not None:
            node.setFocused(True)

        self._focusedNode = node

        if node is not None and scrollIntoView:
            # Delay scrolling the focused node into view if we are still
            # rendering. #5396
            if not self._rendering:
                node.scrollIntoView()
            else:

                class _7_(Command):

                    def execute(self):
                        VTree_this._focusedNode.scrollIntoView()

                _7_ = _7_()
                Scheduler.get().scheduleDeferred(_7_)


    def onFocus(self, event):
        self._treeHasFocus = True
        # If no node has focus, focus the first item in the tree
        if (self._focusedNode is None and self._lastSelection is None
                and self._selectable):
            self.setFocusedNode(self.getFirstRootNode(), False)
        elif self._focusedNode is not None and self._selectable:
            self.setFocusedNode(self._focusedNode, False)
        elif self._lastSelection is not None and self._selectable:
            self.setFocusedNode(self._lastSelection, False)


    def onBlur(self, event):
        self._treeHasFocus = False
        if self._focusedNode is not None:
            self._focusedNode.setFocused(False)


    def onKeyPress(self, event):
        nativeEvent = event.getNativeEvent()
        keyCode = nativeEvent.getKeyCode()
        if keyCode == 0 and nativeEvent.getCharCode() == ' ':
            # Provide a keyCode for space to be compatible with FireFox
            # keypress event
            keyCode = self._CHARCODE_SPACE
        if (self.handleKeyNavigation(keyCode, event.isControlKeyDown()
                or event.isMetaKeyDown(), event.isShiftKeyDown())):
            event.preventDefault()
            event.stopPropagation()


    def onKeyDown(self, event):
        if (self.handleKeyNavigation(event.getNativeEvent().getKeyCode(),
                event.isControlKeyDown() or event.isMetaKeyDown(),
                event.isShiftKeyDown())):
            event.preventDefault()
            event.stopPropagation()


    def handleKeyNavigation(self, keycode, ctrl, shift):
        """Handles the keyboard navigation

        @param keycode:
                   The keycode of the pressed key
        @param ctrl:
                   Was ctrl pressed
        @param shift:
                   Was shift pressed
        @return: Returns true if the key was handled, else false
        """
        # Navigate down
        if keycode == self.getNavigationDownKey():
            node = None
            # If node is open and has children then move in to the children
            if (not self._focusedNode.isLeaf() and self._focusedNode.getState()
                    and len(self._focusedNode.getChildren()) > 0):
                # Else move down to the next sibling
                node = self._focusedNode.getChildren().get(0)
            else:
                node = self.getNextSibling(self._focusedNode)
                if node is None:
                    # Else jump to the parent and try to select the next
                    # sibling there
                    current = self._focusedNode
                    while node is None and current.getParentNode() is not None:
                        node = self.getNextSibling(current.getParentNode())
                        current = current.getParentNode()

            if node is not None:
                self.setFocusedNode(node)
                if self._selectable:
                    if not ctrl and not shift:
                        self.selectNode(node, True)
                    elif shift and self._isMultiselect:
                        self.deselectAll()
                        self.selectNodeRange(self._lastSelection.key, node.key)
                    elif shift:
                        self.selectNode(node, True)

            return True

        # Navigate up
        if keycode == self.getNavigationUpKey():
            prev = self.getPreviousSibling(self._focusedNode)
            node = None
            if prev is not None:
                node = self.getLastVisibleChildInTree(prev)
            elif self._focusedNode.getParentNode() is not None:
                node = self._focusedNode.getParentNode()

            if node is not None:
                self.setFocusedNode(node)
                if self._selectable:
                    if not ctrl and not shift:
                        self.selectNode(node, True)
                    elif shift and self._isMultiselect:
                        self.deselectAll()
                        self.selectNodeRange(self._lastSelection.key, node.key)
                    elif shift:
                        self.selectNode(node, True)

            return True

        # Navigate left (close branch)
        if keycode == self.getNavigationLeftKey():
            if not self._focusedNode.isLeaf() and self._focusedNode.getState():
                self._focusedNode.setState(False, True)
            elif (self._focusedNode.getParentNode() is not None
                    and self._focusedNode.isLeaf()
                    or (not self._focusedNode.getState())):
                if ctrl or (not self._selectable):
                    self.setFocusedNode(self._focusedNode.getParentNode())
                elif shift:
                    self.doRelationSelection(self._focusedNode.getParentNode(), self._focusedNode)
                    self.setFocusedNode(self._focusedNode.getParentNode())
                else:
                    self.focusAndSelectNode(self._focusedNode.getParentNode())

            return True

        # Navigate right (open branch)
        if keycode == self.getNavigationRightKey():
            if (not self._focusedNode.isLeaf()
                    and not self._focusedNode.getState()):
                self._focusedNode.setState(True, True)
            elif not self._focusedNode.isLeaf():
                if ctrl or (not self._selectable):
                    self.setFocusedNode(self._focusedNode.getChildren().get(0))
                elif shift:
                    self.setSelected(self._focusedNode, True)
                    self.setFocusedNode(self._focusedNode.getChildren().get(0))
                    self.setSelected(self._focusedNode, True)
                else:
                    self.focusAndSelectNode(self._focusedNode.getChildren().get(0))

            return True

        # Selection
        if keycode == self.getNavigationSelectKey():
            if not self._focusedNode.isSelected():
                self.selectNode(self._focusedNode,
                        (not self._isMultiselect)
                        or (self._multiSelectMode == self.MULTISELECT_MODE_SIMPLE)
                        and self._selectable)
            else:
                self.deselectNode(self._focusedNode)

            return True

        # Home selection
        if keycode == self.getNavigationStartKey():
            node = self.getFirstRootNode()
            if ctrl or (not self._selectable):
                self.setFocusedNode(node)
            elif shift:
                self.deselectAll()
                self.selectNodeRange(self._focusedNode.key, node.key)
            else:
                self.selectNode(node, True)

            self.sendSelectionToServer()

            return True

        # End selection
        if keycode == self.getNavigationEndKey():
            lastNode = self.getLastRootNode()
            node = self.getLastVisibleChildInTree(lastNode)
            if ctrl or (not self._selectable):
                self.setFocusedNode(node)
            elif shift:
                self.deselectAll()
                self.selectNodeRange(self._focusedNode.key, node.key)
            else:
                self.selectNode(node, True)

            self.sendSelectionToServer()

            return True

        return False


    def focusAndSelectNode(self, node):
        # Keyboard navigation doesn't work reliably if the tree is in
        # multiselect mode as well as isNullSelectionAllowed = false. It first
        # tries to deselect the old focused node, which fails since there must
        # be at least one selection. After this the newly focused node is
        # selected and we've ended up with two selected nodes even though we
        # only navigated with the arrow keys.
        #
        # Because of this, we first select the next node and later de-select
        # the old one.
        oldFocusedNode = self._focusedNode
        self.setFocusedNode(node)
        self.setSelected(self._focusedNode, True)
        self.setSelected(oldFocusedNode, False)


    def getLastVisibleChildInTree(self, root):
        """Traverses the tree to the bottom most child

        @param root:
                   The root of the tree
        @return: The bottom most child
        """
        if (root.isLeaf() or (not root.getState())
                or (len(root.getChildren()) == 0)):
            return root

        children = root.getChildren()
        return self.getLastVisibleChildInTree(children[len(children) - 1])


    def getNextSibling(self, node):
        """Gets the next sibling in the tree

        @param node:
                   The node to get the sibling for
        @return: The sibling node or null if the node is the last sibling
        """
        parent = node.getParentNode()
        if parent is None:
            children = self.getRootNodes()
        else:
            children = parent.getChildren()

        idx = children.index(node)

        if idx < len(children) - 1:
            return children[idx + 1]

        return None


    def getPreviousSibling(self, node):
        """Returns the previous sibling in the tree

        @param node:
                   The node to get the sibling for
        @return: The sibling node or null if the node is the first sibling
        """
        parent = node.getParentNode()
        if parent is None:
            children = self.getRootNodes()
        else:
            children = parent.getChildren()

        idx = children.index(node)

        if idx > 0:
            return children[idx - 1]

        return None


    def applyDisableTextSelectionIEHack(self):
        """Add this to the element mouse down event by using
        element.setPropertyJSO
        ("onselectstart",applyDisableTextSelectionIEHack()); Remove it then
        again when the mouse is depressed in the mouse up event.

        @return: Returns the JSO preventing text selection
        """
        JS("""
            return function(){ return false; };
        """)
        pass


    def getNavigationUpKey(self):
        """Get the key that moves the selection head upwards. By default it
        is the up arrow key but by overriding this you can change the key to
        whatever you want.

        @return: The keycode of the key
        """
        return KeyboardListener.KEY_UP


    def getNavigationDownKey(self):
        """Get the key that moves the selection head downwards. By default it
        is the down arrow key but by overriding this you can change the key to
        whatever you want.

        @return: The keycode of the key
        """
        return KeyboardListener.KEY_DOWN


    def getNavigationLeftKey(self):
        """Get the key that scrolls to the left in the table. By default it is
        the left arrow key but by overriding this you can change the key to
        whatever you want.

        @return: The keycode of the key
        """
        return KeyboardListener.KEY_LEFT


    def getNavigationRightKey(self):
        """Get the key that scroll to the right on the table. By default it is
        the right arrow key but by overriding this you can change the key to
        whatever you want.

        @return: The keycode of the key
        """
        return KeyboardListener.KEY_RIGHT


    def getNavigationSelectKey(self):
        """Get the key that selects an item in the table. By default it is the
        space bar key but by overriding this you can change the key to whatever
        you want.
        """
        return self._CHARCODE_SPACE


    def getNavigationPageUpKey(self):
        """Get the key the moves the selection one page up in the table. By
        default this is the Page Up key but by overriding this you can change
        the key to whatever you want.
        """
        return KeyboardListener.KEY_PAGEUP


    def getNavigationPageDownKey(self):
        """Get the key the moves the selection one page down in the table. By
        default this is the Page Down key but by overriding this you can change
        the key to whatever you want.
        """
        return KeyboardListener.KEY_PAGEDOWN


    def getNavigationStartKey(self):
        """Get the key the moves the selection to the beginning of the table.
        By default this is the Home key but by overriding this you can change
        the key to whatever you want.
        """
        return KeyboardListener.KEY_HOME


    def getNavigationEndKey(self):
        """Get the key the moves the selection to the end of the table. By
        default this is the End key but by overriding this you can change the
        key to whatever you want.
        """
        return KeyboardListener.KEY_END


    def getSubPartElement(self, subPart):
        if 'fe' == subPart:
            if self.isIE6OrOpera() and self._focusedNode is not None:
                return self._focusedNode.getElement()
            return self.getFocusElement()

        if subPart.startswith(self._SUBPART_NODE_PREFIX + '['):
            expandCollapse = False
            # Node
            nodes = subPart.split('/')
            treeNode = None
            # Invalid locator string or node could not be found
            try:
                for node in nodes:
                    if node.startswith(self._SUBPART_NODE_PREFIX):
                        # skip SUBPART_NODE_PREFIX"["
                        node = node[len(self._SUBPART_NODE_PREFIX) + 1:]
                        # skip "]"
                        node = node[:-1]
                        position = int(node)
                        if treeNode is None:
                            treeNode = self.getRootNodes().get(position)
                        else:
                            treeNode = treeNode.getChildren().get(position)
                    elif node.startswith(self._EXPAND_IDENTIFIER):
                        expandCollapse = True

                if expandCollapse:
                    if treeNode.ie6compatnode is not None:
                        return treeNode.ie6compatnode
                    else:
                        return treeNode.getElement()
                else:
                    return treeNode.nodeCaptionSpan
            except Exception:
                return None

        return None


    def getSubPartName(self, subElement):
        # Supported identifiers:
        #
        # n[index]/n[index]/n[index]{/expand}
        #
        # Ends with "/expand" if the target is expand/collapse indicator,
        # otherwise ends with the node

        isExpandCollapse = False

        if not self.getElement().isOrHasChild(subElement):
            return None

        if subElement == self.getFocusElement():
            return 'fe'

        treeNode = Util.findWidget(subElement, self.TreeNode)
        if treeNode is None:
            # Did not click on a node, let somebody else take care of the
            # locator string
            return None

        if ((subElement == treeNode.getElement())
                or (subElement == treeNode.ie6compatnode)):
            # Targets expand/collapse arrow
            isExpandCollapse = True

        positions = list()
        while treeNode.getParentNode() is not None:
            positions.insert(0,
                    treeNode.getParentNode().getChildren().index(treeNode))
            treeNode = treeNode.getParentNode()
        positions.insert(0, self.getRootNodes().index(treeNode))

        locator = ''
        for i in positions:
            locator += self._SUBPART_NODE_PREFIX + '[' + i + ']/'

        locator = locator[:-1]
        if isExpandCollapse:
            locator += '/' + self._EXPAND_IDENTIFIER

        return locator


    def getActions(self):
        if self._bodyActionKeys is None:
            return []

        actions = [None] * len(self._bodyActionKeys)
        for i in range(len(actions)):
            actionKey = self._bodyActionKeys[i]
            a = TreeAction(self, None, actionKey)
            a.setCaption(self.getActionCaption(actionKey))
            a.setIconUrl(self.getActionIcon(actionKey))
            actions[i] = a

        return actions


    def getClient(self):
        return self._client


    def getPaintableId(self):
        return self._paintableId


    def handleBodyContextMenu(self, event):
        if not self._readonly and not self._disabled:
            if self._bodyActionKeys is not None:
                left = event.getNativeEvent().getClientX()
                top = event.getNativeEvent().getClientY()
                top += Window.getScrollTop()
                left += Window.getScrollLeft()
                self._client.getContextMenu().showAt(self, left, top)
            event.stopPropagation()
            event.preventDefault()


    def isIE6OrOpera(self):
        return BrowserInfo.get().isIE6() or BrowserInfo.get().isOpera()


class TreeNode(SimplePanel, ActionOwner):

    CLASSNAME = 'v-tree-node'
    CLASSNAME_FOCUSED = CLASSNAME + '-focused'

    def __init__(self, tree):
        self._tree = tree

        self.key = None
        self._actionKeys = None
        self._childrenLoaded = None
        self._nodeCaptionDiv = None
        self.nodeCaptionSpan = None
        self._childNodeContainer = None
        self._open = None
        self._icon = None
        self._ie6compatnode = None
        self._mouseDownEvent = None
        self._cachedHeight = -1
        self._focused = False
        # Track onload events as IE6 sends two
        self._onloadHandled = False

        self.constructDom()
        self.sinkEvents(Event.ONCLICK | Event.ONDBLCLICK | Event.MOUSEEVENTS
                | Event.TOUCHEVENTS | Event.ONCONTEXTMENU)


    def getDropDetail(self, currentGwtEvent):
        if self._cachedHeight < 0:
            # Height is cached to avoid flickering (drop hints may change
            # the reported offsetheight -> would change the drop detail)
            self._cachedHeight = self._nodeCaptionDiv.getOffsetHeight()

        verticalDropLocation = DDUtil.getVerticalDropLocation(
            self._nodeCaptionDiv, self._cachedHeight, currentGwtEvent, 0.15)

        return verticalDropLocation


    def emphasis(self, detail):
        base = 'v-tree-node-drag-'
        UIObject.setStyleName(self.getElement(), base + 'top',
                VerticalDropLocation.TOP == detail)
        UIObject.setStyleName(self.getElement(), base + 'bottom',
                VerticalDropLocation.BOTTOM == detail)
        UIObject.setStyleName(self.getElement(), base + 'center',
                VerticalDropLocation.MIDDLE == detail)
        base = 'v-tree-node-caption-drag-'
        UIObject.setStyleName(self._nodeCaptionDiv, base + 'top',
                VerticalDropLocation.TOP == detail)
        UIObject.setStyleName(self._nodeCaptionDiv, base + 'bottom',
                VerticalDropLocation.BOTTOM == detail)
        UIObject.setStyleName(self._nodeCaptionDiv, base + 'center',
                VerticalDropLocation.MIDDLE == detail)

        # also add classname to "folder node" into which the drag is
        # targeted

        folder = None
        # Possible parent of this TreeNode will be stored here
        parentFolder = self.getParentNode()

        # TODO: fix my bugs
        if self.isLeaf():
            folder = parentFolder
            # note, parent folder may be null if this is root node => no
            # folder target exists
        else:
            if detail == VerticalDropLocation.TOP:
                folder = parentFolder
            else:
                folder = self

            # ensure we remove the dragfolder classname from the previous
            # folder node
            self.setDragFolderStyleName(self, False)
            self.setDragFolderStyleName(parentFolder, False)

        if folder is not None:
            self.setDragFolderStyleName(folder, detail is not None)


    def getParentNode(self):
        parent2 = self.getParent().getParent()
        if isinstance(parent2, TreeNode):
            return parent2
        return None


    def setDragFolderStyleName(self, folder, add):
        if folder is not None:
            UIObject.setStyleName(folder.getElement(),
                    'v-tree-node-dragfolder', add)
            UIObject.setStyleName(folder.nodeCaptionDiv,
                    'v-tree-node-caption-dragfolder', add)


    def handleClickSelection(self, ctrl, shift):
        """Handles mouse selection

        @param ctrl:
                   Was the ctrl-key pressed
        @param shift:
                   Was the shift-key pressed
        @return: Returns true if event was handled, else false
        """
        # always when clicking an item, focus it
        self._tree.setFocusedNode(self, False)

        if not self._tree.isIE6OrOpera():
            # Ensure that the tree's focus element also gains focus
            # (TreeNodes focus is faked using FocusElementPanel in browsers
            # other than IE6 and Opera).
            self.focus()

        class command(ScheduledCommand):

            def __init__(self, tree, node):
                self._tree = tree
                self._node = node

            def execute(self):
                if ((self._tree._multiSelectMode == self._tree.MULTISELECT_MODE_SIMPLE)
                        or (not self._tree._isMultiselect)):
                    self._node.toggleSelection()
                    self._tree._lastSelection = self._node
                elif (self._tree._multiSelectMode
                        == self._tree.MULTISELECT_MODE_DEFAULT):
                    # Handle ctrl+click
                    if self._tree._isMultiselect and self.ctrl and not self.shift:
                        self._node.toggleSelection()
                        self._tree._lastSelection = self._node
                        # Handle shift+click
                    elif (self._tree._isMultiselect and not self.ctrl
                            and self.shift):
                        self._tree.deselectAll()
                        self._tree.selectNodeRange(
                                self._tree._lastSelection.key, self._node.key)
                        self._tree.sendSelectionToServer()
                        # Handle ctrl+shift click
                    elif (self._tree._isMultiselect and self.ctrl
                            and self.shift):
                        self._tree.selectNodeRange(
                                self._tree._lastSelection.key, self._node.key)
                        # Handle click
                    else:
                        # TODO: should happen only if this alone not yet
                        # selected, now sending excess server calls
                        self._tree.deselectAll()
                        self._node.toggleSelection()
                        self._tree._lastSelection = self._node


        if BrowserInfo.get().isWebkit() and not self._tree._treeHasFocus:
            # Safari may need to wait for focus. See FocusImplSafari.
            # VConsole.log("Deferring click handling to let webkit gain focus...");
            Scheduler.get().scheduleDeferred(command)
        else:
            command.execute()
        return True


    def onBrowserEvent(self, event):
        super(TreeNode, self).onBrowserEvent(event)
        type = DOM.eventGetType(event)
        target = DOM.eventGetTarget(event)

        if type == Event.ONLOAD and target == self._icon.getElement():
            if self._onloadHandled:
                return
            if BrowserInfo.get().isIE6():
                self.fixWidth()
            self.iconLoaded.trigger()
            self._onloadHandled = True

        if self._tree._disabled:
            return

        if target == self.nodeCaptionSpan:
            self._tree._client.handleTooltipEvent(event, self._tree, self.key)

        inCaption = ((target == self.nodeCaptionSpan)
                or (self._icon is not None
                        and target == self._icon.getElement()))
        if (inCaption and self._tree._client.hasEventListeners(self._tree,
                self._tree.ITEM_CLICK_EVENT_ID)
                        and (type == Event.ONDBLCLICK)
                        or (type == Event.ONMOUSEUP)):
            self.fireClick(event)

        if type == Event.ONCLICK:
            if (self.getElement() == target) or (self._ie6compatnode == target):
                # state change
                self.toggleState()
            elif not self._tree._readonly and inCaption:
                if self._tree._selectable:
                    # caption click = selection change && possible click
                    # event
                    if (self.handleClickSelection(event.getCtrlKey()
                            or event.getMetaKey(), event.getShiftKey())):
                        event.preventDefault()
                else:
                    # Not selectable, only focus the node.
                    self._tree.setFocusedNode(self)

            event.stopPropagation()
        elif type == Event.ONCONTEXTMENU:
            self.showContextMenu(event)

        if (self._tree._dragMode != 0) or (self._tree._dropHandler is not None):
            if (type == Event.ONMOUSEDOWN) or (type == Event.ONTOUCHSTART):
                if self._nodeCaptionDiv.isOrHasChild(event.getEventTarget()):
                    if (self._tree._dragMode > 0
                            and (type == Event.ONTOUCHSTART)
                            or (event.getButton() == NativeEvent.BUTTON_LEFT)):
                        self._mouseDownEvent = event
                        # save event for possible
                        # dd operation
                        if type == Event.ONMOUSEDOWN:
                            event.preventDefault()
                            # prevent text
                            # selection
                        else:
                            # FIXME: We prevent touch start event to be used
                            # as a scroll start event. Note that we cannot
                            # easily distinguish whether the user wants to
                            # drag or scroll. The same issue is in table
                            # that has scrollable area and has drag and
                            # drop enable. Some kind of timer might be used
                            # to resolve the issue.
                            event.stopPropagation()
            elif ((type == Event.ONMOUSEMOVE) or (type == Event.ONMOUSEOUT)
                    or (type == Event.ONTOUCHMOVE)):
                if self._mouseDownEvent is not None:
                    # start actual drag on slight move when mouse is down
                    t = VTransferable()
                    t.setDragSource(self._tree)
                    t.setData('itemId', self.key)
                    drag = VDragAndDropManager.get().startDrag(t,
                            self._mouseDownEvent, True)
                    drag.createDragImage(self._nodeCaptionDiv, True)
                    event.stopPropagation()
                    self._mouseDownEvent = None
            elif type == Event.ONMOUSEUP:
                self._mouseDownEvent = None

            if type == Event.ONMOUSEOVER:
                self._mouseDownEvent = None
                self._tree._currentMouseOverKey = self.key
                event.stopPropagation()

        elif (type == Event.ONMOUSEDOWN
                and event.getButton() == NativeEvent.BUTTON_LEFT):
            event.preventDefault()  # text selection


    def fireClick(self, evt):
        # Ensure we have focus in tree before sending variables. Otherwise
        # previously modified field may contain dirty variables.
        if not self._tree._treeHasFocus:
            if self._tree.isIE6OrOpera():
                if self._tree._focusedNode is None:
                    self._tree.getNodeByKey(self.key).setFocused(True)
                else:
                    self._tree._focusedNode.setFocused(True)
            else:
                self.focus()
        details = MouseEventDetails(evt)

        class command(ScheduledCommand):

            def execute(self):
                # Determine if we should send the event immediately to the
                # server. We do not want to send the event if there is a
                # selection event happening after this. In all other cases
                # we want to send it immediately.
                sendClickEventNow = True
                if (self.details.getButton() == NativeEvent.BUTTON_LEFT
                        and self._tree._immediate and self._tree._selectable):
                    # Probably a selection that will cause a value change
                    # event to be sent
                    sendClickEventNow = False
                    # The exception is that user clicked on the
                    # currently selected row and null selection is not
                    # allowed == no selection event
                    if (self._node.isSelected()
                            and len(self._tree._selectedIds) == 1
                            and not self._tree._isNullSelectionAllowed):
                        sendClickEventNow = True

                self._tree._client.updateVariable(self._tree._paintableId,
                        'clickedKey', self._node.key, False)
                self._tree._client.updateVariable(self._tree._paintableId,
                        'clickEvent', str(self.details), sendClickEventNow)

        if self._tree._treeHasFocus:
            command.execute()
        else:
            # Webkits need a deferring due to FocusImplSafari uses timeout
            Scheduler.get().scheduleDeferred(command)


    def toggleSelection(self):
        if self._tree._selectable:
            self._tree.setSelected(self, not self.isSelected())


    def toggleState(self):
        self.setState(not self.getState(), True)


    def constructDom(self):
        self.addStyleName(self.CLASSNAME)
        # workaround for a very weird IE6 issue #1245
        if BrowserInfo.get().isIE6():
            self._ie6compatnode = DOM.createDiv()
            self.setStyleName(self._ie6compatnode,
                    self.CLASSNAME + '-ie6compatnode')
            DOM.setInnerText(self._ie6compatnode, ' ')
            DOM.appendChild(self.getElement(), self._ie6compatnode)

            DOM.sinkEvents(self._ie6compatnode, Event.ONCLICK)

        self._nodeCaptionDiv = DOM.createDiv()
        DOM.setElemAttribute(self._nodeCaptionDiv, 'className',
                self.CLASSNAME + '-caption')
        wrapper = DOM.createDiv()
        self.nodeCaptionSpan = DOM.createSpan()
        DOM.sinkEvents(self.nodeCaptionSpan, VTooltip.TOOLTIP_EVENTS)
        DOM.appendChild(self.getElement(), self._nodeCaptionDiv)
        DOM.appendChild(self._nodeCaptionDiv, wrapper)
        DOM.appendChild(wrapper, self.nodeCaptionSpan)

        if self._tree.isIE6OrOpera():
            # Focus the caption div of the node to get keyboard navigation
            # to work without scrolling up or down when focusing a node.
            self._nodeCaptionDiv.setTabIndex(-1)

        self._childNodeContainer = FlowPanel()
        self._childNodeContainer.setStyleName(self.CLASSNAME + '-children')
        self.setWidget(self._childNodeContainer)


    def updateFromUIDL(self, uidl, client):
        self.setText(uidl.getStringAttribute('caption'))
        self.key = uidl.getStringAttribute('key')

        self._tree._keyToNode.put(self.key, self)

        if uidl.hasAttribute('al'):
            self._actionKeys = uidl.getStringArrayAttribute('al')

        if uidl.getTag() == 'node':
            if uidl.getChildCount() == 0:
                self._childNodeContainer.setVisible(False)
            else:
                self.renderChildNodes(uidl.getChildIterator())
                self._childrenLoaded = True
        else:
            self.addStyleName(self.CLASSNAME + '-leaf')

        if uidl.hasAttribute('style'):
            self.addStyleName(
                    self.CLASSNAME + '-' + uidl.getStringAttribute('style'))
            Widget.setStyleName(self._nodeCaptionDiv,
                    self.CLASSNAME + '-caption-'
                    + uidl.getStringAttribute('style'), True)
            self._childNodeContainer.addStyleName(self.CLASSNAME
                    + '-children-' + uidl.getStringAttribute('style'))

        description = uidl.getStringAttribute('descr')
        if description is not None and client is not None:
            # Set tooltip
            info = TooltipInfo(description)
            client.registerTooltip(self._tree, self.key, info)
        else:
            # Remove possible previous tooltip
            client.registerTooltip(self._tree, self.key, None)

        if uidl.getBooleanAttribute('expanded') and not self.getState():
            self.setState(True, False)

        if uidl.getBooleanAttribute('selected'):
            self.setSelected(True)
            # ensure that identifier is in selectedIds array (this may be a
            # partial update)
            self._tree._selectedIds.add(self.key)

        if uidl.hasAttribute('icon'):
            if self._icon is None:
                self._onloadHandled = False
                self._icon = Icon(client)
                DOM.insertBefore(DOM.getFirstChild(self._nodeCaptionDiv),
                        self._icon.getElement(), self.nodeCaptionSpan)

            self._icon.setUri(uidl.getStringAttribute('icon'))
        elif self._icon is not None:
            DOM.removeChild(DOM.getFirstChild(self._nodeCaptionDiv),
                    self._icon.getElement())
            self._icon = None

        if BrowserInfo.get().isIE6() and self.isAttached():
            self.fixWidth()


    def isLeaf(self):
        styleNames = self.getStyleName().split(' ')
        for styleName in styleNames:
            if styleName == self.CLASSNAME + '-leaf':
                return True
        return False


    def setState(self, state, notifyServer):
        if self._open == state:
            return

        if state:
            if not self._childrenLoaded and notifyServer:
                self._tree._client.updateVariable(self._tree._paintableId,
                        'requestChildTree', True, False)

            if notifyServer:
                self._tree._client.updateVariable(self._tree._paintableId,
                        'expand', [self.key], True)

            self.addStyleName(self.CLASSNAME + '-expanded')
            self._childNodeContainer.setVisible(True)
        else:
            self.removeStyleName(self.CLASSNAME + '-expanded')
            self._childNodeContainer.setVisible(False)
            if notifyServer:
                self._tree._client.updateVariable(self._tree._paintableId,
                        'collapse', [self.key], True)

        self._open = state

        if not self._tree._rendering:
            Util.notifyParentOfSizeChange(self._tree, False)


    def getState(self):
        return self._open


    def setText(self, text):
        DOM.setInnerText(self.nodeCaptionSpan, text)


    def renderChildNodes(self, i):
        self._childNodeContainer.clear()
        self._childNodeContainer.setVisible(True)
        while i.hasNext():
            childUidl = i.next()
            # actions are in bit weird place, don't mix them with children,
            # but current node's actions
            if 'actions' == childUidl.getTag():
                self._tree.updateActionMap(childUidl)
                continue

            childTree = TreeNode()
            if self._ie6compatnode is not None:
                self._childNodeContainer.add(childTree)

            childTree.updateFromUIDL(childUidl, self._tree._client)

            if self._ie6compatnode is None:
                self._childNodeContainer.add(childTree)

            if not i.hasNext():
                childTree.addStyleDependentName(
                        'leaf-last' if childTree.isLeaf() else 'last')
                childTree.childNodeContainer.addStyleDependentName('last')

        self._childrenLoaded = True


    def isChildrenLoaded(self):
        return self._childrenLoaded


    def getChildren(self):
        """Returns the children of the node

        @return: A set of tree nodes
        """
        nodes = list()

        if not self.isLeaf() and self.isChildrenLoaded():
            iter = self._childNodeContainer
            while iter.hasNext():
                node = iter.next()
                nodes.append(node)

        return nodes


    def getActions(self):
        if self._actionKeys is None:
            return []

        actions = [None] * len(self._actionKeys)
        for i in range(len(actions)):
            actionKey = self._actionKeys[i]
            a = TreeAction(self, str(self.key), actionKey)
            a.setCaption(self._tree.getActionCaption(actionKey))
            a.setIconUrl(self._tree.getActionIcon(actionKey))
            actions[i] = a

        return actions


    def getClient(self):
        return self._tree._client


    def getPaintableId(self):
        return self._tree._paintableId


    def setSelected(self, selected):
        """Adds/removes Muntjac specific style name. This method ought to be
        called only from VTree.
        """
        # add style name to caption dom structure only, not to subtree
        self.setStyleName(self._nodeCaptionDiv, 'v-tree-node-selected',
                selected)


    def isSelected(self):
        return self._tree.isSelected(self)


    def isGrandParentOf(self, child):
        """Travels up the hierarchy looking for this node

        @param child:
                   The child which grandparent this is or is not
        @return: True if this is a grandparent of the child node
        """
        currentNode = child
        isGrandParent = False
        while currentNode is not None:
            currentNode = currentNode.getParentNode()
            if currentNode is self:
                isGrandParent = True
                break
        return isGrandParent


    def isSibling(self, node):
        return node.getParentNode() == self.getParentNode()


    def showContextMenu(self, event):
        # We need to fix the width of TreeNodes so that the float in
        # ie6compatNode does not wrap (see ticket #1245)
        if not self._tree._readonly and not self._tree._disabled:
            if self._actionKeys is not None:
                left = event.getClientX()
                top = event.getClientY()
                top += Window.getScrollTop()
                left += Window.getScrollLeft()
                self._tree._client.getContextMenu().showAt(self, left, top)
            event.stopPropagation()
            event.preventDefault()


    def fixWidth(self):
        self._nodeCaptionDiv.getStyle().setProperty('styleFloat', 'left')
        self._nodeCaptionDiv.getStyle().setProperty('display', 'inline')
        self._nodeCaptionDiv.getStyle().setProperty('marginLeft', '0')
        captionWidth = (self._ie6compatnode.getOffsetWidth()
                + self._nodeCaptionDiv.getOffsetWidth())
        self.setWidth(captionWidth + 'px')


    def onAttach(self):
        super(TreeNode, self).onAttach()
        if self._ie6compatnode is not None:
            self.fixWidth()


    def onDetach(self):
        super(TreeNode, self).onDetach()
        self._tree._client.getContextMenu().ensureHidden(self)


    def toString(self):
        return self.nodeCaptionSpan.getInnerText()


    def __str__(self):
        return self.toString()


    def setFocused(self, focused):
        """Is the node focused?

        @param focused:
                   True if focused, false if not
        """
        if not self._focused and focused:
            self._nodeCaptionDiv.addClassName(self.CLASSNAME_FOCUSED)
            if BrowserInfo.get().isIE6():
                self._ie6compatnode.addClassName(self.CLASSNAME_FOCUSED)
            self._focused = focused
            if self._tree.isIE6OrOpera():
                self._nodeCaptionDiv.focus()
            self._tree._treeHasFocus = True
        elif self._focused and not focused:
            self._nodeCaptionDiv.removeClassName(self.CLASSNAME_FOCUSED)
            if BrowserInfo.get().isIE6():
                self._ie6compatnode.removeClassName(self.CLASSNAME_FOCUSED)
            self._focused = focused
            self._tree._treeHasFocus = False


    def scrollIntoView(self):
        """Scrolls the caption into view"""
        Util.scrollIntoViewVertically(self._nodeCaptionDiv)
