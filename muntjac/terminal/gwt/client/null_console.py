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

import pygwt as GWT

from muntjac.terminal.gwt.client.console import IConsole


class NullConsole(IConsole):
    """Client side console implementation for non-debug mode that discards
    all messages.
    """

    def dirUIDL(self, u, cnf):
        pass


    def error(self, e_or_msg):
        if isinstance(e_or_msg, BaseException):
            e = e_or_msg
            GWT.log(e.getMessage(), e)
        else:
            msg = e_or_msg
            GWT.log(msg)


    def log(self, e_or_msg):
        if isinstance(e_or_msg, BaseException):
            e = e_or_msg
            GWT.log(e.getMessage(), e)
        else:
            msg = e_or_msg
            GWT.log(msg)


    def printObject(self, msg):
        GWT.log(str(msg))


    def printLayoutProblems(self, meta, applicationConnection,
            zeroHeightComponents, zeroWidthComponents):
        pass
