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

"""Criterion that accepts all drops anywhere on the component."""

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class AcceptAll(ClientSideCriterion):
    """Criterion that accepts all drops anywhere on the component.

    Note! Class is singleton, use L{get} method to get the instance.
    """

    _singleton = None

    def __init__(self):
        pass

    @classmethod
    def get(cls):
        return cls._singleton


    def accept(self, dragEvent):
        return True


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.AcceptAll'

AcceptAll._singleton = AcceptAll()
