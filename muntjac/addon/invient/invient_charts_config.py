# @INVIENT_COPYRIGHT@
# @MUNTJAC_LICENSE@

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from muntjac.addon.invient.paint \
    import IPaint

from muntjac.util \
    import OrderedSet


class InvientChartsConfig(object):
    """This class encapsulates a number of configuration options for the
    InvientChars. These configuration options are L{Title}, L{SubTitle}
    , L{GeneralChartConfig}, L{Credit}, L{Legend}, L{Tooltip}
    , L{ChartLabel}, L{SeriesConfig}, L{XAxis} and L{YAxis}

    All configuration properties which are of object type are initialized
    with an object instance.

    These configuration options are static and generally set once. After a
    chart (L{InvientCharts}) created, any changes made to the configuration
    options will not reflect in the chart. You would have to create a new
    chart L{InvientCharts}

    For some APIs, the description has been taken from
    U{http://www.highcharts.com/ref/}

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self):
        self._title = Title()
        self._subtitle = SubTitle()
        self._generalChartConfig = GeneralChartConfig()
        self._credit = Credit()
        self._legend = Legend()
        self._tooltip = Tooltip()
        self._chartLabel = ChartLabel()
        self._seriesTypeConfig = OrderedDict()
        self._xAxes = OrderedSet()
        self._yAxes = OrderedSet()
        self._invientCharts = None


    def getInvientCharts(self):
        return self._invientCharts


    def setInvientCharts(self, invientCharts):
        self._invientCharts = invientCharts


    def getChartLabel(self):
        """@return: The L{ChartLabel} object representing labels at arbitrary
                    position in the chart.
        """
        return self._chartLabel


    def setChartLabel(self, chartLabel):
        """Sets the argument L{ChartLabel} object only if it is non-null

        @param chartLabel:
        """
        if chartLabel is not None:
            self._chartLabel = chartLabel


    def getXAxes(self):
        """@return: Returns a collection of x-axis."""
        return self._xAxes


    def setXAxes(self, xAxes):
        """Sets a collection of x-axis for the chart. The collection of x-axis
        is set only if argument xAxes is non-null.

        @param xAxes:
        """
        if xAxes is not None:
            self._xAxes = xAxes


    def addXAxes(self, xAxis):
        """Adds specified x-axis to the collection of x-axis.

        @param xAxis:
        @return: Returns true if the x-axis is added successfully otherwise
                 false
        """
        return self._xAxes.add(xAxis)


    def getYAxes(self):
        """@return: Returns a collection of y-axis."""
        return self._yAxes


    def setYAxes(self, yAxes):
        """Sets a collection of y-axis for the chart. The collection of y-axis
        is set only if argument yAxes is non-null

        @param yAxes:
        """
        if yAxes is not None:
            self._yAxes = yAxes


    def addYAxes(self, yAxis):
        """Adds specified y-axis to the collection of y-axis.

        @param yAxis:
        @return: Returns true if the y-axis is added successfully otherwise
                 false
        """
        return self._yAxes.add(yAxis)


    def getTitle(self):
        """@return: Returns L{Title} object"""
        return self._title


    def setTitle(self, title):
        """Sets the argument title only if the argument title is non-null

        @param title:
        """
        if title is not None:
            self._title = title


    def getSubtitle(self):
        """@return: Returns subtitle"""
        return self._subtitle


    def setSubtitle(self, subtitle):
        """Sets the argument subtitle only if the argument is non-null

        @param subtitle:
        """
        if subtitle is not None:
            self._subtitle = subtitle


    def getTooltip(self):
        """@return: Returns tooltip object associated with this class"""
        return self._tooltip


    def setTooltip(self, tooltip):
        """Sets L{Tooltip} object only if the argument tooltip is non-null

        @param tooltip:
        """
        if tooltip is not None:
            self._tooltip = tooltip


    def getLegend(self):
        """@return: Returns legend object of the chart"""
        return self._legend


    def setLegend(self, legend):
        """Sets L{Legend} object only if the argument legend is non-null

        @param legend:
        """
        if legend is not None:
            self._legend = legend


    def getCredit(self):
        """@return: Returns credit object of the chart"""
        return self._credit


    def setCredit(self, credit):
        """Sets the L{Credit} object only if the argument credit is non-null

        @param credit:
        """
        if credit is not None:
            self._credit = credit


    def getGeneralChartConfig(self):
        """@return: Returns L{GeneralChartConfig} object"""
        return self._generalChartConfig


    def setGeneralChartConfig(self, generalChartConfig):
        """Sets L{GeneralChartConfig} object only if the argument is non-null

        @param generalChartConfig:
        """
        if generalChartConfig is not None:
            self._generalChartConfig = generalChartConfig


    def getSeriesConfig(self):
        return self._seriesTypeConfig


    def setSeriesConfig(self, seriesConfigs):
        """Sets a set of {@link SeriesConfig} objects only if the argument is
        non-null.

        @param seriesConfigs:
        """
        if self._seriesTypeConfig is not None:
            self._seriesTypeConfig.clear()
            for config in seriesConfigs:
                self.addSeriesConfig(config)


    def addSeriesConfig(self, seriesConfig):
        """Adds the specified argument only if it is non-null.

        @param seriesConfig:
        @raise ValueError:
                    if the argument is null
        """
        if seriesConfig is None:
            raise ValueError, 'Argument SeriesConfig cannot be null.'
        self._seriesTypeConfig[self.getSeriesType(seriesConfig)] = seriesConfig


    @classmethod
    def getSeriesType(cls, seriesConfig):
        """@param seriesConfig:
        @return:
        """
        from muntjac.addon.invient.invient_charts import SeriesType

        seriesType = SeriesType.COMMONSERIES
        if LineConfig == seriesConfig.__class__:
            seriesType = SeriesType.LINE
        elif SplineConfig == seriesConfig.__class__:
            seriesType = SeriesType.SPLINE
        elif ScatterConfig == seriesConfig.__class__:
            seriesType = SeriesType.SCATTER
        elif AreaConfig == seriesConfig.__class__:
            seriesType = SeriesType.AREA
        elif AreaSplineConfig == seriesConfig.__class__:
            seriesType = SeriesType.AREASPLINE
        elif BarConfig == seriesConfig.__class__:
            seriesType = SeriesType.BAR
        elif ColumnConfig == seriesConfig.__class__:
            seriesType = SeriesType.COLUMN
        elif PieConfig == seriesConfig.__class__:
            seriesType = SeriesType.PIE
        return seriesType


class ChartLabel(object):
    """The L{ChartLabel} class represents a set of labels which an be
    placed at arbitrary position in the chart.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self):
        self._style = None
        self._labels = list()


    def getStyle(self):
        """@return: Returns css style."""
        return self._style


    def setStyle(self, style):
        """Sets css style for all labels in this class

        @param style:
                   css style string
        """
        self._style = style


    def getLabels(self):
        """@return: Returns a list of L{ChartLabelItem} objects"""
        return self._labels


    def setLabels(self, labels):
        """Sets a list of L{ChartLabelItem} objects

        @param labels:
        """
        if labels is not None:
            self._labels = labels


    def addLabel(self, label):
        """Appends the specified element at the end of L{ChartLabelItem}
        list.

        @param label:
                   element to be appended
        """
        self._labels.append(label)


    def removeLabel(self, label):
        """Removes the specified element from the list of L{ChartLabelItem}

        @param label:
        """
        self._labels.remove(label)


class ChartLabelItem(object):
    """This class represents a label placed at arbitrary location in the
    chart. The label can have html text and it can be styled using
    css-style.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, html, style):
        """Creates a new instance with specified html and style arguments.

        @param html:
        @param style:
        """
        super(ChartLabelItem, self).__init__()
        self._html = html
        self._style = style


    def getHtml(self):
        """@return Returns html of this label"""
        return self._html


    def setHtml(self, html):
        """Sets html for this label

        @param html:
                   It can be plain or html string.
        """
        self._html = html


    def getStyle(self):
        """@return: Returns css-style of this label"""
        return self._style


    def setStyle(self, style):
        """Sets css style for this label

        @param style:
        """
        self._style = style


class GeneralChartConfig(object):
    """This class contains configuration properties at a chart level.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self):
        from muntjac.addon.invient.invient_charts import SeriesType

        self._backgroundColor = None
        self._borderColor = None
        self._borderRadius = None
        self._borderWidth = None
        self._height = None
        self._width = None
        self._ignoreHiddenSeries = None
        self._inverted = None
        self._margin = None
        self._spacing = None
        self._showAxes = None
        self._type = SeriesType.LINE
        self._zoomType = ZoomType.NONE
        self._clientZoom = True
        self._alignTicks = None
        self._animation = None
        self._className = None
        self._reflow = None
        self._shadow = None
        self._plot = None
        self._style = None


    def getAlignTicks(self):
        """@return: align ticks"""
        return self._alignTicks


    def setAlignTicks(self, alignTicks):
        """When using multiple axis, the ticks of two or more opposite axes
        will automatically be aligned by adding ticks to the axis or axes with
        the least ticks. This can be prevented by setting alignTicks to false.

        @param alignTicks:
        """
        self._alignTicks = alignTicks


    def getAnimation(self):
        """@return: animation"""
        return self._animation


    def setAnimation(self, animation):
        """Set the overall animation for all chart updating.

        @param animation:
        """
        self._animation = animation


    def getClassName(self):
        """@return"""
        return self._className


    def setClassName(self, className):
        """A CSS class name to apply to the charts container

        @param className:
        """
        self._className = className

    def getPlot(self):
        """@return: Returns plot object representing chart's drawing area"""
        return self._plot


    def setPlot(self, plot):
        """Sets plot object

        @param plot:
        """
        self._plot = plot


    def getReflow(self):
        """@return:"""
        return self._reflow


    def setReflow(self, reflow):
        """A value of true indicates that the chart will fit the width of the
        charts container otherwise not.

        @param reflow:
        """
        self._reflow = reflow


    def getShadow(self):
        """@return:"""
        return self._shadow


    def setShadow(self, shadow):
        """A value of true indicates that the drop shadow will apply to the
        outer chart area otherwise not.

        @param shadow:
        """
        self._shadow = shadow


    def getStyle(self):
        """@return:"""
        return self._style


    def setStyle(self, style):
        """A CSS string to apply to the charts container

        @param style:
        """
        self._style = style


    def getBackgroundColor(self):
        """@return:"""
        return self._backgroundColor


    def setBackgroundColor(self, backgroundColor):
        """Sets the background color for the outer chart area

        @param backgroundColor
        """
        self._backgroundColor = backgroundColor


    def getBorderColor(self):
        """@return"""
        return self._borderColor


    def setBorderColor(self, borderColor):
        """Sets the border color for the outer chart border

        @param borderColor
        """
        self._borderColor = borderColor


    def getBorderRadius(self):
        """@return"""
        return self._borderRadius


    def setBorderRadius(self, borderRadius):
        """Sets radius for the outer chart border

        @param borderRadius
        """
        self._borderRadius = borderRadius


    def getBorderWidth(self):
        """@return"""
        return self._borderWidth


    def setBorderWidth(self, borderWidth):
        """Sets pixel width of the outer chart border

        @param borderWidth
        """
        self._borderWidth = borderWidth


    def getHeight(self):
        """@return"""
        return self._height


    def setHeight(self, height):
        """Sets height for the chart

        @param height
        """
        self._height = height


    def getWidth(self):
        """@return"""
        return self._width


    def setWidth(self, width):
        """Sets width for the chart

        @param width
        """
        self._width = width


    def getIgnoreHiddenSeries(self):
        """@return"""
        return self._ignoreHiddenSeries


    def setIgnoreHiddenSeries(self, ignoreHiddenSeries):
        """If the argument is true, the axes will scale to the remaining
        visible series once one series is hidden. If the argument is false,
        hiding and showing a series will not affect the axes or the other
        series.

        @param ignoreHiddenSeries
        """
        self._ignoreHiddenSeries = ignoreHiddenSeries


    def getInverted(self):
        """@return"""
        return self._inverted


    def setInverted(self, inverted):
        """If the argument is true then the x-axis is reversed. If a bar
        plot is present, it will be inverted automatically.

        @param inverted
        """
        self._inverted = inverted


    def getMargin(self):
        """@return"""
        return self._margin


    def setMargin(self, margin):
        """@param margin"""
        self._margin = margin


    def getShowAxes(self):
        """@return"""
        return self._showAxes


    def setShowAxes(self, showAxes):
        """If the argument is true then the axes will be shown initially.
        This is useful when the chart is empty and axes must be shown.

        @param showAxes
        """
        self._showAxes = showAxes


    def getSpacing(self):
        """@return"""
        return self._spacing


    def setSpacing(self, spacing):
        """@param spacing"""
        self._spacing = spacing


    def getType(self):
        """@return"""
        return self._type


    def setType(self, typ):
        """Sets series type to one of line, spline, scatter, area,
        areaspline, pie, bar and column.

        @param typ
        """
        self._type = typ


    def getZoomType(self):
        """@return"""
        return self._zoomType


    def setZoomType(self, zoomType):
        """Sets zoom type. It decides how a chart can be zoomed by
        dragging the mouse.

        @param zoomType
        """
        self._zoomType = zoomType


    def isClientZoom(self):
        """@return"""
        return self._clientZoom


    def setClientZoom(self, clientZoom):
        """If the argument is true then the scaling will happen on client. If
        the argument is false then the chart will not scale. In any case, the
        server will receive event notification if registered.

        @param clientZoom
        """
        self._clientZoom = clientZoom


    def __str__(self):
        return ('Chart [backgroundColor=' + str(self._backgroundColor)
                + ', borderColor=' + str(self._borderColor)
                + ', borderRadius=' + str(self._borderRadius)
                + ', borderWidth=' + str(self._borderWidth)
                + ', height=' + str(self._height)
                + ', width=' + str(self._width)
                + ', ignoreHiddenSeries=' + str(self._ignoreHiddenSeries)
                + ', inverted=' + str(self._inverted)
                + ', margin=' + str(self._margin)
                + ', spacing=' + str(self._spacing)
                + ', showAxes=' + str(self._showAxes)
                + ', type=' + str(self._type)
                + ', zoomType=' + str(self._zoomType)
                + ', alignTicks=' + str(self._alignTicks)
                + ', animation=' + str(self._animation)
                + ', className=' + str(self._className)
                + ', reflow=' + str(self._reflow)
                + ', shadow=' + str(self._shadow)
                + ', plot=' + str(self._plot)
                + ', style=' + str(self._style) + ']')


