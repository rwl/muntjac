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

"""Client side criteria that checks if the drag source is one of the given
components."""

from muntjac.event.transferable_impl import TransferableImpl

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class SourceIs(ClientSideCriterion):
    """Client side criteria that checks if the drag source is one of the given
    components.
    """

    def __init__(self, *component):
        self._component = component


    def paintContent(self, target):
        super(SourceIs, self).paintContent(target)
        target.addAttribute('c', len(self._component))
        for i, c in enumerate(self._component):
            target.addAttribute('component' + i, c)


    def accept(self, dragEvent):
        if isinstance(dragEvent.getTransferable(), TransferableImpl):
            sourceComponent = dragEvent.getTransferable().getSourceComponent()
            for c in self._component:
                if c == sourceComponent:
                    return True
        return False


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.SourceIs'
