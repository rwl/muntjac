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

import locale

from time import mktime
from datetime import datetime

from muntjac.event.FieldEvents import BlurEvent, BlurListener, BlurNotifier, \
    FieldEvents, FocusEvent, FocusListener, FocusNotifier

from muntjac.ui.AbstractField import AbstractField
from muntjac.data.Property import Property, ConversionException
from muntjac.terminal.gwt.client.ui.VDateField import VDateField
from muntjac.terminal.gwt.client.ui.VPopupCalendar import VPopupCalendar
from muntjac.ui.ClientWidget import LoadStyle
from muntjac.ui.Form import Form
from muntjac.data.Validator import InvalidValueException


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

    CLIENT_WIDGET = VPopupCalendar
    LOAD_STYLE = LoadStyle.EAGER

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

    # Specified largest modifiable unit.
    _largestModifiable = RESOLUTION_YEAR


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
        # The internal calendar to be used in java.utl.Date conversions.
        self._calendar = None

        # Overridden format string
        self._dateFormat = None

        self._lenient = False

        self._dateString = None

        # Was the last entered string parsable? If this flag is false, datefields
        # internal validator does not pass.
        self._uiHasValidDateString = True

        # Determines if week numbers are shown in the date selector.
        self._showISOWeekNumbers = False

        self._currentParseErrorMessage = None

        self._defaultParseErrorMessage = 'Date format not recognized'

        # Specified smallest modifiable unit.
        self._resolution = self.RESOLUTION_MSEC

        args = args
        nargs = len(args)
        if nargs == 0:
            pass
        elif nargs == 1:
            if isinstance(args[0], Property):
                dataSource, = args
                if not issubclass(dataSource.getType(), datetime):
                    raise ValueError, 'Can\'t use ' \
                            + dataSource.getType().__name__ \
                            + ' typed property as datasource'
                self.setPropertyDataSource(dataSource)
            else:
                caption, = args
                self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], datetime):
                caption, value = args
                self.setValue(value)
                self.setCaption(caption)
            else:
                caption, dataSource = args
                self.__init__(dataSource)
                self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'


    # Component basic features

    def paintContent(self, target):
        # Paints this component. Don't add a JavaDoc comment here, we use the
        # default documentation from implemented interface.

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

        r = self._resolution
        while r <= self._largestModifiable:

            if r == self.RESOLUTION_MSEC:
                target.addVariable(self, 'msec', calendar.microsecond / 1e03 if currentDate is not None else -1)

            elif r == self.RESOLUTION_SEC:
                target.addVariable(self, 'sec', calendar.second if currentDate is not None else -1)

            elif r == self.RESOLUTION_MIN:
                target.addVariable(self, 'min', calendar.minute if currentDate is not None else -1)

            elif r == self.RESOLUTION_HOUR:
                target.addVariable(self, 'hour', calendar.hour if currentDate is not None else -1)

            elif r == self.RESOLUTION_DAY:
                target.addVariable(self, 'day', calendar.day if currentDate is not None else -1)

            elif r == self.RESOLUTION_MONTH:
                target.addVariable(self, 'month', calendar.month + 1 if currentDate is not None else -1)

            elif r == self.RESOLUTION_YEAR:
                target.addVariable(self, 'year', calendar.year if currentDate is not None else -1)

            r += 1


    def changeVariables(self, source, variables):
        # Invoked when a variable of the component changes. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        super(DateField, self).changeVariables(source, variables)
        if not self.isReadOnly() \
                and (('year' in variables) \
                    or ('month' in variables) \
                    or ('day' in variables) \
                    or ('hour' in variables) \
                    or ('min' in variables) \
                    or ('sec' in variables) \
                    or ('msec' in variables) \
                    or ('dateString' in variables)):

            # Old and new dates
            oldDate = self.getValue()
            newDate = None

            # this enables analyzing invalid input on the server
            newDateString = variables.get('dateString')
            self._dateString = newDateString

            # Gets the new date in parts
            # Null values are converted to negative values.
            year  = -1 if variables.get('year')  is None else int(variables.get('year'))      if 'year'  in variables else -1
            month = -1 if variables.get('month') is None else int(variables.get('month')) - 1 if 'month' in variables else -1
            day   = -1 if variables.get('day')   is None else int(variables.get('day'))       if 'day'   in variables else -1
            hour  = -1 if variables.get('hour')  is None else int(variables.get('hour'))      if 'hour'  in variables else -1
            minn  = -1 if variables.get('min')   is None else int(variables.get('min'))       if 'min'   in variables else -1
            sec   = -1 if variables.get('sec')   is None else int(variables.get('sec'))       if 'sec'   in variables else -1
            msec  = -1 if variables.get('msec')  is None else int(variables.get('msec'))      if 'msec'  in variables else -1

            # If all of the components is < 0 use the previous value
            if year < 0 and month < 0 and day < 0 and hour < 0 and min < 0 \
                    and sec < 0 and msec < 0:
                newDate = None
            else:
                # Clone the calendar for date operation
                cal = self.getCalendar()

                # Make sure that meaningful values exists
                # Use the previous value if some of the variables
                # have not been changed.
                year = cal.year if year < 0 else year
                month = cal.month if month < 0 else month
                day = cal.day if day < 0 else day
                hour = cal.hour if hour < 0 else hour
                minn = cal.minute if minn < 0 else minn
                sec = cal.second if sec < 0 else sec
                msec = cal.microsecond / 1e03 if msec < 0 else msec

                # Sets the calendar fields
                cal = datetime(year, month, day, hour, minn, sec, msec * 1e03)

                # Assigns the date
                newDate = mktime(cal.timetuple())
                ## FIXME use: timestamp = (dt - datetime(1970, 1, 1, tzinfo=timezone.utc)) / timedelta(seconds=1)

            if newDate is None and self._dateString is not None \
                    and not ('' == self._dateString):
                try:
                    parsedDate = self.handleUnparsableDateString(self._dateString)
                    self.setValue(parsedDate, True)

                    # Ensure the value is sent to the client if the value is
                    # set to the same as the previous (#4304). Does not repaint
                    # if handleUnparsableDateString throws an exception. In
                    # this case the invalid text remains in the DateField.
                    self.requestRepaint()
                except ConversionException, e:

                    # Datefield now contains some text that could't be parsed
                    # into date.
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
            elif newDate != oldDate \
                    and (newDate is None or (not (newDate == oldDate))):
                self.setValue(newDate, True)  # Don't require a repaint, client
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
        self._currentParseErrorMessage = None
        raise ConversionException(self.getParseErrorMessage())


    def getType(self):
        # Gets the edited property's type.
        return datetime


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

        if (newValue is None) or isinstance(newValue, datetime):
            super(DateField, self).setValue(newValue, repaintIsNotNeeded)
        else:
            # Try to parse the given string value to Date
            try:
                val = datetime.strptime(str(newValue), locale.D_T_FMT)
                super(DateField, self).setValue(val, repaintIsNotNeeded)
            except ValueError:
                self._uiHasValidDateString = False
                raise ConversionException(self.getParseErrorMessage())


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
        if (newDataSource is None) or issubclass(newDataSource.getType(), datetime):
            super(DateField, self).setPropertyDataSource(newDataSource)
        else:
            raise ValueError, 'DateField only supports Date properties'


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
            self._calendar = datetime.now()
        # Clone the instance
        ## FIXME use: timestamp = (dt - datetime(1970, 1, 1)) / timedelta(seconds=1)
        newCal = datetime.fromtimestamp( mktime(self._calendar.timetuple()) )
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


    def addListener(self, listener):
        if isinstance(listener, BlurListener):
            self.addListener(BlurEvent.EVENT_ID, BlurEvent, listener,
                             BlurListener.blurMethod)
        else:
            self.addListener(FocusEvent.EVENT_ID, FocusEvent, listener,
                             FocusListener.focusMethod)


    def removeListener(self, listener):
        if isinstance(listener, BlurListener):
            self.removeListener(BlurEvent.EVENT_ID, BlurEvent, listener)
        else:
            self.removeListener(FocusEvent.EVENT_ID, FocusEvent, listener)


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


class UnparsableDateString(InvalidValueException):

    def __init__(self, message):
        super(UnparsableDateString, self)(message)