class Plot(object):
    """This class represents drawing area of the chart and contains methods
    specific to it.

    @author chirag:
    """

    def __init__(self):
        self._backgroundColor = None
        self._backgroundImage = None
        self._borderColor = None
        self._borderWidth = None
        self._shadow = None

    def getBackgroundColor(self):
        return self._backgroundColor

    def setBackgroundColor(self, backgroundColor):
        self._backgroundColor = backgroundColor

    def getBackgroundImage(self):
        return self._backgroundImage

    def setBackgroundImage(self, backgroundImage):
        self._backgroundImage = backgroundImage

    def getBorderColor(self):
        return self._borderColor

    def setBorderColor(self, borderColor):
        self._borderColor = borderColor

    def getBorderWidth(self):
        return self._borderWidth

    def setBorderWidth(self, borderWidth):
        self._borderWidth = borderWidth

    def getShadow(self):
        return self._shadow

    def setShadow(self, shadow):
        self._shadow = shadow

    def __str__(self):
        return ('Plot [backgroundColor=' + str(self._backgroundColor)
                + ', backgroundImage=' + str(self._backgroundImage)
                + ', borderColor=' + str(self._borderColor)
                + ', borderWidth=' + str(self._borderWidth)
                + ', shadow=' + str(self._shadow) + ']')


class Spacing(object):
    """This class represents space around the chart. The boundary of the
    chart includes axis, axis labels, legend, chart title and subtitle.

    @author: Invient
    @author: Richard Lincoln
    """
    def __init__(self):
        self._left = None
        self._top = None
        self._right = None
        self._bottom = None

    def getLeft(self):
        return self._left

    def setLeft(self, left):
        self._left = left

    def getTop(self):
        return self._top

    def setTop(self, top):
        self._top = top

    def getRight(self):
        return self._right

    def setRight(self, right):
        self._right = right

    def getBottom(self):
        return self._bottom

    def setBottom(self, bottom):
        self._bottom = bottom

    def __str__(self):
        return ('Spacing [left=' + str(self._left)
                + ', top=' + str(self._top)
                + ', right=' + str(self._right)
                + ', bottom=' + str(self._bottom)
                + ']')


class Margin(object):
    """This class represents margin between the outer edge of the chart
    and the plot area.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, top=None, right=None, bottom=None, left=None):
        self._top = top
        self._right = right
        self._bottom = bottom
        self._left = left

    def getLeft(self):
        return self._left

    def setLeft(self, left):
        self._left = left

    def getTop(self):
        return self._top

    def setTop(self, top):
        self._top = top

    def getRight(self):
        return self._right

    def setRight(self, right):
        self._right = right

    def getBottom(self):
        return self._bottom

    def setBottom(self, bottom):
        self._bottom = bottom

    def __str__(self):
        return ('Margin [left=' + str(self._left)
                + ', top=' + str(self._top)
                + ', right=' + str(self._right)
                + ', bottom=' + str(self._bottom)
                + ']')


class ZoomType(object):
    """The value L{ZoomType.X} represents horizontal zoom. The value
    L{ZoomType.Y} represents vertical zoom. The value
    L{ZoomType.XY} represents horizontal as well as vertical zoom.

    @author: Invient
    @author: Richard Lincoln
    """
    X = None
    Y = None
    XY = None
    NONE = None

    def __init__(self, typ):
        self._type = typ

    def getName(self):
        return self._type

    @classmethod
    def values(cls):
        return [cls.X, cls.Y, cls.XY, cls.NONE]


ZoomType.X = ZoomType('x')
ZoomType.Y = ZoomType('y')
ZoomType.XY = ZoomType('xy')
ZoomType.NONE = ZoomType('')


class SeriesConfig(object):
    """This class contains general configuration options for all series
    types such as line, area and pie.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self):
        self._allowPointSelect = None
        self._animation = None
        self._enableMouseTracking = None
        self._showInLegend = None
        self._cursor = None
        # No impact in case of Pie chart
        self._stacking = None
        self._showCheckbox = None
        # private Boolean selected;
        self._visible = None
        # NA for pie
        self._shadow = None
        # NA for pie and scatter
        self._hoverState = None
        self._dataLabel = None
        self._color = None


    def getAllowPointSelect(self):
        """@return"""
        return self._allowPointSelect


    def setAllowPointSelect(self, allowPointSelect):
        """If the argument is true then the points of a can be selected
        otherwise not. Defaults to false, The point on a chart will toggle.
        Also, whenever a point is selected or deselected, the registered
        event listeners will be triggered.

        @param allowPointSelect
        """
        self._allowPointSelect = allowPointSelect


    def getAnimation(self):
        return self._animation


    def setAnimation(self, animation):
        """If the argument is true then animation will be enabled when a
        series will be displayed otherwise not. Defaults to false.

        @param animation
        """
        self._animation = animation


    def getEnableMouseTracking(self):
        """@return"""
        return self._enableMouseTracking


    def setEnableMouseTracking(self, enableMouseTracking):
        """If the argument is true then the mouse tracking will be enabled
        for a series otherwise not. Defaults to true.

        @param enableMouseTracking
        """
        self._enableMouseTracking = enableMouseTracking


    def getShowInLegend(self):
        """@return"""
        return self._showInLegend


    def setShowInLegend(self, showInLegend):
        """If the argument is true then a series will be displayed in the
        legend otherwise not. Defaults to true.

        @param showInLegend
        """
        self._showInLegend = showInLegend


    def getCursor(self):
        """@return"""
        return self._cursor


    def setCursor(self, cursor):
        """Sets the cursor style. E.g. cursor can be set to css cursor style
        'pointer', 'hand' or any other. Defaults to null.

        @param cursor
        """
        self._cursor = cursor


    def getStacking(self):
        """@return"""
        return self._stacking


    def setStacking(self, stacking):
        """Specifies whether the values of each series should be stacked on
        top of each other or not. Defaults to null. If the argument is null
        then the values of each series are not stacked.

        @param stacking
        """
        self._stacking = stacking


    def getShowCheckbox(self):
        """@return"""
        return self._showCheckbox


    def setShowCheckbox(self, showCheckbox):
        """If the argument is true then a checkbox is displayed next to the
        legend item in the legend area. Defaults to false

        @param showCheckbox
        """
        self._showCheckbox = showCheckbox


    def getVisible(self):
        """@return"""
        return self._visible


    def setVisible(self, visible):
        """If the argument is true then the series is visible otherwise not
        when a chart is rendered initially. Defaults to true However, this
        is not applicable for series related to Pie chart.

        @param visible
        @raise NotImplementedError:
                    If this method is invoked on L{PieConfig}
        """
        self._visible = visible


    def getShadow(self):
        """@return"""
        return self._shadow


    def setShadow(self, shadow):
        """If the argument is true then a shadow will be shown to the graph
        line otherwise not. Defaults to true.

        @param shadow:
        @raise NotImplementedError:
                    If this method is invoked on L{PieConfig}
        """
        self._shadow = shadow


    def getHoverState(self):
        """@return"""
        return self._hoverState


    def setHoverState(self, state):
        """Sets attributes which should be applied to a series when series
        is hovered.

        @param state
        """
        self._hoverState = state


    def getDataLabel(self):
        """@return"""
        return self._dataLabel


    def setDataLabel(self, dataLabel):
        """Sets how point value should be formatted and displayed for each
        point.

        @param dataLabel
        """
        self._dataLabel = dataLabel


    def getColor(self):
        """@return"""
        return self._color


    def setColor(self, color):
        """Sets color for the series.

        @param color
        """
        self._color = color


