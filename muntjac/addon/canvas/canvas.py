# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

from muntjac.ui.abstract_component import AbstractComponent


class Canvas(AbstractComponent):
    """Server side component for the VCanvas widget."""

    CLIENT_WIDGET = None #ClientWidget(VCanvas)

    TYPE_MAPPING = 'org.vaadin.hezamu.canvas.Canvas'

    BEVEL = 'BEVEL'
    BUTT = 'BUTT'
    DESTINATION_OVER = 'DESTINATION_OVER'
    SOURCE_OVER = 'SOURCE_OVER'
    MITER = 'MITER'
    TRANSPARENT = 'TRANSPARENT'
    ROUND = 'ROUND'
    SQUARE = 'SQUARE'

    def __init__(self):
        super(Canvas, self).__init__()

        self._commands = list()
        self._downListeners = list()
        self._upListeners = list()


    def createLinearGradient(self, name, x0, y0, x1, y1):
        arguments = dict()
        arguments['command'] = 'createLinearGradient'
        arguments['name'] = name
        arguments['x0'] = x0
        arguments['y0'] = y0
        arguments['x1'] = x1
        arguments['y1'] = y1
        self._commands.append(arguments)
        self.requestRepaint()


    def createRadialGradient(self, name, x0, y0, r0, x1, y1, r1):
        arguments = dict()
        arguments['command'] = 'createRadialGradient'
        arguments['name'] = name
        arguments['x0'] = x0
        arguments['y0'] = y0
        arguments['r0'] = r0
        arguments['x1'] = x1
        arguments['y1'] = y1
        arguments['r1'] = r1
        self._commands.append(arguments)
        self.requestRepaint()


    def cubicCurveTo(self, cp1x, cp1y, cp2x, cp2y, x, y):
        arguments = dict()
        arguments['command'] = 'cubicCurveTo'
        arguments['cp1x'] = cp1x
        arguments['cp1y'] = cp1y
        arguments['cp2x'] = cp2x
        arguments['cp2y'] = cp2y
        arguments['x'] = x
        arguments['y'] = y
        self._commands.append(arguments)
        self.requestRepaint()


    def drawImage(self, *args):
        nargs = len(args)
        if nargs == 3:
            url, offsetX, offsetY = args
            arguments = dict()
            arguments['command'] = 'drawImage1'
            arguments['url'] = url
            arguments['offsetX'] = offsetX
            arguments['offsetY'] = offsetY
            self._commands.append(arguments)
            self.requestRepaint()
        elif nargs == 5:
            url, offsetX, offsetY, width, height = args
            arguments = dict()
            arguments['command'] = 'drawImage2'
            arguments['url'] = url
            arguments['offsetX'] = offsetX
            arguments['offsetY'] = offsetY
            arguments['width'] = width
            arguments['height'] = height
            self._commands.append(arguments)
            self.requestRepaint()
        elif nargs == 9:
            (url, sourceX, sourceY, sourceWidth, sourceHeight, destX, destY,
                destWidth, destHeight) = args
            arguments = dict()
            arguments['command'] = 'drawImage3'
            arguments['url'] = url
            arguments['sourceX'] = sourceX
            arguments['sourceY'] = sourceY
            arguments['sourceWidth'] = sourceWidth
            arguments['sourceHeight'] = sourceHeight
            arguments['destX'] = destX
            arguments['destY'] = destY
            arguments['destWidth'] = destWidth
            arguments['destHeight'] = destHeight
            self._commands.append(arguments)
            self.requestRepaint()
        else:
            raise ValueError


    def fill(self):
        arguments = dict()
        arguments['command'] = 'fill'
        self._commands.append(arguments)
        self.requestRepaint()


    def fillRect(self, startX, startY, width, height):
        arguments = dict()
        arguments['command'] = 'fillRect'
        arguments['startX'] = startX
        arguments['startY'] = startY
        arguments['width'] = width
        arguments['height'] = height
        self._commands.append(arguments)
        self.requestRepaint()


    def lineTo(self, x, y):
        arguments = dict()
        arguments['command'] = 'lineTo'
        arguments['x'] = x
        arguments['y'] = y
        self._commands.append(arguments)
        self.requestRepaint()


    def moveTo(self, x, y):
        arguments = dict()
        arguments['command'] = 'moveTo'
        arguments['x'] = x
        arguments['y'] = y
        self._commands.append(arguments)
        self.requestRepaint()


    def quadraticCurveTo(self, cpx, cpy, x, y):
        arguments = dict()
        arguments['command'] = 'quadraticCurveTo'
        arguments['cpx'] = cpx
        arguments['cpy'] = cpy
        arguments['x'] = x
        arguments['y'] = y
        self._commands.append(arguments)
        self.requestRepaint()


    def rect(self, startX, startY, width, height):
        arguments = dict()
        arguments['command'] = 'rect'
        arguments['startX'] = startX
        arguments['startY'] = startY
        arguments['width'] = width
        arguments['height'] = height
        self._commands.append(arguments)
        self.requestRepaint()


    def rotate(self, angle):
        arguments = dict()
        arguments['command'] = 'rotate'
        arguments['angle'] = angle
        self._commands.append(arguments)
        self.requestRepaint()


    def setGradientFillStyle(self, gradient):
        arguments = dict()
        arguments['command'] = 'setGradientFillStyle'
        arguments['gradient'] = gradient
        self._commands.append(arguments)
        self.requestRepaint()


    def setFillStyle(self, *args):
        nargs = len(args)
        if nargs == 1:
            color, = args
            arguments = dict()
            arguments['command'] = 'setFillStyle'
            arguments['color'] = color
            self._commands.append(arguments)
            self.requestRepaint()
        elif nargs == 3:
            r, g, b = args
            self.setFillStyle('#%02x%02x%02x' % r, g, b)
        else:
            raise ValueError


    def setLineCap(self, lineCap):
        arguments = dict()
        arguments['command'] = 'setLineCap'
        arguments['lineCap'] = lineCap
        self._commands.append(arguments)
        self.requestRepaint()


    def setLineJoin(self, lineJoin):
        arguments = dict()
        arguments['command'] = 'setLineJoin'
        arguments['lineJoin'] = lineJoin
        self._commands.append(arguments)
        self.requestRepaint()


    def setLineWidth(self, width):
        arguments = dict()
        arguments['command'] = 'setLineWidth'
        arguments['width'] = width
        self._commands.append(arguments)
        self.requestRepaint()


    def setMiterLimit(self, miterLimit):
        arguments = dict()
        arguments['command'] = 'setMiterLimit'
        arguments['miterLimit'] = miterLimit
        self._commands.append(arguments)
        self.requestRepaint()


    def setGradientStrokeStyle(self, gradient):
        arguments = dict()
        arguments['command'] = 'setGradientStrokeStyle'
        arguments['gradient'] = gradient
        self._commands.append(arguments)
        self.requestRepaint()


    def setColorStrokeStyle(self, color):
        arguments = dict()
        arguments['command'] = 'setColorStrokeStyle'
        arguments['color'] = color
        self._commands.append(arguments)
        self.requestRepaint()


    def strokeRect(self, startX, startY, width, height):
        arguments = dict()
        arguments['command'] = 'strokeRect'
        arguments['startX'] = startX
        arguments['startY'] = startY
        arguments['width'] = width
        arguments['height'] = height
        self._commands.append(arguments)
        self.requestRepaint()


    def transform(self, m11, m12, m21, m22, dx, dy):
        arguments = dict()
        arguments['command'] = 'transform'
        arguments['m11'] = m11
        arguments['m12'] = m12
        arguments['m21'] = m21
        arguments['m22'] = m22
        arguments['dx'] = dx
        arguments['dy'] = dy
        self._commands.append(arguments)
        self.requestRepaint()


    def arc(self, x, y, radius, startAngle, endAngle, antiClockwise):
        arguments = dict()
        arguments['command'] = 'arc'
        arguments['x'] = x
        arguments['y'] = y
        arguments['radius'] = radius
        arguments['startAngle'] = startAngle
        arguments['endAngle'] = endAngle
        self._commands.append(arguments)
        self.requestRepaint()


    def translate(self, x, y):
        arguments = dict()
        arguments['command'] = 'translate'
        arguments['x'] = x
        arguments['y'] = y
        self._commands.append(arguments)
        self.requestRepaint()


    def scale(self, x, y):
        arguments = dict()
        arguments['command'] = 'scale'
        arguments['x'] = x
        arguments['y'] = y
        self._commands.append(arguments)
        self.requestRepaint()


    def stroke(self):
        arguments = dict()
        arguments['command'] = 'stroke'
        self._commands.append(arguments)
        self.requestRepaint()


    def saveContext(self):
        arguments = dict()
        arguments['command'] = 'saveContext'
        self._commands.append(arguments)
        self.requestRepaint()


    def restoreContext(self):
        arguments = dict()
        arguments['command'] = 'restoreContext'
        self._commands.append(arguments)
        self.requestRepaint()


    def setBackgroundColor(self, rgb):
        arguments = dict()
        arguments['command'] = 'setBackgroundColor'
        arguments['rgb'] = rgb
        self._commands.append(arguments)
        self.requestRepaint()


    def setStrokeColor(self, rgb):
        arguments = dict()
        arguments['command'] = 'setStrokeColor'
        arguments['rgb'] = rgb
        self._commands.append(arguments)
        self.requestRepaint()


    def beginPath(self):
        arguments = dict()
        arguments['command'] = 'beginPath'
        self._commands.append(arguments)
        self.requestRepaint()


    def clear(self):
        arguments = dict()
        arguments['command'] = 'clear'
        self._commands.append(arguments)
        self.requestRepaint()


    def reset(self):
        self._commands.clear()
        self.clear()


    def paintContent(self, target):
        super(Canvas, self).paintContent(target)
        for command in self._commands:
            target.startTag(command.get('command'))

            for key in command:
                if key == 'command':
                    continue  # This is already in tag name

                value = command.get(key)
                target.addAttribute(key, value)

            target.endTag(command.get('command'))


    def changeVariables(self, source, variables):
        if 'sizeChanged' in variables:
            print 'Canvass size now ' + str(variables['sizeChanged'])
            self.requestRepaint()
        elif 'event' in variables:
            eventtype = variables['event']
            x = variables['mx']
            y = variables['my']
            if eventtype == 'mousedown':
                self.fireMouseDown(x, y)
            elif eventtype == 'mouseup':
                self.fireMouseUp(x, y)
            else:
                print 'Unknown event type: ' + eventtype


    def setStrokeStyle(self, r, g, b):
        self.setStrokeColor('#%02x%02x%02x' % (r, g, b))


    def setGlobalAlpha(self, alpha):
        arguments = dict()
        arguments['command'] = 'setGlobalAlpha'
        arguments['alpha'] = alpha
        self._commands.append(arguments)
        self.requestRepaint()


    def closePath(self):
        arguments = dict()
        arguments['command'] = 'closePath'
        self._commands.append(arguments)
        self.requestRepaint()


    def setGlobalCompositeOperation(self, mode):
        arguments = dict()
        arguments['command'] = 'setGlobalCompositeOperation'
        arguments['mode'] = mode
        self._commands.append(arguments)
        self.requestRepaint()


    def addColorStop(self, gradient, offset, color):
        arguments = dict()
        arguments['command'] = 'addColorStop'
        arguments['gradient'] = gradient
        arguments['offset'] = offset
        arguments['color'] = color
        self._commands.append(arguments)
        self.requestRepaint()


    def addListener(self, listener, iface=None):
        if isinstance(listener, ICanvasMouseDownListener):
            if listener not in self._downListeners:
                self._downListeners.append(listener)
        else:
            if listener not in self._upListeners:
                self._upListeners.append(listener)


    def removeListener(self, listener, iface=None):
        if isinstance(listener, ICanvasMouseDownListener):
            if listener in self._downListeners:
                self._downListeners.remove(listener)
        else:
            if listener in self._upListeners:
                self._upListeners.remove(listener)


    def fireMouseDown(self, x, y):
        for listener in self._downListeners:
            listener.mouseDown(x, y)


    def fireMouseUp(self, x, y):
        for listener in self._upListeners:
            listener.mouseDown(x, y)


class ICanvasMouseDownListener(object):

    def mouseDown(self, x, y):
        raise NotImplementedError


class ICanvasMouseUpListener(object):

    def mouseDown(self, x, y):
        raise NotImplementedError
