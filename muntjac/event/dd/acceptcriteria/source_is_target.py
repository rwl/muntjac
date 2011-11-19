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

"""A criterion that ensures the drag source is the same as drop target."""

from muntjac.event.transferable_impl import TransferableImpl

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class SourceIsTarget(ClientSideCriterion):
    """A criterion that ensures the drag source is the same as drop target.
    Eg. L{Tree} or L{Table} could support only re-ordering of items,
    but no L{Transferable}s coming outside.

    Note! Class is singleton, use L{get} method to get the instance.
    """

    _instance = None

    def __init__(self):
        pass


    def accept(self, dragEvent):
        if isinstance(dragEvent.getTransferable(), TransferableImpl):
            sourceComponent = dragEvent.getTransferable().getSourceComponent()
            target = dragEvent.getTargetDetails().getTarget()
            return sourceComponent == target
        return False


    @classmethod
    def get(cls):
        return cls._instance


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.SourceIsTarget'


SourceIsTarget._instance = SourceIsTarget()