class DataLabel(object):
    """This class contains various attributes to format data labels. The
    data labels are displayed along with points and axis.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, enabled=True):
        """If the argument is true then the datalabels will be displayed
        otherwise not.

        @param enabled
        """
        self._align = None
        # NA for pie
        self._enabled = True
        self._formatterJsFunc = None
        self._rotation = None
        self._style = None
        self._x = None
        self._y = None
        self._color = None


    def getAlign(self):
        """@return"""
        return self._align


    def setAlign(self, align):
        """@param align"""
        self._align = align


    def getEnabled(self):
        """@return"""
        return self._enabled


    def setEnabled(self, enabled):
        """If the argument is true then the datalabels will be displayed
        otherwise not.

        @param enabled
        """
        self._enabled = enabled


    def getFormatterJsFunc(self):
        """@return"""
        return self._formatterJsFunc


    def setFormatterJsFunc(self, formatterJsFunc):
        """Sets the argument string JavaScript function. This function will
        be called to format the data label. Refer to highchart documentation
        for more details on this
        U{http://www.highcharts.com/ref/#plotOptions-series-dataLabels}

        @param formatterJsFunc
        """
        self._formatterJsFunc = formatterJsFunc


    def getRotation(self):
        """@return"""
        return self._rotation


    def setRotation(self, rotation):
        """Sets text rotation in degrees

        @param rotation
        """
        self._rotation = rotation


    def getStyle(self):
        """@return"""
        return self._style


    def setStyle(self, style):
        """Sets css style for the data label

        @param style
        """
        self._style = style


    def getX(self):
        """@return"""
        return self._x


    def setX(self, x):
        """Sets the x position offset of the label relative to the point.
        Defaults to 0.

        @param x
        """
        self._x = x


    def getY(self):
        """@return"""
        return self._y


    def setY(self, y):
        """Sets the y position offset of the label relative to the point.
        Defaults to -6.

        @param y
        """
        self._y = y


    def getColor(self):
        """@return"""
        return self._color


    def setColor(self, color):
        """Sets color for the data labels. e.g. if the color is blue then in
        case of line series, for each point, the data label will be displayed
        in blue color.

        @param color
        """
        self._color = color


    def __str__(self):
        return ('DataLabel [align=' + str(self._align)
                + ', enabled=' + str(self._enabled)
                + ', formatter=' + str(self._formatterJsFunc)
                + ', rotation=' + str(self._rotation)
                + ', style=' + str(self._style)
                + ', x=' + str(self._x)
                + ', y=' + str(self._y) + ']')


class PieDataLabel(DataLabel):
    """This class contains configuration attributes of data labels specific
    to Pie series.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, enabled=False):
        """If the argument is true then the datalabels will be displayed
        otherwise not.

        @param enabled
        """
        self._connectorWidth = None
        self._connectorColor = None
        self._connectorPadding = None
        self._distance = None

        super(PieDataLabel, self).__init__(enabled)


    def getConnectorWidth(self):
        """@return"""
        return self._connectorWidth


    def setConnectorWidth(self, connectorWidth):
        """Sets width (in pixel) of the line connecting the data label to
        the pie slice. Defaults to 1.

        @param connectorWidth
        """
        self._connectorWidth = connectorWidth


    def getConnectorColor(self):
        """@return"""
        return self._connectorColor


    def setConnectorColor(self, connectorColor):
        """Sets the color of the line connecting the data label to the pie
        slice.

        @param connectorColor
        """
        self._connectorColor = connectorColor


    def getConnectorPadding(self):
        """@return"""
        return self._connectorPadding


    def setConnectorPadding(self, connectorPadding):
        """Sets the distance (in pixel) from the data label to the connector.
        Defaults to 5.

        @param connectorPadding
        """
        self._connectorPadding = connectorPadding


    def getDistance(self):
        """@return"""
        return self._distance


    def setDistance(self, distance):
        """Sets the distance (in pixel) of the data label from the pie's edge.

        @param distance
        """
        self._distance = distance


    def __str__(self):
        return ('PieDataLabel [connectorWidth=' + str(self._connectorWidth)
                + ', connectorColor=' + str(self._connectorColor)
                + ', connectorPadding=' + str(self._connectorPadding)
                + ', distance=' + str(self._distance)
                + ', getAlign()=' + str(self.getAlign())
                + ', getEnabled()=' + str(self.getEnabled())
                + ', getFormatter()=' + str(self.getFormatterJsFunc())
                + ', getRotation()=' + str(self.getRotation())
                + ', getStyle()=' + str(self.getStyle())
                + ', getX()=' + str(self.getX())
                + ', getY()=' + str(self.getY())
                + ', __str__()=' + super(PieDataLabel, self).__str__()
                + ', __class__=' + self.__class__
                + ', __hash__()=' + self.__hash__() + ']')


class AxisDataLabel(DataLabel):
    """This class contains configuration properties for axis labels. The axis
    labels are the one which are displayed for each tick.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, enabled=False):
        """If the argument is true then the data labels will be displayed
        otherwise not.

        @param enabled
        """
        self._step = None

        super(AxisDataLabel, self).__init__(enabled)


    def getStep(self):
        """@return"""
        return self._step


    def setStep(self, step):
        """Sets at what interval the labels on the axis should be displayed.
        Setting the step to 2 shows every other label. Defaults to null

        @param step
        """
        self._step = step


class XAxisDataLabel(AxisDataLabel):
    """This class contains configuration properties specifically for x-axis
    labels.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, enabled=False):
        """If the argument is true then the data labels will be displayed
        otherwise not.

        @param enabled
        """
        self._staggerLines = None

        super(XAxisDataLabel, self).__init__(enabled)


    def getStaggerLines(self):
        """@return"""
        return self._staggerLines


    def setStaggerLines(self, staggerLines):
        """Sets number of lines to spread the labels over to make room or
        tighter labels.

        @param staggerLines
        """
        self._staggerLines = staggerLines


class YAxisDataLabel(AxisDataLabel):
    """This class contains configuration properties specifically for x-axis
    labels.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, enabled=False):
        """If the argument is true then the data labels will be displayed
        otherwise not.

        @param enabled
        """
        super(YAxisDataLabel, self).__init__(enabled)


class BaseLineConfig(SeriesConfig):
    """This class contains configuration options for line series such as
    line and area but not column series.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self):
        super(BaseLineConfig, self).__init__()

        self._pointStart = None
        self._pointInterval = None
        self._stickyTracking = None
        self._marker = None
        self._dashStyle = None
        self._lineWidth = None


    def getPointStart(self):
        """@return"""
        return self._pointStart


    def setPointStart(self, pointStart):
        """If no x values are given for the points in a series, the argument
        pointStart defines on what value to start. Defaults to 0. e.g. if a
        series contains values higher than 2 m $ then sets pointStart to
        2,000,000

        @param pointStart
        """
        self._pointStart = pointStart


    def getPointInterval(self):
        """@return"""
        return self._pointInterval


    def setPointInterval(self, pointInterval):
        """If no x values are given for the points in a series, the argument
        pointInterval defines the interval of the x values. For example, if
        a series contains one value every day then set pointInterval to
        24 * 3600 * 1000

        @param pointInterval
        """
        self._pointInterval = pointInterval


    def getStickyTracking(self):
        """@return"""
        return self._stickyTracking


    def setStickyTracking(self, stickyTracking):
        """If the argument is true then the mouseout event on a series is not
        triggered until mouse moves over another series or comes out of the
        plot area. If the argument is true then the mouseout event occurs as
        soon as mouse leaves area near to the point or marker

        @param stickyTracking
        """
        self._stickyTracking = stickyTracking


    def getMarker(self):
        """@return"""
        return self._marker


    def setMarker(self, marker):
        """Sets marker for points of a series

        @param marker
        """
        self._marker = marker


    def getDashStyle(self):
        """@return"""
        return self._dashStyle


    def setDashStyle(self, dashStyle):
        """Sets dash style to use when drawing a series.

        @param dashStyle
        """
        self._dashStyle = dashStyle


    def getLineWidth(self):
        """@return"""
        return self._lineWidth


    def setLineWidth(self, lineWidth):
        """Sets width of a line

        @param lineWidth
        """
        self._lineWidth = lineWidth


class DashStyle(object):

    SOLID = None
    SHORT_DASH = None
    SHORT_DOT = None
    SHORT_DASH_DOT = None
    SHORT_DASH_DOT_DOT = None
    DOT = None
    DASH = None
    LONG_DASH = None
    DASH_DOT = None
    LONG_DASH_DOT = None
    LONG_DASH_DOT_DOT = None

    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    @classmethod
    def values(cls):
        return [cls.SOLID, cls.SHORT_DASH, cls.SHORT_DOT, cls.SHORT_DASH_DOT,
                cls.SHORT_DASH_DOT_DOT, cls.DOT, cls.DASH, cls.LONG_DASH,
                cls.DASH_DOT, cls.LONG_DASH_DOT, cls.LONG_DASH_DOT_DOT]

DashStyle.SOLID = DashStyle('Solid')
DashStyle.SHORT_DASH = DashStyle('ShortDash')
DashStyle.SHORT_DOT = DashStyle('ShortDot')
DashStyle.SHORT_DASH_DOT = DashStyle('ShortDashDot')
DashStyle.SHORT_DASH_DOT_DOT = DashStyle('ShortDashDotDot')
DashStyle.DOT = DashStyle('Dot')
DashStyle.DASH = DashStyle('Dash')
DashStyle.LONG_DASH = DashStyle('LongDash')
DashStyle.DASH_DOT = DashStyle('DashDot')
DashStyle.LONG_DASH_DOT = DashStyle('LongDashDot')
DashStyle.LONG_DASH_DOT_DOT = DashStyle('LongDashDotDot')


class AreaConfig(BaseLineConfig):
    """This class contains configuration options for area series, area and
    areaspline.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self):
        super(AreaConfig, self).__init__()

        self._fillColor = None
        self._lineColor = None
        self._fillOpacity = None
        self._threshold = None


    def getFillColor(self):
        """@return Returns fill color of the area."""
        return self._fillColor


    def setFillColor(self, fillColor):
        """Sets fill gradient for the area

        @param fillColor
        """
        self._fillColor = fillColor


    def getLineColor(self):
        """@return: Returns color of a line drawing above the area"""
        return self._lineColor


    def setLineColor(self, lineColor):
        """Sets line color for the line of an area.

        @param lineColor
        """
        self._lineColor = lineColor


    def getFillOpacity(self):
        """@return: Returns opacity (transparency) which will be used when
        the area is filled with the fill color"""
        return self._fillOpacity


    def setFillOpacity(self, fillOpacity):
        """Sets opacity for the area

        @param fillOpacity
        """
        self._fillOpacity = fillOpacity


    def getThreshold(self):
        """@return: Returns threadshold of the area"""
        return self._threshold


    def setThreshold(self, threshold):
        """Sets threshold value which servers as the base for the area, for
        distinguishing between values above and below a threshold. Defaults
        to 0.

        @param threshold
        """
        self._threshold = threshold


class AreaSplineConfig(AreaConfig):
    """This class contains configuration options for areaspline series

    @author: Invient
    @author: Richard Lincoln
    """
    pass


class LineConfig(BaseLineConfig):
    """This class contains configuration options for line series

    @author: Invient
    @author: Richard Lincoln
    """
    def __init__(self):
        super(LineConfig, self).__init__()
        self._step = None


    def getStep(self):
        """@return: Returns true if the line should be drawn using steps
        otherwise false."""
        return self._step


    def setStep(self, step):
        """If the argument is true then line will be drawn using steps
        otherwise not. Defaults to false.

        @param step
        """
        self._step = step


class ScatterConfig(BaseLineConfig):
    """This class contains configuration options for scatter series

    @author: Invient
    @author: Richard Lincoln
    """

    def setShadow(self, shadow):
        """@param shadow:
        @raise NotImplementedError:
                       Scatter series does not support shadow so this method
                       throws an exception if invoked.
        """
        raise NotImplementedError, 'Scatter chart does not support shadow.'


    def getShadow(self):
        """@return: Returns null as scatter series does not have shadow."""
        return None


class SplineConfig(BaseLineConfig):
    """This class contains configuration options for spline series

    @author: Invient
    @author: Richard Lincoln
    """
    pass


class PieConfig(SeriesConfig):
    """This class contains configuration options for pie series.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self):
        super(PieConfig, self).__init__()

        self._centerX = None
        self._centerY = None
        self._borderColor = None
        self._borderWidth = None
        self._innerSize = None
        self._size = None
        self._slicedOffset = None


    def getCenterX(self):
        """@return: Returns x position (in pixel) of the center of the pie
        chart relative to the plot area.
        """
        return self._centerX


    def setCenterX(self, centerX):
        """Sets x position (in pixel) of the center of the pie chart relative
        to the plot area.

        @param centerX
        """
        self._centerX = centerX


    def getCenterY(self):
        """@return: Returns y position (in pixel) of the center of the pie
        chart relative to the plot area.
        """
        return self._centerY


    def setCenterY(self, centerY):
        """Sets y position (in pixel) of the center of the pie chart relative
        to the plot area.

        @param centerY
        """
        self._centerY = centerY


    def getBorderColor(self):
        """@return: Returns color of border surrounding each slice."""
        return self._borderColor


    def setBorderColor(self, borderColor):
        """Sets color of border surrounding each slice.

        @param borderColor
        """
        self._borderColor = borderColor


    def getBorderWidth(self):
        """@return: Returns width of the border surrounding each slice."""
        return self._borderWidth


    def setBorderWidth(self, borderWidth):
        """Sets width of border surrounding each slice.

        @param borderWidth
        """
        self._borderWidth = borderWidth


    def getInnerSize(self):
        """@return: Returns size of the inner diameter of the pie."""
        return self._innerSize


    def setInnerSize(self, innerSize):
        """Sets the size of the inner diameter for the pie. Any value greater
        than 0 renders a donut chart.

        @param innerSize
        """
        self._innerSize = innerSize


    def getSize(self):
        """@return: Returns size of diameter of the pie relative to the plot
        area."""
        return self._size


    def setSize(self, size):
        """Sets size of diameter of the pie relative to the plot area.

        @param size
        """
        self._size = size


    def getSlicedOffset(self):
        """@return: Returns offset in pixel by which a slice should be moved
        out from the center.
        """
        return self._slicedOffset


    def setSlicedOffset(self, slicedOffset):
        """Sets offset in pixel by which a slice should be moved out from the
        center.

        @param slicedOffset
        """
        self._slicedOffset = slicedOffset


    def setVisible(self, visible):
        """@raise NotimplementedError:
                       Pie chart does not support visible property so this
                       method throws an exception if invoked.
        """
        raise NotImplementedError('Pie chart does not support visible property.')


    def setShadow(self, shadow):
        """@raise NotImplementedError:
                       Pie chart does not support shadow property so this
                       method throws an exception if invoked.
        """
        raise NotImplementedError('Pie chart does not support shadow.')


    def getVisible(self):
        """@return: Returns null as pie does not support toggle (show/hide
        pie) feature."""
        return None


    def getShadow(self):
        """@return: Returns null as pie series does not support shadow."""
        return None


    def setDataLabel(self, dataLabel):
        """Sets an object of L{PieDataLabel} which contains configuration
        for formatting data labels.

        @param dataLabel
        """
        super(PieConfig, self).setDataLabel(dataLabel)


    def getDataLabel(self):
        return super(PieConfig, self).getDataLabel()


    def setHoverState(self, state):
        """Sets state which should be applied to a slice when a mouse is
        over the slice

        @param state
        """
        super(PieConfig, self).setHoverState(state)


    def getHoverState(self):
        if (isinstance(super(PieConfig, self).getHoverState(),
                       NonLinearSeriesState)):
            return super(PieConfig, self).getHoverState()
        return None


