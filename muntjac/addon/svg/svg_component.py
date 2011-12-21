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

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from muntjac.ui.embedded import Embedded
from muntjac.ui.component import Event

from muntjac.terminal.stream_resource import StreamResource, StreamSource


class SvgMessageListener(object):
    """SvgMessageListener can be used to build simple communication between SVG
    document and the corresponding Muntjac wrapper. In SVG documents context
    calling::

        parent.updateToVaadin(&quot;Foo&quot;);

    will cause listeners to be notified with message "Foo";
    """

    def handleMessage(self, event):
        raise NotImplementedError


_SVG_MSG_METHOD = getattr(SvgMessageListener, 'handleMessage')


class SvgComponent(Embedded):
    """SvgComponent helps to use of SVG in Muntjac. Plain L{Embedded} supports
    SVG as well, but SvgComponent has some enhancements like simple
    client-server communication and IE support.

    The SVG can be provided as L{Resource} via
    L{Embedded.setSource}. The SvgComponent also has helper methods L{setSvg}
    and L{setSvg}.

    To support Internet Explorer, SvgComponent uses svgweb library built by
    Bradd Neuberg. Svgweb uses javascript and flash to provide SVG support
    providing closer to 99% browser support. See
    http://code.google.com/p/svgweb/ for more information. Note that for other
    browsers svgweb is not used.

    NOTE: the svgweb fallback requires mime type mapping for .htc file.

    The component also provides a simple messaging mechanism from SVG to the
    wrapping L{SvgComponent}. See L{SvgMessageListener}.
    """

    _DEFAULT_W = '400px'
    _DEFAULT_H = '200px'

    def __init__(self):
        self._svg = None

        self.setWidth(self._DEFAULT_W)
        self.setHeight(self._DEFAULT_H)


    def attach(self):
        super(SvgComponent, self).attach()
        if self._svg is not None:
            streamResource = StreamResource(self.getStreamSource(),
                    self.getFilename(), self.getApplication())
            streamResource.setCacheTime(self.getCacheTime())
            self.setSource(streamResource)


    def getCacheTime(self):
        """@return: the cache time in millis if builtin resource, -1 by
        default"""
        return -1


    def getStreamSource(self):
        return SvgStreamSource(self)


    def setSvg(self, svg):
        """A helper method to set svg in a string. Another approach is to use
        L{Embedded.setSizeFull} method.

        @param svg:
                   svg file contents
        """
        if isinstance(svg, StringIO):
            resourceAsStream = svg
            self.setSvg(resourceAsStream.read())
        else:
            self._svg = svg


    def getSvg(self):
        return self._svg


    def getFilename(self):
        return 'svg.svg'


    def changeVariables(self, source, variables):
        super(SvgComponent, self).changeVariables(source, variables)
        if 'svgMsg' in variables:
            self.handleMsg(variables['svgMsg'])


    def handleMsg(self, obj):
        # Implementation note: parent is used as attaching method svg doc
        # context didn't work in svgweb
        svgMessageEvent = SvgMessageEvent(self, obj)
        self.fireEvent(svgMessageEvent)


    def addListener(self, listener):
        self.addListener('svgmsg', SvgMessageEvent, listener, _SVG_MSG_METHOD)


    def removeListener(self, listener):
        self.removeListener('svgmsg', SvgMessageEvent, listener)


class SvgMessageEvent(Event):

    def __init__(self, source, msg):
        super(SvgMessageEvent, self).__init__(source)
        self._msg = msg


    def getMessage(self):
        """@return: the message sent from the SVG document"""
        return self._msg


class SvgStreamSource(StreamSource):

    def __init__(self, svgc):
        self._svgc = svgc

    def getStream(self):
        return StringIO(self._svgc.getSvg().getBytes())
