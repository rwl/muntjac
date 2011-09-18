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

from com.vaadin.event.dd.acceptcriteria.AcceptCriterion import (AcceptCriterion,)
# from java.io.Serializable import (Serializable,)


class ClientSideCriterion(Serializable, AcceptCriterion):
    """Parent class for criteria that can be completely validated on client side.
    All classes that provide criteria that can be completely validated on client
    side should extend this class.

    It is recommended that subclasses of ClientSideCriterion re-validate the
    condition on the server side in
    {@link AcceptCriterion#accept(com.vaadin.event.dd.DragAndDropEvent)} after
    the client side validation has accepted a transfer.

    @since 6.3
    """
    # All criteria that extend this must be completely validatable on client
    # side.
    # 
    # (non-Javadoc)
    # 
    # @see
    # com.vaadin.event.dd.acceptCriteria.AcceptCriterion#isClientSideVerifiable
    # ()

    def isClientSideVerifiable(self):
        return True

    def paint(self, target):
        target.startTag('-ac')
        target.addAttribute('name', self.getIdentifier())
        self.paintContent(target)
        target.endTag('-ac')

    def paintContent(self, target):
        pass

    def getIdentifier(self):
        return self.getClass().getCanonicalName()

    def paintResponse(self, target):
        # NOP, nothing to do as this is client side verified criterion
        pass
