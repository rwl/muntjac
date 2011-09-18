# Copyright (C) 2011 Vaadin Ltd
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

from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.richtextarea.VRichTextToolbar import (VRichTextToolbar,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.Field import (Field,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.ui.ShortcutActionHandler import (BeforeShortcutActionListener,)
# from com.google.gwt.core.client.Scheduler import (Scheduler,)
# from com.google.gwt.event.dom.client.BlurEvent import (BlurEvent,)
# from com.google.gwt.event.dom.client.BlurHandler import (BlurHandler,)
# from com.google.gwt.event.dom.client.ChangeEvent import (ChangeEvent,)
# from com.google.gwt.event.dom.client.ChangeHandler import (ChangeHandler,)
# from com.google.gwt.event.dom.client.KeyDownEvent import (KeyDownEvent,)
# from com.google.gwt.event.dom.client.KeyDownHandler import (KeyDownHandler,)
# from com.google.gwt.event.dom.client.KeyPressEvent import (KeyPressEvent,)
# from com.google.gwt.event.dom.client.KeyPressHandler import (KeyPressHandler,)
# from com.google.gwt.event.shared.HandlerRegistration import (HandlerRegistration,)
# from com.google.gwt.user.client.Command import (Command,)
# from com.google.gwt.user.client.DOM import (DOM,)
# from com.google.gwt.user.client.Element import (Element,)
# from com.google.gwt.user.client.Event import (Event,)
# from com.google.gwt.user.client.Timer import (Timer,)
# from com.google.gwt.user.client.ui.Composite import (Composite,)
# from com.google.gwt.user.client.ui.FlowPanel import (FlowPanel,)
# from com.google.gwt.user.client.ui.Focusable import (Focusable,)
# from com.google.gwt.user.client.ui.HTML import (HTML,)
# from com.google.gwt.user.client.ui.RichTextArea import (RichTextArea,)
# from com.google.gwt.user.client.ui.Widget import (Widget,)
# from com.vaadin.terminal.gwt.client.ui.ShortcutActionHandler.BeforeShortcutActionListener import (BeforeShortcutActionListener,)
# from com.vaadin.terminal.gwt.client.ui.ShortcutActionHandler.ShortcutActionHandlerOwner import (ShortcutActionHandlerOwner,)


class VRichTextArea(Composite, Paintable, Field, ChangeHandler, BlurHandler, KeyPressHandler, KeyDownHandler, BeforeShortcutActionListener, Focusable):
    """This class implements a basic client side rich text editor component.

    @author IT Mill Ltd.
    """
    # The input node CSS classname.
    CLASSNAME = 'v-richtextarea'
    id = None
    client = None
    _immediate = False
    _rta = None
    _formatter = None
    _html = HTML()
    _fp = FlowPanel()
    _enabled = True
    _extraHorizontalPixels = -1
    _extraVerticalPixels = -1
    _maxLength = -1
    _toolbarNaturalWidth = 500
    _keyPressHandler = None
    _hasShortcutActionHandler = None
    _currentValue = ''
    _readOnly = False

    def __init__(self):
        self.createRTAComponents()
        self._fp.add(self._formatter)
        self._fp.add(self._rta)
        self.initWidget(self._fp)
        self.setStyleName(self.CLASSNAME)

    def createRTAComponents(self):
        self._rta = RichTextArea()
        self._rta.setWidth('100%')
        self._rta.addBlurHandler(self)
        self._rta.addKeyDownHandler(self)
        self._formatter = VRichTextToolbar(self._rta)

    def setEnabled(self, enabled):
        if self._enabled != enabled:
            # rta.setEnabled(enabled);
            self.swapEditableArea()
            self._enabled = enabled

    def swapEditableArea(self):
        """Swaps html to rta and visa versa."""
        if self._html.isAttached():
            self._fp.remove(self._html)
            if BrowserInfo.get().isWebkit():
                self._fp.remove(self._formatter)
                self.createRTAComponents()
                # recreate new RTA to bypass #5379
                self._fp.add(self._formatter)
            self._rta.setHTML(self._currentValue)
            self._fp.add(self._rta)
        else:
            self._html.setHTML(self._currentValue)
            self._fp.remove(self._rta)
            self._fp.add(self._html)

    def updateFromUIDL(self, uidl, client):
        self.client = client
        self.id = uidl.getId()
        if uidl.hasVariable('text'):
            self._currentValue = uidl.getStringVariable('text')
            if self._rta.isAttached():
                self._rta.setHTML(self._currentValue)
            else:
                self._html.setHTML(self._currentValue)
        if not uidl.hasAttribute('cached'):
            self.setEnabled(not uidl.getBooleanAttribute('disabled'))
        if client.updateComponent(self, uidl, True):
            return
        self.setReadOnly(uidl.getBooleanAttribute('readonly'))
        self._immediate = uidl.getBooleanAttribute('immediate')
        newMaxLength = uidl.getIntAttribute('maxLength') if uidl.hasAttribute('maxLength') else -1
        if newMaxLength >= 0:
            if self._maxLength == -1:
                self._keyPressHandler = self._rta.addKeyPressHandler(self)
            self._maxLength = newMaxLength
        elif self._maxLength != -1:
            self.getElement().setAttribute('maxlength', '')
            self._maxLength = -1
            self._keyPressHandler.removeHandler()
        if uidl.hasAttribute('selectAll'):
            self.selectAll()

    def selectAll(self):
        # There is a timing issue if trying to select all immediately on first
        # render. Simple deferred command is not enough. Using Timer with
        # moderated timeout. If this appears to fail on many (most likely slow)
        # environments, consider increasing the timeout.
        # 
        # FF seems to require the most time to stabilize its RTA. On Vaadin
        # tiergarden test machines, 200ms was not enough always (about 50%
        # success rate) - 300 ms was 100% successful. This however was not
        # enough on a sluggish old non-virtualized XP test machine. A bullet
        # proof solution would be nice, GWT 2.1 might however solve these. At
        # least setFocus has a workaround for this kind of issue.



        class _0_(Timer):

            def run(self):
                self.rta.getFormatter().selectAll()


        _0_ = self._0_()
        _0_.schedule(320)

    def setReadOnly(self, b):
        if self.isReadOnly() != b:
            self.swapEditableArea()
            self._readOnly = b
        # reset visibility in case enabled state changed and the formatter was
        # recreated
        self._formatter.setVisible(not self._readOnly)

    def isReadOnly(self):
        # TODO is this really used, or does everything go via onBlur() only?
        return self._readOnly

    def onChange(self, event):
        self.synchronizeContentToServer()

    def synchronizeContentToServer(self):
        """Method is public to let popupview force synchronization on close."""
        if self.client is not None and self.id is not None:
            html = self._rta.getHTML()
            if not (html == self._currentValue):
                self.client.updateVariable(self.id, 'text', html, self._immediate)
                self._currentValue = html

    def onBlur(self, event):
        self.synchronizeContentToServer()
        # TODO notify possible server side blur/focus listeners

    def getExtraHorizontalPixels(self):
        """@return space used by components paddings and borders"""
        if self._extraHorizontalPixels < 0:
            self.detectExtraSizes()
        return self._extraHorizontalPixels

    def getExtraVerticalPixels(self):
        """@return space used by components paddings and borders"""
        if self._extraVerticalPixels < 0:
            self.detectExtraSizes()
        return self._extraVerticalPixels

    def detectExtraSizes(self):
        """Detects space used by components paddings and borders."""
        clone = Util.cloneNode(self.getElement(), False)
        DOM.setElementAttribute(clone, 'id', '')
        DOM.setStyleAttribute(clone, 'visibility', 'hidden')
        DOM.setStyleAttribute(clone, 'position', 'absolute')
        # due FF3 bug set size to 10px and later subtract it from extra pixels
        DOM.setStyleAttribute(clone, 'width', '10px')
        DOM.setStyleAttribute(clone, 'height', '10px')
        DOM.appendChild(DOM.getParent(self.getElement()), clone)
        self._extraHorizontalPixels = DOM.getElementPropertyInt(clone, 'offsetWidth') - 10
        self._extraVerticalPixels = DOM.getElementPropertyInt(clone, 'offsetHeight') - 10
        DOM.removeChild(DOM.getParent(self.getElement()), clone)

    def setHeight(self, height):
        if height.endswith('px'):
            h = int(height[:-2])
            h -= self.getExtraVerticalPixels()
            if h < 0:
                h = 0
            super(VRichTextArea, self).setHeight(h + 'px')
        else:
            super(VRichTextArea, self).setHeight(height)
        if (height is None) or (height == ''):
            self._rta.setHeight('')
        else:
            # The formatter height will be initially calculated wrong so we
            # delay the height setting so the DOM has had time to stabilize.

            class _1_(Command):

                def execute(self):
                    editorHeight = self.getOffsetHeight() - self.getExtraVerticalPixels() - self.formatter.getOffsetHeight()
                    if editorHeight < 0:
                        editorHeight = 0
                    self.rta.setHeight(editorHeight + 'px')

            _1_ = self._1_()
            Scheduler.get().scheduleDeferred(_1_)

    def setWidth(self, width):
        if width.endswith('px'):
            w = int(width[:-2])
            w -= self.getExtraHorizontalPixels()
            if w < 0:
                w = 0
            super(VRichTextArea, self).setWidth(w + 'px')
        elif width == '':
            # IE cannot calculate the width of the 100% iframe correctly if
            # there is no width specified for the parent. In this case we would
            # use the toolbar but IE cannot calculate the width of that one
            # correctly either in all cases. So we end up using a default width
            # for a RichTextArea with no width definition in all browsers (for
            # compatibility).

            super(VRichTextArea, self).setWidth(self._toolbarNaturalWidth + 'px')
        else:
            super(VRichTextArea, self).setWidth(width)

    def onKeyPress(self, event):
        if self._maxLength >= 0:

            class _2_(Command):

                def execute(self):
                    if len(self.rta.getHTML()) > self.maxLength:
                        self.rta.setHTML(self.rta.getHTML()[:self.maxLength])

            _2_ = self._2_()
            Scheduler.get().scheduleDeferred(_2_)

    def onKeyDown(self, event):
        # delegate to closest shortcut action handler
        # throw event from the iframe forward to the shortcuthandler
        shortcutHandler = self.getShortcutHandlerOwner().getShortcutActionHandler()
        if shortcutHandler is not None:
            shortcutHandler.handleKeyboardEvent(self.com.google.gwt.user.client.Event.as_(event.getNativeEvent()), self)

    def getShortcutHandlerOwner(self):
        if self._hasShortcutActionHandler is None:
            parent = self.getParent()
            while parent is not None:
                if isinstance(parent, ShortcutActionHandlerOwner):
                    break
                parent = parent.getParent()
            self._hasShortcutActionHandler = parent
        return self._hasShortcutActionHandler

    def onBeforeShortcutAction(self, e):
        self.synchronizeContentToServer()

    def getTabIndex(self):
        return self._rta.getTabIndex()

    def setAccessKey(self, key):
        self._rta.setAccessKey(key)

    def setFocus(self, focused):
        # Similar issue as with selectAll. Focusing must happen before possible
        # selectall, so keep the timeout here lower.



        class _3_(Timer):

            def run(self):
                self.rta.setFocus(True)


        _3_ = self._3_()
        _3_.schedule(300)

    def setTabIndex(self, index):
        self._rta.setTabIndex(index)
