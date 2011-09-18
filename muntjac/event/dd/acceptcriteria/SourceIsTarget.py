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

from com.vaadin.event.dd.acceptcriteria.ClientSideCriterion import (ClientSideCriterion,)


class SourceIsTarget(ClientSideCriterion):
    """A criterion that ensures the drag source is the same as drop target. Eg.
    {@link Tree} or {@link Table} could support only re-ordering of items, but no
    {@link Transferable}s coming outside.
    <p>
    Note! Class is singleton, use {@link #get()} method to get the instance.

    @since 6.3
    """
    _serialVersionUID = -451399314705532584L
    _instance = SourceIsTarget()

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
