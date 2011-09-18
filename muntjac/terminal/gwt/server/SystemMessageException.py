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


class SystemMessageException(RuntimeError):
    # Cause of the method exception
    _cause = None

    def __init__(self, *args):
        """Constructs a new <code>SystemMessageException</code> with the specified
        detail message.

        @param msg
                   the detail message.
        ---
        Constructs a new <code>SystemMessageException</code> with the specified
        detail message and cause.

        @param msg
                   the detail message.
        @param cause
                   the cause of the exception.
        ---
        Constructs a new <code>SystemMessageException</code> from another
        exception.

        @param cause
                   the cause of the exception.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Throwable):
                cause, = _0
                self._cause = cause
            else:
                msg, = _0
                super(SystemMessageException, self)(msg)
        elif _1 == 2:
            msg, cause = _0
            super(SystemMessageException, self)(msg, cause)
        else:
            raise ARGERROR(1, 2)

    def getCause(self):
        """@see java.lang.Throwable#getCause()"""
        return self._cause
