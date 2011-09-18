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
from com.vaadin.data.util.ObjectProperty import (ObjectProperty,)
from com.vaadin.ui.AbstractField import (AbstractField,)
from com.vaadin.data.Property import (Property, ValueChangeListener, Viewer,)


class ProgressIndicator(AbstractField, Property, Property, Viewer, Property, ValueChangeListener):
    """<code>ProgressIndicator</code> is component that shows user state of a
    process (like long computing or file upload)

    <code>ProgressIndicator</code> has two mainmodes. One for indeterminate
    processes and other (default) for processes which progress can be measured

    May view an other property that indicates progress 0...1

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 4
    """
    # Content mode, where the label contains only plain text. The getValue()
    # result is coded to XML when painting.

    CONTENT_TEXT = 0
    # Content mode, where the label contains preformatted text.
    CONTENT_PREFORMATTED = 1
    _indeterminate = False
    _dataSource = None
    _pollingInterval = 1000

    def __init__(self, *args):
        """Creates an a new ProgressIndicator.
        ---
        Creates a new instance of ProgressIndicator with given state.

        @param value
        ---
        Creates a new instance of ProgressIndicator with stae read from given
        datasource.

        @param contentSource
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setPropertyDataSource(ObjectProperty(float(0), float))
        elif _1 == 1:
            if isinstance(_0[0], Property):
                contentSource, = _0
                self.setPropertyDataSource(contentSource)
            else:
                value, = _0
                self.setPropertyDataSource(ObjectProperty(value, float))
        else:
            raise ARGERROR(0, 1)

    def setReadOnly(self, readOnly):
        """Sets the component to read-only. Readonly is not used in
        ProgressIndicator.

        @param readOnly
                   True to enable read-only mode, False to disable it.
        """
        if self._dataSource is None:
            raise self.IllegalStateException('Datasource must be se')
        self._dataSource.setReadOnly(readOnly)

    def isReadOnly(self):
        """Is the component read-only ? Readonly is not used in ProgressIndicator -
        this returns allways false.

        @return True if the component is in read only mode.
        """
        if self._dataSource is None:
            raise self.IllegalStateException('Datasource must be se')
        return self._dataSource.isReadOnly()

    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   the Paint Event.
        @throws PaintException
                    if the Paint Operation fails.
        """
        target.addAttribute('indeterminate', self._indeterminate)
        target.addAttribute('pollinginterval', self._pollingInterval)
        target.addAttribute('state', str(self.getValue()))

    def getValue(self):
        """Gets the value of the ProgressIndicator. Value of the ProgressIndicator
        is Float between 0 and 1.

        @return the Value of the ProgressIndicator.
        @see com.vaadin.ui.AbstractField#getValue()
        """
        if self._dataSource is None:
            raise self.IllegalStateException('Datasource must be set')
        return self._dataSource.getValue()

    def setValue(self, newValue):
        """Sets the value of the ProgressIndicator. Value of the ProgressIndicator
        is the Float between 0 and 1.

        @param newValue
                   the New value of the ProgressIndicator.
        @see com.vaadin.ui.AbstractField#setValue(java.lang.Object)
        """
        if self._dataSource is None:
            raise self.IllegalStateException('Datasource must be set')
        self._dataSource.setValue(newValue)

    def toString(self):
        """@see com.vaadin.ui.AbstractField#toString()"""
        if self._dataSource is None:
            raise self.IllegalStateException('Datasource must be set')
        return str(self._dataSource)

    def getType(self):
        """@see com.vaadin.ui.AbstractField#getType()"""
        if self._dataSource is None:
            raise self.IllegalStateException('Datasource must be set')
        return self._dataSource.getType()

    def getPropertyDataSource(self):
        """Gets the viewing data-source property.

        @return the datasource.
        @see com.vaadin.ui.AbstractField#getPropertyDataSource()
        """
        return self._dataSource

    def setPropertyDataSource(self, newDataSource):
        """Sets the property as data-source for viewing.

        @param newDataSource
                   the new data source.
        @see com.vaadin.ui.AbstractField#setPropertyDataSource(com.vaadin.data.Property)
        """
        # Stops listening the old data source changes
        if (
            self._dataSource is not None and Property.ValueChangeNotifier.isAssignableFrom(self._dataSource.getClass())
        ):
            self._dataSource.removeListener(self)
        # Sets the new data source
        self._dataSource = newDataSource
        # Listens the new data source if possible
        if (
            self._dataSource is not None and Property.ValueChangeNotifier.isAssignableFrom(self._dataSource.getClass())
        ):
            self._dataSource.addListener(self)

    def getContentMode(self):
        """Gets the mode of ProgressIndicator.

        @return true if in indeterminate mode.
        """
        return self._indeterminate

    def setIndeterminate(self, newValue):
        """Sets wheter or not the ProgressIndicator is indeterminate.

        @param newValue
                   true to set to indeterminate mode.
        """
        self._indeterminate = newValue
        self.requestRepaint()

    def isIndeterminate(self):
        """Gets whether or not the ProgressIndicator is indeterminate.

        @return true to set to indeterminate mode.
        """
        return self._indeterminate

    def setPollingInterval(self, newValue):
        """Sets the interval that component checks for progress.

        @param newValue
                   the interval in milliseconds.
        """
        self._pollingInterval = newValue
        self.requestRepaint()

    def getPollingInterval(self):
        """Gets the interval that component checks for progress.

        @return the interval in milliseconds.
        """
        return self._pollingInterval
