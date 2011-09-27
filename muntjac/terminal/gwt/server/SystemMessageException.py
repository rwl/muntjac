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


class SystemMessageException(RuntimeError):

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
        nargs = len(args)
        if nargs == 1:
            if isinstance(args[0], Exception):
                self._cause = args[0]
            else:
                msg = args[0]
                super(SystemMessageException, self)(msg)
        elif nargs == 2:
            msg, cause = args
            super(SystemMessageException, self)(msg)
            self._cause = cause
        else:
            raise ValueError, 'too many arguments'


    def getCause(self):
        return self._cause
