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

from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.ui.VButton import (VButton,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.ui.UploadIFrameOnloadStrategy import (UploadIFrameOnloadStrategy,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
# from com.google.gwt.dom.client.FormElement import (FormElement,)
# from com.google.gwt.user.client.ui.FileUpload import (FileUpload,)
# from com.google.gwt.user.client.ui.FormPanel import (FormPanel,)
# from com.google.gwt.user.client.ui.Hidden import (Hidden,)


class VUpload(SimplePanel, Paintable):
    """Note, we are not using GWT FormPanel as we want to listen submitcomplete
    events even though the upload component is already detached.
    """

    class MyFileUpload(FileUpload):

        def onBrowserEvent(self, event):
            super(MyFileUpload, self).onBrowserEvent(event)
            if event.getTypeInt() == self.Event.ONCHANGE:
                if (
                    self.immediate and self.fu.getFilename() is not None and not ('' == self.fu.getFilename())
                ):
                    self.submit()
            elif BrowserInfo.get().isIE() and event.getTypeInt() == self.Event.ONFOCUS:
                # IE and user has clicked on hidden textarea part of upload
                # field. Manually open file selector, other browsers do it by
                # default.
                self.fireNativeClick(self.fu.getElement())
                # also remove focus to enable hack if user presses cancel
                # button
                self.fireNativeBlur(self.fu.getElement())

    CLASSNAME = 'v-upload'
    # FileUpload component that opens native OS dialog to select file.
    _fu = MyFileUpload()
    _panel = FlowPanel()
    _onloadstrategy = GWT.create(UploadIFrameOnloadStrategy)
    _client = None
    _paintableId = None
    # Button that initiates uploading
    _submitButton = None
    # When expecting big files, programmer may initiate some UI changes when
    # uploading the file starts. Bit after submitting file we'll visit the
    # server to check possible changes.

    _t = None
    # some browsers tries to send form twice if submit is called in button
    # click handler, some don't submit at all without it, so we need to track
    # if form is already being submitted

    _submitted = False
    _enabled = True
    _immediate = None
    _maxfilesize = Hidden()
    _element = None
    _synthesizedFrame = None
    _nextUploadId = None

    def __init__(self):
        super(VUpload, self)(self.com.google.gwt.dom.client.Document.get().createFormElement())
        self._element = self.getElement()
        self.setEncoding(self.getElement(), FormPanel.ENCODING_MULTIPART)
        self._element.setMethod(FormPanel.METHOD_POST)
        self.setWidget(self._panel)
        self._panel.add(self._maxfilesize)
        self._panel.add(self._fu)
        self._submitButton = VButton()

        class _0_(ClickHandler):

            def onClick(self, event):
                if self.immediate:
                    # fire click on upload (eg. focused button and hit space)
                    self.fireNativeClick(self.fu.getElement())
                else:
                    self.submit()

        _0_ = self._0_()
        self._submitButton.addClickHandler(_0_)
        self._panel.add(self._submitButton)
        self.setStyleName(self.CLASSNAME)
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)

    def onBrowserEvent(self, event):
        if event.getTypeInt() & VTooltip.TOOLTIP_EVENTS > 0:
            self._client.handleTooltipEvent(event, self)
        super(VUpload, self).onBrowserEvent(event)

    @classmethod
    def setEncoding(cls, form, encoding):
        # -{
        #       form.enctype = encoding;
        #       // For IE6
        #       form.encoding = encoding;
        #     }-

        pass

    def updateFromUIDL(self, uidl, client):
        if client.updateComponent(self, uidl, True):
            return
        if uidl.hasAttribute('notStarted'):
            self._t.schedule(400)
            return
        if uidl.hasAttribute('forceSubmit'):
            self.submit()
            return
        self.setImmediate(uidl.getBooleanAttribute('immediate'))
        self._client = client
        self._paintableId = uidl.getId()
        self._nextUploadId = uidl.getIntAttribute('nextid')
        action = client.translateVaadinUri(uidl.getStringVariable('action'))
        self._element.setAction(action)
        if uidl.hasAttribute('buttoncaption'):
            self._submitButton.setText(uidl.getStringAttribute('buttoncaption'))
            self._submitButton.setVisible(True)
        else:
            self._submitButton.setVisible(False)
        self._fu.setName(self._paintableId + '_file')
        if uidl.hasAttribute('disabled') or uidl.hasAttribute('readonly'):
            self.disableUpload()
        elif not uidl.getBooleanAttribute('state'):
            # Enable the button only if an upload is not in progress
            self.enableUpload()
            self.ensureTargetFrame()

    def setImmediate(self, booleanAttribute):
        if self._immediate != booleanAttribute:
            self._immediate = booleanAttribute
            if self._immediate:
                self._fu.sinkEvents(self.Event.ONCHANGE)
                self._fu.sinkEvents(self.Event.ONFOCUS)
        self.setStyleName(self.getElement(), self.CLASSNAME + '-immediate', self._immediate)

    @classmethod
    def fireNativeClick(cls, element):
        # -{
        #         element.click();
        #     }-

        pass

    @classmethod
    def fireNativeBlur(cls, element):
        # -{
        #         element.blur();
        #     }-

        pass

    def disableUpload(self):
        self._submitButton.setEnabled(False)
        if not self._submitted:
            # Cannot disable the fileupload while submitting or the file won't
            # be submitted at all
            self._fu.getElement().setPropertyBoolean('disabled', True)
        self._enabled = False

    def enableUpload(self):
        self._submitButton.setEnabled(True)
        self._fu.getElement().setPropertyBoolean('disabled', False)
        self._enabled = True
        if self._submitted:
            # An old request is still in progress (most likely cancelled),
            # ditching that target frame to make it possible to send a new
            # file. A new target frame is created later."

            self.cleanTargetFrame()
            self._submitted = False

    def rebuildPanel(self):
        """Re-creates file input field and populates panel. This is needed as we
        want to clear existing values from our current file input field.
        """
        self._panel.remove(self._submitButton)
        self._panel.remove(self._fu)
        self._fu = self.MyFileUpload()
        self._fu.setName(self._paintableId + '_file')
        self._fu.getElement().setPropertyBoolean('disabled', not self._enabled)
        self._panel.add(self._fu)
        self._panel.add(self._submitButton)
        if self._immediate:
            self._fu.sinkEvents(self.Event.ONCHANGE)

    def onSubmitComplete(self):
        """Called by JSNI (hooked via {@link #onloadstrategy})"""
        # Needs to be run dereferred to avoid various browser issues.

        class _1_(Command):

            def execute(self):
                if self.submitted:
                    if self.client is not None:
                        if self.t is not None:
                            self.t.cancel()
                        VConsole.log('VUpload:Submit complete')
                        self.client.sendPendingVariableChanges()
                    self.rebuildPanel()
                    self.submitted = False
                    self.enableUpload()
                    if not self.isAttached():
                        # Upload is complete when upload is already abandoned.
                        self.cleanTargetFrame()

        _1_ = self._1_()
        self.Scheduler.get().scheduleDeferred(_1_)

    def submit(self):
        if (
            ((len(self._fu.getFilename()) == 0) or self._submitted) or (not self._enabled)
        ):
            VConsole.log('Submit cancelled (disabled, no file or already submitted)')
            return
        # flush possibly pending variable changes, so they will be handled
        # before upload
        self._client.sendPendingVariableChanges()
        self._element.submit()
        self._submitted = True
        VConsole.log('Submitted form')
        self.disableUpload()
        # Visit server a moment after upload has started to see possible
        # changes from UploadStarted event. Will be cleared on complete.

        class _2_(Timer):

            def run(self):
                VConsole.log('Visiting server to see if upload started event changed UI.')
                self.client.updateVariable(self.paintableId, 'pollForStart', self.nextUploadId, True)

        _2_ = self._2_()
        self._t = _2_
        self._t.schedule(800)

    def onAttach(self):
        super(VUpload, self).onAttach()
        if self._client is not None:
            self.ensureTargetFrame()

    def ensureTargetFrame(self):
        if self._synthesizedFrame is None:
            # Attach a hidden IFrame to the form. This is the target iframe to
            # which
            # the form will be submitted. We have to create the iframe using
            # innerHTML,
            # because setting an iframe's 'name' property dynamically doesn't
            # work on
            # most browsers.
            dummy = self.Document.get().createDivElement()
            dummy.setInnerHTML('<iframe src=\"javascript:\'\'\" name=\'' + self.getFrameName() + '\' style=\'position:absolute;width:0;height:0;border:0\'>')
            self._synthesizedFrame = dummy.getFirstChildElement()
            self.Document.get().getBody().appendChild(self._synthesizedFrame)
            self._element.setTarget(self.getFrameName())
            self._onloadstrategy.hookEvents(self._synthesizedFrame, self)

    def getFrameName(self):
        return self._paintableId + '_TGT_FRAME'

    def onDetach(self):
        super(VUpload, self).onDetach()
        if not self._submitted:
            self.cleanTargetFrame()

    def cleanTargetFrame(self):
        if self._synthesizedFrame is not None:
            self.Document.get().getBody().removeChild(self._synthesizedFrame)
            self._onloadstrategy.unHookEvents(self._synthesizedFrame)
            self._synthesizedFrame = None
