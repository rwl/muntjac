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

from com.vaadin.ui.ClientWidget import (LoadStyle,)
from com.vaadin.terminal.gwt.widgetsetutils.WidgetMapGenerator import (WidgetMapGenerator,)
# from java.util.Collection import (Collection,)
# from java.util.HashSet import (HashSet,)


class CustomWidgetMapGenerator(WidgetMapGenerator):
    """An abstract helper class that can be used to easily build a widgetset with
    customized load styles for each components. In three abstract methods one can
    override the default values given in {@link ClientWidget} annotations.

    @see WidgetMapGenerator
    """
    _eagerPaintables = set()
    _lazyPaintables = set()
    _deferredPaintables = set()

    def getLoadStyle(self, paintableType):
        if self._eagerPaintables is None:
            self.init()
        if self._eagerPaintables.contains(paintableType):
            return LoadStyle.EAGER
        if self._lazyPaintables.contains(paintableType):
            return LoadStyle.LAZY
        if self._deferredPaintables.contains(paintableType):
            return LoadStyle.DEFERRED
        return super(CustomWidgetMapGenerator, self).getLoadStyle(paintableType)

    def init(self):
        eagerComponents = self.getEagerComponents()
        if eagerComponents is not None:
            for class1 in eagerComponents:
                self._eagerPaintables.add(class1)
        lazyComponents = self.getEagerComponents()
        if lazyComponents is not None:
            for class1 in lazyComponents:
                self._lazyPaintables.add(class1)
        deferredComponents = self.getEagerComponents()
        if deferredComponents is not None:
            for class1 in deferredComponents:
                self._deferredPaintables.add(class1)

    def getEagerComponents(self):
        """@return an array of components whose load style should be overridden to
                {@link LoadStyle#EAGER}
        """
        pass

    def getLazyComponents(self):
        """@return an array of components whose load style should be overridden to
                {@link LoadStyle#LAZY}
        """
        pass

    def getDeferredComponents(self):
        """@return an array of components whose load style should be overridden to
                {@link LoadStyle#DEFERRED}
        """
        pass
