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
from com.vaadin.terminal.ErrorMessage import (ErrorMessage,)
# from java.io.Serializable import (Serializable,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.Iterator import (Iterator,)
# from java.util.List import (List,)


class CompositeErrorMessage(ErrorMessage, Serializable):
    """Class for combining multiple error messages together.

    @author IT Mill Ltd
    @version
    @VERSION@
    @since 3.0
    """
    # Array of all the errors.
    _errors = None
    # Level of the error.
    _level = None

    def __init__(self, *args):
        """Constructor for CompositeErrorMessage.

        @param errorMessages
                   the Array of error messages that are listed togeter. Nulls are
                   ignored, but at least one message is required.
        ---
        Constructor for CompositeErrorMessage.

        @param errorMessages
                   the Collection of error messages that are listed together. At
                   least one message is required.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Collection):
                errorMessages, = _0
                self._errors = list(len(errorMessages))
                self._level = Integer.MIN_VALUE.MIN_VALUE
                _0 = True
                i = errorMessages
                while True:
                    if _0 is True:
                        _0 = False
                    if not i.hasNext():
                        break
                    self.addErrorMessage(i.next())
                if len(self._errors) == 0:
                    raise self.IllegalArgumentException('Composite error message must have at least one error')
            else:
                errorMessages, = _0
                self._errors = list(len(errorMessages))
                self._level = Integer.MIN_VALUE.MIN_VALUE
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(errorMessages)):
                        break
                    self.addErrorMessage(errorMessages[i])
                if len(self._errors) == 0:
                    raise self.IllegalArgumentException('Composite error message must have at least one error')
        else:
            raise ARGERROR(1, 1)

    def getErrorLevel(self):
        """The error level is the largest error level in

        @see com.vaadin.terminal.ErrorMessage#getErrorLevel()
        """
        return self._level

    def addErrorMessage(self, error):
        """Adds a error message into this composite message. Updates the level
        field.

        @param error
                   the error message to be added. Duplicate errors are ignored.
        """
        if error is not None and not self._errors.contains(error):
            self._errors.add(error)
            l = error.getErrorLevel()
            if l > self._level:
                self._level = l

    def iterator(self):
        """Gets Error Iterator.

        @return the error iterator.
        """
        return self._errors

    def paint(self, target):
        """@see com.vaadin.terminal.Paintable#paint(com.vaadin.terminal.PaintTarget)"""
        # Documented in super interface
        if len(self._errors) == 1:
            self._errors.next().paint(target)
        else:
            target.startTag('error')
            if self._level > 0 and self._level <= ErrorMessage.INFORMATION:
                target.addAttribute('level', 'info')
            elif self._level <= ErrorMessage.WARNING:
                target.addAttribute('level', 'warning')
            elif self._level <= ErrorMessage.ERROR:
                target.addAttribute('level', 'error')
            elif self._level <= ErrorMessage.CRITICAL:
                target.addAttribute('level', 'critical')
            else:
                target.addAttribute('level', 'system')
            # Paint all the exceptions
            _0 = True
            i = self._errors
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                i.next().paint(target)
            target.endTag('error')

    def addListener(self, listener):
        # Documented in super interface
        pass

    def removeListener(self, listener):
        # Documented in super interface
        pass

    def requestRepaint(self):
        # Documented in super interface
        pass

    def requestRepaintRequests(self):
        pass

    def toString(self):
        """Returns a comma separated list of the error messages.

        @return String, comma separated list of error messages.
        """
        retval = '['
        pos = 0
        _0 = True
        i = self._errors
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            if pos > 0:
                retval += ','
            pos += 1
            retval += str(i.next())
        retval += ']'
        return retval

    def getDebugId(self):
        return None

    def setDebugId(self, id):
        raise self.UnsupportedOperationException('Setting testing id for this Paintable is not implemented')
