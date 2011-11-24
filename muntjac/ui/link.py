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

"""Used to create external or internal URL links."""

from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.window import Window


class Link(AbstractComponent):
    """Link is used to create external or internal URL links.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.3
    """

    CLIENT_WIDGET = None #ClientWidget(VLink, LoadStyle.EAGER)

    # Target window border type constant: No window border
    TARGET_BORDER_NONE = Window.BORDER_NONE

    # Target window border type constant: Minimal window border
    TARGET_BORDER_MINIMAL = Window.BORDER_MINIMAL

    # Target window border type constant: Default window border
    TARGET_BORDER_DEFAULT = Window.BORDER_DEFAULT


    def __init__(self, caption=None, resource=None, targetName=None,
                 width=None, height=None, border=None):
        """Creates a new instance of Link.

        @param caption:
                   the Link text.
        @param resource:
        @param targetName:
                   the name of the target window where the link opens to. Empty
                   name of null implies that the target is opened to the window
                   containing the link.
        @param width:
                   the Width of the target window.
        @param height:
                   the Height of the target window.
        @param border:
                   the Border style of the target window.
        """
        super(Link, self).__init__()

        self._resource = None
        self._targetName = None
        self._targetBorder = self.TARGET_BORDER_DEFAULT
        self._targetWidth = -1
        self._targetHeight = -1

        if caption is not None:
            self.setCaption(caption)

        if resource is not None:
            self._resource = resource

        if targetName is not None:
            self.setTargetName(targetName)

        if width is not None:
            self.setTargetWidth(width)

        if height is not None:
            self.setTargetHeight(height)

        if border is not None:
            self.setTargetBorder(border)


    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the Paint Event.
        @raise PaintException:
                    if the paint operation failed.
        """
        if self._resource is not None:
            target.addAttribute('src', self._resource)
        else:
            return

        # Target window name
        name = self.getTargetName()
        if name is not None and len(name) > 0:
            target.addAttribute('name', name)

        # Target window size
        if self.getTargetWidth() >= 0:
            target.addAttribute('targetWidth', self.getTargetWidth())

        if self.getTargetHeight() >= 0:
            target.addAttribute('targetHeight', self.getTargetHeight())

        # Target window border
        test = self.getTargetBorder()
        if test == self.TARGET_BORDER_MINIMAL:
            target.addAttribute('border', 'minimal')
        elif test == self.TARGET_BORDER_NONE:
            target.addAttribute('border', 'none')


    def getTargetBorder(self):
        """Returns the target window border.

        @return: the target window border.
        """
        return self._targetBorder


    def getTargetHeight(self):
        """Returns the target window height or -1 if not set.

        @return: the target window height.
        """
        return -1 if self._targetHeight < 0 else self._targetHeight


    def getTargetName(self):
        """Returns the target window name. Empty name of null implies
        that the target is opened to the window containing the link.

        @return: the target window name.
        """
        return self._targetName


    def getTargetWidth(self):
        """Returns the target window width or -1 if not set.

        @return: the target window width.
        """
        return -1 if self._targetWidth < 0 else self._targetWidth


    def setTargetBorder(self, targetBorder):
        """Sets the border of the target window.

        @param targetBorder:
                   the targetBorder to set.
        """
        if (targetBorder == self.TARGET_BORDER_DEFAULT
                or targetBorder == self.TARGET_BORDER_MINIMAL
                or targetBorder == self.TARGET_BORDER_NONE):
            self._targetBorder = targetBorder
            self.requestRepaint()


    def setTargetHeight(self, targetHeight):
        """Sets the target window height.

        @param targetHeight:
                   the targetHeight to set.
        """
        self._targetHeight = targetHeight
        self.requestRepaint()


    def setTargetName(self, targetName):
        """Sets the target window name.

        @param targetName:
                   the targetName to set.
        """
        self._targetName = targetName
        self.requestRepaint()


    def setTargetWidth(self, targetWidth):
        """Sets the target window width.

        @param targetWidth:
                   the targetWidth to set.
        """
        self._targetWidth = targetWidth
        self.requestRepaint()


    def getResource(self):
        """Returns the resource this link opens.

        @return: the Resource.
        """
        return self._resource


    def setResource(self, resource):
        """Sets the resource this link opens.

        @param resource:
                   the resource to set.
        """
        self._resource = resource
        self.requestRepaint()
