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

# from com.google.gwt.user.client.Command import (Command,)


class Action(Command):
    owner = None
    iconUrl = None
    caption = ''

    def __init__(self, owner):
        self.owner = owner

    def execute(self):
        """Executed when action fired"""
        pass

    def getHTML(self):
        sb = str()
        sb.__add__('<div>')
        if self.getIconUrl() is not None:
            sb.__add__('<img src=\"' + self.getIconUrl() + '\" alt=\"icon\" />')
        sb.__add__(self.getCaption())
        sb.__add__('</div>')
        return str(sb)

    def getCaption(self):
        return self.caption

    def setCaption(self, caption):
        self.caption = caption

    def getIconUrl(self):
        return self.iconUrl

    def setIconUrl(self, url):
        self.iconUrl = url
