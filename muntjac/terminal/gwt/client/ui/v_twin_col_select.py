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

from pyjamas import DOM

from pyjamas.ui import KeyboardListener

from pyjamas.ui.FlowPanel import FlowPanel
from pyjamas.ui.HTML import HTML
from pyjamas.ui.ListBox import ListBox

from muntjac.terminal.gwt.client.ui.v_button import VButton
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.ui.v_option_group_base import VOptionGroupBase
from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.ui.sub_part_aware import ISubPartAware


class VTwinColSelect(VOptionGroupBase, ISubPartAware):
#    KeyDownHandler, MouseDownHandler, DoubleClickHandler):

    _CLASSNAME = 'v-select-twincol'
    ATTRIBUTE_LEFT_CAPTION = 'lc'
    ATTRIBUTE_RIGHT_CAPTION = 'rc'

    _VISIBLE_COUNT = 10

    _DEFAULT_COLUMN_COUNT = 10

    _SUBPART_OPTION_SELECT = 'leftSelect'
    _SUBPART_OPTION_SELECT_ITEM = _SUBPART_OPTION_SELECT + '-item'
    _SUBPART_SELECTION_SELECT = 'rightSelect'
    _SUBPART_SELECTION_SELECT_ITEM = _SUBPART_SELECTION_SELECT + '-item'
    _SUBPART_LEFT_CAPTION = 'leftCaption'
    _SUBPART_RIGHT_CAPTION = 'rightCaption'
    _SUBPART_ADD_BUTTON = 'add'
    _SUBPART_REMOVE_BUTTON = 'remove'

    def __init__(self):
        self._options = None
        self._selections = None
        self._captionWrapper = None
        self._optionsCaption = None
        self._selectionsCaption = None
        self._add = None
        self._remove = None
        self._buttons = None
        self._panel = None
        self._widthSet = False

        super(VTwinColSelect, self)(self._CLASSNAME)

        self._captionWrapper = FlowPanel()
        self._options = self.DoubleClickListBox()
        self._options.addClickHandler(self)
        self._options.addDoubleClickHandler(self)
        self._options.setVisibleItemCount(self._VISIBLE_COUNT)
        self._options.setStyleName(self._CLASSNAME + '-options')
        self._selections = self.DoubleClickListBox()
        self._selections.addClickHandler(self)
        self._selections.addDoubleClickHandler(self)
        self._selections.setVisibleItemCount(self._VISIBLE_COUNT)
        self._selections.setStyleName(self._CLASSNAME + '-selections')
        self._buttons = FlowPanel()
        self._buttons.setStyleName(self._CLASSNAME + '-buttons')
        self._add = VButton()
        self._add.setText('>>')
        self._add.addClickHandler(self)
        self._remove = VButton()
        self._remove.setText('<<')
        self._remove.addClickHandler(self)
        self._panel = self.optionsContainer
        self._panel.add(self._captionWrapper)
        self._captionWrapper.getElement().getStyle().setOverflow('hidden')#Overflow.HIDDEN)

        # Hide until there actually is a caption to prevent IE from rendering
        # extra empty space
        self._captionWrapper.setVisible(False)
        self._panel.add(self._options)
        self._buttons.add(self._add)
        br = HTML('<span/>')
        br.setStyleName(self._CLASSNAME + '-deco')
        self._buttons.add(br)
        self._buttons.add(self._remove)
        self._panel.add(self._buttons)
        self._panel.add(self._selections)

        self._options.addKeyDownHandler(self)
        self._options.addMouseDownHandler(self)

        self._selections.addMouseDownHandler(self)
        self._selections.addKeyDownHandler(self)


    def getOptionsCaption(self):
        if self._optionsCaption is None:
            self._optionsCaption = HTML()
            self._optionsCaption.setStyleName(self._CLASSNAME
                    + '-caption-left')
            self._optionsCaption.getElement().getStyle().setFloat('left')#self.com.google.gwt.dom.client.Style.Float.LEFT)
            self._captionWrapper.add(self._optionsCaption)
        return self._optionsCaption


    def getSelectionsCaption(self):
        if self._selectionsCaption is None:
            self._selectionsCaption = HTML()
            self._selectionsCaption.setStyleName(self._CLASSNAME
                    + '-caption-right')
            self._selectionsCaption.getElement().getStyle().setFloat('right')#self.com.google.gwt.dom.client.Style.Float.RIGHT)
            self._captionWrapper.add(self._selectionsCaption)
        return self._selectionsCaption


    def updateFromUIDL(self, uidl, client):
        # Captions are updated before super call to ensure the widths are set
        # correctly
        if not uidl.getBooleanAttribute('cached'):
            self.updateCaptions(uidl)
        super(VTwinColSelect, self).updateFromUIDL(uidl, client)


    def updateCaptions(self, uidl):
        leftCaption = uidl.getStringAttribute(self.ATTRIBUTE_LEFT_CAPTION) if uidl.hasAttribute(self.ATTRIBUTE_LEFT_CAPTION) else None
        rightCaption = uidl.getStringAttribute(self.ATTRIBUTE_RIGHT_CAPTION) if uidl.hasAttribute(self.ATTRIBUTE_RIGHT_CAPTION) else None

        hasCaptions = (leftCaption is not None) or (rightCaption is not None)

        if leftCaption is None:
            self.removeOptionsCaption()
        else:
            self.getOptionsCaption().setText(leftCaption)

        if rightCaption is None:
            self.removeSelectionsCaption()
        else:
            self.getSelectionsCaption().setText(rightCaption)

        self._captionWrapper.setVisible(hasCaptions)


    def removeOptionsCaption(self):
        if self._optionsCaption is None:
            return

        if self._optionsCaption.getParent() is not None:
            self._captionWrapper.remove(self._optionsCaption)

        self._optionsCaption = None


    def removeSelectionsCaption(self):
        if self._selectionsCaption is None:
            return

        if self._selectionsCaption.getParent() is not None:
            self._captionWrapper.remove(self._selectionsCaption)

        self._selectionsCaption = None


    def buildOptions(self, uidl):
        enabled = not self.isDisabled() and not self.isReadonly()
        self._options.setMultipleSelect(self.isMultiselect())
        self._selections.setMultipleSelect(self.isMultiselect())
        self._options.setEnabled(enabled)
        self._selections.setEnabled(enabled)
        self._add.setEnabled(enabled)
        self._remove.setEnabled(enabled)
        self._options.clear()
        self._selections.clear()
        i = uidl.getChildIterator()
        while i.hasNext():
            optionUidl = i.next()
            if optionUidl.hasAttribute('selected'):
                self._selections.addItem(
                        optionUidl.getStringAttribute('caption'),
                        optionUidl.getStringAttribute('key'))
            else:
                self._options.addItem(
                        optionUidl.getStringAttribute('caption'),
                        optionUidl.getStringAttribute('key'))

        cols = -1
        if self.getColumns() > 0:
            cols = self.getColumns()
        elif not self._widthSet:
            cols = self._DEFAULT_COLUMN_COUNT

        if cols >= 0:
            colWidth = cols + 'em'
            containerWidth = (2 * cols) + 4 + 'em'
            # Caption wrapper width == optionsSelect + buttons +
            # selectionsSelect
            captionWrapperWidth = (((2 * cols) + 4) - 0.5) + 'em'

            self._options.setWidth(colWidth)
            if self._optionsCaption is not None:
                self._optionsCaption.setWidth(colWidth)

            self._selections.setWidth(colWidth)
            if self._selectionsCaption is not None:
                self._selectionsCaption.setWidth(colWidth)

            self._buttons.setWidth('3.5em')
            self.optionsContainer.setWidth(containerWidth)
            self._captionWrapper.setWidth(captionWrapperWidth)
        if self.getRows() > 0:
            self._options.setVisibleItemCount(self.getRows())
            self._selections.setVisibleItemCount(self.getRows())


    def getSelectedItems(self):
        selectedItemKeys = list()
        for i in range(self._selections.getItemCount()):
            selectedItemKeys.append(self._selections.getValue(i))
        return list(selectedItemKeys)


    def getSelectionBitmap(self, listBox):
        selectedIndexes = [None] * listBox.getItemCount()
        for i in range(listBox.getItemCount()):
            if listBox.isItemSelected(i):
                selectedIndexes[i] = True
            else:
                selectedIndexes[i] = False
        return selectedIndexes


    def addItem(self):
        movedItems = self.moveSelectedItems(self._options, self._selections)
        self.selectedKeys.addAll(movedItems)
        self.client.updateVariable(self.id, 'selected',
                list(self.selectedKeys), self.isImmediate())


    def removeItem(self):
        movedItems = self.moveSelectedItems(self._selections, self._options)
        self.selectedKeys.removeAll(movedItems)
        self.client.updateVariable(self.id, 'selected',
                list(self.selectedKeys), self.isImmediate())


    def moveSelectedItems(self, source, target):
        sel = self.getSelectionBitmap(source)
        movedItems = set()
        lastSelected = 0
        for i in range(len(sel)):
            if sel[i]:
                optionIndex = i - len(sel) - source.getItemCount()
                movedItems.add(source.getValue(optionIndex))

                # Move selection to another column
                text = source.getItemText(optionIndex)
                value = source.getValue(optionIndex)
                target.addItem(text, value)
                target.setItemSelected(target.getItemCount() - 1, True)
                source.removeItem(optionIndex)

                if source.getItemCount() > 0:
                    lastSelected = optionIndex - 1 if optionIndex > 0 else 0

        if source.getItemCount() > 0:
            source.setSelectedIndex(lastSelected)

        # If no items are left move the focus to the selections
        if source.getItemCount() == 0:
            target.setFocus(True)
        else:
            source.setFocus(True)

        return movedItems


    def onClick(self, event):
        super(VTwinColSelect, self).onClick(event)
        if event.getSource() == self._add:
            self.addItem()
        elif event.getSource() == self._remove:
            self.removeItem()
        elif event.getSource() == self._options:
            # unselect all in other list, to avoid mistakes (i.e wrong button)
            c = self._selections.getItemCount()
            for i in range(c):
                self._selections.setItemSelected(i, False)
        elif event.getSource() == self._selections:
            # unselect all in other list, to avoid mistakes (i.e wrong button)
            c = self._options.getItemCount()
            for i in range(c):
                self._options.setItemSelected(i, False)


    def setHeight(self, height):
        super(VTwinColSelect, self).setHeight(height)
        if '' == height:
            self._options.setHeight('')
            self._selections.setHeight('')
        else:
            self.setInternalHeights()


    def setInternalHeights(self):
        captionHeight = 0
        if BrowserInfo.get().isIE6():
            o = self.getElement().getStyle().getOverflow()

            self.getElement().getStyle().setOverflow('hidden')#Overflow.HIDDEN)
            totalHeight = self.getOffsetHeight()
            self.getElement().getStyle().setProperty('overflow', o)
        else:
            totalHeight = self.getOffsetHeight()

        if self._optionsCaption is not None:
            captionHeight = Util.getRequiredHeight(self._optionsCaption)
        elif self._selectionsCaption is not None:
            captionHeight = Util.getRequiredHeight(self._selectionsCaption)

        selectHeight = (totalHeight - captionHeight) + 'px'

        self._selections.setHeight(selectHeight)
        self._options.setHeight(selectHeight)


    def setWidth(self, width):
        super(VTwinColSelect, self).setWidth(width)
        if not ('' == width) and width is not None:
            self.setInternalWidths()
            self._widthSet = True
        else:
            self._widthSet = False


    def setInternalWidths(self):
        DOM.setStyleAttribute(self.getElement(), 'position', 'relative')
        bordersAndPaddings = Util.measureHorizontalPaddingAndBorder(
                self._buttons.getElement(), 0)

        if BrowserInfo.get().isIE6():
            # IE6 sets a border on selects by default..
            bordersAndPaddings += 4

        buttonWidth = Util.getRequiredWidth(self._buttons)
        totalWidth = self.getOffsetWidth()

        spaceForSelect = (totalWidth - buttonWidth - bordersAndPaddings) / 2

        self._options.setWidth(spaceForSelect + 'px')
        if self._optionsCaption is not None:
            self._optionsCaption.setWidth(spaceForSelect + 'px')

        self._selections.setWidth(spaceForSelect + 'px')
        if self._selectionsCaption is not None:
            self._selectionsCaption.setWidth(spaceForSelect + 'px')

        self._captionWrapper.setWidth('100%')


    def setTabIndex(self, tabIndex):
        self._options.setTabIndex(tabIndex)
        self._selections.setTabIndex(tabIndex)
        self._add.setTabIndex(tabIndex)
        self._remove.setTabIndex(tabIndex)


    def focus(self):
        self._options.setFocus(True)


    def getNavigationSelectKey(self):
        """Get the key that selects an item in the table. By default it
        is the Enter key but by overriding this you can change the key to
        whatever you want.
        """
        return KeyboardListener.KEY_ENTER


    def onKeyDown(self, event):
        keycode = event.getNativeKeyCode()

        # Catch tab and move between select:s
        if (keycode == KeyboardListener.KEY_TAB
                and event.getSource() == self._options):
            # Prevent default behavior
            event.preventDefault()

            # Remove current selections
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < self._options.getItemCount()):
                    break
                self._options.setItemSelected(i, False)
            # Focus selections
            self._selections.setFocus(True)

        if (keycode == KeyboardListener.KEY_TAB and event.isShiftKeyDown()
                and event.getSource() == self._selections):
            # Prevent default behavior
            event.preventDefault()

            # Remove current selections
            for i in range(self._selections.getItemCount()):
                self._selections.setItemSelected(i, False)

            # Focus options
            self._options.setFocus(True)

        if keycode == self.getNavigationSelectKey():
            # Prevent default behavior
            event.preventDefault()

            # Decide which select the selection was made in
            if event.getSource() == self._options:
                # Prevents the selection to become a single selection when
                # using Enter key
                # as the selection key (default)
                self._options.setFocus(False)

                self.addItem()
            elif event.getSource() == self._selections:
                # Prevents the selection to become a single selection when
                # using Enter key
                # as the selection key (default)
                self._selections.setFocus(False)

                self.removeItem()


    def onMouseDown(self, event):
        # Ensure that items are deselected when selecting
        # from a different source. See #3699 for details.
        if event.getSource() == self._options:
            for i in range(self._selections.getItemCount()):
                self._selections.setItemSelected(i, False)
        elif event.getSource() == self._selections:
            for i in range(self._options.getItemCount()):
                self._options.setItemSelected(i, False)


    def onDoubleClick(self, event):
        if event.getSource() == self._options:
            self.addItem()
            self._options.setSelectedIndex(-1)
            self._options.setFocus(False)
        elif event.getSource() == self._selections:
            self.removeItem()
            self._selections.setSelectedIndex(-1)
            self._selections.setFocus(False)


    def getSubPartElement(self, subPart):
        if self._SUBPART_OPTION_SELECT == subPart:
            return self._options.getElement()
        elif subPart.startswith(self._SUBPART_OPTION_SELECT_ITEM):
            idx = subPart[len(self._SUBPART_OPTION_SELECT_ITEM):]
            return self._options.getElement().getChild(int(idx))
        elif self._SUBPART_SELECTION_SELECT == subPart:
            return self._selections.getElement()
        elif subPart.startswith(self._SUBPART_SELECTION_SELECT_ITEM):
            idx = subPart[len(self._SUBPART_SELECTION_SELECT_ITEM):]
            return self._selections.getElement().getChild(int(idx))
        elif (self._optionsCaption is not None
                and self._SUBPART_LEFT_CAPTION == subPart):
            return self._optionsCaption.getElement()
        elif (self._selectionsCaption is not None
                and self._SUBPART_RIGHT_CAPTION == subPart):
            return self._selectionsCaption.getElement()
        elif self._SUBPART_ADD_BUTTON == subPart:
            return self._add.getElement()
        elif self._SUBPART_REMOVE_BUTTON == subPart:
            return self._remove.getElement()
        return None


    def getSubPartName(self, subElement):
        if (self._optionsCaption is not None
            and self._optionsCaption.getElement().isOrHasChild(subElement)):
            return self._SUBPART_LEFT_CAPTION
        elif (self._selectionsCaption is not None
            and self._selectionsCaption.getElement().isOrHasChild(subElement)):
            return self._SUBPART_RIGHT_CAPTION
        elif self._options.getElement().isOrHasChild(subElement):
            if self._options.getElement() == subElement:
                return self._SUBPART_OPTION_SELECT
            else:
                idx = Util.getChildElementIndex(subElement)
                return self._SUBPART_OPTION_SELECT_ITEM + idx
        elif self._selections.getElement().isOrHasChild(subElement):
            if self._selections.getElement() == subElement:
                return self._SUBPART_SELECTION_SELECT
            else:
                idx = Util.getChildElementIndex(subElement)
                return self._SUBPART_SELECTION_SELECT_ITEM + idx
        elif self._add.getElement().isOrHasChild(subElement):
            return self._SUBPART_ADD_BUTTON
        elif self._remove.getElement().isOrHasChild(subElement):
            return self._SUBPART_REMOVE_BUTTON
        return None


class DoubleClickListBox(ListBox):#, HasDoubleClickHandlers):
    """A ListBox which catches double clicks"""

    def __init__(self, isMultipleSelect=None):
        if isMultipleSelect is None:
            super(DoubleClickListBox, self).__init__()
        else:
            super(DoubleClickListBox, self).__init__(isMultipleSelect)


    def addDoubleClickHandler(self, handler):
        return self.addDomHandler(handler, DoubleClickEvent.getType())