class BaseBarConfig(SeriesConfig):
    """This class contains configuration options for bar and column series.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self):
        super(BaseBarConfig, self).__init__()

        self._borderColor = None
        self._borderRadius = None
        self._borderWidth = None
        self._colorByPoint = None
        self._groupPadding = None
        self._minPointLength = None
        self._pointPadding = None
        self._pointWidth = None


    def getBorderColor(self):
        """@return"""
        return self._borderColor


    def setBorderColor(self, borderColor):
        """Sets the color of the border surronding each column or bar.

        @param borderColor
        """
        self._borderColor = borderColor


    def getBorderRadius(self):
        """@return"""
        return self._borderRadius


    def setBorderRadius(self, borderRadius):
        """Sets corner radius of the border surronding each column or bar.

        @param borderRadius
        """
        self._borderRadius = borderRadius


    def getBorderWidth(self):
        """@return"""
        return self._borderWidth


    def setBorderWidth(self, borderWidth):
        """Sets width of the border surronding each column or bar.

        @param borderWidth
        """
        self._borderWidth = borderWidth


    def getColorByPoint(self):
        """@return"""
        return self._colorByPoint


    def setColorByPoint(self, colorByPoint):
        """If the argument is true then each point (bar or column in a series
        will have a different color otherwise all points (bars/columns) of a
        series will have same color.

        @param colorByPoint
        """
        self._colorByPoint = colorByPoint


    def getGroupPadding(self):
        """@return"""
        return self._groupPadding


    def setGroupPadding(self, groupPadding):
        """Sets padding between each value groups, in x axis units. Defaults
        to 0.2.

        @param groupPadding
        """
        self._groupPadding = groupPadding


    def getMinPointLength(self):
        """@return"""
        return self._minPointLength


    def setMinPointLength(self, minPointLength):
        """Sets the minimal height for a column or width for a bar. By default,
        0 values are not shown. To visualize a 0 (or close to zero) point,
        set the minimal point length to a pixel value like 3. In stacked
        column charts, minPointLength might not be respected for tightly
        packed values. Defaults to 0. (For detail, refer to
        U{http://www.highcharts.com/ref/#plotOptions-bar});

        @param minPointLength
        """
        self._minPointLength = minPointLength


    def getPointPadding(self):
        """@return"""
        return self._pointPadding


    def setPointPadding(self, pointPadding):
        """Sets padding between each column or bar, in x axis units.

        @param pointPadding
        """
        self._pointPadding = pointPadding


    def getPointWidth(self):
        """@return"""
        return self._pointWidth


    def setPointWidth(self, pointWidth):
        """Sets width of each bar or column in pixel.

        @param pointWidth
        """
        self._pointWidth = pointWidth


    def setHoverState(self, state):
        """Sets state which should be applied to a bar or column when a
        mouse is over the bar or column

        @param state
        """
        super(BaseBarConfig, self).setHoverState(state)


    def getHoverState(self):
        if (isinstance(super(BaseBarConfig, self).getHoverState(),
                       NonLinearSeriesState)):
            return super(BaseBarConfig, self).getHoverState()
        return None


class ColumnConfig(BaseBarConfig):
    """This class contains configuration options for column series.

    @author: Invient
    @author: Richard Lincoln
    """
    pass


class BarConfig(BaseBarConfig):
    """This class contains configuration options for bar series.

    @author: Invient
    @author: Richard Lincoln
    """
    pass


class Stacking(object):
    """Defines ways in which series of a chart can be stacked.

    Stacking.Normal - represents that the values of each series are stacked.

    Stacking.Percent - represents that the the values of each series are
    stacked based on percentage of sum of total value, where total value is
    sum of values of all points on a particular tick of an axis.

    @author Invient
    """
    NORMAL = None
    PERCENT = None

    def __init__(self, stacking):
        self._stacking = stacking

    def getName(self):
        return self._stacking

    @classmethod
    def values(cls):
        return [cls.NORMAL, cls.PERCENT]

Stacking.NORMAL = Stacking('normal')
Stacking.PERCENT = Stacking('percent')


class PointConfig(object):
    """Defines configuration per point in a series. It is possible to assign
    each point a different color and marker.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, sliced_or_color_or_marker, selected=None, color=None,
                marker=None):
        """Creates an instance of this class with specified argument. The
        sliced attribute has meaning only for Pie chart/series.

        @param sliced_or_color_or_marker:
                   - If true then the slice of a pie will be at an offset
                   from the center of the pie. Applicable only for Pie
                   chart/series.
        @param selected:
                   - If true then the point, to which this object is
                   associated, will be shown as selected otherwise not.
        @param color:
                   - Specifies individual color for a point, to which this
                   object is associated.
        @param marker:
                   - Specifies marker for a point, to which this object is
                   associated.
        @see: L{Marker}
        @see: L{Color}
        """
        if selected is None:
            if isinstance(sliced_or_color_or_marker, Marker):
                marker = sliced_or_color_or_marker
                sliced = selected = color = None
            elif isinstance(sliced_or_color_or_marker, IPaint):
                color = sliced_or_color_or_marker
                sliced = selected = marker = None
            else:
                sliced = selected = sliced_or_color_or_marker
                marker = color = None

        super(PointConfig, self).__init__()
        self._sliced = sliced
        self._selected = selected
        self._color = color
        self._marker = marker


    def getSliced(self):
        """@return"""
        return self._sliced


    def setSliced(self, sliced):
        """@param sliced"""
        self._sliced = sliced


    def getSelected(self):
        """@return"""
        return self._selected


    def setSelected(self, selected):
        """@param selected"""
        self._selected = selected


    def getColor(self):
        """@return"""
        return self._color


    def setColor(self, color):
        """@param color"""
        self._color = color


    def getMarker(self):
        """@return"""
        return self._marker


    def setMarker(self, marker):
        """@param marker"""
        self._marker = marker


    def __str__(self):
        """@return: Returns string representation of this object."""
        return ('PointConfig [sliced=' + str(self._sliced)
                + ', selected=' + str(self._selected)
                + ', color=' + str(self._color)
                + ', marker=' + str(self._marker)
                + ']')


class TitleBase(object):
    """A chart has a title and a subtitle. This class defines attributes
    which are common to both.

    The text of a title can be plain text or html text containing html
    elements. It is also possible to apply css to the title. The css must
    be valid css string e.g. { color: 'red' }

    @author: Invient
    @author: Richard Lincoln

    @see: L{Title}
    @see: L{SubTitle}
    @see: L{HorzAlign}
    @see: L{VertAlign}
    """

    def __init__(self):
        self._align = None
        self._vertAlign = None
        self._floating = None
        self._text = None
        self._x = None
        self._y = None
        self._style = None


    def getAlign(self):
        return self._align


    def setAlign(self, align):
        """Sets horizontal alignment of the title. Defaults to HorzAlign.CENTER
        """
        self._align = align


    def getVertAlign(self):
        return self._vertAlign


    def setVertAlign(self, vertAlign):
        """Sets horizontal alignment of the title. Defaults to VertAlign.TOP
        """
        self._vertAlign = vertAlign


    def getFloating(self):
        return self._floating


    def setFloating(self, floating):
        """If the argument is true then the plot area will not move to make
        space for the chart title. Defaults to false.
        """
        self._floating = floating


    def getText(self):
        return self._text


    def setText(self, text):
        """Sets text for the chart's title. The text can be plain or html
        string.
        """
        self._text = text


    def getX(self):
        return self._x


    def setX(self, x):
        """Sets x position (in pixel) of the title relative to the alignment
        within Spacing.left and Spacing.right. Defaults to 0
        """
        self._x = x


    def getY(self):
        return self._y


    def setY(self, y):
        """Sets y position (in pixel) of the title relative to the alignment
        within Spacing.top and Spacing.bottom. Defaults to 0
        """
        self._y = y


    def getStyle(self):
        return self._style


    def setStyle(self, style):
        """Sets css for the title. The css must be a valid css object. e.g. css
        string "{ color:'red' }" is valid but "{ color: 'red'" is invalid.
        """
        self._style = style


class Title(TitleBase):
    """Defines attributes of chart title.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self):
        super(Title, self).__init__()
        self._margin = None


    def getMargin(self):
        return self._margin


    def setMargin(self, margin):
        """Sets margin (in pixel) between the chart title and subtitle, if any.
        If chart subtitle doesn't exist then it indicates the margin between
        subtitle and plotarea. Defaults to 15
        """
        self._margin = margin


class SubTitle(TitleBase):
    """Defines attributes of chart subtitle.

    @author: Invient
    @author: Richard Lincoln
    """
    pass


class HorzAlign(object):

    LEFT = None
    CENTER = None
    RIGHT = None

    def __init__(self, align):
        self._align = align

    def getName(self):
        return self._align

    @classmethod
    def values(cls):
        return [cls.LEFT, cls.CENTER, cls.RIGHT]

HorzAlign.LEFT = HorzAlign('left')
HorzAlign.CENTER = HorzAlign('center')
HorzAlign.RIGHT = HorzAlign('right')


class VertAlign(object):

    TOP = None
    MIDDLE = None
    BOTTOM = None

    def __init__(self, align):
        self._align = align

    def getName(self):
        return self._align

    @classmethod
    def values(cls):
        return [cls.TOP, cls.MIDDLE, cls.BOTTOM]

VertAlign.TOP = VertAlign('top')
VertAlign.MIDDLE = VertAlign('middle')
VertAlign.BOTTOM = VertAlign('bottom')


class State(object):
    """Defines state for a series and point. A series can be in hover state.
    A point can be in hover and select state. In each state, a series and a
    point can have different visual clues. This is achived by setting some
    attributes of a seires and point.

    @author: Invient
    @author: Richard Lincoln

    @see: L{SeriesState}
    """

    def getEnabled(self):
        pass


class SeriesState(State):
    """Defines a set of attributes which will be applied to a series upon
    hover. The attributes linWidth is not applicable for Pie, Scatter, Bar
    and Column series.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self):
        self._enabled = None
        self._lineWidth = None


    def getEnabled(self):
        return self._enabled


    def setEnabled(self, enabled):
        """If the argument is true then the other properties of this class
        have impact on visual rendering of the series when a series is hovered
        or when a mouse is over the legend. Enabling this has a performance
        penalty.

        Defaults to false.
        """
        self._enabled = enabled


    def getLineWidth(self):
        return self._lineWidth


    def setLineWidth(self, lineWidth):
        """Sets width of a line in pixel. Defaults to 2.
        """
        self._lineWidth = lineWidth


class NonLinearSeriesState(SeriesState):
    """Defines a set of attributes which are meaningful for bar and colum
    series.

    @author: Invient
    @author: Richard Lincoln
    """
    def __init__(self):
        self._brightness = None


    def getBrightness(self):
        return self._brightness


    def setBrightness(self, brightness):
        """Sets intensity of brightness for a point. This applies only to
        bar and column series/chart

        Defaults to 0.1
        """
        self._brightness = brightness


class MarkerAttribute(object):
    """Defines a collection of attributes which makes a marker. Markers
    are generally used to annotate a graph points.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self):
        self._enabled = None
        self._fillColor = None
        self._lineColor = None
        self._lineWidth = None
        self._radius = None

    def getEnabled(self):
        return self._enabled

    def setEnabled(self, enabled):
        self._enabled = enabled

    def getFillColor(self):
        return self._fillColor

    def setFillColor(self, fillColor):
        self._fillColor = fillColor

    def getLineColor(self):
        return self._lineColor

    def setLineColor(self, lineColor):
        self._lineColor = lineColor

    def getLineWidth(self):
        return self._lineWidth

    def setLineWidth(self, lineWidth):
        self._lineWidth = lineWidth

    def getRadius(self):
        return self._radius

    def setRadius(self, radius):
        self._radius = radius

    def __str__(self):
        return ('MarkerStateAttribute [enabled=' + str(self._enabled)
                + ', fillColor=' + str(self._fillColor)
                + ', lineColor=' + str(self._lineColor)
                + ', lineWidth=' + str(self._lineWidth)
                + ', radius=' + str(self._radius)
                + ']')


class MarkerState(State):
    """Defines a set of attributes which gets applied to a point when a point
    is selected or hovered. By default, markers are enabled so when a mouse is
    over a point marker gets applied. To turn off marker, set flag enabled to
    false.

    A point marker is useful only if the marker is not an image.

    @author: Invient
    @author: Richard Lincoln

    @see: L{ImageMarker}
    @see: L{SymbolMarker}
    """

    def __init__(self, enabled=True):
        """Creates this marker with specified argument. If enabled = false
        then the marker will not be applied to a point on hover or select
        state.
        """
        self._markerAttribute = MarkerAttribute()

        self._markerAttribute.setEnabled(True)


    def getEnabled(self):
        return self._markerAttribute.getEnabled()


    def setEnabled(self, enabled):
        """If enabled = false then the marker will not be applied to a point
        on hover or select state. Defaults to true
        """
        self._markerAttribute.setEnabled(enabled)


    def getFillColor(self):
        return self._markerAttribute.getFillColor()


    def setFillColor(self, fillColor):
        """Sets fill color for the marker. When not specified it takes color
        of a series or point.
        """
        self._markerAttribute.setFillColor(fillColor)


    def getLineColor(self):
        return self._markerAttribute.getLineColor()


    def setLineColor(self, lineColor):
        """Sets color of the point marker's outline. When not specified it
        takes color of a series or point.
        """
        self._markerAttribute.setLineColor(lineColor)


    def getLineWidth(self):
        return self._markerAttribute.getLineWidth()


    def setLineWidth(self, lineWidth):
        """Sets width of the point marker's outline. Defaults to 0.
        """
        self._markerAttribute.setLineWidth(lineWidth)


    def getRadius(self):
        return self._markerAttribute.getRadius()


    def setRadius(self, radius):
        """Sets radius of the point marker. Defaults to 0.
        """
        self._markerAttribute.setRadius(radius)


    def __str__(self):
        return ('MarkerState [enabled=' + str(self.getEnabled())
                + ', fillColor=' + str(self.getFillColor())
                + ', lineColor=' + str(self.getLineColor())
                + ', lineWidth=' + str(self.getLineWidth())
                + ', radius=' + str(self.getRadius())
                + ']')


class Marker(object):
    """Defines a marker for a point. Markers are applied to a point of
    chart's series. The marker can be applied at the time of drawing the
    chart or when a point is selcted or hovered.

    There are two types of marker.
      * L{SymbolMarker}
      * L{ImageMarker}

    @author: Invient
    @author: Richard Lincoln

    @see: L{SymbolMarker}
    @see: L{ImageMarker}
    """

    def getEnabled(self):
        raise NotImplementedError

    def setEnabled(self, enabled):
        raise NotImplementedError


class AbstractMarker(Marker):
    """Defines attributes for a marker.

    @author: Invient
    @author: Richard Lincoln

    @see: L{SymbolMarker}
    @see: L{ImageMarker}
    """

    def __init__(self, enabled=True):
        self._markerAttribute = MarkerAttribute()
        self._markerAttribute.setEnabled(enabled)

    def getLineColor(self):
        return self._markerAttribute.getLineColor()

    def setLineColor(self, lineColor):
        self._markerAttribute.setLineColor(lineColor)

    def getFillColor(self):
        return self._markerAttribute.getFillColor()

    def setFillColor(self, fillColor):
        self._markerAttribute.setFillColor(fillColor)

    def getLineWidth(self):
        return self._markerAttribute.getLineWidth()

    def setLineWidth(self, lineWidth):
        self._markerAttribute.setLineWidth(lineWidth)

    def getRadius(self):
        return self._markerAttribute.getRadius()

    def setRadius(self, radius):
        self._markerAttribute.setRadius(radius)

    def getEnabled(self):
        return self._markerAttribute.getEnabled()

    def setEnabled(self, enabled):
        self._markerAttribute.setEnabled(enabled)


class ImageMarker(AbstractMarker):
    """This marker can take url of an image which will be used as a marker
    for a point or all points of a series.

    The url of an image must be with respect to root of the web application.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, imageURL, enabled=True):
        """Creates this marker with specified arguments.

        @param imageURL:
                   - URL of an image
        @param enabled:
                   - If false then this marker will not be applied to a
                   point. What this means is that the data points of a line
                   chart will not stand out.
        """
        super(ImageMarker, self).__init__(enabled)
        self._imageURL = imageURL


    def getImageURL(self):
        return self._imageURL


    def setImageURL(self, imageURL):
        self._imageURL = imageURL


    def __str__(self):
        return ('ImageMarker [imageURL=' + str(self._imageURL)
                + ', enabled' + str(self.getEnabled())
                + ']')


