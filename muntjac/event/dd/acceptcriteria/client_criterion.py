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


class ClientCriterion(object):
    """An annotation type used to point the client side counterpart for server
    side a L{AcceptCriterion} class. Usage is pretty similar to L{ClientWidget}
    which is used with Muntjac components that have a specialized client side
    counterpart.

    Annotations are used at GWT compilation phase, so remember to rebuild your
    widgetset if you do changes for L{ClientCriterion} mappings.
    """

    # the client side counterpart for the annotated criterion
    value = None
