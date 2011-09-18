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
# from java.io.IOException import (IOException,)
# from java.io.Serializable import (Serializable,)


class PaintException(IOException, Serializable):
    """<code>PaintExcepection</code> is thrown if painting of a component fails.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def __init__(self, *args):
        """Constructs an instance of <code>PaintExeception</code> with the specified
        detail message.

        @param msg
                   the detail message.
        ---
        Constructs an instance of <code>PaintExeception</code> from IOException.

        @param exception
                   the original exception.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], IOException):
                exception, = _0
                super(PaintException, self)(exception.getMessage())
            else:
                msg, = _0
                super(PaintException, self)(msg)
        else:
            raise ARGERROR(1, 1)