class SymbolMarker(AbstractMarker):
    """This marker has predefined shape which cannot be changed. However,
    marker attributes can be set.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, *args):
        """Creates this marker with enabled = true
        ---
        Creates this marker with specified arguments.

        @param enabled
                   If false then this marker will not be applied to a point.
                   What this means is that the data points of a line chart
                   will not stand out.
        ---
        Creates this marker with specified arguments.

        @param lineColor
                   - Color of the point marker's outline
        ---
        Creates this marker with specified arguments.

        @param radius
                   Radius of the point marker.
        ---
        Creates this marker with specified arguments.

        @param symbol
                   It must be one of the predefine symbol such as
                   Symbol.CIRCLE or Symbol.DIAMOND
        ---
        Creates this marker with specified arguments.

        @param lineColor
                   Color of the point marker's outline
        @param radius
                   Radius of the point marker.
        ---
        Creates this marker with specified arguments.

        @param lineColor
                   - Color of the point marker's outline
        @param radius
                   Radius of the point marker.
        @param symbol
                   It must be one of the predefine symbol such as
                   Symbol.CIRCLE or Symbol.DIAMOND
        """
        self._symbol = None
        self._hoverState = None
        self._selectState = None

        nargs = len(args)
        if nargs == 0:
            super(SymbolMarker, self).__init__(True)
        elif nargs == 1:
            if isinstance(args[0], IPaint):
                lineColor, = args
                super(SymbolMarker, self).__init__(True)
                super(SymbolMarker, self).setLineColor(lineColor)
            elif isinstance(args[0], bool):
                enabled, = args
                super(SymbolMarker, self).__init__(enabled)
            elif isinstance(args[0], int):
                radius, = args
                super(SymbolMarker, self).__init__(True)
                self.setRadius(radius)
            else:
                symbol, = args
                super(SymbolMarker, self).__init__(True)
                self._symbol = symbol
        elif nargs == 2:
            lineColor, radius = args
            super(SymbolMarker, self).__init__(True)
            super(SymbolMarker, self).setLineColor(lineColor)
            super(SymbolMarker, self).setRadius(radius)
        elif nargs == 3:
            lineColor, radius, symbol = args
            super(SymbolMarker, self).__init__(True)
            super(SymbolMarker, self).setLineColor(lineColor)
            super(SymbolMarker, self).setRadius(radius)
            self._symbol = symbol
        else:
            raise ValueError


    def getLineColor(self):
        return super(SymbolMarker, self).getLineColor()


    def setLineColor(self, lineColor):
        """Sets color of the point marker's outline
        """
        super(SymbolMarker, self).setLineColor(lineColor)


    def getFillColor(self):
        return super(SymbolMarker, self).getFillColor()


    def setFillColor(self, fillColor):
        """Sets color of the point marker
        """
        super(SymbolMarker, self).setFillColor(fillColor)


    def getLineWidth(self):
        return super(SymbolMarker, self).getLineWidth()


    def setLineWidth(self, lineWidth):
        """Sets width of the point marker outline
        """
        super(SymbolMarker, self).setLineWidth(lineWidth)


    def getRadius(self):
        return super(SymbolMarker, self).getRadius()


    def setRadius(self, radius):
        """Sets radius of the point marker
        """
        super(SymbolMarker, self).setRadius(radius)


    def getSymbol(self):
        return self._symbol


    def setSymbol(self, symbol):
        """Sets symbol for the point marker. It must be one of the predefine
        symbol such as Symbol.CIRCLE or Symbol.DIAMOND
        """
        self._symbol = symbol


    def getHoverState(self):
        return self._hoverState


    def setHoverState(self, hoverState):
        """Sets marker to be applied to a point when it is hovered.
        """
        self._hoverState = hoverState


    def getSelectState(self):
        return self._selectState


    def setSelectState(self, selectState):
        """Sets marker to be applied to a point when it is selected.
        """
        self._selectState = selectState


    def __str__(self):
        return ('SymbolMarker [symbol=' + str(self._symbol)
                + ', hoverState=' + str(self._hoverState)
                + ', selectState=' + str(self._selectState)
                + ', getLineColor()=' + str(self.getLineColor())
                + ', getFillColor()=' + str(self.getFillColor())
                + ', getLineWidth()=' + str(self.getLineWidth())
                + ', getRadius()=' + str(self.getRadius())
                + ', getSymbol()=' + str(self.getSymbol())
                + ', getHoverState()=' + str(self.getHoverState())
                + ', getSelectState()=' + str(self.getSelectState())
                + ']')


class Symbol(object):
    """Defines predefined marker shapes to be used along with
    L{SymbolMarker}

    @author: Invient
    @author: Richard Lincoln

    @see: L{SymbolMarker}
    """

    CIRCLE = None
    DIAMOND = None
    SQUARE = None
    TRIANGLE = None
    TRIANGLE_DOWN = None

    def __init__(self, symbol):
        self._symbol = symbol

    def getName(self):
        return self._symbol

    @classmethod
    def values(cls):
        return [cls.CIRCLE, cls.DIAMOND, cls.SQUARE,
                cls.TRIANGLE, cls.TRIANGLE_DOWN]

Symbol.CIRCLE = Symbol('circle')
Symbol.DIAMOND = Symbol('diamond')
Symbol.SQUARE = Symbol('square')
Symbol.TRIANGLE = Symbol('triangle')
Symbol.TRIANGLE_DOWN = Symbol('triangle-down')


class Axis(object):

    def getId(self):
        pass

    def setId(self, Id):
        pass

    def getTick(self):
        pass

    def setTick(self, tick):
        pass

    def getMaxZoom(self):
        pass

    def setMaxZoom(self, maxZoom):
        pass

    def getReversed(self):
        pass

    def setReversed(self, r):
        pass

    def getOpposite(self):
        pass

    def setOpposite(self, opposite):
        pass

    def getType(self):
        pass

    def getTitle(self):
        pass

    def setTitle(self, title):
        pass

    def getAlternateGridColor(self):
        pass

    def setAlternateGridColor(self, alternateGridColor):
        pass

    def getEndOnTick(self):
        pass

    def setEndOnTick(self, endOnTick):
        pass

    def getGrid(self):
        pass

    def setGrid(self, grid):
        pass

    def getLineColor(self):
        pass

    def setLineColor(self, lineColor):
        pass

    def getLineWidth(self):
        pass

    def setLineWidth(self, lineWidth):
        pass

    def getLinkedTo(self):
        pass

    def setLinkedTo(self, linkedTo):
        pass

    def getMaxPadding(self):
        pass

    def setMaxPadding(self, maxPadding):
        pass

    def getMinPadding(self):
        pass

    def setMinPadding(self, minPadding):
        pass

    def getMinorGrid(self):
        pass

    def setMinorGrid(self, minorGrid):
        pass

    def getMinorTick(self):
        pass

    def setMinorTick(self, minorTick):
        pass

    def getOffset(self):
        pass

    def setOffset(self, offset):
        pass

    def getShowFirstLabel(self):
        pass

    def setShowFirstLabel(self, showFirstLabel):
        pass

    def getShowLastLabel(self):
        pass

    def setShowLastLabel(self, showLastLabel):
        pass

    def getStartOfWeek(self):
        pass

    def setStartOfWeek(self, startOfWeek):
        pass

    def getStartOnTick(self):
        pass

    def setStartOnTick(self, startOnTick):
        pass


class XAxis(Axis):
    pass


class YAxis(Axis):
    pass


class AxisBase(Axis):
    """This class defines attributes common to X axis and Y axis. A chart can
    have one or more axis of each type.

    @author: chirag
    @author: Richard Lincoln

    @see: L{XAxis}
    @see: L{YAxis}
    """

    def __init__(self):
        super(AxisBase, self).__init__()

        self._id = None
        self._type = AxisType.LINEAR
        self._title = None
        self._label = None
        self._plotBands = OrderedSet()
        self._plotLines = OrderedSet()
        self._alternateGridColor = None
        self._endOnTick = None
        self._grid = None
        self._lineColor = None
        self._lineWidth = None
        self._linkedTo = None
        self._maxPadding = None
        self._maxZoom = None
        # private Double max;
        # private Double min;
        self._minPadding = None
        self._tick = None
        self._minorGrid = None
        self._minorTick = None
        self._offset = None
        self._opposite = None
        self._reversed = None
        self._showFirstLabel = None
        self._showLastLabel = None
        self._startOfWeek = None
        self._startOnTick = None


    def getAllPlotBands(self):
        return self._plotBands


    def setAllPlotBands(self, plotBands):
        if plotBands is not None:
            self._plotBands = plotBands


    def addPlotBand(self, plotBand):
        self._plotBands.add(plotBand)


    def removePlotBand(self, plotBand_or_id):
        """Removes a plotband with given id.
        """
        if isinstance(plotBand_or_id, PlotBand):
            plotBand = plotBand_or_id
            self._plotBands.remove(plotBand)
        else:
            Id = plotBand_or_id
            for pb in set(self._plotBands):
                if pb.getId() == Id:
                    self._plotBands.remove(pb)
                    break


    def getAllPlotLines(self):
        return self._plotLines


    def setAllPlotLines(self, plotLines):
        if plotLines is not None:
            self._plotLines = plotLines


    def addPlotLine(self, plotLine):
        self._plotLines.add(plotLine)


    def removePlotLine(self, plotLine_or_id):
        if isinstance(plotLine_or_id, PlotLine):
            plotLine = plotLine_or_id
            self._plotLines.remove(plotLine)
        else:
            Id = plotLine_or_id
            for i, pl in enumerate(self._plotLines[:]):
                if pl.getId() == Id:
                    del self._plotLines[i]
                    break


    def getId(self):
        return self._id


    def setId(self, Id):
        """Sets an id for the axis"""
        self._id = Id


    def getTick(self):
        return self._tick


    def setTick(self, tick):
        """Sets tick for the axis"""
        self._tick = tick


    def getMaxZoom(self):
        return self._maxZoom


    def setMaxZoom(self, maxZoom):
        """Sets maximum amount of zoom for this axis. For datetime axis, the
        maxZoom must be specified in milliseconds. For example, for a
        datetime axis the main unit is milliseconds. If maxZoom is set to
        3600000, you can't zoom in more than to one hour. (Above example is
        taken from Highcharts documentation)
        """
        self._maxZoom = maxZoom


    def getReversed(self):
        return self._reversed


    def setReversed(self, r):
        """If the argument it true then this axis will be reversed. Defaults
        to false.
        """
        self._reversed = r


    def getOpposite(self):
        return self._opposite


    def setOpposite(self, opposite):
        """If the argument is true then another axis on the opposite side of
        this axis will be displayed. The normal axis is on left side for
        vertical axes and bottom for horzontal axes.
        """
        self._opposite = opposite


    def getType(self):
        return self._type


    def setType(self, typ):
        """Sets type of this axis. Used by subclasses

        @see: L{NumberXAxis}
        @see: L{NumberYAxis}
        @see: L{DateTimeAxis}
        """
        self._type = typ


    def getTitle(self):
        return self._title


    def setTitle(self, title):
        """Sets title for the axis

        @see: L{AxisTitle}
        """
        self._title = title


    def getLabel(self):
        return self._label


    def setLabel(self, label):
        self._label = label


    def getAlternateGridColor(self):
        return self._alternateGridColor


    def setAlternateGridColor(self, alternateGridColor):
        """Sets a color to be used for alternate grids of the chart"""
        self._alternateGridColor = alternateGridColor


    def getEndOnTick(self):
        return self._endOnTick


    def setEndOnTick(self, endOnTick):
        """If the argument is true then this axis will end on a tick."""
        self._endOnTick = endOnTick


    def getGrid(self):
        return self._grid


    def setGrid(self, grid):
        """Sets grid for this axis

        @see: L{Grid}
        """
        self._grid = grid


    def getLineColor(self):
        return self._lineColor


    def setLineColor(self, lineColor):
        """Sets a color for line of this axis. This line indicate this axis"""
        self._lineColor = lineColor


    def getLineWidth(self):
        return self._lineWidth


    def setLineWidth(self, lineWidth):
        """Sets width of this axis line"""
        self._lineWidth = lineWidth


    def getLinkedTo(self):
        return self._linkedTo


    def setLinkedTo(self, linkedTo):
        """Sets another axis which is linked with this axis. The following
        description is copied from Highcharts API documentation
        U{http://www.highcharts.com/ref/#xAxis}.

        When an axis is linked to a master axis, it will take the same
        extremes as the master, but as assigned by min or max or by
        setExtremes. It can be used to show additional info, or to ease
        reading the chart by duplicating the scales. Defaults to null.
        """
        if linkedTo is not self:
            self._linkedTo = linkedTo


    def getMaxPadding(self):
        return self._maxPadding


    def setMaxPadding(self, maxPadding):
        self._maxPadding = maxPadding


    def getMinPadding(self):
        return self._minPadding


    def setMinPadding(self, minPadding):
        self._minPadding = minPadding


    def getMinorGrid(self):
        return self._minorGrid


    def setMinorGrid(self, minorGrid):
        self._minorGrid = minorGrid


    def getMinorTick(self):
        return self._minorTick


    def setMinorTick(self, minorTick):
        self._minorTick = minorTick


    def getOffset(self):
        return self._offset


    def setOffset(self, offset):
        """Sets distance of this axis from the plot area"""
        self._offset = offset


    def getShowFirstLabel(self):
        return self._showFirstLabel


    def setShowFirstLabel(self, showFirstLabel):
        """If the argument is true then the label of this axis' first tick
        will be displayed. Defaults to true.
        """
        self._showFirstLabel = showFirstLabel


    def getShowLastLabel(self):
        return self._showLastLabel


    def setShowLastLabel(self, showLastLabel):
        """If the argument is true then the label of this axis' last tick
        will be displayed. Defaults to false
        """
        self._showLastLabel = showLastLabel


    def getStartOfWeek(self):
        return self._startOfWeek


    def setStartOfWeek(self, startOfWeek):
        """Sets a day to be considered as start of the week. For datetime axis,
        this decides where to put tick. e.g. if startOfWeek = THURSDAY then
        tick will be placed on every thursday.
        """
        self._startOfWeek = startOfWeek


    def getStartOnTick(self):
        return self._startOnTick


    def setStartOnTick(self, startOnTick):
        """If the argument is true then this axis must start on a tick.
        Defaults to false.
        """
        self._startOnTick = startOnTick


class MinorTick(object):
    """Defines attributes of a minor tick. The minor ticks do not have a
    label. By default, minor ticks are not shown. To display minor ticks,
    set interval property.

    @author: Invient
    @author: Richard Lincoln

    @see: L{Tick}
    """

    def __init__(self):
        self._color = None
        self._interval = None
        self._length = None
        self._position = None
        self._width = None


    def getColor(self):
        return self._color


    def setColor(self, color):
        self._color = color


    def getInterval(self):
        return self._interval


    def setInterval(self, interval):
        """Sets interval for the minor tick. The interval must be specified
        in the axis unit. e.g. If an axis has tick interval of 50 units
        then setting minortick interval to 10 will show 5 minor ticks.
        """
        self._interval = interval


    def getLength(self):
        return self._length


    def setLength(self, length):
        """Sets length of the minorticks in pixel
        """
        self._length = length


    def getPosition(self):
        return self._position


    def setPosition(self, position):
        self._position = position


    def getWidth(self):
        return self._width


    def setWidth(self, width):
        """Sets width of the minorticks in pixel
        """
        self._width = width


    def __str__(self):
        return ('MinorTick [color=' + str(self._color)
                + ', length=' + str(self._length)
                + ', position=' + str(self._position)
                + ', width=' + str(self._width)
                + ']')


class Tick(MinorTick):
    """Defines attributes of a tick marks. The interval of the tick marks
    must be specified in axis unit. For datetime axis, the interval must
    be in millisecond.

    The default tick interval is 1.

    @author: Invient
    @author: Richard Lincoln

    @see: L{MinorTick}
    @see: L{TickmarkPlacement}
    """

    def __init__(self):
        super(Tick, self).__init__()
        self._placement = None
        self._pixelInterval = None


    def getPlacement(self):
        return self._placement


    def setPlacement(self, placement):
        """Sets placement of the tick marks.
        """
        self._placement = placement


    def getPixelInterval(self):
        return self._pixelInterval


    def setPixelInterval(self, pixelInterval):
        """Sets pixel interval of the tick marks
        """
        self._pixelInterval = pixelInterval


    def __str__(self):
        return ('Tick [placement=' + str(self._placement)
                + ', pixelInterval=' + str(self._pixelInterval)
                + ', getColor()=' + str(self.getColor())
                + ', getLength()=' + str(self.getLength())
                + ', getPosition()=' + str(self.getPosition())
                + ', getWidth()=' + str(self.getWidth())
                + ']')


class MinorGrid(object):
    """Defines attributes of minor grid lines of the chart. In order to show
    minor grid lines, you must specify set MinorTick for the axis also.

    @author: Invient
    @author: Richard Lincoln

    @see: L{MinorTick}
    @see: L{Grid}
    """

    def __init__(self):
        self._lineColor = None
        self._lineDashStyle = None
        self._lineWidth = None


    def getLineColor(self):
        return self._lineColor


    def setLineColor(self, lineColor):
        """Sets color of the minor grid lines
        """
        self._lineColor = lineColor


    def getLineDashStyle(self):
        """@return"""
        return self._lineDashStyle


    def setLineDashStyle(self, lineDashStyle):
        """Sets dash or dot style of the minor grid lines. Defaults to
        DashStyle.SOLID

        @see: L{DashStyle}
        """
        self._lineDashStyle = lineDashStyle


    def getLineWidth(self):
        """@return"""
        return self._lineWidth


    def setLineWidth(self, lineWidth):
        """Sets width (in pixel) of the minor grid lines. Defaults to 1
        """
        self._lineWidth = lineWidth


    def __str__(self):
        return ('MinorGrid [lineColor=' + str(self._lineColor)
                + ', lineDashStyle=' + str(self._lineDashStyle)
                + ', lineWidth=' + str(self._lineWidth)
                + ']')


class Grid(MinorGrid):
    """Defines attributes of grid lines of the chart. By default, the grid
    lines are shown. To hide them set property lineWidth to 0.

    @author: Invient
    @author: Richard Lincoln
    """
    pass


class WeekDay(object):

    SUNDAY = 'SUNDAY'
    MONDAY = 'MONDAY'
    TUESDAY = 'TUESDAY'
    WEDNESDAY = 'WEDNESDAY'
    THURSDAY = 'THURSDAY'
    FRIDAY = 'FRIDAY'
    SATURDAY = 'SATURDAY'

    _values = [SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY]

    @classmethod
    def values(cls):
        return cls._values[:]


class TickmarkPlacement(object):
    """Defines position of the tick marks with respect to the axis
    categories. It is applicable only for categorized axes.

    TickmarkPlacement.ON - tick mark is placed in the center of the
    category

    TickmarkPlacement.BETWEEN - tick mark is placed between categories

    @author: Invient
    @author: Richard Lincoln
    """

    ON = None
    BETWEEN = None

    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    @classmethod
    def values(cls):
        return [cls.ON, cls.BETWEEN]

TickmarkPlacement.ON = TickmarkPlacement('on')
TickmarkPlacement.BETWEEN = TickmarkPlacement('between')


class TickPosition(object):
    """Defines position of the axis ticks with respect to the axis line

    @author: Invient
    @author: Richard Lincoln
    """

    OUTSIDE = None
    INSIDE = None

    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    @classmethod
    def values(cls):
        return [cls.OUTSIDE, cls.INSIDE]

TickPosition.OUTSIDE = TickPosition('outside')
TickPosition.INSIDE = TickPosition('inside')


class AxisType(object):
    """Defines axis types.

    AxisType.LINEAR -

    AxisType.DATETIME - For datetime axis, the values are given in date
    except for L{BaseLineConfig.pointStart} and L{BaseLineConfig.pointInterval}
    properties, which are specified in milliseconds.

    @author: Invient
    @author: Richard Lincoln

    @see: L{NumberXAxis}
    @see: L{NumberYAxis}
    @see: L{DateTimeAxis}
    """

    LINEAR = None
    DATETIME = None

    def __init__(self, typ):
        self._type = typ

    def getName(self):
        return self._type

    @classmethod
    def values(cls):
        return [cls.LINEAR, cls.DATETIME]

AxisType.LINEAR = AxisType('linear')
AxisType.DATETIME = AxisType('datetime')


class AxisTitleAlign(object):

    LOW = ['low']
    MIDDLE = ['middle']
    HIGH = ['high']

    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    @classmethod
    def values(cls):
        return [cls.LOW, cls.MIDDLE, cls.HIGH]

AxisTitleAlign.LOW = AxisTitleAlign('low')
AxisTitleAlign.MIDDLE = AxisTitleAlign('middle')
AxisTitleAlign.HIGH = AxisTitleAlign('high')


class AxisTitle(object):

    def __init__(self, text):
        self._text = text
        self._align = None
        self._style = None
        self._rotation = None
        self._margin = None

    def getText(self):
        return self._text

    def setText(self, text):
        self._text = text

    def getAlign(self):
        return self._align

    def setAlign(self, align):
        self._align = align

    def getStyle(self):
        return self._style

    def setStyle(self, style):
        self._style = style

    def getRotation(self):
        return self._rotation

    def setRotation(self, rotation):
        self._rotation = rotation

    def getMargin(self):
        return self._margin

    def setMargin(self, margin):
        self._margin = margin


class PlotLabel(object):

    def __init__(self, text):
        super(PlotLabel, self).__init__()
        self._text = text
        self._align = None
        self._vertAlign = None
        self._rotation = None
        self._style = None
        self._textAlign = None
        self._x = None
        self._y = None

    def getText(self):
        return self._text

    def setText(self, text):
        self._text = text

    def getAlign(self):
        return self._align

    def setAlign(self, align):
        self._align = align

    def getVertAlign(self):
        return self._vertAlign

    def setVertAlign(self, vertAlign):
        self._vertAlign = vertAlign

    def getRotation(self):
        return self._rotation

    def setRotation(self, rotation):
        self._rotation = rotation

    def getStyle(self):
        return self._style

    def setStyle(self, style):
        self._style = style

    def getTextAlign(self):
        return self._textAlign

    def setTextAlign(self, textAlign):
        self._textAlign = textAlign

    def getX(self):
        return self._x

    def setX(self, x):
        self._x = x

    def getY(self):
        return self._y

    def setY(self, y):
        self._y = y


class PlotBand(object):

    def __init__(self, Id):
        self._id = Id
        self._color = None
        self._range = None
        self._zIndex = None
        self._label = None

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color

    def getRange(self):
        return self._range

    def setRange(self, rng):
        self._range = rng

    def getId(self):
        return self._id

    def getZIndex(self):
        return self._zIndex

    def setZIndex(self, zIndex):
        self._zIndex = zIndex

    def getLabel(self):
        return self._label

    def setLabel(self, label):
        self._label = label

    def __hash__(self):
        prime = 31
        result = 1
        result = (prime * result) + (0 if self._id is None else self._id.__hash__())
        return result

    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        if self._id is None:
            if other.id is not None:
                return False
        elif not (self._id == other.id):
            return False
        return True


class Range(object):
    pass


class NumberPlotBand(PlotBand):

    def __init__(self, Id):
        super(NumberPlotBand, self).__init__(Id)

    def getRange(self):
        return super(NumberPlotBand, self).getRange()

    def setRange(self, rang):
        super(NumberPlotBand, self).setRange(rang)


class NumberRange(Range):

    def __init__(self, from_, to):
        super(NumberRange, self).__init__()
        self._from = from_
        self._to = to

    def getFrom(self):
        return self._from

    def setFrom(self, from_):
        self._from = from_

    def getTo(self):
        return self._to

    def setTo(self, to):
        self._to = to


class DateTimePlotBand(PlotBand):

    def __init__(self, Id):
        super(DateTimePlotBand, self).__init__(Id)

    def getRange(self):
        return super(DateTimePlotBand, self).getRange()

    def setRange(self, rang):
        super(DateTimePlotBand, self).setRange(rang)


class DateTimeRange(Range):

    def __init__(self, from_, to):
        super(DateTimeRange, self).__init__()
        self._from = from_
        self._to = to

    def getFrom(self):
        return self._from

    def setFrom(self, from_):
        self._from = from_

    def getTo(self):
        return self._to

    def setTo(self, to):
        self._to = to


class PlotLine(object):

    def __init__(self, Id):
        self._id = Id
        self._color = None
        self._dashStyle = None
        self._value = None
        self._width = 1
        self._zIndex = None
        self._label = None

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color

    def getDashStyle(self):
        return self._dashStyle

    def setDashStyle(self, dashStyle):
        self._dashStyle = dashStyle

    def getId(self):
        return self._id

    def setId(self, Id):
        self._id = Id

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value

    def getWidth(self):
        return self._width

    def setWidth(self, width):
        self._width = width

    def getZIndex(self):
        return self._zIndex

    def setZIndex(self, zIndex):
        self._zIndex = zIndex

    def getLabel(self):
        return self._label

    def setLabel(self, label):
        self._label = label


class Value(object):
    pass


class NumberPlotLine(PlotLine):

    def __init__(self, Id):
        super(NumberPlotLine, self).__init__(Id)

    def getValue(self):
        return super(NumberPlotLine, self).getValue()

    def setValue(self, value):
        super(NumberPlotLine, self).setValue(value)


class NumberValue(Value):

    def __init__(self, value):
        super(NumberValue, self).__init__()
        self._value = value

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value


class DateTimePlotLine(PlotLine):

    def __init__(self, Id):
        super(DateTimePlotLine, self).__init__(Id)

    def getValue(self):
        return super(DateTimePlotLine, self).getValue()

    def setValue(self, value):
        super(DateTimePlotLine, self).setValue(value)


class DateTimeValue(Value):

    def __init__(self, value):
        super(DateTimeValue, self).__init__()
        self._value = value

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value


class NumberAxis(AxisBase):

    def __init__(self):
        super(NumberAxis, self).__init__()
        super(NumberAxis, self).setType(AxisType.LINEAR)
        self._allowDecimals = None
        self._max = None
        self._min = None

    def getAllowDecimals(self):
        return self._allowDecimals

    def setAllowDecimals(self, allowDecimals):
        self._allowDecimals = allowDecimals

    def setMax(self, mx):
        self._max = mx

    def setMin(self, mn):
        self._min = mn

    def getMin(self):
        return self._min

    def getMax(self):
        return self._max

    def getPlotBands(self):
        return super(NumberAxis, self).getAllPlotBands()

    def setPlotBands(self, plotBands):
        super(NumberAxis, self).setAllPlotBands(plotBands)

    def addPlotBand(self, plotBand):
        super(NumberAxis, self).addPlotBand(plotBand)

    def removePlotBand(self, plotBand):
        super(NumberAxis, self).removePlotBand(plotBand)

    def getPlotLines(self):
        return super(NumberAxis, self).getAllPlotLines()

    def setPlotLines(self, plotLines):
        super(NumberAxis, self).setAllPlotLines(plotLines)

    def addPlotLine(self, plotLine):
        super(NumberAxis, self).addPlotLine(plotLine)

    def removePlotLine(self, plotLine):
        super(NumberAxis, self).removePlotLine(plotLine)


class NumberXAxis(NumberAxis, XAxis):

    def setLabel(self, label):
        super(NumberXAxis, self).setLabel(label)

    def getLabel(self):
        return super(NumberXAxis, self).getLabel()


class NumberYAxis(NumberAxis, YAxis):

    def setLabel(self, label):
        super(NumberYAxis, self).setLabel(label)

    def getLabel(self):
        return super(NumberYAxis, self).getLabel()


class DateTimeAxis(AxisBase, XAxis):

    def __init__(self):
        super(DateTimeAxis, self).__init__()
        super(DateTimeAxis, self).setType(AxisType.DATETIME)
        self._dateTimeLabelFormats = None
        self._max = None
        self._min = None

    def getDateTimeLabelFormat(self):
        return self._dateTimeLabelFormats

    def setDateTimeLabelFormat(self, dateTimeLabelFormat):
        self._dateTimeLabelFormats = dateTimeLabelFormat

    def setMax(self, mx):
        self._max = mx

    def setMin(self, mn):
        self._min = mn

    def getMin(self):
        return self._min

    def getMax(self):
        return self._max

    def getPlotBands(self):
        return super(DateTimeAxis, self).getAllPlotBands()

    def setPlotBands(self, plotBands):
        super(DateTimeAxis, self).setAllPlotBands(plotBands)

    def addPlotBand(self, plotBand):
        super(DateTimeAxis, self).addPlotBand(plotBand)

    def removePlotBand(self, plotBand):
        super(DateTimeAxis, self).removePlotBand(plotBand)

    def getPlotLines(self):
        return super(DateTimeAxis, self).getAllPlotLines()

    def setPlotLines(self, plotLines):
        super(DateTimeAxis, self).setAllPlotLines(plotLines)

    def addPlotLine(self, plotLine):
        super(DateTimeAxis, self).addPlotLine(plotLine)

    def removePlotLine(self, plotLine):
        super(DateTimeAxis, self).removePlotLine(plotLine)


class DateTimeLabelFormat(object):
    def __init__(self):
        self._second = '%H:%M:%S'
        self._minute = '%H:%M'
        self._hour = '%H:%M'
        self._day = '%e. %b'
        self._week = '%e. %b'
        self._month = '%b \'%y'
        self._year = '%Y'

    def getSecond(self):
        return self._second

    def setSecond(self, second):
        self._second = second

    def getMinute(self):
        return self._minute

    def setMinute(self, minute):
        self._minute = minute

    def getHour(self):
        return self._hour

    def setHour(self, hour):
        self._hour = hour

    def getDay(self):
        return self._day

    def setDay(self, day):
        self._day = day

    def getWeek(self):
        return self._week

    def setWeek(self, week):
        self._week = week

    def getMonth(self):
        return self._month

    def setMonth(self, month):
        self._month = month

    def getYear(self):
        return self._year

    def setYear(self, year):
        self._year = year

    def __str__(self):
        return ('DateTimeLabelFormat [second=' + self._second
                + ', minute=' + self._minute
                + ', hour=' + self._hour
                + ', day=' + self._day
                + ', week=' + self._week
                + ', month=' + self._month
                + ', year=' + self._year + ']')


class CategoryAxis(AxisBase, XAxis):

    def __init__(self):
        super(CategoryAxis, self).__init__()
        self._categories = list()

    def getCategories(self):
        return self._categories

    def setCategories(self, categories):
        if categories is not None:
            self._categories = categories

    def setLabel(self, label):
        super(CategoryAxis, self).setLabel(label)

    def getLabel(self):
        return super(CategoryAxis, self).getLabel()

    def getPlotBands(self):
        return super(CategoryAxis, self).getAllPlotBands()

    def setPlotBands(self, plotBands):
        super(CategoryAxis, self).setAllPlotBands(plotBands)

    def addPlotBand(self, plotBand):
        super(CategoryAxis, self).addPlotBand(plotBand)

    def removePlotBand(self, plotBand):
        super(CategoryAxis, self).removePlotBand(plotBand)

    def getPlotLines(self):
        return super(CategoryAxis, self).getAllPlotLines()

    def setPlotLines(self, plotLines):
        super(CategoryAxis, self).setAllPlotLines(plotLines)

    def addPlotLine(self, plotLine):
        super(CategoryAxis, self).addPlotLine(plotLine)

    def removePlotLine(self, plotLine):
        super(CategoryAxis, self).removePlotLine(plotLine)


class Legend(object):

    def __init__(self, enabled=True):
        self._backgroundColor = None
        self._borderColor = None
        self._borderRadius = None
        self._borderWidth = None
        self._enabled = enabled
        self._floating = None
        self._itemHiddenStyle = None
        self._itemHoverStyle = None
        self._itemStyle = None
        self._itemWidth = None
        self._layout = None
        self._labelFormatterJsFunc = None
        self._margin = None
        self._reversed = None
        self._shadow = None
        self._symbolPadding = None
        self._symbolWidth = None
        self._width = None
        self._position = None

    def getBackgroundColor(self):
        return self._backgroundColor

    def setBackgroundColor(self, backgroundColor):
        self._backgroundColor = backgroundColor

    def getBorderColor(self):
        return self._borderColor

    def setBorderColor(self, borderColor):
        self._borderColor = borderColor

    def getBorderRadius(self):
        return self._borderRadius

    def setBorderRadius(self, borderRadius):
        self._borderRadius = borderRadius

    def getBorderWidth(self):
        return self._borderWidth

    def setBorderWidth(self, borderWidth):
        self._borderWidth = borderWidth

    def getEnabled(self):
        return self._enabled

    def setEnabled(self, enabled):
        self._enabled = enabled

    def getFloating(self):
        return self._floating

    def setFloating(self, floating):
        self._floating = floating

    def getItemHiddenStyle(self):
        return self._itemHiddenStyle

    def setItemHiddenStyle(self, itemHiddenStyle):
        self._itemHiddenStyle = itemHiddenStyle

    def getItemHoverStyle(self):
        return self._itemHoverStyle

    def setItemHoverStyle(self, itemHoverStyle):
        self._itemHoverStyle = itemHoverStyle

    def getItemStyle(self):
        return self._itemStyle

    def setItemStyle(self, itemStyle):
        self._itemStyle = itemStyle

    def getItemWidth(self):
        return self._itemWidth

    def setItemWidth(self, itemWidth):
        self._itemWidth = itemWidth

    def getLayout(self):
        return self._layout

    def setLayout(self, layout):
        self._layout = layout

    def getLabelFormatterJsFunc(self):
        return self._labelFormatterJsFunc

    def setLabelFormatterJsFunc(self, labelFormatterJsFunc):
        self._labelFormatterJsFunc = labelFormatterJsFunc

    def getMargin(self):
        return self._margin

    def setMargin(self, margin):
        self._margin = margin

    def getReversed(self):
        return self._reversed

    def setReversed(self, r):
        self._reversed = r

    def getShadow(self):
        return self._shadow

    def setShadow(self, shadow):
        self._shadow = shadow

    def getSymbolPadding(self):
        return self._symbolPadding

    def setSymbolPadding(self, symbolPadding):
        self._symbolPadding = symbolPadding

    def getSymbolWidth(self):
        return self._symbolWidth

    def setSymbolWidth(self, symbolWidth):
        self._symbolWidth = symbolWidth

    def getWidth(self):
        return self._width

    def setWidth(self, width):
        self._width = width

    def getPosition(self):
        return self._position

    def setPosition(self, position):
        self._position = position

    def __str__(self):
        return ('Legend [backgroundColor=' + str(self._backgroundColor)
                + ', borderColor=' + str(self._borderColor)
                + ', borderRadius=' + str(self._borderRadius)
                + ', borderWidth=' + str(self._borderWidth)
                + ', enabled=' + str(self._enabled)
                + ', floating=' + str(self._floating)
                + ', itemHiddenStyle=' + str(self._itemHiddenStyle)
                + ', itemHoverStyle=' + str(self._itemHoverStyle)
                + ', itemStyle=' + str(self._itemStyle)
                + ', itemWidth=' + str(self._itemWidth)
                + ', layout=' + str(self._layout)
                + ', labelFormatter=' + str(self._labelFormatterJsFunc)
                + ', margin=' + str(self._margin)
                + ', reversed=' + str(self._reversed)
                + ', shadow=' + str(self._shadow)
                + ', symbolPadding=' + str(self._symbolPadding)
                + ', symbolWidth=' + str(self._symbolWidth)
                + ', width=' + str(self._width)
                + ', position=' + str(self._position)
                + ']')


class Layout(object):

    HORIZONTAL = None
    VERTICAL = None

    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    @classmethod
    def values(cls):
        return [cls.HORIZONTAL, cls.VERTICAL]

Layout.HORIZONTAL = Layout('horizontal')
Layout.VERTICAL = Layout('vertical')


class Credit(object):

    def __init__(self):
        self._enabled = None
        self._link = None
        self._style = None
        self._text = None
        self._position = None

    def getEnabled(self):
        return self._enabled

    def setEnabled(self, enabled):
        self._enabled = enabled

    def getLink(self):
        return self._link

    def setLink(self, link):
        self._link = link

    def getStyle(self):
        return self._style

    def setStyle(self, style):
        self._style = style

    def getText(self):
        return self._text

    def setText(self, text):
        self._text = text

    def getPosition(self):
        return self._position

    def setPosition(self, position):
        self._position = position

    def __str__(self):
        return ('Credit [enabled=' + str(self._enabled)
                + ', link=' + str(self._link)
                + ', style=' + str(self._style)
                + ', text=' + str(self._text)
                + ', position=' + str(self._position)
                + ']')


class Position(object):

    def __init__(self):
        self._align = None
        self._vertAlign = None
        self._x = None
        self._y = None

    def getAlign(self):
        return self._align

    def setAlign(self, align):
        self._align = align

    def getVertAlign(self):
        return self._vertAlign

    def setVertAlign(self, vertAlign):
        self._vertAlign = vertAlign

    def getX(self):
        return self._x

    def setX(self, x):
        self._x = x

    def getY(self):
        return self._y

    def setY(self, y):
        self._y = y

    def __str__(self):
        return ('Position [align=' + str(self._align)
                + ', vertAlign=' + str(self._vertAlign)
                + ', x=' + str(self._x)
                + ', y=' + str(self._y) + ']')


class Tooltip(object):

    def __init__(self):
        self._backgroundColor = None
        self._borderColor = None
        self._borderRadius = None
        self._borderWidth = None
        self._crosshairs = None
        # FIMXE
        self._enabled = None
        self._formatterJsFunc = None
        self._shadow = None
        self._shared = None
        self._snap = None
        # NA for pie/bar/column
        self._style = None

    def getBackgroundColor(self):
        return self._backgroundColor

    def setBackgroundColor(self, backgroundColor):
        self._backgroundColor = backgroundColor

    def getBorderColor(self):
        return self._borderColor

    def setBorderColor(self, borderColor):
        self._borderColor = borderColor

    def getBorderRadius(self):
        return self._borderRadius

    def setBorderRadius(self, borderRadius):
        self._borderRadius = borderRadius

    def getBorderWidth(self):
        return self._borderWidth

    def setBorderWidth(self, borderWidth):
        self._borderWidth = borderWidth

    def getCrosshairs(self):
        return self._crosshairs

    def setCrosshairs(self, crosshairs):
        self._crosshairs = crosshairs

    def getEnabled(self):
        return self._enabled

    def setEnabled(self, enabled):
        self._enabled = enabled

    def getFormatterJsFunc(self):
        return self._formatterJsFunc

    def setFormatterJsFunc(self, formatterJsFunc):
        self._formatterJsFunc = formatterJsFunc

    def getShadow(self):
        return self._shadow

    def setShadow(self, shadow):
        self._shadow = shadow

    def getShared(self):
        return self._shared

    def setShared(self, shared):
        self._shared = shared

    def getSnap(self):
        return self._snap

    def setSnap(self, snap):
        self._snap = snap

    def getStyle(self):
        return self._style

    def setStyle(self, style):
        self._style = style

    def __str__(self):
        return ('Tooltip [backgroundColor=' + str(self._backgroundColor)
                + ', borderColor=' + str(self._borderColor)
                + ', borderRadius=' + str(self._borderRadius)
                + ', borderWidth=' + str(self._borderWidth)
                + ', crosshairs=' + str(self._crosshairs)
                + ', enabled=' + str(self._enabled)
                + ', formatter=' + str(self._formatterJsFunc)
                + ', shadow=' + str(self._shadow)
                + ', shared=' + str(self._shared)
                + ', snap=' + str(self._snap)
                + ', style=' + str(self._style)
                + ']')
