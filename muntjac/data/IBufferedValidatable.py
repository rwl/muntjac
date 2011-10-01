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

from muntjac.data.IValidatable import IValidatable
from muntjac.data.IBuffered import IBuffered


class IBufferedValidatable(IBuffered, IValidatable):
    """This interface defines the combination of <code>IValidatable</code> and
    <code>IBuffered</code> interfaces. The combination of the interfaces defines
    if the invalid data is committed to datasource.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def isInvalidCommitted(self):
        """Tests if the invalid data is committed to datasource. The default is
        <code>false</code>.
        """
        raise NotImplementedError


    def setInvalidCommitted(self, isCommitted):
        """Sets if the invalid data should be committed to datasource. The
        default is <code>false</code>.
        """
        raise NotImplementedError
