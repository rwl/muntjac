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

"""Bitmask values for client server communication"""


class Bits(object):
    """Bitmask values for client server communication"""

    ALIGNMENT_LEFT = 1
    ALIGNMENT_RIGHT = 2
    ALIGNMENT_TOP = 4
    ALIGNMENT_BOTTOM = 8
    ALIGNMENT_HORIZONTAL_CENTER = 16
    ALIGNMENT_VERTICAL_CENTER = 32
