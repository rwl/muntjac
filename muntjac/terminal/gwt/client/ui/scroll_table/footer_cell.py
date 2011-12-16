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

from pyjamas.ui import Event

from pyjamas.ui.Widget import Widget

from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails


class FooterCell(Widget):
    """A cell in the footer"""


    def __init__(self, colId, headerText, st):
        self._st = st

        self._td = DOM.createTD()
        self._captionContainer = DOM.createDiv()
        self._align = st.ALIGN_LEFT
        self._width = -1
        self._expandRatio = 0
        self._definedWidth = False
        self._naturalWidth = -1

        self._cid = colId
        self.setText(headerText)
        DOM.setElemAttribute(self._captionContainer, 'className',
                st.CLASSNAME + '-footer-container')
        # ensure no clipping initially (problem on column additions)
        DOM.setStyleAttribute(self._captionContainer, 'overflow', 'visible')
        DOM.sinkEvents(self._captionContainer, Event.MOUSEEVENTS)
        DOM.appendChild(self._td, self._captionContainer)
        DOM.sinkEvents(self._td, Event.MOUSEEVENTS)
        self.setElement(self._td)


    def setText(self, footerText):
        """Sets the text of the footer

        @param footerText:
                   The text in the footer
        """
        DOM.setInnerHTML(self._captionContainer, footerText)


    def setAlign(self, c):
        """Set alignment of the text in the cell

        @param c:
                   The alignment which can be ALIGN_CENTER, ALIGN_LEFT,
                   ALIGN_RIGHT
        """
        if self._align != c:
            if c == self._st.ALIGN_CENTER:
                DOM.setStyleAttribute(self._captionContainer, 'textAlign',
                        'center')
            elif c == self._st.ALIGN_RIGHT:
                DOM.setStyleAttribute(self._captionContainer, 'textAlign',
                        'right')
            else:
                DOM.setStyleAttribute(self._captionContainer, 'textAlign',
                        '')

        self._align = c


    def getAlign(self):
        """Get the alignment of the text int the cell

        @return: Returns either ALIGN_CENTER, ALIGN_LEFT or ALIGN_RIGHT
        """
        return self._align


    def setWidth(self, w, ensureDefinedWidth):
        """Sets the width of the cell

        @param w:
                   The width of the cell
        @param ensureDefinedWidth:
                   Ensures the the given width is not recalculated
        """
        if ensureDefinedWidth:
            self._definedWidth = True
            # on column resize expand ratio becomes zero
            self._expandRatio = 0

        if self._width == w:
            return

        if self._width == -1:
            # go to default mode, clip content if necessary
            DOM.setStyleAttribute(self._captionContainer, 'overflow', '')

        self._width = w
        if w == -1:
            DOM.setStyleAttribute(self._captionContainer, 'width', '')
            self.setWidth('')
        else:
            # Reduce width with one pixel for the right border since the
            # footers does not have any spacers between them.
            borderWidths = 1

            # Set the container width (check for negative value)
            if w - borderWidths >= 0:
                self._captionContainer.getStyle().setPropertyPx('width',
                        w - borderWidths)
            else:
                self._captionContainer.getStyle().setPropertyPx('width', 0)

            # if we already have tBody, set the header width properly, if
            # not defer it. IE will fail with complex float in table header
            # unless TD width is not explicitly set.
            if self._st._scrollBody is not None:
                # Reduce with one since footer does not have any spacers,
                # instead a 1 pixel border.
                tdWidth = (self._width
                    + self._st._scrollBody.getCellExtraWidth()) - borderWidths
                self.setWidth(tdWidth + 'px')
            else:

                class _9_(Command):

                    def execute(self):
                        borderWidths = 1
                        tdWidth = ((FooterCell_this._width
                                + self._st._scrollBody.getCellExtraWidth())
                                        - borderWidths)
                        FooterCell_this.setWidth(tdWidth + 'px')

                _9_ = _9_()
                Scheduler.get().scheduleDeferred(_9_)


    def setUndefinedWidth(self):
        """Sets the width to undefined"""
        self.setWidth(-1, False)


    def isDefinedWidth(self):
        """Detects if width is fixed by developer on server side or resized
        to current width by user.

        @return: true if defined, false if "natural" width
        """
        return self._definedWidth and self._width >= 0


    def getWidth(self):
        """Returns the pixels width of the footer cell

        @return: The width in pixels
        """
        return self._width


    def setExpandRatio(self, floatAttribute):
        """Sets the expand ratio of the cell

        @param floatAttribute:
                   The expand ratio
        """
        self._expandRatio = floatAttribute


    def getExpandRatio(self):
        """Returns the expand ration of the cell

        @return: The expand ratio
        """
        return self._expandRatio

    def isEnabled(self):
        """Is the cell enabled?

        @return: True if enabled else False
        """
        return self.getParent() is not None


    def onBrowserEvent(self, event):
        """Handle column clicking"""
        if self._st._enabled and event is not None:
            self.handleCaptionEvent(event)
            if DOM.eventGetType(event) == Event.ONMOUSEUP:
                self._st._scrollBodyPanel.setFocus(True)
            event.stopPropagation()
            event.preventDefault()


    def handleCaptionEvent(self, event):
        """Handles a event on the captions

        @param event:
                   The event to handle
        """
        if DOM.eventGetType(event) == Event.ONMOUSEUP:
            self.fireFooterClickedEvent(event)


    def fireFooterClickedEvent(self, event):
        """Fires a footer click event after the user has clicked a column
        footer cell

        @param event:
                   The click event
        """
        if self._st.client.hasEventListeners(self._st,
                self._st.FOOTER_CLICK_EVENT_ID):
            details = MouseEventDetails(event)
            self._st.client.updateVariable(self._st.paintableId,
                    'footerClickEvent', str(details), False)
            self._st.client.updateVariable(self._st.paintableId,
                    'footerClickCID', self._cid, True)


    def getColKey(self):
        """Returns the column key of the column

        @return The column key
        """
        return self._cid


    def getNaturalColumnWidth(self, columnIndex):
        """Detects the natural minimum width for the column of this header cell.
        If column is resized by user or the width is defined by server the
        actual width is returned. Else the natural min width is returned.

        @param columnIndex:
                   column index hint, if -1 (unknown) it will be detected
        """
        if self.isDefinedWidth():
            return self._width
        else:
            if self._naturalWidth < 0:
                # This is recently revealed column. Try to detect a proper
                # value (greater of header and data
                # cols)
                hw = (self.getElement().getLastChild().getOffsetWidth()
                        + self._st._scrollBody.getCellExtraWidth())
                if columnIndex < 0:
                    columnIndex = 0
                    _0 = True
                    it = self._st.tHead
                    while it.hasNext():
                        if it.next() is self:
                            break
                        columnIndex += 1

                cw = self._st._scrollBody.getColWidth(columnIndex)

                self._naturalWidth = hw if hw > cw else cw

            return self._naturalWidth


    def setNaturalMinimumColumnWidth(self, w):
        self._naturalWidth = w


class RowHeadersFooterCell(FooterCell):
    """HeaderCell that is header cell for row headers.

    Reordering disabled and clicking on it resets sorting.
    """

    def __init__(self, st):
        super(RowHeadersFooterCell, self).__init__(st._ROW_HEADER_COLUMN_KEY,
                '')


    def handleCaptionEvent(self, event):
        # NOP: RowHeaders cannot be reordered
        # TODO It'd be nice to reset sorting here
        pass
