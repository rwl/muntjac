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


class InfoWindowTab(object):

    def __init__(self, parent, content, label=None, selected=False):
        self._content = content
        self._content.setParent(parent)
        self._label = label
        self._selected = selected

    def getContent(self):
        return self._content

    def getLabel(self):
        return self._label

    def setLabel(self, label):
        self._label = label

    def isSelected(self):
        return self._selected

    def setSelected(self, selected):
        self._selected = selected
