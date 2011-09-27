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

import sys

from muntjac.terminal.SystemError import SystemErr
from muntjac.terminal.ErrorMessage import ErrorMessage


class Buffered(object):
    """<p>
    Defines the interface to commit and discard changes to an object, supporting
    read-through and write-through modes.
    </p>

    <p>
    <i>Read-through mode</i> means that the value read from the buffered object
    is constantly up to date with the data source. <i>Write-through</i> mode
    means that all changes to the object are immediately updated to the data
    source.
    </p>

    <p>
    Since these modes are independent, their combinations may result in some
    behaviour that may sound surprising.
    </p>

    <p>
    For example, if a <code>Buffered</code> object is in read-through mode but
    not in write-through mode, the result is an object whose value is updated
    directly from the data source only if it's not locally modified. If the value
    is locally modified, retrieving the value from the object would result in a
    value that is different than the one stored in the data source, even though
    the object is in read-through mode.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def commit(self):
        """Updates all changes since the previous commit to the data source. The
        value stored in the object will always be updated into the data source
        when <code>commit</code> is called.

        @throws SourceException
                    if the operation fails because of an exception is thrown by
                    the data source. The cause is included in the exception.
        @throws InvalidValueException
                    if the operation fails because validation is enabled and the
                    values do not validate
        """
        pass

    def discard(self):
        """Discards all changes since last commit. The object updates its value from
        the data source.

        @throws SourceException
                    if the operation fails because of an exception is thrown by
                    the data source. The cause is included in the exception.
        """
        pass

    def isWriteThrough(self):
        """Tests if the object is in write-through mode. If the object is in
        write-through mode, all modifications to it will result in
        <code>commit</code> being called after the modification.

        @return <code>true</code> if the object is in write-through mode,
                <code>false</code> if it's not.
        """
        pass

    def setWriteThrough(self, writeThrough):
        """Sets the object's write-through mode to the specified status. When
        switching the write-through mode on, the <code>commit</code> operation
        will be performed.

        @param writeThrough
                   Boolean value to indicate if the object should be in
                   write-through mode after the call.
        @throws SourceException
                    If the operation fails because of an exception is thrown by
                    the data source.
        @throws InvalidValueException
                    If the implicit commit operation fails because of a
                    validation error.
        """
        pass

    def isReadThrough(self):
        """Tests if the object is in read-through mode. If the object is in
        read-through mode, retrieving its value will result in the value being
        first updated from the data source to the object.
        <p>
        The only exception to this rule is that when the object is not in
        write-through mode and it's buffer contains a modified value, the value
        retrieved from the object will be the locally modified value in the
        buffer which may differ from the value in the data source.
        </p>

        @return <code>true</code> if the object is in read-through mode,
                <code>false</code> if it's not.
        """
        pass

    def setReadThrough(self, readThrough):
        """Sets the object's read-through mode to the specified status. When
        switching read-through mode on, the object's value is updated from the
        data source.

        @param readThrough
                   Boolean value to indicate if the object should be in
                   read-through mode after the call.

        @throws SourceException
                    If the operation fails because of an exception is thrown by
                    the data source. The cause is included in the exception.
        """
        pass

    def isModified(self):
        """Tests if the value stored in the object has been modified since it was
        last updated from the data source.

        @return <code>true</code> if the value in the object has been modified
                since the last data source update, <code>false</code> if not.
        """
        pass


class SourceException(RuntimeError, ErrorMessage):
    """An exception that signals that one or more exceptions occurred while a
    buffered object tried to access its data source or if there is a problem
    in processing a data source.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def __init__(self, source, cause=None):
        """Creates a source exception that does not include a cause.

        @param source
                   the source object implementing the Buffered interface.
        ---
        Creates a source exception from a cause exception.

        @param source
                   the source object implementing the Buffered interface.
        @param cause
                   the original cause for this exception.
        ---
        Creates a source exception from multiple causes.

        @param source
                   the source object implementing the Buffered interface.
        @param causes
                   the original causes for this exception.
        """
        # Source class implementing the buffered interface
        self._source = source

        # Original cause of the source exception
        self._causes = list()

        if isinstance(cause, list):
            self._causes = cause
        elif cause is not None:
            self._causes = [cause]


    def getCause(self):
        """Gets the cause of the exception.

        @return The cause for the exception.
        @throws MoreThanOneCauseException
                    if there is more than one cause for the exception. This
                    is possible if the commit operation triggers more than
                    one error at the same time.
        """
        if len(self._causes) == 0:
            return None
        return self._causes[0]


    def getCauses(self):
        """Gets all the causes for this exception.

        @return throwables that caused this exception
        """
        return self._causes


    def getSource(self):
        """Gets a source of the exception.

        @return the Buffered object which generated this exception.
        """
        return self._source


    def getErrorLevel(self):
        """Gets the error level of this buffered source exception. The level of
        the exception is maximum error level of all the contained causes.
        <p>
        The causes that do not specify error level default to
        <code>ERROR</code> level. Also source exception without any causes
        are of level <code>ERROR</code>.
        </p>

        @see com.vaadin.terminal.ErrorMessage#getErrorLevel()
        """
        level = -sys.maxint - 1

        for i in range(len(self._causes)):
            causeLevel = self._causes[i].getErrorLevel() if isinstance(self._causes[i], ErrorMessage) else ErrorMessage.ERROR
            if causeLevel > level:
                level = causeLevel
        return ErrorMessage.ERROR if level == -sys.maxint - 1 else level


    def paint(self, target):
        target.startTag('error')
        level = self.getErrorLevel()

        if level > 0 and level <= ErrorMessage.INFORMATION:
            target.addAttribute('level', 'info')

        elif level <= ErrorMessage.WARNING:
            target.addAttribute('level', 'warning')

        elif level <= ErrorMessage.ERROR:
            target.addAttribute('level', 'error')

        elif level <= ErrorMessage.CRITICAL:
            target.addAttribute('level', 'critical')

        else:
            target.addAttribute('level', 'system')

        # Paint all the exceptions
        for i in range(len(self._causes)):
            if isinstance(self._causes[i], ErrorMessage):
                self._causes[i].paint(target)
            else:
                SystemErr(self._causes[i]).paint(target)

        target.endTag('error')


    def addListener(self, listener):
        pass


    def removeListener(self, listener):
        pass


    def requestRepaint(self):
        pass


    def requestRepaintRequests(self):
        pass


    def getDebugId(self):
        return None


    def setDebugId(self, idd):
        raise NotImplementedError, 'Setting testing id for this Paintable is not implemented'
