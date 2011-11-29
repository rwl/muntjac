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

from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.ui.VTextField import (VTextField,)
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
from com.vaadin.terminal.gwt.client.LocaleNotLoadedException import (LocaleNotLoadedException,)
from com.vaadin.terminal.gwt.client.ContainerResizedListener import (ContainerResizedListener,)
from com.vaadin.terminal.gwt.client.LocaleService import (LocaleService,)
from com.vaadin.terminal.gwt.client.ui.Field import (Field,)
from com.vaadin.terminal.gwt.client.ui.VDateField import (VDateField,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.SubPartAware import (SubPartAware,)
from com.vaadin.terminal.gwt.client.Focusable import (Focusable,)
# from com.google.gwt.event.dom.client.ChangeHandler import (ChangeHandler,)
# from java.util.Date import (Date,)


class VTextualDate(VDateField, Paintable, Field, ChangeHandler, ContainerResizedListener, Focusable, SubPartAware):
    _PARSE_ERROR_CLASSNAME = SELF.CLASSNAME + '-parseerror'
    _text = None
    _formatStr = None
    _width = None
    _needLayout = None
    fieldExtraWidth = -1
    _lenient = None
    _CLASSNAME_PROMPT = 'prompt'
    _ATTR_INPUTPROMPT = 'prompt'
    _inputPrompt = ''
    _prompting = False

    def __init__(self):
        super(VTextualDate, self)()
        self._text = TextBox()
        # use normal textfield styles as a basis
        self._text.setStyleName(VTextField.CLASSNAME)
        # add datefield spesific style name also
        self._text.addStyleName(self.CLASSNAME + '-textfield')
        self._text.addChangeHandler(self)
        VTextualDate_this = self

        class _0_(FocusHandler):

            def onFocus(self, event):
                VTextualDate_this._text.addStyleName(VTextField.CLASSNAME + '-' + VTextField.CLASSNAME_FOCUS)
                if VTextualDate_this._prompting:
                    VTextualDate_this._text.setText('')
                    VTextualDate_this.setPrompting(False)
                if (
                    self.getClient() is not None and self.getClient().hasEventListeners(VTextualDate_this, EventId.FOCUS)
                ):
                    self.getClient().updateVariable(self.getId(), EventId.FOCUS, '', True)

        _0_ = _0_()
        self._text.addFocusHandler(_0_)
        VTextualDate_this = self

        class _1_(BlurHandler):

            def onBlur(self, event):
                VTextualDate_this._text.removeStyleName(VTextField.CLASSNAME + '-' + VTextField.CLASSNAME_FOCUS)
                value = VTextualDate_this.getText()
                VTextualDate_this.setPrompting(VTextualDate_this._inputPrompt is not None and (value is None) or ('' == value))
                if VTextualDate_this._prompting:
                    VTextualDate_this._text.setText('' if self.readonly else VTextualDate_this._inputPrompt)
                if (
                    self.getClient() is not None and self.getClient().hasEventListeners(VTextualDate_this, EventId.BLUR)
                ):
                    self.getClient().updateVariable(self.getId(), EventId.BLUR, '', True)

        _1_ = _1_()
        self._text.addBlurHandler(_1_)
        self.add(self._text)

    def updateFromUIDL(self, uidl, client):
        origRes = self.currentResolution
        oldLocale = self.currentLocale
        super(VTextualDate, self).updateFromUIDL(uidl, client)
        if (origRes != self.currentResolution) or (oldLocale != self.currentLocale):
            # force recreating format string
            self._formatStr = None
        if uidl.hasAttribute('format'):
            self._formatStr = uidl.getStringAttribute('format')
        self._inputPrompt = uidl.getStringAttribute(self._ATTR_INPUTPROMPT)
        self._lenient = not uidl.getBooleanAttribute('strict')
        self.buildDate()
        # not a FocusWidget -> needs own tabindex handling
        if uidl.hasAttribute('tabindex'):
            self._text.setTabIndex(uidl.getIntAttribute('tabindex'))
        if self.readonly:
            self._text.addStyleDependentName('readonly')
        else:
            self._text.removeStyleDependentName('readonly')

    def getFormatString(self):
        if self._formatStr is None:
            if self.currentResolution == self.RESOLUTION_YEAR:
                self._formatStr = 'yyyy'
                # force full year
            else:
                # TODO should die instead? Can the component survive
                # without format string?
                try:
                    frmString = LocaleService.getDateFormat(self.currentLocale)
                    frmString = self.cleanFormat(frmString)
                    # String delim = LocaleService
                    # .getClockDelimiter(currentLocale);
                    if self.currentResolution >= self.RESOLUTION_HOUR:
                        if self.dts.isTwelveHourClock():
                            frmString += ' hh'
                        else:
                            frmString += ' HH'
                        if self.currentResolution >= self.RESOLUTION_MIN:
                            frmString += ':mm'
                            if self.currentResolution >= self.RESOLUTION_SEC:
                                frmString += ':ss'
                                if self.currentResolution >= self.RESOLUTION_MSEC:
                                    frmString += '.SSS'
                        if self.dts.isTwelveHourClock():
                            frmString += ' aaa'
                    self._formatStr = frmString
                except LocaleNotLoadedException, e:
                    VConsole.error(e)
        return self._formatStr

    def buildDate(self):
        """Updates the text field according to the current date (provided by
        {@link #getDate()}). Takes care of updating text, enabling and disabling
        the field, setting/removing readonly status and updating readonly styles.

        TODO: Split part of this into a method that only updates the text as this
        is what usually is needed except for updateFromUIDL.
        """
        self.removeStyleName(self._PARSE_ERROR_CLASSNAME)
        # Create the initial text for the textfield
        currentDate = self.getDate()
        if currentDate is not None:
            dateText = self.getDateTimeService().formatDate(currentDate, self.getFormatString())
        else:
            dateText = ''
        self.setText(dateText)
        self._text.setEnabled(self.enabled)
        self._text.setReadOnly(self.readonly)
        if self.readonly:
            self._text.addStyleName('v-readonly')
        else:
            self._text.removeStyleName('v-readonly')

    def setPrompting(self, prompting):
        self._prompting = prompting
        if prompting:
            self.addStyleDependentName(self._CLASSNAME_PROMPT)
        else:
            self.removeStyleDependentName(self._CLASSNAME_PROMPT)

    def onChange(self, event):
        if not (self._text.getText() == ''):
            try:
                enteredDate = self._text.getText()
                self.setDate(self.getDateTimeService().parseDate(enteredDate, self.getFormatString(), self._lenient))
                if self._lenient:
                    # If date value was leniently parsed, normalize text
                    # presentation.
                    # FIXME: Add a description/example here of when this is
                    # needed
                    self._text.setValue(self.getDateTimeService().formatDate(self.getDate(), self.getFormatString()), False)
                # remove possibly added invalid value indication
                self.removeStyleName(self._PARSE_ERROR_CLASSNAME)
            except Exception, e:
                VConsole.log(e)
                self.addStyleName(self._PARSE_ERROR_CLASSNAME)
                # this is a hack that may eventually be removed
                self.getClient().updateVariable(self.getId(), 'lastInvalidDateString', self._text.getText(), False)
                self.setDate(None)
        else:
            self.setDate(None)
            # remove possibly added invalid value indication
            self.removeStyleName(self._PARSE_ERROR_CLASSNAME)
        # always send the date string
        self.getClient().updateVariable(self.getId(), 'dateString', self._text.getText(), False)
        # Update variables
        # (only the smallest defining resolution needs to be
        # immediate)
        currentDate = self.getDate()
        self.getClient().updateVariable(self.getId(), 'year', currentDate.getYear() + 1900 if currentDate is not None else -1, self.currentResolution == VDateField.RESOLUTION_YEAR and self.immediate)
        if self.currentResolution >= VDateField.RESOLUTION_MONTH:
            self.getClient().updateVariable(self.getId(), 'month', currentDate.getMonth() + 1 if currentDate is not None else -1, self.currentResolution == VDateField.RESOLUTION_MONTH and self.immediate)
        if self.currentResolution >= VDateField.RESOLUTION_DAY:
            self.getClient().updateVariable(self.getId(), 'day', currentDate.getDate() if currentDate is not None else -1, self.currentResolution == VDateField.RESOLUTION_DAY and self.immediate)
        if self.currentResolution >= VDateField.RESOLUTION_HOUR:
            self.getClient().updateVariable(self.getId(), 'hour', currentDate.getHours() if currentDate is not None else -1, self.currentResolution == VDateField.RESOLUTION_HOUR and self.immediate)
        if self.currentResolution >= VDateField.RESOLUTION_MIN:
            self.getClient().updateVariable(self.getId(), 'min', currentDate.getMinutes() if currentDate is not None else -1, self.currentResolution == VDateField.RESOLUTION_MIN and self.immediate)
        if self.currentResolution >= VDateField.RESOLUTION_SEC:
            self.getClient().updateVariable(self.getId(), 'sec', currentDate.getSeconds() if currentDate is not None else -1, self.currentResolution == VDateField.RESOLUTION_SEC and self.immediate)
        if self.currentResolution == VDateField.RESOLUTION_MSEC:
            self.getClient().updateVariable(self.getId(), 'msec', self.getMilliseconds() if currentDate is not None else -1, self.immediate)

    def cleanFormat(self, format):
        # Remove unnecessary d & M if resolution is too low
        if self.currentResolution < VDateField.RESOLUTION_DAY:
            format = format.replaceAll('d', '')
        if self.currentResolution < VDateField.RESOLUTION_MONTH:
            format = format.replaceAll('M', '')
        # Remove unsupported patterns
        # TODO support for 'G', era designator (used at least in Japan)
        format = format.replaceAll('[GzZwWkK]', '')
        # Remove extra delimiters ('/' and '.')
        while (
            (format.startswith('/') or format.startswith('.')) or format.startswith('-')
        ):
            format = format[1:]
        while (format.endswith('/') or format.endswith('.')) or format.endswith('-'):
            format = format[:-1]
        # Remove duplicate delimiters
        format = format.replaceAll('//', '/')
        format = format.replaceAll('\\.\\.', '.')
        format = format.replaceAll('--', '-')
        return format.trim()

    def setWidth(self, newWidth):
        if (
            not ('' == newWidth) and (self._width is None) or (not (newWidth == self._width))
        ):
            if BrowserInfo.get().isIE6():
                # in IE6 cols ~ min-width
                DOM.setElementProperty(self._text.getElement(), 'size', '1')
            self._needLayout = True
            self._width = newWidth
            super(VTextualDate, self).setWidth(self._width)
            self.iLayout()
            if newWidth.find('%') < 0:
                self._needLayout = False
        elif '' == newWidth and self._width is not None and not ('' == self._width):
            if BrowserInfo.get().isIE6():
                # revert IE6 hack
                DOM.setElementProperty(self._text.getElement(), 'size', '')
            super(VTextualDate, self).setWidth('')
            self._needLayout = True
            self.iLayout()
            self._needLayout = False
            self._width = None

    def getFieldExtraWidth(self):
        """Returns pixels in x-axis reserved for other than textfield content.

        @return extra width in pixels
        """
        if self.fieldExtraWidth < 0:
            self._text.setWidth('0')
            self.fieldExtraWidth = self._text.getOffsetWidth()
            if BrowserInfo.get().isFF3():
                # Firefox somehow always leaves the INPUT element 2px wide
                self.fieldExtraWidth -= 2
        return self.fieldExtraWidth

    def updateWidth(self):
        self._needLayout = True
        self.fieldExtraWidth = -1
        self.iLayout()

    def iLayout(self):
        if self._needLayout:
            textFieldWidth = self.getOffsetWidth() - self.getFieldExtraWidth()
            if textFieldWidth < 0:
                # Field can never be smaller than 0 (causes exception in IE)
                textFieldWidth = 0
            self._text.setWidth(textFieldWidth + 'px')

    def focus(self):
        self._text.setFocus(True)

    def getText(self):
        if self._prompting:
            return ''
        return self._text.getText()

    def setText(self, text):
        if self._inputPrompt is not None and (text is None) or ('' == text):
            text = '' if self.readonly else self._inputPrompt
            self.setPrompting(True)
        else:
            self.setPrompting(False)
        self._text.setText(text)

    _TEXTFIELD_ID = 'field'

    def getSubPartElement(self, subPart):
        if subPart == self._TEXTFIELD_ID:
            return self._text.getElement()
        return None

    def getSubPartName(self, subElement):
        if self._text.getElement().isOrHasChild(subElement):
            return self._TEXTFIELD_ID
        return None
