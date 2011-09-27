# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.data.util.AbstractProperty import AbstractProperty
from muntjac.data.Property import \
    ConversionException, Property, ReadOnlyStatusChangeListener, \
    ValueChangeListener, ValueChangeNotifier


class PropertyFormatter(AbstractProperty, Property, ValueChangeListener,
                        Property, ReadOnlyStatusChangeListener):
    """Formatting proxy for a {@link Property}.

    <p>
    This class can be used to implement formatting for any type of Property
    datasources. The idea is to connect this as proxy between UI component and
    the original datasource.
    </p>

    <p>
    For example <code>
    <pre>textfield.setPropertyDataSource(new PropertyFormatter(property) {
                public String format(Object value) {
                    return ((Double) value).toString() + "000000000";
                }

                public Object parse(String formattedValue) throws Exception {
                    return Double.parseDouble(formattedValue);
                }

            });</pre></code> adds formatter for Double-typed property that extends
    standard "1.0" notation with more zeroes.
    </p>

    @author IT Mill Ltd.
    @since 5.3.0
    """

    def __init__(self, *args):
        """Construct a new {@code PropertyFormatter} that is not connected to any
        data source. Call {@link #setPropertyDataSource(Property)} later on to
        attach it to a property.
        ---
        Construct a new formatter that is connected to given data source. Calls
        {@link #format(Object)} which can be a problem if the formatter has not
        yet been initialized.

        @param propertyDataSource
                   to connect this property to.
        """
        # Datasource that stores the actual value.
        self._dataSource = None

        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 1:
            propertyDataSource, = _0
            self.setPropertyDataSource(propertyDataSource)
        else:
            raise ValueError


    def getPropertyDataSource(self):
        """Gets the current data source of the formatter, if any.

        @return the current data source as a Property, or <code>null</code> if
                none defined.
        """
        return self._dataSource


    def setPropertyDataSource(self, newDataSource):
        """Sets the specified Property as the data source for the formatter.


        <p>
        Remember that new data sources getValue() must return objects that are
        compatible with parse() and format() methods.
        </p>

        @param newDataSource
                   the new data source Property.
        """
        readOnly = False
        prevValue = None
        if self._dataSource is not None:
            if isinstance(self._dataSource, ValueChangeNotifier):
                self._dataSource.removeListener(self)
            if isinstance(self._dataSource, ReadOnlyStatusChangeListener):
                self._dataSource.removeListener(self)
            readOnly = self.isReadOnly()
            prevValue = str(self)
        self._dataSource = newDataSource
        if self._dataSource is not None:
            if isinstance(self._dataSource, ValueChangeNotifier):
                self._dataSource.addListener(self)
            if isinstance(self._dataSource, ReadOnlyStatusChangeListener):
                self._dataSource.addListener(self)
        if self.isReadOnly() != readOnly:
            self.fireReadOnlyStatusChange()
        newVal = str(self)
        if (
            (prevValue is None and newVal is not None) or (prevValue is not None and not (prevValue == newVal))
        ):
            self.fireValueChange()


    def getType(self):
        return str


    def getValue(self):
        """Get the formatted value.

        @return If the datasource returns null, this is null. Otherwise this is
                String given by format().
        """
        return str(self)


    def toString(self):
        """Get the formatted value.

        @return If the datasource returns null, this is null. Otherwise this is
                String given by format().
        """
        value = False if self._dataSource is None else self._dataSource.getValue()
        if value is None:
            return None
        return self.format(value)


    def isReadOnly(self):
        """Reflects the read-only status of the datasource."""
        return False if self._dataSource is None else self._dataSource.isReadOnly()


    def format(self, value):  #@PydevCodeAnalysisIgnore
        """This method must be implemented to format the values received from
        DataSource.

        @param value
                   Value object got from the datasource. This is guaranteed to be
                   non-null and of the type compatible with getType() of the
                   datasource.
        @return
        """
        pass


    def parse(self, formattedValue):
        """Parse string and convert it to format compatible with datasource.

        The method is required to assure that parse(format(x)) equals x.

        @param formattedValue
                   This is guaranteed to be non-null string.
        @return Non-null value compatible with datasource.
        @throws Exception
                    Any type of exception can be thrown to indicate that the
                    conversion was not succesful.
        """
        pass


    def setReadOnly(self, newStatus):
        """Sets the Property's read-only mode to the specified status.

        @param newStatus
                   the new read-only status of the Property.
        """
        if self._dataSource is not None:
            self._dataSource.setReadOnly(newStatus)


    def setValue(self, newValue):
        if self._dataSource is None:
            return
        if newValue is None:
            if self._dataSource.getValue() is not None:
                self._dataSource.setValue(None)
                self.fireValueChange()
        else:
            try:
                self._dataSource.setValue(self.parse(newValue))
                if not (newValue == str(self)):
                    self.fireValueChange()
            except Exception, e:
                if isinstance(e, ConversionException):
                    raise e
                else:
                    raise ConversionException(e)


    def valueChange(self, event):
        """Listens for changes in the datasource.

        This should not be called directly.
        """
        self.fireValueChange()


    def readOnlyStatusChange(self, event):
        """Listens for changes in the datasource.

        This should not be called directly.
        """
        self.fireReadOnlyStatusChange()
