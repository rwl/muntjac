# @INVIENT_COPYRIGHT@
# @MUNTJAC_LICENSE@

from __pyjamas__ import (ARGERROR,)
from com.invient.vaadin.charts.InvientCharts import (InvientCharts,)
from com.invient.vaadin.charts.Paint import (Paint,)
# from java.io.Serializable import (Serializable,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Date import (Date,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedHashMap import (LinkedHashMap,)
# from java.util.LinkedHashSet import (LinkedHashSet,)
# from java.util.List import (List,)
SeriesType = InvientCharts.SeriesType
AxisType = InvientChartsConfig.AxisBase.AxisType
ZoomType = InvientChartsConfig.GeneralChartConfig.ZoomType


class InvientChartsConfig(Serializable):
    """This class encapsulates a number of configuration options for the
    InvientChars. These configuration options are {@link Title}, {@link SubTitle}
    , {@link GeneralChartConfig}, {@link Credit}, {@link Legend}, {@link Tooltip}
    , {@link ChartLabel}, {@link SeriesConfig}, {@link XAxis} and {@link YAxis}

    All configuration properties which are of object type are initialized with an
    object instance.

    These configuration options are static and generally set once. After a chart
    ({@link InvientCharts}) created, any changes made to the configuration options
    will not reflect in the chart. You would have to create a new chart
    {@link InvientCharts}

    For some APIs, the description has been taken from
    http://www.highcharts.com/ref/

    @author Invient
    """
    _title = Title()
    _subtitle = SubTitle()
    _generalChartConfig = GeneralChartConfig()
    _credit = Credit()
    _legend = Legend()
    _tooltip = Tooltip()
    _chartLabel = ChartLabel()
    _seriesTypeConfig = LinkedHashMap()
    _xAxes = LinkedHashSet()
    _yAxes = LinkedHashSet()
    _invientCharts = None

    def getInvientCharts(self):
        return self._invientCharts

    def setInvientCharts(self, invientCharts):
        self._invientCharts = invientCharts

    def getChartLabel(self):
        """@return The {@link ChartLabel} object representing labels at arbitrary
                position in the chart.
        """
        return self._chartLabel

    def setChartLabel(self, chartLabel):
        """Sets the argument {@link ChartLabel} object only if it is non-null

        @param chartLabel
        """
        if chartLabel is not None:
            self._chartLabel = chartLabel

    class ChartLabel(Serializable):
        """The {@link ChartLabel} class represents a set of labels which an be
        placed at arbitrary position in the chart.

        @author Invient
        """
        _style = None
        _labels = list()

        def getStyle(self):
            """@return Returns css style."""
            return self._style

        def setStyle(self, style):
            """Sets css style for all labels in this class

            @param style
                       css style string
            """
            self._style = style

        def getLabels(self):
            """@return Returns a list of {@link ChartLabelItem} objects"""
            return self._labels

        def setLabels(self, labels):
            """Sets a list of {@link ChartLabelItem} objects

            @param labels
            """
            if labels is not None:
                self._labels = labels

        def addLabel(self, label):
            """Appends the specified element at the end of {@link ChartLabelItem}
            list

            @param label
                       element to be appended
            """
            self._labels.add(label)

        def removeLabel(self, label):
            """Removes the specified element from the list of {@link ChartLabelItem}

            @param label
            """
            self._labels.remove(label)

        class ChartLabelItem(Serializable):
            """This class represents a label placed at arbitrary location in the
            chart. The label can have html text and it can be styled using
            css-style.

            @author Invient
            """
            _html = None
            _style = None

            def __init__(self, html, style):
                """Creates a new instance with specified html and style arguments.

                @param html
                @param style
                """
                super(ChartLabelItem, self)()
                self._html = html
                self._style = style

            def getHtml(self):
                """@return Returns html of this label"""
                return self._html

            def setHtml(self, html):
                """Sets html for this label

                @param html
                           It can be plain or html string.
                """
                self._html = html

            def getStyle(self):
                """@return Returns css-style of this label"""
                return self._style

            def setStyle(self, style):
                """Sets css style for this label

                @param style
                """
                self._style = style

    def getXAxes(self):
        """@return Returns a collection of x-axis."""
        return self._xAxes

    def setXAxes(self, xAxes):
        """Sets a collection of x-axis for the chart. The collection of x-axis is
        set only if argument xAxes is non-null.

        @param xAxes
        """
        if xAxes is not None:
            self._xAxes = xAxes

    def addXAxes(self, xAxis):
        """Adds specified x-axis to the collection of x-axis

        @param xAxis
        @return Returns true if the x-axis is added successfully otherwise false
        """
        return self._xAxes.add(xAxis)

    def getYAxes(self):
        """@return Returns a collection of y-axis."""
        return self._yAxes

    def setYAxes(self, yAxes):
        """Sets a collection of y-axis for the chart. The collection of y-axis is
        set only if argument yAxes is non-null

        @param yAxes
        """
        if yAxes is not None:
            self._yAxes = yAxes

    def addYAxes(self, yAxis):
        """Adds specified y-axis to the collection of y-axis

        @param yAxis
        @return Returns true if the y-axis is added successfully otherwise false
        """
        return self._yAxes.add(yAxis)

    def getTitle(self):
        """@return Returns {@link Title} object"""
        return self._title

    def setTitle(self, title):
        """Sets the argument title only if the argument title is non-null

        @param title
        """
        if title is not None:
            self._title = title

    def getSubtitle(self):
        """@return Returns subtitle"""
        return self._subtitle

    def setSubtitle(self, subtitle):
        """Sets the argument subtitle only if the argument is non-null

        @param subtitle
        """
        if subtitle is not None:
            self._subtitle = subtitle

    def getTooltip(self):
        """@return Returns tooltip object associated with this class"""
        return self._tooltip

    def setTooltip(self, tooltip):
        """Sets {@link Tooltip} object only if the argument tooltip is non-null

        @param tooltip
        """
        if tooltip is not None:
            self._tooltip = tooltip

    def getLegend(self):
        """@return Returns legend object of the chart"""
        return self._legend

    def setLegend(self, legend):
        """Sets {@link Legend} object only if the argument legend is non-null

        @param legend
        """
        if legend is not None:
            self._legend = legend

    def getCredit(self):
        """@return Returns credit object of the chart"""
        return self._credit

    def setCredit(self, credit):
        """Sets the {@link Credit} object only if the argument credit is non-null

        @param credit
        """
        if credit is not None:
            self._credit = credit

    def getGeneralChartConfig(self):
        """@return Returns {@link GeneralChartConfig} object"""
        return self._generalChartConfig

    def setGeneralChartConfig(self, generalChartConfig):
        """Sets {@link GeneralChartConfig} object only if the argument is non-null

        @param generalChartConfig
        """
        if generalChartConfig is not None:
            self._generalChartConfig = generalChartConfig

    def getSeriesConfig(self):
        return self._seriesTypeConfig

    def setSeriesConfig(self, seriesConfigs):
        """Sets a set of {@link SeriesConfig} objects only if the argument is
        non-null

        @param seriesConfigs
        """
        if self._seriesTypeConfig is not None:
            self._seriesTypeConfig.clear()
            for config in seriesConfigs:
                self.addSeriesConfig(config)

    def addSeriesConfig(self, seriesConfig):
        """Adds the specified argument only if it is non-null.

        @param seriesConfig
        @throws IllegalArgumentException
                    if the argument is null
        """
        if seriesConfig is None:
            raise self.IllegalArgumentException('Argument SeriesConfig cannot be null.')
        self._seriesTypeConfig.put(self.getSeriesType(seriesConfig), seriesConfig)

    @classmethod
    def getSeriesType(cls, seriesConfig):
        """@param seriesConfig
        @return
        """
        seriesType = SeriesType.COMMONSERIES
        if cls.LineConfig == seriesConfig.getClass():
            seriesType = SeriesType.LINE
        elif cls.SplineConfig == seriesConfig.getClass():
            seriesType = SeriesType.SPLINE
        elif cls.ScatterConfig == seriesConfig.getClass():
            seriesType = SeriesType.SCATTER
        elif cls.AreaConfig == seriesConfig.getClass():
            seriesType = SeriesType.AREA
        elif cls.AreaSplineConfig == seriesConfig.getClass():
            seriesType = SeriesType.AREASPLINE
        elif cls.BarConfig == seriesConfig.getClass():
            seriesType = SeriesType.BAR
        elif cls.ColumnConfig == seriesConfig.getClass():
            seriesType = SeriesType.COLUMN
        elif cls.PieConfig == seriesConfig.getClass():
            seriesType = SeriesType.PIE
        return seriesType

    class GeneralChartConfig(Serializable):
        """This class contains configuration properties at a chart level.

        @author Invient
        """
        _backgroundColor = None
        _borderColor = None
        _borderRadius = None
        _borderWidth = None
        _height = None
        _width = None
        _ignoreHiddenSeries = None
        _inverted = None
        _margin = None
        _spacing = None
        _showAxes = None
        _type = SeriesType.LINE
        _zoomType = ZoomType.NONE
        _clientZoom = True
        _alignTicks = None
        _animation = None
        _className = None
        _reflow = None
        _shadow = None
        _plot = None
        _style = None

        class Plot(Serializable):
            """This class represents drawing area of the chart and contains methods
            specific to it.

            @author chirag
            """
            _backgroundColor = None
            _backgroundImage = None
            _borderColor = None
            _borderWidth = None
            _shadow = None

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

            def toString(self):
                return 'Plot [backgroundColor=' + self._backgroundColor + ', backgroundImage=' + self._backgroundImage + ', borderColor=' + self._borderColor + ', borderWidth=' + self._borderWidth + ', shadow=' + self._shadow + ']'

        class Spacing(Serializable):
            """This class represents space around the chart. The boundary of the
            chart includes axis, axis labels, legend, chart title and subtitle.

            @author Invient
            """
            _left = None
            _top = None
            _right = None
            _bottom = None

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

            def toString(self):
                return 'Spacing [left=' + self._left + ', top=' + self._top + ', right=' + self._right + ', bottom=' + self._bottom + ']'

        class Margin(Serializable):
            """This class represents margin between the outer edge of the chart and
            the plot area.

            @author Invient
            """
            _left = None
            _top = None
            _right = None
            _bottom = None

            def __init__(self, *args):
                _0 = args
                _1 = len(args)
                if _1 == 0:
                    pass # astStmt: [Stmt([]), None]
                elif _1 == 4:
                    top, right, bottom, left = _0
                    self._top = top
                    self._right = right
                    self._bottom = bottom
                    self._left = left
                else:
                    raise ARGERROR(0, 4)

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

            def toString(self):
                return 'Margin [left=' + self._left + ', top=' + self._top + ', right=' + self._right + ', bottom=' + self._bottom + ']'

        def getAlignTicks(self):
            """@return"""
            return self._alignTicks

        def setAlignTicks(self, alignTicks):
            """When using multiple axis, the ticks of two or more opposite axes will
            automatically be aligned by adding ticks to the axis or axes with the
            least ticks. This can be prevented by setting alignTicks to false.

            @param alignTicks
            """
            self._alignTicks = alignTicks

        def getAnimation(self):
            """@return"""
            return self._animation

        def setAnimation(self, animation):
            """Set the overall animation for all chart updating.

            @param animation
            """
            self._animation = animation

        def getClassName(self):
            """@return"""
            return self._className

        def setClassName(self, className):
            """A CSS class name to apply to the charts container

            @param className
            """
            self._className = className

        def getPlot(self):
            """@return Returns plot object representing chart's drawing area"""
            return self._plot

        def setPlot(self, plot):
            """Sets plot object

            @param plot
            """
            self._plot = plot

        def getReflow(self):
            """@return"""
            return self._reflow

        def setReflow(self, reflow):
            """A value of true indicates that the chart will fit the width of the
            charts container otherwise not.

            @param reflow
            """
            self._reflow = reflow

        def getShadow(self):
            """@return"""
            return self._shadow

        def setShadow(self, shadow):
            """A value of true indicates that the drop shadow will apply to the
            outer chart area otherwise not.

            @param shadow
            """
            self._shadow = shadow

        def getStyle(self):
            """@return"""
            return self._style

        def setStyle(self, style):
            """A CSS string to apply to the charts container

            @param style
            """
            self._style = style

        def getBackgroundColor(self):
            """@return"""
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
            """If the argument is true, the axes will scale to the remaining visible
            series once one series is hidden. If the argument is false, hiding
            and showing a series will not affect the axes or the other series.

            @param ignoreHiddenSeries
            """
            self._ignoreHiddenSeries = ignoreHiddenSeries

        def getInverted(self):
            """@return"""
            return self._inverted

        def setInverted(self, inverted):
            """If the argument is true then the x-axis is reversed. If a bar plot is
            present, it will be inverted automatically.

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
            """If the argument is true then the axes will be shown initially. This
            is useful when the chart is empty and axes must be shown.

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

        def setType(self, type):
            """Sets series type to one of line, spline, scatter, area, areaspline,
            pie, bar and column.

            @param type
            """
            self._type = type

        def getZoomType(self):
            """@return"""
            return self._zoomType

        def setZoomType(self, zoomType):
            """Sets zoom type. It decides how a chart can be zoomed by dragging the
            mouse.

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

        def toString(self):
            return 'Chart [backgroundColor=' + self._backgroundColor + ', borderColor=' + self._borderColor + ', borderRadius=' + self._borderRadius + ', borderWidth=' + self._borderWidth + ', height=' + self._height + ', width=' + self._width + ', ignoreHiddenSeries=' + self._ignoreHiddenSeries + ', inverted=' + self._inverted + ', margin=' + self._margin + ', spacing=' + self._spacing + ', showAxes=' + self._showAxes + ', type=' + self._type + ', zoomType=' + self._zoomType + ', alignTicks=' + self._alignTicks + ', animation=' + self._animation + ', className=' + self._className + ', reflow=' + self._reflow + ', shadow=' + self._shadow + ', plot=' + self._plot + ', style=' + self._style + ']'

        class ZoomType(object):
            """The value {@link ZoomType.X} represents horizontal zoom. The value
            {@link ZoomType.Y} represents vertical zoom. The value
            {@link ZoomType.XY} represents horizontal as well as vertical zoom.

            @author Invient
            """
            X = ['x']
            Y = ['y']
            XY = ['xy']
            NONE = ['']
            _type = None

            def __init__(self, type):
                self._type = type

            def getName(self):
                return self._type

            _values = [X, Y, XY, NONE]

            @classmethod
            def values(cls):
                return cls._enum_values[:]

        ZoomType._enum_values = [ZoomType(*v) for v in ZoomType._enum_values]

    class SeriesConfig(Serializable):
        """This class contains general configuration options for all series types
        such as line, area and pie.

        @author Invient
        """
        _allowPointSelect = None
        _animation = None
        _enableMouseTracking = None
        _showInLegend = None
        _cursor = None
        # No impact in case of Pie chart
        _stacking = None
        _showCheckbox = None
        # private Boolean selected;
        _visible = None
        # NA for pie
        _shadow = None
        # NA for pie and scatter
        _hoverState = None
        _dataLabel = None
        _color = None

        def __init__(self):
            pass

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
            """If the argument is true then animation will be enabled when a series
            will be displayed otherwise not. Defaults to false.

            @param animation
            """
            self._animation = animation

        def getEnableMouseTracking(self):
            """@return"""
            return self._enableMouseTracking

        def setEnableMouseTracking(self, enableMouseTracking):
            """If the argument is true then the mouse tracking will be enabled for a
            series otherwise not. Defaults to true.

            @param enableMouseTracking
            """
            self._enableMouseTracking = enableMouseTracking

        def getShowInLegend(self):
            """@return"""
            return self._showInLegend

        def setShowInLegend(self, showInLegend):
            """If the argument is true then a series will be displayed in the legend
            otherwise not. Defaults to true.

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
            """Specifies whether the values of each series should be stacked on top
            of each other or not. Defaults to null. If the argument is null then
            the values of each series are not stacked.

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
            # public Boolean getSelected() {
            # return selected;
            # }
            # public void setSelected(Boolean selected) {
            # this.selected = selected;
            # }
            self._showCheckbox = showCheckbox

        def getVisible(self):
            """@return"""
            # Only in case of Pie chart exception is thrown
            return self._visible

        def setVisible(self, visible):
            """If the argument is true then the series is visible otherwise not when
            a chart is rendered initially. Defaults to true However, this is not
            applicable for series related to Pie chart.

            @param visible
            @throws UnsupportedOperationException
                        If this method is invoked on {@link PieConfig}
            """
            self._visible = visible

        def getShadow(self):
            """@return"""
            # Only in case of Pie and Scatter chart exception is thrown
            return self._shadow

        def setShadow(self, shadow):
            """If the argument is true then a shadow will be shown to the graph line
            otherwise not. Defaults to true.

            @param shadow
            @throws UnsupportedOperationException
                        If this method is invoked on {@link PieConfig}
            """
            self._shadow = shadow

        def getHoverState(self):
            """@return"""
            return self._hoverState

        def setHoverState(self, state):
            """Sets attributes which should be applied to a series when series is
            hovered.

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

    class DataLabel(Serializable):
        """This class contains various attributes to format data labels. The data
        labels are displayed along with points and axis.

        @author Invient
        """
        _align = None
        # NA for pie
        _enabled = Boolean.TRUE.TRUE
        _formatterJsFunc = None
        _rotation = None
        _style = None
        _x = None
        _y = None
        _color = None

        def __init__(self, *args):
            """None
            ---
            If the argument is true then the datalabels will be displayed
            otherwise not.

            @param enabled
            """
            _0 = args
            _1 = len(args)
            if _1 == 0:
                pass # astStmt: [Stmt([]), None]
            elif _1 == 1:
                enabled, = _0
                self._enabled = enabled
            else:
                raise ARGERROR(0, 1)

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
            """Sets the argument string JavaScript function. This function will be
            called to format the data label. Refer to highchart documentation for
            more details on this
            http://www.highcharts.com/ref/#plotOptions-series-dataLabels

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

        def toString(self):
            return 'DataLabel [align=' + self._align + ', enabled=' + self._enabled + ', formatter=' + self._formatterJsFunc + ', rotation=' + self._rotation + ', style=' + self._style + ', x=' + self._x + ', y=' + self._y + ']'

    class PieDataLabel(DataLabel):
        """This class contains configuration attributes of data labels specific to
        Pie series.

        @author Invient
        """
        _connectorWidth = None
        _connectorColor = None
        _connectorPadding = None
        _distance = None

        def __init__(self, *args):
            """None
            ---
            If the argument is true then the datalabels will be displayed
            otherwise not.

            @param enabled
            """
            _0 = args
            _1 = len(args)
            if _1 == 0:
                pass # astStmt: [Stmt([]), None]
            elif _1 == 1:
                enabled, = _0
                super(PieDataLabel, self)(enabled)
            else:
                raise ARGERROR(0, 1)

        def getConnectorWidth(self):
            """@return"""
            return self._connectorWidth

        def setConnectorWidth(self, connectorWidth):
            """Sets width (in pixel) of the line connecting the data label to the
            pie slice. Defaults to 1.

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

        def toString(self):
            return 'PieDataLabel [connectorWidth=' + self._connectorWidth + ', connectorColor=' + self._connectorColor + ', connectorPadding=' + self._connectorPadding + ', distance=' + self._distance + ', getAlign()=' + self.getAlign() + ', getEnabled()=' + self.getEnabled() + ', getFormatter()=' + self.getFormatterJsFunc() + ', getRotation()=' + self.getRotation() + ', getStyle()=' + self.getStyle() + ', getX()=' + self.getX() + ', getY()=' + self.getY() + ', toString()=' + str(super(PieDataLabel, self)) + ', getClass()=' + self.getClass() + ', hashCode()=' + self.hashCode() + ']'

    class AxisDataLabel(DataLabel):
        """This class contains configuration properties for axis labels. The axis
        labels are the one which are displayed for each tick.

        @author Invient
        """
        _step = None

        def __init__(self, *args):
            """None
            ---
            If the argument is true then the data labels will be displayed
            otherwise not.

            @param enabled
            """
            _0 = args
            _1 = len(args)
            if _1 == 0:
                super(AxisDataLabel, self)()
            elif _1 == 1:
                enabled, = _0
                super(AxisDataLabel, self)(enabled)
            else:
                raise ARGERROR(0, 1)

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

        @author Invient
        """
        _staggerLines = None

        def __init__(self, *args):
            """If the argument is true then the data labels will be displayed
            otherwise not.

            @param enabled
            """
            _0 = args
            _1 = len(args)
            if _1 == 0:
                super(XAxisDataLabel, self)()
            elif _1 == 1:
                enabled, = _0
                super(XAxisDataLabel, self)(enabled)
            else:
                raise ARGERROR(0, 1)

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

        @author Invient
        """

        def __init__(self, *args):
            """None
            ---
            If the argument is true then the data labels will be displayed
            otherwise not.

            @param enabled
            """
            _0 = args
            _1 = len(args)
            if _1 == 0:
                super(YAxisDataLabel, self)()
            elif _1 == 1:
                enabled, = _0
                super(YAxisDataLabel, self)(enabled)
            else:
                raise ARGERROR(0, 1)

    class BaseLineConfig(SeriesConfig):
        """This class contains configuration options for line series such as line
        and area but not column series.

        @author Invient
        """
        _pointStart = None
        _pointInterval = None
        _stickyTracking = None
        _marker = None
        _dashStyle = None
        _lineWidth = None

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
            pointInterval defines the interval of the x values. For example, if a
            series contains one value every day then set pointInterval to 24 *
            3600 * 1000

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
        SOLID = ['Solid']
        SHORT_DASH = ['ShortDash']
        SHORT_DOT = ['ShortDot']
        SHORT_DASH_DOT = ['ShortDashDot']
        SHORT_DASH_DOT_DOT = ['ShortDashDotDot']
        DOT = ['Dot']
        DASH = ['Dash']
        LONG_DASH = ['LongDash']
        DASH_DOT = ['DashDot']
        LONG_DASH_DOT = ['LongDashDot']
        LONG_DASH_DOT_DOT = ['LongDashDotDot']
        _name = None

        def __init__(self, name):
            self._name = name

        def getName(self):
            return self._name

        _values = [SOLID, SHORT_DASH, SHORT_DOT, SHORT_DASH_DOT, SHORT_DASH_DOT_DOT, DOT, DASH, LONG_DASH, DASH_DOT, LONG_DASH_DOT, LONG_DASH_DOT_DOT]

        @classmethod
        def values(cls):
            return cls._enum_values[:]

    DashStyle._enum_values = [DashStyle(*v) for v in DashStyle._enum_values]

    class AreaConfig(BaseLineConfig):
        """This class contains configuration options for area series, area and
        areaspline.

        @author Invient
        """
        _fillColor = None
        _lineColor = None
        _fillOpacity = None
        _threshold = None

        def getFillColor(self):
            """@return Returns fill color of the area."""
            return self._fillColor

        def setFillColor(self, fillColor):
            """Sets fill gradient for the area

            @param fillColor
            """
            self._fillColor = fillColor

        def getLineColor(self):
            """@return Returns color of a line drawing above the area"""
            return self._lineColor

        def setLineColor(self, lineColor):
            """Sets line color for the line of an area.

            @param lineColor
            """
            self._lineColor = lineColor

        def getFillOpacity(self):
            """@return Returns opacity (transparency) which will be used when the area is filled with the fill color"""
            return self._fillOpacity

        def setFillOpacity(self, fillOpacity):
            """Sets opacity for the area

            @param fillOpacity
            """
            self._fillOpacity = fillOpacity

        def getThreshold(self):
            """@return Returns threadshold of the area"""
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

        @author Invient
        """
        pass

    class LineConfig(BaseLineConfig):
        """This class contains configuration options for line series

        @author Invient
        """
        _step = None

        def getStep(self):
            """@return Returns true if the line should be drawn using steps otherwise false."""
            return self._step

        def setStep(self, step):
            """If the argument is true then line will be drawn using steps otherwise
            not. Defaults to false.

            @param step
            """
            self._step = step

    class ScatterConfig(BaseLineConfig):
        """This class contains configuration options for scatter series

        @author Invient
        """

        def setShadow(self, shadow):
            """@param shadow
            @exception UnsupportedOperationException
                           Scatter series does not support shadow so this method
                           throws an exception if invoked.
            """
            raise self.UnsupportedOperationException('Scatter chart does not support shadow.')

        def getShadow(self):
            """@return Returns null as scatter series does not have shadow."""
            return None

    class SplineConfig(BaseLineConfig):
        """This class contains configuration options for spline series

        @author Invient
        """
        pass

    def PieConfig(InvientChartsConfig_this, *args, **kwargs):

        class PieConfig(SeriesConfig):
            """This class contains configuration options for pie series.

            @author Invient
            """
            _centerX = None
            _centerY = None
            _borderColor = None
            _borderWidth = None
            _innerSize = None
            _size = None
            _slicedOffset = None

            def getCenterX(self):
                """@return Returns x position (in pixel) of the center of the pie chart relative to
                the plot area.
                """
                return self._centerX

            def setCenterX(self, centerX):
                """Sets x position (in pixel) of the center of the pie chart relative to
                the plot area.

                @param centerX
                """
                self._centerX = centerX

            def getCenterY(self):
                """@return Returns y position (in pixel) of the center of the pie chart relative to
                the plot area.
                """
                return self._centerY

            def setCenterY(self, centerY):
                """Sets y position (in pixel) of the center of the pie chart relative to
                the plot area.

                @param centerY
                """
                self._centerY = centerY

            def getBorderColor(self):
                """@return Returns color of border surrounding each slice."""
                return self._borderColor

            def setBorderColor(self, borderColor):
                """Sets color of border surrounding each slice.

                @param borderColor
                """
                self._borderColor = borderColor

            def getBorderWidth(self):
                """@return Returns width of the border surrounding each slice."""
                return self._borderWidth

            def setBorderWidth(self, borderWidth):
                """Sets width of border surrounding each slice.

                @param borderWidth
                """
                self._borderWidth = borderWidth

            def getInnerSize(self):
                """@return Returns size of the inner diameter of the pie."""
                return self._innerSize

            def setInnerSize(self, innerSize):
                """Sets the size of the inner diameter for the pie. Any value greater
                than 0 renders a donut chart.

                @param innerSize
                """
                self._innerSize = innerSize

            def getSize(self):
                """@return Returns size of diameter of the pie relative to the plot area."""
                return self._size

            def setSize(self, size):
                """Sets size of diameter of the pie relative to the plot area.

                @param size
                """
                self._size = size

            def getSlicedOffset(self):
                """@return Returns offset in pixel by which a slice should be moved out from the
                center.
                """
                return self._slicedOffset

            def setSlicedOffset(self, slicedOffset):
                """Sets offset in pixel by which a slice should be moved out from the
                center.

                @param slicedOffset
                """
                self._slicedOffset = slicedOffset

            def setVisible(self, visible):
                """@exception UnsupportedOperationException
                               Pie chart does not support visible property so this
                               method throws an exception if invoked.
                """
                raise self.UnsupportedOperationException('Pie chart does not support visible property.')

            def setShadow(self, shadow):
                """@exception UnsupportedOperationException
                               Pie chart does not support shadow property so this
                               method throws an exception if invoked.
                """
                raise self.UnsupportedOperationException('Pie chart does not support shadow.')

            def getVisible(self):
                """@return Returns null as pie does not support toggle (show/hide pie) feature."""
                return None

            def getShadow(self):
                """@return Returns null as pie series does not support shadow."""
                return None

            def setDataLabel(self, dataLabel):
                """Sets an object of {@link PieDataLabel} which contains configuration
                for formatting data labels.

                @param dataLabel
                """
                super(PieConfig, self).setDataLabel(dataLabel)

            def getDataLabel(self):
                return super(PieConfig, self).getDataLabel()

            def setHoverState(self, state):
                """Sets state which should be applied to a slice when a mouse is over
                the slice

                @param state
                """
                super(PieConfig, self).setHoverState(state)

            def getHoverState(self):
                if (
                    isinstance(super(PieConfig, self).getHoverState(), InvientChartsConfig_this.NonLinearSeriesState)
                ):
                    return super(PieConfig, self).getHoverState()
                return None

        return PieConfig(*args, **kwargs)

    def BaseBarConfig(InvientChartsConfig_this, *args, **kwargs):

        class BaseBarConfig(SeriesConfig):
            """This class contains configuration options for bar and column series.

            @author Invient
            """
            _borderColor = None
            _borderRadius = None
            _borderWidth = None
            _colorByPoint = None
            _groupPadding = None
            _minPointLength = None
            _pointPadding = None
            _pointWidth = None

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
                """Sets padding between each value groups, in x axis units. Defaults to
                0.2.

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
                http://www.highcharts.com/ref/#plotOptions-bar);

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
                """Sets state which should be applied to a bar or column when a mouse is
                over the bar or column

                @param state
                """
                super(BaseBarConfig, self).setHoverState(state)

            def getHoverState(self):
                if (
                    isinstance(super(BaseBarConfig, self).getHoverState(), InvientChartsConfig_this.NonLinearSeriesState)
                ):
                    return super(BaseBarConfig, self).getHoverState()
                return None

        return BaseBarConfig(*args, **kwargs)

    class ColumnConfig(BaseBarConfig):
        """This class contains configuration options for column series.

        @author Invient
        """
        pass

    class BarConfig(BaseBarConfig):
        """This class contains configuration options for bar series.

        @author Invient
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
        NORMAL = ['normal']
        PERCENT = ['percent']
        _stacking = None

        def __init__(self, stacking):
            self._stacking = stacking

        def getName(self):
            return self._stacking

        _values = [NORMAL, PERCENT]

        @classmethod
        def values(cls):
            return cls._enum_values[:]

    Stacking._enum_values = [Stacking(*v) for v in Stacking._enum_values]

    def PointConfig(InvientChartsConfig_this, *args, **kwargs):

        class PointConfig(Serializable):
            """Defines configuration per point in a series. It is possible to assign
            each point a different color and marker.

            @author Invient
            """
            _sliced = None
            _selected = None
            _color = None
            _marker = None

            def __init__(self, *args):
                """Creates an instance of this class with specified marker

                @param marker
                ---
                Creates an instance of this class with specified color

                @param color
                ---
                Creates an instance of this class with specified argument. The sliced
                attribute has meaning only for Pie chart/series.

                @param sliced
                ---
                @param sliced
                           - If true then the slice of a pie will be at an offset
                           from the center of the pie. Applicable only for Pie
                           chart/series.
                @param selected
                           - If true then the point, to which this object is
                           associated, will be shown as selected otherwise not.
                @param color
                           - Specifies individual color for a point, to which this
                           object is associated.
                @param marker
                           - Specifies marker for a point, to which this object is
                           associated.
                @see Marker
                @see Color
                """
                _0 = args
                _1 = len(args)
                if _1 == 1:
                    if isinstance(_0[0], InvientChartsConfig_this.Marker):
                        marker, = _0
                        self.__init__(None, None, None, marker)
                    elif isinstance(_0[0], Paint):
                        color, = _0
                        self.__init__(None, None, color, None)
                    else:
                        sliced, = _0
                        self.__init__(sliced, sliced, None, None)
                elif _1 == 4:
                    sliced, selected, color, marker = _0
                    super(PointConfig, self)()
                    self._sliced = sliced
                    self._selected = selected
                    self._color = color
                    self._marker = marker
                else:
                    raise ARGERROR(1, 4)

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

            def toString(self):
                """@return Returns string representation of this object."""
                return 'PointConfig [sliced=' + self._sliced + ', selected=' + self._selected + ', color=' + self._color + ', marker=' + self._marker + ']'

        return PointConfig(*args, **kwargs)

    class TitleBase(Serializable):
        """A chart has a title and a subtitle. This class defines attributes which
        are common to both.

        The text of a title can be plain text or html text containing html
        elements. It is also possible to apply css to the title. The css must be
        valid css string e.g. { color: 'red' }

        @author Invient

        @see Title
        @see SubTitle
        @see HorzAlign
        @see VertAlign
        """
        _align = None
        _vertAlign = None
        _floating = None
        _text = None
        _x = None
        _y = None
        _style = None

        def getAlign(self):
            """@return"""
            return self._align

        def setAlign(self, align):
            """Sets horizontal alignment of the title. Defaults to HorzAlign.CENTER

            @param align
            """
            self._align = align

        def getVertAlign(self):
            """@return"""
            return self._vertAlign

        def setVertAlign(self, vertAlign):
            """Sets horizontal alignment of the title. Defaults to VertAlign.TOP

            @param vertAlign
            """
            self._vertAlign = vertAlign

        def getFloating(self):
            """@return"""
            return self._floating

        def setFloating(self, floating):
            """If the argument is true then the plot area will not move to make
            space for the chart title. Defaults to false.

            @param floating
            """
            self._floating = floating

        def getText(self):
            """@return"""
            return self._text

        def setText(self, text):
            """Sets text for the chart's title. The text can be plain or html
            string.

            @param text
            """
            self._text = text

        def getX(self):
            """@return"""
            return self._x

        def setX(self, x):
            """Sets x position (in pixel) of the title relative to the alignment
            within Spacing.left and Spacing.right. Defaults to 0

            @param x
            """
            self._x = x

        def getY(self):
            """@return"""
            return self._y

        def setY(self, y):
            """Sets y position (in pixel) of the title relative to the alignment
            within Spacing.top and Spacing.bottom. Defaults to 0

            @param y
            """
            self._y = y

        def getStyle(self):
            """@return"""
            return self._style

        def setStyle(self, style):
            """Sets css for the title. The css must be a valid css object. e.g. css
            string "{ color:'red' }" is valid but "{ color: 'red'" is invalid.

            @param style
            """
            self._style = style

    class Title(TitleBase):
        """Defines attributes of chart title.

        @author Invient
        """
        _margin = None

        def getMargin(self):
            """@return"""
            return self._margin

        def setMargin(self, margin):
            """Sets margin (in pixel) between the chart title and subtitle, if any.
            If chart subtitle doesn't exist then it indicates the margin between
            subtitle and plotarea. Defaults to 15

            @param margin
            """
            self._margin = margin

    class SubTitle(TitleBase):
        """Defines attributes of chart subtitle.

        @author Invient
        """
        pass

    class HorzAlign(object):
        LEFT = ['left']
        CENTER = ['center']
        RIGHT = ['right']
        _align = None

        def __init__(self, align):
            self._align = align

        def getName(self):
            return self._align

        _values = [LEFT, CENTER, RIGHT]

        @classmethod
        def values(cls):
            return cls._enum_values[:]

    HorzAlign._enum_values = [HorzAlign(*v) for v in HorzAlign._enum_values]

    class VertAlign(object):
        TOP = ['top']
        MIDDLE = ['middle']
        BOTTOM = ['bottom']
        _align = None

        def __init__(self, align):
            self._align = align

        def getName(self):
            return self._align

        _values = [TOP, MIDDLE, BOTTOM]

        @classmethod
        def values(cls):
            return cls._enum_values[:]

    VertAlign._enum_values = [VertAlign(*v) for v in VertAlign._enum_values]

    class State(Serializable):
        """Defines state for a series and point. A series can be in hover state. A
        point can be in hover and select state. In each state, a series and a
        point can have different visual clues. This is achived by setting some
        attributes of a seires and point.

        @author Invient

        @see SeriesState
        """

        def getEnabled(self):
            pass

    class SeriesState(State):
        """Defines a set of attributes which will be applied to a series upon hover.
        The attributes linWidth is not applicable for Pie, Scatter, Bar and
        Column series.

        @author Invient
        """
        _enabled = None
        _lineWidth = None

        def getEnabled(self):
            return self._enabled

        def setEnabled(self, enabled):
            """If the argument is true then the other properties of this class have
            impact on visual rendering of the series when a series is hovered or
            when a mouse is over the legend. Enabling this has a performance
            penalty.

            Defaults to false.

            @param enabled
            """
            self._enabled = enabled

        def getLineWidth(self):
            """@return"""
            return self._lineWidth

        def setLineWidth(self, lineWidth):
            """Sets width of a line in pixel. Defaults to 2.

            @param lineWidth
            """
            self._lineWidth = lineWidth

    class NonLinearSeriesState(SeriesState):
        """Defines a set of attributes which are meaningful for bar and colum
        series.

        @author Invient
        """
        _brightness = None

        def getBrightness(self):
            """@return"""
            return self._brightness

        def setBrightness(self, brightness):
            """Sets intensity of brightness for a point. This applies only to bar
            and column series/chart

            Defaults to 0.1

            @param brightness
            """
            self._brightness = brightness

    class MarkerAttribute(Serializable):
        """Defines a collection of attributes which makes a marker. Markers are
        generally used to annotate a graph points.

        @author Invient
        """
        _enabled = None
        _fillColor = None
        _lineColor = None
        _lineWidth = None
        _radius = None

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

        def toString(self):
            return 'MarkerStateAttribute [enabled=' + self._enabled + ', fillColor=' + self._fillColor + ', lineColor=' + self._lineColor + ', lineWidth=' + self._lineWidth + ', radius=' + self._radius + ']'

    def MarkerState(InvientChartsConfig_this, *args, **kwargs):

        class MarkerState(State):
            """Defines a set of attributes which gets applied to a point when a point is
            selected or hovered. By default, markers are enabled so when a mouse is
            over a point marker gets applied. To turn off marker, set flag enabled to
            false.

            A point marker is useful only if the marker is not an image.

            @author Invient

            @see ImageMarker
            @see SymbolMarker
            """
            _markerAttribute = InvientChartsConfig_this.MarkerAttribute()

            def __init__(self, *args):
                """Creates this marker with enabled = true
                ---
                Creates this marker with specified argument. If enabled = false then
                the marker will not be applied to a point on hover or select state.
                """
                _0 = args
                _1 = len(args)
                if _1 == 0:
                    self._markerAttribute.setEnabled(True)
                elif _1 == 1:
                    enabled, = _0
                    self._markerAttribute.setEnabled(enabled)
                else:
                    raise ARGERROR(0, 1)

            def getEnabled(self):
                return self._markerAttribute.getEnabled()

            def setEnabled(self, enabled):
                """If enabled = false then the marker will not be applied to a point on
                hover or select state. Defaults to true

                @param enabled
                """
                self._markerAttribute.setEnabled(enabled)

            def getFillColor(self):
                """@return"""
                return self._markerAttribute.getFillColor()

            def setFillColor(self, fillColor):
                """Sets fill color for the marker. When not specified it takes color of
                a series or point.

                @param fillColor
                """
                self._markerAttribute.setFillColor(fillColor)

            def getLineColor(self):
                """@return"""
                return self._markerAttribute.getLineColor()

            def setLineColor(self, lineColor):
                """Sets color of the point marker's outline. When not specified it takes
                color of a series or point.

                @param lineColor
                """
                self._markerAttribute.setLineColor(lineColor)

            def getLineWidth(self):
                """@return"""
                return self._markerAttribute.getLineWidth()

            def setLineWidth(self, lineWidth):
                """Sets width of the point marker's outline. Defaults to 0.

                @param lineWidth
                """
                self._markerAttribute.setLineWidth(lineWidth)

            def getRadius(self):
                """@return"""
                return self._markerAttribute.getRadius()

            def setRadius(self, radius):
                """Sets radius of the point marker. Defaults to 0.

                @param radius
                """
                self._markerAttribute.setRadius(radius)

            def toString(self):
                return 'MarkerState [enabled=' + self.getEnabled() + ', fillColor=' + self.getFillColor() + ', lineColor=' + self.getLineColor() + ', lineWidth=' + self.getLineWidth() + ', radius=' + self.getRadius() + ']'

        return MarkerState(*args, **kwargs)

    class Marker(Serializable):
        """Defines a marker for a point. Markers are applied to a point of chart's
        series. The marker can be applied at the time of drawing the chart or
        when a point is selcted or hovered.

        There are two types of marker.
        <ul>
        <li>
        {@link SymbolMarker}</li>
        <li>
        {@link ImageMarker}</li>
        </ul>

        @author Invient

        @see SymbolMarker
        @see ImageMarker
        """

        def getEnabled(self):
            pass

        def setEnabled(self, enabled):
            pass

    def AbstractMarker(InvientChartsConfig_this, *args, **kwargs):

        class AbstractMarker(Marker):
            """Defines attributes for a marker.

            @author Invient

            @see SymbolMarker
            @see ImageMarker
            """
            _markerAttribute = InvientChartsConfig_this.MarkerAttribute()

            def __init__(self, *args):
                _0 = args
                _1 = len(args)
                if _1 == 0:
                    pass # astStmt: [Stmt([]), None]
                elif _1 == 1:
                    enabled, = _0
                    self._markerAttribute.setEnabled(enabled)
                else:
                    raise ARGERROR(0, 1)

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

        return AbstractMarker(*args, **kwargs)

    class ImageMarker(AbstractMarker):
        """This marker can take url of an image which will be used as a marker for a
        point or all points of a series.

        The url of an image must be with respect to root of the web application.
        e.g. If an image named temperature.png is under directory
        <app.root.war>/img/climate then the url must be
        /img/climate/temperature.png

        @author Invient
        """
        _imageURL = None

        def __init__(self, *args):
            """Creates this marker with specified arguments.

            @param imageURL
                       - URL of an image
            @param enabled
                       - If false then this marker will not be applied to a
                       point. What this means is that the data points of a line
                       chart will not stand out.
            ---
            Creates this marker with specified arguments.

            @param imageURL
                       - URL of an image
            """
            _0 = args
            _1 = len(args)
            if _1 == 1:
                imageURL, = _0
                super(ImageMarker, self)(True)
                self._imageURL = imageURL
            elif _1 == 2:
                imageURL, enabled = _0
                super(ImageMarker, self)(enabled)
                self._imageURL = imageURL
            else:
                raise ARGERROR(1, 2)

        def getImageURL(self):
            """@return"""
            return self._imageURL

        def setImageURL(self, imageURL):
            """@param imageURL"""
            self._imageURL = imageURL

        def toString(self):
            return 'ImageMarker [imageURL=' + self._imageURL + ', enabled' + self.getEnabled() + ']'

    class SymbolMarker(AbstractMarker):
        """This marker has predefined shape which cannot be changed. However, marker
        attributes can be set.

        @author Invient
        """
        _symbol = None
        _hoverState = None
        _selectState = None

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
            _0 = args
            _1 = len(args)
            if _1 == 0:
                super(SymbolMarker, self)(True)
            elif _1 == 1:
                if isinstance(_0[0], Paint):
                    lineColor, = _0
                    super(SymbolMarker, self)(True)
                    super(SymbolMarker, self).setLineColor(lineColor)
                elif isinstance(_0[0], boolean):
                    enabled, = _0
                    super(SymbolMarker, self)(enabled)
                elif isinstance(_0[0], int):
                    radius, = _0
                    super(SymbolMarker, self)(True)
                    self.setRadius(radius)
                else:
                    symbol, = _0
                    super(SymbolMarker, self)(True)
                    self._symbol = symbol
            elif _1 == 2:
                lineColor, radius = _0
                super(SymbolMarker, self)(True)
                super(SymbolMarker, self).setLineColor(lineColor)
                super(SymbolMarker, self).setRadius(radius)
            elif _1 == 3:
                lineColor, radius, symbol = _0
                super(SymbolMarker, self)(True)
                super(SymbolMarker, self).setLineColor(lineColor)
                super(SymbolMarker, self).setRadius(radius)
                self._symbol = symbol
            else:
                raise ARGERROR(0, 3)

        def getLineColor(self):
            return super(SymbolMarker, self).getLineColor()

        def setLineColor(self, lineColor):
            """Sets color of the point marker's outline

            @param lineColor
            """
            super(SymbolMarker, self).setLineColor(lineColor)

        def getFillColor(self):
            return super(SymbolMarker, self).getFillColor()

        def setFillColor(self, fillColor):
            """Sets color of the point marker

            @param fillColor
            """
            super(SymbolMarker, self).setFillColor(fillColor)

        def getLineWidth(self):
            return super(SymbolMarker, self).getLineWidth()

        def setLineWidth(self, lineWidth):
            """Sets width of the point marker outline

            @param lineWidth
            """
            super(SymbolMarker, self).setLineWidth(lineWidth)

        def getRadius(self):
            return super(SymbolMarker, self).getRadius()

        def setRadius(self, radius):
            """Sets radius of the point marker

            @param radius
            """
            super(SymbolMarker, self).setRadius(radius)

        def getSymbol(self):
            """@return"""
            return self._symbol

        def setSymbol(self, symbol):
            """Sets symbol for the point marker. It must be one of the predefine
            symbol such as Symbol.CIRCLE or Symbol.DIAMOND

            @param symbol
            """
            self._symbol = symbol

        def getHoverState(self):
            """@return"""
            return self._hoverState

        def setHoverState(self, hoverState):
            """Sets marker to be applied to a point when it is hovered.

            @param hoverState
            """
            self._hoverState = hoverState

        def getSelectState(self):
            """@return"""
            return self._selectState

        def setSelectState(self, selectState):
            """Sets marker to be applied to a point when it is selected.

            @param selectState
            """
            self._selectState = selectState

        def toString(self):
            return 'SymbolMarker [symbol=' + self._symbol + ', hoverState=' + self._hoverState + ', selectState=' + self._selectState + ', getLineColor()=' + self.getLineColor() + ', getFillColor()=' + self.getFillColor() + ', getLineWidth()=' + self.getLineWidth() + ', getRadius()=' + self.getRadius() + ', getSymbol()=' + self.getSymbol() + ', getHoverState()=' + self.getHoverState() + ', getSelectState()=' + self.getSelectState() + ']'

        class Symbol(object):
            """Defines predefined marker shapes to be used along with
            {@link SymbolMarker}

            @author Invient

            @see SymbolMarker
            """
            CIRCLE = ['circle']
            DIAMOND = ['diamond']
            SQUARE = ['square']
            TRIANGLE = ['triangle']
            TRIANGLE_DOWN = ['triangle-down']
            _symbol = None

            def __init__(self, symbol):
                self._symbol = symbol

            def getName(self):
                return self._symbol

            _values = [CIRCLE, DIAMOND, SQUARE, TRIANGLE, TRIANGLE_DOWN]

            @classmethod
            def values(cls):
                return cls._enum_values[:]

        Symbol._enum_values = [Symbol(*v) for v in Symbol._enum_values]

    class AxisBase(Axis):
        """This class defines attributes common to X axis and Y axis. A chart can
        have one or more axis of each type.

        @author chirag

        @see XAxis
        @see YAxis
        """
        _id = None
        _type = AxisType.LINEAR
        _title = None
        _label = None
        _plotBands = LinkedHashSet()
        _plotLines = LinkedHashSet()
        _alternateGridColor = None
        _endOnTick = None
        _grid = None
        _lineColor = None
        _lineWidth = None
        _linkedTo = None
        _maxPadding = None
        _maxZoom = None
        # private Double max;
        # private Double min;
        _minPadding = None
        _tick = None
        _minorGrid = None
        _minorTick = None
        _offset = None
        _opposite = None
        _reversed = None
        _showFirstLabel = None
        _showLastLabel = None
        _startOfWeek = None
        _startOnTick = None

        class MinorTick(Serializable):
            """Defines attributes of a minor tick. The minor ticks do not have a
            label. By default, minor ticks are not shown. To display minor ticks,
            set interval property.

            @author Invient

            @see Tick
            """
            _color = None
            _interval = None
            _length = None
            _position = None
            _width = None

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

                @param interval
                """
                self._interval = interval

            def getLength(self):
                return self._length

            def setLength(self, length):
                """Sets length of the minorticks in pixel

                @param length
                """
                self._length = length

            def getPosition(self):
                """@return"""
                return self._position

            def setPosition(self, position):
                """@param position"""
                self._position = position

            def getWidth(self):
                """@return"""
                return self._width

            def setWidth(self, width):
                """Sets width of the minorticks in pixel

                @param width
                """
                self._width = width

            def toString(self):
                return 'MinorTick [color=' + self._color + ', length=' + self._length + ', position=' + self._position + ', width=' + self._width + ']'

        class Tick(MinorTick):
            """Defines attributes of a tick marks. The interval of the tick marks
            must be specified in axis unit. For datetime axis, the interval must
            be in millisecond.

            The default tick interval is 1.

            @author Invient

            @see MinorTick
            @see TickmarkPlacement
            """
            _placement = None
            _pixelInterval = None

            def getPlacement(self):
                """@return"""
                return self._placement

            def setPlacement(self, placement):
                """Sets placement of the tick marks.

                @param placement
                """
                self._placement = placement

            def getPixelInterval(self):
                """@return"""
                return self._pixelInterval

            def setPixelInterval(self, pixelInterval):
                """Sets pixel interval of the tick marks

                @param pixelInterval
                """
                self._pixelInterval = pixelInterval

            def toString(self):
                return 'Tick [placement=' + self._placement + ', pixelInterval=' + self._pixelInterval + ', getColor()=' + self.getColor() + ', getLength()=' + self.getLength() + ', getPosition()=' + self.getPosition() + ', getWidth()=' + self.getWidth() + ']'

        class MinorGrid(Serializable):
            """Defines attributes of minor grid lines of the chart. In order to show
            minor grid lines, you must specify set MinorTick for the axis also.

            @author Invient
            @see MinorTick
            @see Grid
            """
            _lineColor = None
            _lineDashStyle = None
            _lineWidth = None

            def getLineColor(self):
                return self._lineColor

            def setLineColor(self, lineColor):
                """Sets color of the minor grid lines

                @param lineColor
                """
                self._lineColor = lineColor

            def getLineDashStyle(self):
                """@return"""
                return self._lineDashStyle

            def setLineDashStyle(self, lineDashStyle):
                """Sets dash or dot style of the minor grid lines. Defaults to
                DashStyle.SOLID

                @param lineDashStyle

                @see DashStyle
                """
                self._lineDashStyle = lineDashStyle

            def getLineWidth(self):
                """@return"""
                return self._lineWidth

            def setLineWidth(self, lineWidth):
                """Sets width (in pixel) of the minor grid lines. Defaults to 1

                @param lineWidth
                """
                self._lineWidth = lineWidth

            def toString(self):
                return 'MinorGrid [lineColor=' + self._lineColor + ', lineDashStyle=' + self._lineDashStyle + ', lineWidth=' + self._lineWidth + ']'

        class Grid(MinorGrid):
            """Defines attributes of grid lines of the chart. By default, the grid
            lines are shown. To hide them set property lineWidth to 0.

            @author Invient
            """
            pass

        def getAllPlotBands(self):
            return self._plotBands

        def setAllPlotBands(self, plotBands):
            if plotBands is not None:
                self._plotBands = plotBands

        def addPlotBand(self, plotBand):
            self._plotBands.add(plotBand)

        def removePlotBand(self, *args):
            """None
            ---
            Removes a plotband with given id.

            @param id
            """
            _0 = args
            _1 = len(args)
            if _1 == 1:
                if isinstance(_0[0], self.PlotBand):
                    plotBand, = _0
                    self._plotBands.remove(plotBand)
                else:
                    id, = _0
                    plotBandItr = self._plotBands
                    while plotBandItr.hasNext():
                        if plotBandItr.next().getId() == id:
                            plotBandItr.remove()
                            break
            else:
                raise ARGERROR(1, 1)

        def getAllPlotLines(self):
            """@return"""
            return self._plotLines

        def setAllPlotLines(self, plotLines):
            """@param plotLines"""
            if plotLines is not None:
                self._plotLines = plotLines

        def addPlotLine(self, plotLine):
            """@param plotLine"""
            self._plotLines.add(plotLine)

        def removePlotLine(self, *args):
            """@param plotLine
            ---
            @param id
            """
            _0 = args
            _1 = len(args)
            if _1 == 1:
                if isinstance(_0[0], self.PlotLine):
                    plotLine, = _0
                    self._plotLines.remove(plotLine)
                else:
                    id, = _0
                    plotLineItr = self._plotLines
                    while plotLineItr.hasNext():
                        if plotLineItr.next().getId() == id:
                            plotLineItr.remove()
                            break
            else:
                raise ARGERROR(1, 1)

        def getId(self):
            return self._id

        def setId(self, id):
            """Sets an id for the axis"""
            self._id = id

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

        def setReversed(self, reversed):
            """If the argument it true then this axis will be reversed. Defaults to
            false.
            """
            self._reversed = reversed

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

        def setType(self, type):
            """Sets type of this axis. Used by subclasses

            @param type

            @see NumberXAxis
            @see NumberYAxis
            @see DateTimeAxis
            """
            self._type = type

        def getTitle(self):
            return self._title

        def setTitle(self, title):
            """Sets title for the axis

            @see AxisTitle
            """
            self._title = title

        def getLabel(self):
            """@return"""
            return self._label

        def setLabel(self, label):
            """@param label"""
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

            @see Grid
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
            http://www.highcharts.com/ref/#xAxis.

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
            """If the argument is true then the label of this axis' first tick will
            be displayed. Defaults to true.
            """
            self._showFirstLabel = showFirstLabel

        def getShowLastLabel(self):
            return self._showLastLabel

        def setShowLastLabel(self, showLastLabel):
            """If the argument is true then the label of this axis' last tick will
            be displayed. Defaults to false
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
            """If the argument is true then this axis must start on a tick. Defaults
            to false
            """
            self._startOnTick = startOnTick

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
                return cls._enum_values[:]

        class TickmarkPlacement(object):
            """Defines position of the tick marks with respect to the axis
            categories. It is applicable only for categorized axes.

            TickmarkPlacement.ON - tick mark is placed in the center of the
            category

            TickmarkPlacement.BETWEEN - tick mark is placed between categories

            @author Invient
            """
            ON = ['on']
            BETWEEN = ['between']
            _name = None

            def __init__(self, name):
                self._name = name

            def getName(self):
                return self._name

            _values = [ON, BETWEEN]

            @classmethod
            def values(cls):
                return cls._enum_values[:]

        TickmarkPlacement._enum_values = [TickmarkPlacement(*v) for v in TickmarkPlacement._enum_values]

        class TickPosition(object):
            """Defines position of the axis ticks with respect to the axis line

            @author Invient
            """
            OUTSIDE = ['outside']
            INSIDE = ['inside']
            _name = None

            def __init__(self, name):
                self._name = name

            def getName(self):
                return self._name

            _values = [OUTSIDE, INSIDE]

            @classmethod
            def values(cls):
                return cls._enum_values[:]

        TickPosition._enum_values = [TickPosition(*v) for v in TickPosition._enum_values]

        class AxisType(object):
            """Defines axis types.

            AxisType.LINEAR -

            AxisType.DATETIME - For datetime axis, the values are given in date
            except for {@link BaseLineConfig}.pointStart and {@link BaseLineConfig}.pointInterval
            properties, which are specified in milliseconds.

            @author Invient

            @see NumberXAxis
            @see NumberYAxis
            @see DateTimeAxis
            """
            LINEAR = ['linear']
            DATETIME = ['datetime']
            _type = None

            def __init__(self, type):
                self._type = type

            def getName(self):
                return self._type

            _values = [LINEAR, DATETIME]

            @classmethod
            def values(cls):
                return cls._enum_values[:]

        AxisType._enum_values = [AxisType(*v) for v in AxisType._enum_values]

        class AxisTitleAlign(object):
            LOW = ['low']
            MIDDLE = ['middle']
            HIGH = ['high']
            _name = None

            def __init__(self, name):
                self._name = name

            def getName(self):
                return self._name

            _values = [LOW, MIDDLE, HIGH]

            @classmethod
            def values(cls):
                return cls._enum_values[:]

        AxisTitleAlign._enum_values = [AxisTitleAlign(*v) for v in AxisTitleAlign._enum_values]

        class AxisTitle(Serializable):
            _text = None
            _align = None
            _style = None
            _rotation = None
            _margin = None

            def __init__(self, text):
                self._text = text

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

        class PlotLabel(Serializable):
            _align = None
            _vertAlign = None
            _rotation = None
            _style = None
            _textAlign = None
            _x = None
            _y = None
            _text = None

            def __init__(self, text):
                super(PlotLabel, self)()
                self._text = text

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

        class PlotBand(Serializable):
            _color = None
            _range = None
            _id = None
            _zIndex = None
            _label = None

            def __init__(self, id):
                self._id = id

            def getColor(self):
                return self._color

            def setColor(self, color):
                self._color = color

            def getRange(self):
                return self._range

            def setRange(self, range):
                self._range = range

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

            class Range(Serializable):
                pass

            def hashCode(self):
                prime = 31
                result = 1
                result = (prime * result) + (0 if self._id is None else self._id.hashCode())
                return result

            def equals(self, obj):
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

        class NumberPlotBand(PlotBand):

            def __init__(self, id):
                super(NumberPlotBand, self)(id)

            def getRange(self):
                return super(NumberPlotBand, self).getRange()

            def setRange(self, range):
                super(NumberPlotBand, self).setRange(range)

            class NumberRange(Range):
                _from = None
                _to = None

                def __init__(self, from_, to):
                    super(NumberRange, self)()
                    self._from = from_
                    self._to = to

                def getFrom(self):
                    return self.from_

                def setFrom(self, from_):
                    self._from = from_

                def getTo(self):
                    return self._to

                def setTo(self, to):
                    self._to = to

        class DateTimePlotBand(PlotBand):

            def __init__(self, id):
                super(DateTimePlotBand, self)(id)

            def getRange(self):
                return super(DateTimePlotBand, self).getRange()

            def setRange(self, range):
                super(DateTimePlotBand, self).setRange(range)

            class DateTimeRange(Range):
                _from = None
                _to = None

                def __init__(self, from_, to):
                    super(DateTimeRange, self)()
                    self._from = from_
                    self._to = to

                def getFrom(self):
                    return self.from_

                def setFrom(self, from_):
                    self._from = from_

                def getTo(self):
                    return self._to

                def setTo(self, to):
                    self._to = to

        class PlotLine(Serializable):
            _color = None
            _dashStyle = None
            _id = None
            _value = None
            _width = 1
            _zIndex = None
            _label = None

            def __init__(self, id):
                self._id = id

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

            def setId(self, id):
                self._id = id

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

            class Value(Serializable):
                pass

        class NumberPlotLine(PlotLine):

            def __init__(self, id):
                super(NumberPlotLine, self)(id)

            def getValue(self):
                return super(NumberPlotLine, self).getValue()

            def setValue(self, value):
                super(NumberPlotLine, self).setValue(value)

            class NumberValue(Value):

                def __init__(self, value):
                    super(NumberValue, self)()
                    self._value = value

                _value = None

                def getValue(self):
                    return self._value

                def setValue(self, value):
                    self._value = value

        class DateTimePlotLine(PlotLine):

            def __init__(self, id):
                super(DateTimePlotLine, self)(id)

            def getValue(self):
                return super(DateTimePlotLine, self).getValue()

            def setValue(self, value):
                super(DateTimePlotLine, self).setValue(value)

            class DateTimeValue(Value):
                _value = None

                def __init__(self, value):
                    super(DateTimeValue, self)()
                    self._value = value

                def getValue(self):
                    return self._value

                def setValue(self, value):
                    self._value = value

    class Axis(Serializable):

        def getId(self):
            pass

        def setId(self, id):
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

        def setReversed(self, reversed):
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

    class NumberAxis(AxisBase):
        _allowDecimals = None
        _max = None
        _min = None

        def __init__(self):
            super(NumberAxis, self).setType(AxisType.LINEAR)

        def getAllowDecimals(self):
            return self._allowDecimals

        def setAllowDecimals(self, allowDecimals):
            self._allowDecimals = allowDecimals

        def setMax(self, max):
            self._max = max

        def setMin(self, min):
            self._min = min

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
        _dateTimeLabelFormats = None
        _max = None
        _min = None
        # private Date tickInterval; // FIXME It should be more intuitive to
        # specify tick interval such as
        # Month, Week, day, year similar to
        # private Date minorTickInterval;

        class DateTimeLabelFormat(object):
            _second = '%H:%M:%S'
            _minute = '%H:%M'
            _hour = '%H:%M'
            _day = '%e. %b'
            _week = '%e. %b'
            _month = '%b \'%y'
            _year = '%Y'

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

            def toString(self):
                return 'DateTimeLabelFormat [second=' + self._second + ', minute=' + self._minute + ', hour=' + self._hour + ', day=' + self._day + ', week=' + self._week + ', month=' + self._month + ', year=' + self._year + ']'

        def __init__(self):
            super(DateTimeAxis, self).setType(AxisType.DATETIME)

        def getDateTimeLabelFormat(self):
            return self._dateTimeLabelFormats

        def setDateTimeLabelFormat(self, dateTimeLabelFormat):
            self._dateTimeLabelFormats = dateTimeLabelFormat

        def setMax(self, max):
            self._max = max

        def setMin(self, min):
            self._min = min

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

    class CategoryAxis(AxisBase, XAxis):
        # Legend
        _categories = list()

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

    class Legend(Serializable):
        # Credits
        _backgroundColor = None
        _borderColor = None
        _borderRadius = None
        _borderWidth = None
        _enabled = None
        _floating = None
        _itemHiddenStyle = None
        _itemHoverStyle = None
        _itemStyle = None
        _itemWidth = None
        _layout = None
        _labelFormatterJsFunc = None
        _margin = None
        _reversed = None
        _shadow = None
        _symbolPadding = None
        _symbolWidth = None
        _width = None
        _position = None

        def __init__(self, *args):
            _0 = args
            _1 = len(args)
            if _1 == 0:
                pass # astStmt: [Stmt([]), None]
            elif _1 == 1:
                enabled, = _0
                self._enabled = enabled
            else:
                raise ARGERROR(0, 1)

        class Layout(object):
            HORIZONTAL = ['horizontal']
            VERTICAL = ['vertical']
            _name = None

            def __init__(self, name):
                self._name = name

            def getName(self):
                return self._name

            _values = [HORIZONTAL, VERTICAL]

            @classmethod
            def values(cls):
                return cls._enum_values[:]

        Layout._enum_values = [Layout(*v) for v in Layout._enum_values]

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

        def setReversed(self, reversed):
            self._reversed = reversed

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

        def toString(self):
            return 'Legend [backgroundColor=' + self._backgroundColor + ', borderColor=' + self._borderColor + ', borderRadius=' + self._borderRadius + ', borderWidth=' + self._borderWidth + ', enabled=' + self._enabled + ', floating=' + self._floating + ', itemHiddenStyle=' + self._itemHiddenStyle + ', itemHoverStyle=' + self._itemHoverStyle + ', itemStyle=' + self._itemStyle + ', itemWidth=' + self._itemWidth + ', layout=' + self._layout + ', labelFormatter=' + self._labelFormatterJsFunc + ', margin=' + self._margin + ', reversed=' + self._reversed + ', shadow=' + self._shadow + ', symbolPadding=' + self._symbolPadding + ', symbolWidth=' + self._symbolWidth + ', width=' + self._width + ', position=' + self._position + ']'

    class Credit(Serializable):
        _enabled = None
        _link = None
        _style = None
        _text = None
        _position = None

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

        def toString(self):
            return 'Credit [enabled=' + self._enabled + ', link=' + self._link + ', style=' + self._style + ', text=' + self._text + ', position=' + self._position + ']'

    class Position(Serializable):
        # Tooltip
        _align = None
        _vertAlign = None
        _x = None
        _y = None

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

        def toString(self):
            return 'Position [align=' + self._align + ', vertAlign=' + self._vertAlign + ', x=' + self._x + ', y=' + self._y + ']'

    class Tooltip(Serializable):
        _backgroundColor = None
        _borderColor = None
        _borderRadius = None
        _borderWidth = None
        _crosshairs = None
        # FIMXE
        _enabled = None
        _formatterJsFunc = None
        _shadow = None
        _shared = None
        _snap = None
        # NA for pie/bar/column
        _style = None

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

        def toString(self):
            return 'Tooltip [backgroundColor=' + self._backgroundColor + ', borderColor=' + self._borderColor + ', borderRadius=' + self._borderRadius + ', borderWidth=' + self._borderWidth + ', crosshairs=' + self._crosshairs + ', enabled=' + self._enabled + ', formatter=' + self._formatterJsFunc + ', shadow=' + self._shadow + ', shared=' + self._shared + ', snap=' + self._snap + ', style=' + self._style + ']'
