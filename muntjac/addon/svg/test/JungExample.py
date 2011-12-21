# -*- coding: utf-8 -*-
from org.vaadin.svg.SvgComponent import (SvgComponent,)
from org.vaadin.svg.test.ExamplePanel import (ExamplePanel,)
# from com.vaadin.ui.Label import (Label,)
# from edu.uci.ics.jung.algorithms.layout.CircleLayout import (CircleLayout,)
# from edu.uci.ics.jung.algorithms.layout.Layout import (Layout,)
# from edu.uci.ics.jung.graph.SparseMultigraph import (SparseMultigraph,)
# from edu.uci.ics.jung.graph.util.EdgeType import (EdgeType,)
# from edu.uci.ics.jung.visualization.VisualizationImageServer import (VisualizationImageServer,)
# from edu.uci.ics.jung.visualization.decorators.ToStringLabeller import (ToStringLabeller,)
# from edu.uci.ics.jung.visualization.renderers.Renderer.VertexLabel.Position import (Position,)
# from java.awt.BasicStroke import (BasicStroke,)
# from java.awt.Color import (Color,)
# from java.awt.Dimension import (Dimension,)
# from java.awt.Paint import (Paint,)
# from java.awt.Stroke import (Stroke,)
# from java.io.ByteArrayOutputStream import (ByteArrayOutputStream,)
# from java.io.OutputStreamWriter import (OutputStreamWriter,)
# from java.io.Writer import (Writer,)
# from javax.xml.parsers.DocumentBuilder import (DocumentBuilder,)
# from javax.xml.parsers.DocumentBuilderFactory import (DocumentBuilderFactory,)
# from org.apache.batik.svggen.SVGGraphics2D import (SVGGraphics2D,)
# from org.apache.commons.collections15.Transformer import (Transformer,)
# from org.w3c.dom.Document import (Document,)
# from org.w3c.dom.Element import (Element,)


class JungExample(ExamplePanel):

    def __init__(self):
        self.setCaption('This graph is created with JUNG')
        self.addComponent(Label('This graphic is created with JUNG and made to SVG with Batik.'))
        try:
            docBuilderFactory = DocumentBuilderFactory()
            docBuilder = None
            docBuilder = docBuilderFactory.newDocumentBuilder()
            document = docBuilder.newDocument()
            svgelem = document.createElement('svg')
            document.appendChild(svgelem)
            # Create an instance of the SVG Generator
            graphic2d = SVGGraphics2D(document)
            server = self.SimpleGraphView2().getServer()
            server.printAll(graphic2d)
            # svgweb (IE fallback) needs size somehow defined
            el = graphic2d.getRoot()
            el.setAttributeNS(None, 'viewBox', '0 0 350 350')
            el.setAttributeNS(None, 'style', 'width:100%;height:100%;')
            # Finally, stream out SVG to the standard output using
            # UTF-8 encoding.
            useCSS = True
            # we want to use CSS style attributes
            bout = ByteArrayOutputStream()
            out = OutputStreamWriter(bout, 'UTF-8')
            graphic2d.stream(el, out, useCSS, False)
            svgComponent = SvgComponent()
            svgComponent.setWidth(350, self.UNITS_PIXELS)
            svgComponent.setHeight(350, self.UNITS_PIXELS)
            svgComponent.setSvg(str(bout.toByteArray()))
            self.addComponent(svgComponent)
        except Exception, e1:
            raise RuntimeError(e1)

    class SimpleGraphView2(SparseMultigraph):
        """Adapted example from Jung tutorial"""

        def __init__(self):
            """Creates a new instance of SimpleGraphView"""
            self.addVertex(1)
            self.addVertex(2)
            self.addVertex(3)
            self.addEdge('Edge-A', 1, 3)
            self.addEdge('Edge-B', 2, 3, EdgeType.DIRECTED)
            self.addEdge('Edge-C', 2, 1, EdgeType.DIRECTED)

        def getServer(self):
            """@param args
                       the command line arguments
            @return
            """
            # Layout<V, E>, VisualizationComponent<V,E>
            layout = CircleLayout(self)
            layout.setSize(Dimension(300, 300))
            vv = VisualizationImageServer(layout, Dimension(350, 350))
            # Setup up a new vertex to paint transformer...

            class vertexPaint(Transformer):

                def transform(self, i):
                    return Color.GREEN

            # Set up a new stroke Transformer for the edges
            dash = [10.0]
            edgeStroke = BasicStroke(1.0, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER, 10.0, dash, 0.0)

            class edgeStrokeTransformer(Transformer):

                def transform(self, s):
                    return self.edgeStroke

            vv.getRenderContext().setVertexFillPaintTransformer(vertexPaint)
            vv.getRenderContext().setEdgeStrokeTransformer(edgeStrokeTransformer)
            vv.getRenderContext().setVertexLabelTransformer(ToStringLabeller())
            vv.getRenderContext().setEdgeLabelTransformer(ToStringLabeller())
            vv.getRenderer().getVertexLabelRenderer().setPosition(Position.CNTR)
            return vv
