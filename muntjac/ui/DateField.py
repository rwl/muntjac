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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.event.FieldEvents import (BlurEvent, BlurListener, BlurNotifier, FieldEvents, FocusEvent, FocusListener, FocusNotifier,)
from com.vaadin.ui.AbstractField import (AbstractField,)
from com.vaadin.data.Property import (Property,)
from com.vaadin.terminal.gwt.client.ui.VDateField import (VDateField,)
# from java.text.ParseException import (ParseException,)
# from java.text.SimpleDateFormat import (SimpleDateFormat,)
# from java.util.Calendar import (Calendar,)
# from java.util.Collection import (Collection,)
# from java.util.Date import (Date,)
# from java.util.Locale import (Locale,)
# from java.util.Map import (Map,)


class DateField(AbstractField, FieldEvents, BlurNotifier, FieldEvents, FocusNotifier):
    """<p>
    A date editor component that can be bound to any {@link Property} that is
    compatible with <code>java.util.Date</code>.
    </p>
    <p>
    Since <code>DateField</code> extends <code>AbstractField</code> it implements
    the {@link com.vaadin.data.Buffered}interface.
    </p>
    <p>
    A <code>DateField</code> is in write-through mode by default, so
    {@link com.vaadin.ui.AbstractField#setWriteThrough(boolean)}must be called to
    enable buffering.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Private members
    # Resolution identifier: milliseconds.
    RESOLUTION_MSEC = 0
    # Resolution identifier: seconds.
    RESOLUTION_SEC = 1
    # Resolution identifier: minutes.
    RESOLUTION_MIN = 2
    # Resolution identifier: hours.
    RESOLUTION_HOUR = 3
    # Resolution identifier: days.
    RESOLUTION_DAY = 4
    # Resolution identifier: months.
    RESOLUTION_MONTH = 5
    # Resolution identifier: years.
    RESOLUTION_YEAR = 6
    # Specified smallest modifiable unit.
    _resolution = RESOLUTION_MSEC
    # Specified largest modifiable unit.
    _largestModifiable = RESOLUTION_YEAR
    # The internal calendar to be used in java.utl.Date conversions.
    _calendar = None
    # Overridden format string
    _dateFormat = None
    _lenient = False
    _dateString = None
    # Was the last entered string parsable? If this flag is false, datefields
    # internal validator does not pass.

    _uiHasValidDateString = True
    # Determines if week numbers are shown in the date selector.
    _showISOWeekNumbers = False
    _currentParseErrorMessage = None
    _defaultParseErrorMessage = 'Date format not recognized'
    # Constructors

    def __init__(self, *args):
        """Constructs an empty <code>DateField</code> with no caption.
        ---
        Constructs an empty <code>DateField</code> with caption.

        @param caption
                   the caption of the datefield.
        ---
        Constructs a new <code>DateField</code> that's bound to the specified
        <code>Property</code> and has the given caption <code>String</code>.

        @param caption
                   the caption <code>String</code> for the editor.
        @param dataSource
                   the Property to be edited with this editor.
        ---
        Constructs a new <code>DateField</code> that's bound to the specified
        <code>Property</code> and has no caption.

        @param dataSource
                   the Property to be edited with this editor.
        ---
        Constructs a new <code>DateField</code> with the given caption and
        initial text contents. The editor constructed this way will not be bound
        to a Property unless
        {@link com.vaadin.data.Property.Viewer#setPropertyDataSource(Property)}
        is called to bind it.

        @param caption
                   the caption <code>String</code> for the editor.
        @param value
                   the Date value.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 1:
            if isinstance(_0[0], Property):
                dataSource, = _0
                if not Date.isAssignableFrom(dataSource.getType()):
                    raise self.IllegalArgumentException('Can\'t use ' + dataSource.getType().getName() + ' typed property as datasource')
                self.setPropertyDataSource(dataSource)
            else:
                caption, = _0
                self.setCaption(caption)
        elif _1 == 2:
            if isinstance(_0[1], Date):
                caption, value = _0
                self.setValue(value)
                self.setCaption(caption)
            else:
                caption, dataSource = _0
                self.__init__(dataSource)
                self.setCaption(caption)
        else:
            raise ARGERROR(0, 2)

    # Component basic features
    # Paints this component. Don't add a JavaDoc comment here, we use the
    # default documentation from implemented interface.

    def paintContent(self, target):
        # Invoked when a variable of the component changes. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        super(DateField, self).paintContent(target)
        # Adds the locale as attribute
        l = self.getLocale()
        if l is not None:
            target.addAttribute('locale', str(l))
        if self.getDateFormat() is not None:
            target.addAttribute('format', self._dateFormat)
        if not self.isLenient():
            target.addAttribute('strict', True)
        target.addAttribute(VDateField.WEEK_NUMBERS, self.isShowISOWeekNumbers())
        target.addAttribute('parsable', self._uiHasValidDateString)
        # TODO communicate back the invalid date string? E.g. returning back to
        # app or refresh.

        # Gets the calendar
        calendar = self.getCalendar()
        currentDate = self.getValue()
        _0 = True
        r = self._resolution
        while True:
            if _0 is True:
                _0 = False
            else:
                r += 1
            if not (r <= self._largestModifiable):
                break
            _1 = r
            _2 = False
            while True:
                if _1 == self.RESOLUTION_MSEC:
                    _2 = True
                    target.addVariable(self, 'msec', calendar.get(Calendar.MILLISECOND) if currentDate is not None else -1)
                    break
                if (_2 is True) or (_1 == self.RESOLUTION_SEC):
                    _2 = True
                    target.addVariable(self, 'sec', calendar.get(Calendar.SECOND) if currentDate is not None else -1)
                    break
                if (_2 is True) or (_1 == self.RESOLUTION_MIN):
                    _2 = True
                    target.addVariable(self, 'min', calendar.get(Calendar.MINUTE) if currentDate is not None else -1)
                    break
                if (_2 is True) or (_1 == self.RESOLUTION_HOUR):
                    _2 = True
                    target.addVariable(self, 'hour', calendar.get(Calendar.HOUR_OF_DAY) if currentDate is not None else -1)
                    break
                if (_2 is True) or (_1 == self.RESOLUTION_DAY):
                    _2 = True
                    target.addVariable(self, 'day', calendar.get(Calendar.DAY_OF_MONTH) if currentDate is not None else -1)
                    break
                if (_2 is True) or (_1 == self.RESOLUTION_MONTH):
                    _2 = True
                    target.addVariable(self, 'month', calendar.get(Calendar.MONTH) + 1 if currentDate is not None else -1)
                    break
                if (_2 is True) or (_1 == self.RESOLUTION_YEAR):
                    _2 = True
                    target.addVariable(self, 'year', calendar.get(Calendar.YEAR) if currentDate is not None else -1)
                    break
                break

    def changeVariables(self, source, variables):
        super(DateField, self).changeVariables(source, variables)
        if (
            not self.isReadOnly() and ((((((('year' in variables) or ('month' in variables)) or ('day' in variables)) or ('hour' in variables)) or ('min' in variables)) or ('sec' in variables)) or ('msec' in variables)) or ('dateString' in variables)
        ):
            # Old and new dates
            oldDate = self.getValue()
            newDate = None
            # this enables analyzing invalid input on the server
            newDateString = variables['dateString']
            self._dateString = newDateString
            # Gets the new date in parts
            # Null values are converted to negative values.
            year = -1 if variables['year'] is None else variables['year'].intValue() if 'year' in variables else -1
            month = -1 if variables['month'] is None else variables['month'].intValue() - 1 if 'month' in variables else -1
            day = -1 if variables['day'] is None else variables['day'].intValue() if 'day' in variables else -1
            hour = -1 if variables['hour'] is None else variables['hour'].intValue() if 'hour' in variables else -1
            min = -1 if variables['min'] is None else variables['min'].intValue() if 'min' in variables else -1
            sec = -1 if variables['sec'] is None else variables['sec'].intValue() if 'sec' in variables else -1
            msec = -1 if variables['msec'] is None else variables['msec'].intValue() if 'msec' in variables else -1
            # If all of the components is < 0 use the previous value
            if (
                year < 0 and month < 0 and day < 0 and hour < 0 and min < 0 and sec < 0 and msec < 0
            ):
                newDate = None
            else:
                # Clone the calendar for date operation
                cal = self.getCalendar()
                # Make sure that meaningful values exists
                # Use the previous value if some of the variables
                # have not been changed.
                year = cal.get(Calendar.YEAR) if year < 0 else year
                month = cal.get(Calendar.MONTH) if month < 0 else month
                day = cal.get(Calendar.DAY_OF_MONTH) if day < 0 else day
                hour = cal.get(Calendar.HOUR_OF_DAY) if hour < 0 else hour
                min = cal.get(Calendar.MINUTE) if min < 0 else min
                sec = cal.get(Calendar.SECOND) if sec < 0 else sec
                msec = cal.get(Calendar.MILLISECOND) if msec < 0 else msec
                # Sets the calendar fields
                cal.set(Calendar.YEAR, year)
                cal.set(Calendar.MONTH, month)
                cal.set(Calendar.DAY_OF_MONTH, day)
                cal.set(Calendar.HOUR_OF_DAY, hour)
                cal.set(Calendar.MINUTE, min)
                cal.set(Calendar.SECOND, sec)
                cal.set(Calendar.MILLISECOND, msec)
                # Assigns the date
                newDate = cal.getTime()
            if (
                newDate is None and self._dateString is not None and not ('' == self._dateString)
            ):
                # Datefield now contains some text that could't be parsed
                # into date.

                try:
                    parsedDate = self.handleUnparsableDateString(self._dateString)
                    self.setValue(parsedDate, True)
                    # Ensure the value is sent to the client if the value is
                    # set to the same as the previous (#4304). Does not repaint
                    # if handleUnparsableDateString throws an exception. In
                    # this case the invalid text remains in the DateField.

                    self.requestRepaint()
                except ConversionException, e:
                    if oldDate is not None:
                        # Set the logic value to null.
                        self.setValue(None)
                        # Reset the dateString (overridden to null by setValue)
                        self._dateString = newDateString
                    # Saves the localized message of parse error. This can be
                    # overridden in handleUnparsableDateString. The message
                    # will later be used to show a validation error.

                    self._currentParseErrorMessage = e.getLocalizedMessage()
                    # The value of the DateField should be null if an invalid
                    # value has been given. Not using setValue() since we do
                    # not want to cause the client side value to change.

                    self._uiHasValidDateString = False
                    # Because of our custom implementation of isValid(), that
                    # also checks the parsingSucceeded flag, we must also
                    # notify the form (if this is used in one) that the
                    # validity of this field has changed.
                    # 
                    # Normally fields validity doesn't change without value
                    # change and form depends on this implementation detail.

                    self.notifyFormOfValidityChange()
                    self.requestRepaint()
            elif newDate != oldDate and (newDate is None) or (not (newDate == oldDate)):
                self.setValue(newDate, True)
                # Don't require a repaint, client
                # updates itself
            elif not self._uiHasValidDateString:
                # oldDate ==
                # newDate == null
                # Empty value set, previously contained unparsable date string,
                # clear related internal fields
                self.setValue(None)
        if FocusEvent.EVENT_ID in variables:
            self.fireEvent(FocusEvent(self))
        if BlurEvent.EVENT_ID in variables:
            self.fireEvent(BlurEvent(self))

    def handleUnparsableDateString(self, dateString):
        """This method is called to handle a non-empty date string from the client
        if the client could not parse it as a Date.

        By default, a Property.ConversionException is thrown, and the current
        value is not modified.

        This can be overridden to handle conversions, to return null (equivalent
        to empty input), to throw an exception or to fire an event.

        @param dateString
        @return parsed Date
        @throws Property.ConversionException
                    to keep the old value and indicate an error
        """
        # Property features
        # Gets the edited property's type. Don't add a JavaDoc comment here, we use
        # the default documentation from implemented interface.

        self._currentParseErrorMessage = None
        raise Property.ConversionException(self.getParseErrorMessage())

    def getType(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.AbstractField#setValue(java.lang.Object, boolean)

        return Date

    def setValue(self, newValue, repaintIsNotNeeded):
        # First handle special case when the client side component have a date
        # string but value is null (e.g. unparsable date string typed in by the
        # user). No value changes should happen, but we need to do some
        # internal housekeeping.

        if newValue is None and not self._uiHasValidDateString:
            # Side-effects of setInternalValue clears possible previous strings
            # and flags about invalid input.

            self.setInternalValue(None)
            # Due to DateField's special implementation of isValid(),
            # datefields validity may change although the logical value does
            # not change. This is an issue for Form which expects that validity
            # of Fields cannot change unless actual value changes.
            # 
            # So we check if this field is inside a form and the form has
            # registered this as a field. In this case we repaint the form.
            # Without this hacky solution the form might not be able to clean
            # validation errors etc. We could avoid this by firing an extra
            # value change event, but feels like at least as bad solution as
            # this.

            self.notifyFormOfValidityChange()
            self.requestRepaint()
            return
        if (newValue is None) or isinstance(newValue, Date):
            super(DateField, self).setValue(newValue, repaintIsNotNeeded)
        else:
            # Try to parse the given string value to Date
            try:
                parser = SimpleDateFormat()
                val = parser.parse(str(newValue))
                super(DateField, self).setValue(val, repaintIsNotNeeded)
            except ParseException, e:
                self._uiHasValidDateString = False
                raise Property.ConversionException(self.getParseErrorMessage())

    def notifyFormOfValidityChange(self):
        """Detects if this field is used in a Form (logically) and if so, notifies
        it (by repainting it) that the validity of this field might have changed.
        """
        parenOfDateField = self.getParent()
        formFound = False
        while (parenOfDateField is not None) or formFound:
            if isinstance(parenOfDateField, Form):
                f = parenOfDateField
                visibleItemProperties = f.getItemPropertyIds()
                for fieldId in visibleItemProperties:
                    field = fieldId
                    if field == self:
                        # this datefield is logically in a form. Do the same
                        # thing as form does in its value change listener that
                        # it registers to all fields.

                        f.requestRepaint()
                        formFound = True
                        break
            if formFound:
                break
            parenOfDateField = parenOfDateField.getParent()

    def setPropertyDataSource(self, newDataSource):
        """Sets the DateField datasource. Datasource type must assignable to Date.

        @see com.vaadin.data.Property.Viewer#setPropertyDataSource(Property)
        """
        if (newDataSource is None) or Date.isAssignableFrom(newDataSource.getType()):
            super(DateField, self).setPropertyDataSource(newDataSource)
        else:
            raise self.IllegalArgumentException('DateField only supports Date properties')

    def setInternalValue(self, newValue):
        # Also set the internal dateString
        if newValue is not None:
            self._dateString = str(newValue)
        else:
            self._dateString = None
        if not self._uiHasValidDateString:
            # clear component error and parsing flag
            self.setComponentError(None)
            self._uiHasValidDateString = True
            self._currentParseErrorMessage = None
        super(DateField, self).setInternalValue(newValue)

    def getResolution(self):
        """Gets the resolution.

        @return int
        """
        return self._resolution

    def setResolution(self, resolution):
        """Sets the resolution of the DateField.

        @param resolution
                   the resolution to set.
        """
        self._resolution = resolution
        self.requestRepaint()

    def getCalendar(self):
        """Returns new instance calendar used in Date conversions.

        Returns new clone of the calendar object initialized using the the
        current date (if available)

        If this is no calendar is assigned the <code>Calendar.getInstance</code>
        is used.

        @return the Calendar.
        @see #setCalendar(Calendar)
        """
        # Makes sure we have an calendar instance
        if self._calendar is None:
            self._calendar = Calendar.getInstance()
        # Clone the instance
        newCal = self._calendar.clone()
        # Assigns the current time tom calendar.
        currentDate = self.getValue()
        if currentDate is not None:
            newCal.setTime(currentDate)
        return newCal

    def setDateFormat(self, dateFormat):
        """Sets formatting used by some component implementations. See
        {@link SimpleDateFormat} for format details.

        By default it is encouraged to used default formatting defined by Locale,
        but due some JVM bugs it is sometimes necessary to use this method to
        override formatting. See Vaadin issue #2200.

        @param dateFormat
                   the dateFormat to set

        @see com.vaadin.ui.AbstractComponent#setLocale(Locale))
        """
        self._dateFormat = dateFormat
        self.requestRepaint()

    def getDateFormat(self):
        """Returns a format string used to format date value on client side or null
        if default formatting from {@link Component#getLocale()} is used.

        @return the dateFormat
        """
        return self._dateFormat

    def setLenient(self, lenient):
        """Specifies whether or not date/time interpretation in component is to be
        lenient.

        @see Calendar#setLenient(boolean)
        @see #isLenient()

        @param lenient
                   true if the lenient mode is to be turned on; false if it is to
                   be turned off.
        """
        self._lenient = lenient
        self.requestRepaint()

    def isLenient(self):
        """Returns whether date/time interpretation is to be lenient.

        @see #setLenient(boolean)

        @return true if the interpretation mode of this calendar is lenient;
                false otherwise.
        """
        return self._lenient

    def addListener(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BlurListener):
                listener, = _0
                self.addListener(BlurEvent.EVENT_ID, BlurEvent, listener, BlurListener.blurMethod)
            else:
                listener, = _0
                self.addListener(FocusEvent.EVENT_ID, FocusEvent, listener, FocusListener.focusMethod)
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BlurListener):
                listener, = _0
                self.removeListener(BlurEvent.EVENT_ID, BlurEvent, listener)
            else:
                listener, = _0
                self.removeListener(FocusEvent.EVENT_ID, FocusEvent, listener)
        else:
            raise ARGERROR(1, 1)

    def isShowISOWeekNumbers(self):
        """Checks whether ISO 8601 week numbers are shown in the date selector.

        @return true if week numbers are shown, false otherwise.
        """
        return self._showISOWeekNumbers

    def setShowISOWeekNumbers(self, showWeekNumbers):
        """Sets the visibility of ISO 8601 week numbers in the date selector. ISO
        8601 defines that a week always starts with a Monday so the week numbers
        are only shown if this is the case.

        @param showWeekNumbers
                   true if week numbers should be shown, false otherwise.
        """
        self._showISOWeekNumbers = showWeekNumbers
        self.requestRepaint()

    def isValid(self):
        """Tests the current value against registered validators if the field is not
        empty. Note that DateField is considered empty (value == null) and
        invalid if it contains text typed in by the user that couldn't be parsed
        into a Date value.

        @see com.vaadin.ui.AbstractField#isValid()
        """
        return self._uiHasValidDateString and super(DateField, self).isValid()

    def validate(self):
        # To work properly in form we must throw exception if there is
        # currently a parsing error in the datefield. Parsing error is kind of
        # an internal validator.

        if not self._uiHasValidDateString:
            raise self.UnparsableDateString(self._currentParseErrorMessage)
        super(DateField, self).validate()

    def getParseErrorMessage(self):
        """Return the error message that is shown if the user inputted value can't
        be parsed into a Date object. If
        {@link #handleUnparsableDateString(String)} is overridden and it throws a
        custom exception, the message returned by
        {@link Exception#getLocalizedMessage()} will be used instead of the value
        returned by this method.

        @see #setParseErrorMessage(String)

        @return the error message that the DateField uses when it can't parse the
                textual input from user to a Date object
        """
        return self._defaultParseErrorMessage

    def setParseErrorMessage(self, parsingErrorMessage):
        """Sets the default error message used if the DateField cannot parse the
        text input by user to a Date field. Note that if the
        {@link #handleUnparsableDateString(String)} method is overridden, the
        localized message from its exception is used.

        @see #getParseErrorMessage()
        @see #handleUnparsableDateString(String)
        @param parsingErrorMessage
        """
        self._defaultParseErrorMessage = parsingErrorMessage

    class UnparsableDateString(Validator.InvalidValueException):

        def __init__(self, message):
            super(UnparsableDateString, self)(message)
