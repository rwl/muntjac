# -*- coding: utf-8 -*-
from org.vaadin.svg.SvgComponent import (SvgComponent,)
from org.vaadin.svg.test.ExamplePanel import (ExamplePanel,)
# from com.vaadin.ui.Label import (Label,)
# from java.awt.BasicStroke import (BasicStroke,)
# from java.awt.Color import (Color,)
# from java.awt.Graphics2D import (Graphics2D,)
# from java.awt.Shape import (Shape,)
# from java.awt.font.FontRenderContext import (FontRenderContext,)
# from java.awt.font.TextLayout import (TextLayout,)
# from java.awt.geom.CubicCurve2D import (CubicCurve2D,)
# from java.awt.geom.Ellipse2D import (Ellipse2D,)
# from java.awt.geom.FlatteningPathIterator import (FlatteningPathIterator,)
# from java.awt.geom.PathIterator import (PathIterator,)
# from java.awt.geom.QuadCurve2D import (QuadCurve2D,)
# from java.awt.geom.Rectangle2D import (Rectangle2D,)
# from java.io.ByteArrayOutputStream import (ByteArrayOutputStream,)
# from java.io.OutputStreamWriter import (OutputStreamWriter,)
# from java.io.Writer import (Writer,)
# from javax.xml.parsers.DocumentBuilder import (DocumentBuilder,)
# from javax.xml.parsers.DocumentBuilderFactory import (DocumentBuilderFactory,)
# from org.apache.batik.svggen.SVGGraphics2D import (SVGGraphics2D,)
# from org.w3c.dom.Document import (Document,)
# from org.w3c.dom.Element import (Element,)


class Java2DExample(ExamplePanel):
    _height = 300
    _widht = 400

    def __init__(self):
        self.setCaption('This graphic is created with java.awt.Graphics2D')
        self.addComponent(Label('This graphic is created with java.awt.Graphics2D API and made to SVG with Batik.'))
        try:
            docBuilderFactory = DocumentBuilderFactory()
            docBuilder = None
            docBuilder = docBuilderFactory.newDocumentBuilder()
            document = docBuilder.newDocument()
            svgelem = document.createElement('svg')
            document.appendChild(svgelem)
            # Create an instance of the SVG Generator
            graphic2d = SVGGraphics2D(document)
            self.drawDemo(self._widht, self._height, graphic2d)
            # svgweb (IE fallback) needs size somehow defined
            el = graphic2d.getRoot()
            el.setAttributeNS(None, 'viewBox', '0 0 ' + self._widht + ' ' + self._height + '')
            el.setAttributeNS(None, 'style', 'width:100%;height:100%;')
            # Finally, stream out SVG to the standard output using
            # UTF-8 encoding.
            useCSS = True
            # we want to use CSS style attributes
            bout = ByteArrayOutputStream()
            out = OutputStreamWriter(bout, 'UTF-8')
            graphic2d.stream(el, out, useCSS, False)
            svgComponent = SvgComponent()
            svgComponent.setWidth(self._widht, self.UNITS_PIXELS)
            svgComponent.setHeight(self._height, self.UNITS_PIXELS)
            svgComponent.setSvg(str(bout.toByteArray()))
            self.addComponent(svgComponent)
        except Exception, e1:
            raise RuntimeError(e1)

    _colors = [Color.blue, Color.green, Color.red]

    def drawDemo(self, w, h, g2):
        """Example code borrowed from Sun demos:
        http://java.sun.com/products/java-media
        /2D/samples/suite/Arcs_Curves/Curves.java
        """
        g2.setColor(Color.black)
        # draws the word "QuadCurve2D"
        frc = g2.getFontRenderContext()
        tl = TextLayout('QuadCurve2D', g2.getFont(), frc)
        xx = (w * 0.5) - (tl.getBounds().getWidth() / 2)
        tl.draw(g2, xx, tl.getAscent())
        # draws the word "CubicCurve2D"
        tl = TextLayout('CubicCurve2D', g2.getFont(), frc)
        xx = (w * 0.5) - (tl.getBounds().getWidth() / 2)
        tl.draw(g2, xx, h * 0.5)
        g2.setStroke(BasicStroke(5.0))
        yy = 20
        # draws 3 quad curves and 3 cubic curves.
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 2):
                break
            _1 = True
            j = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    j += 1
                if not (j < 3):
                    break
                shape = None
                if i == 0:
                    shape = QuadCurve2D.Float(w * 0.1, yy, w * 0.5, 50, w * 0.9, yy)
                else:
                    shape = CubicCurve2D.Float(w * 0.1, yy, w * 0.4, yy - 15, w * 0.6, yy + 15, w * 0.9, yy)
                g2.setColor(self._colors[j])
                if j != 2:
                    g2.draw(shape)
                if j == 1:
                    g2.setColor(Color.lightGray)
                    # creates an iterator object to iterate the boundary of the
                    # curve.

                    f = shape.getPathIterator(None)
                    # while iteration of the curve is still in process fills
                    # rectangles at the endpoints and control points of the
                    # curve.

                    while not f.isDone():
                        pts = [None] * 6
                        _2 = f.currentSegment(pts)
                        _3 = False
                        while True:
                            if _2 == PathIterator.SEG_MOVETO:
                                _3 = True
                            if (_3 is True) or (_2 == PathIterator.SEG_LINETO):
                                _3 = True
                                g2.fill(Rectangle2D.Float(pts[0], pts[1], 5, 5))
                                break
                            if (_3 is True) or (_2 == PathIterator.SEG_CUBICTO):
                                _3 = True
                            if (_3 is True) or (_2 == PathIterator.SEG_QUADTO):
                                _3 = True
                                g2.fill(Rectangle2D.Float(pts[0], pts[1], 5, 5))
                                if pts[2] != 0:
                                    g2.fill(Rectangle2D.Float(pts[2], pts[3], 5, 5))
                                if pts[4] != 0:
                                    g2.fill(Rectangle2D.Float(pts[4], pts[5], 5, 5))
                            break
                        f.next()
                elif j == 2:
                    # draws red ellipses along the flattened curve.
                    p = shape.getPathIterator(None)
                    f = FlatteningPathIterator(p, 0.1)
                    while not f.isDone():
                        pts = [None] * 6
                        _4 = f.currentSegment(pts)
                        _5 = False
                        while True:
                            if _4 == PathIterator.SEG_MOVETO:
                                _5 = True
                            if (_5 is True) or (_4 == PathIterator.SEG_LINETO):
                                _5 = True
                                g2.fill(Ellipse2D.Float(pts[0], pts[1], 3, 3))
                            break
                        f.next()
                yy += h / 6
            yy = (h / 2) + 15
