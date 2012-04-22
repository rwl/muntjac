# @INVIENT_COPYRIGHT@
# @MUNTJAC_LICENSE@

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from muntjac.util \
    import OrderedSet

from datetime \
    import datetime

from muntjac.ui.abstract_component \
    import AbstractComponent

from muntjac.ui.component \
    import Event as ComponentEvent

from muntjac.addon.invient.invient_charts_config \
    import BaseLineConfig, PointConfig, SeriesConfig

from muntjac.addon.invient.invient_charts_util \
    import writeTitleConfig, writeSubtitleConfig, writeCreditConfig, \
    writeLegendConfig, writeTooltipConfig, writeGeneralChartConfig, \
    writeSeriesConfigPerSeriesType, writeXAxes, writeYAxes, \
    writeChartLabelConfig, writeSeries, writeChartDataUpdates, getDate


class InvientCharts(AbstractComponent):
    """A Muntjac component representing charts. It is a the main class of
    InvientCharts library.

    A chart typically contains one or more series of same or different types.
    This class allows us to specify series of different types say line and pie
    and hence it makes it easy to build a combination chart.

    After a chart L{InvientCharts} is created, the following changes to the
    chart will be reflected rendered on the webkit.

      * Set or update chart L{Title} and/or L{SubTitle}
      * Modify chart size
      * Add, update and remove one or more instances of L{PlotBand} and
        L{PlotLine}
      * Set or update axis categories
      * Set or update axis min and max values
      * Add, update and remove one or more instances of L{Series}
      * Show or hide one or more instances of L{Series}
      * Add and remove one or more instances of L{Point}
      * Register and unregister event listeners

    @author: Invient
    @author: Richard Lincoln
    """

    CLIENT_WIDGET = None #ClientWidget(VInvientCharts)

    TYPE_MAPPING = 'com.invient.vaadin.charts.InvientCharts'

    def __init__(self, chartConfig):
        """Creates this chart object with given chart configuration

        @param chartConfig
        """
        if chartConfig is None:
            raise ValueError('The chart cannot be created without '
                    'chartConfig argument.')

        super(InvientCharts, self).__init__()

        self._chartConfig = chartConfig
        self._chartConfig.setInvientCharts(self)

        self._isRetrieveSVG = False
        self._isPrint = False

        self._pointClickListeners = dict()
        self._pointRemoveListeners = dict()
        self._pointUnselectListeners = dict()
        self._pointSelectListeners = dict()
        self._seriesClickListeners = dict()
        self._seriesHideListeners = dict()
        self._seriesShowListeners = dict()
        self._seriesLegendItemClickListeners = dict()
        self._pieChartLegendItemClickListener = set()
        self._chartClickListener = set()
        self._chartAddSeriesListener = set()
        self._chartZoomListener = set()
        self._chartResetZoomListener = set()
        self._svgAvailableListener = None
        self._chartSeries = OrderedSet()
        self._reloadChartSeries = False
        self._seriesCURMap = OrderedDict()


    def getConfig(self):
        """Returns chart configuration object

        @return: Returns chart configuration object
        """
        return self._chartConfig


    def paintContent(self, target):
        super(InvientCharts, self).paintContent(target)

        # Update all series with reference of x and y axis.
        self.setAxisInAllSeriesIfNotSetAlready()

        # Configurations options
        target.startTag('options')
        if self._chartConfig is not None:
            writeTitleConfig(target, self._chartConfig.getTitle())
            writeSubtitleConfig(target, self._chartConfig.getSubtitle())
            writeCreditConfig(target, self._chartConfig.getCredit())
            writeLegendConfig(target, self._chartConfig.getLegend())
            writeTooltipConfig(target, self._chartConfig.getTooltip())
            writeGeneralChartConfig(target,
                    self._chartConfig.getGeneralChartConfig())
            writeSeriesConfigPerSeriesType(target,
                    self._chartConfig.getSeriesConfig())
            writeXAxes(target, self._chartConfig.getXAxes(), self._chartConfig)
            writeYAxes(target, self._chartConfig.getYAxes(), self._chartConfig)
            writeChartLabelConfig(target, self._chartConfig.getChartLabel())
        target.endTag('options')
        target.startTag('chartData')

        writeSeries(target,
                self._chartConfig.getGeneralChartConfig().getType(),
                self._chartSeries,
                self._chartConfig.getXAxes(),
                self._chartConfig.getYAxes())
        target.endTag('chartData')

        # A flag to indicate whether to retrieve svg from client or not.
        target.addAttribute('isRetrieveSVG', self._isRetrieveSVG)

        # A flag to indicate whether to prompt print dialog on client or not
        target.addAttribute('isPrint', self._isPrint)

        # Events
        target.startTag('events')

        # Chart Events
        self.paintChartEvents(target)

        # Series/Point Events
        self.paintSeriesAndPointEvents(target)
        target.endTag('events')

        # If the flag reloadChartData is true then the
        # client will ignore seriesOperations and
        # remove all existing series of a chart and
        # add series info received from the server.
        target.addAttribute('reloadChartSeries', self._reloadChartSeries)
        target.startTag('chartDataUpdates')
        if not self._reloadChartSeries:
            writeChartDataUpdates(target, self._seriesCURMap)
        target.endTag('chartDataUpdates')

        # reset flag
        self._reloadChartSeries = False

        # reset series operations
        self._seriesCURMap.clear()

        # reset to not retrieve svg when other updates on the chart occurs.
        # The svg is retrieved only when a svg available listener is registered
        # on this chart
        self._isRetrieveSVG = False
        self._isPrint = False


    def paintChartEvents(self, target):
        target.startTag('chartEvents')

        if (self._chartAddSeriesListener is not None
                and len(self._chartAddSeriesListener) > 0):
            target.addAttribute('addSeries', True)

        if (self._chartClickListener is not None
                and len(self._chartClickListener) > 0):
            target.addAttribute('click', True)

        if (self._chartZoomListener is not None
                and len(self._chartZoomListener) > 0):
            target.addAttribute('selection', True)

        target.endTag('chartEvents')


    def paintSeriesAndPointEvents(self, target):
        target.startTag('seriesEvents')
        # For each series type, check if listeners exist. If so then add.
        for seriesType in SeriesType.values():
            self.paintSeriesEvents(target, seriesType)
        target.endTag('seriesEvents')


    def paintSeriesEvents(self, target, seriesType):
        tagName = seriesType.getName()
        target.startTag(tagName)

        if (seriesType in self._seriesClickListeners
                and len(self._seriesClickListeners[seriesType]) > 0):
            target.addAttribute('click', True)

        if (seriesType in self._seriesHideListeners
                and len(self._seriesHideListeners[seriesType]) > 0):
            target.addAttribute('hide', True)

        if (seriesType in self._seriesShowListeners
                and len(self._seriesShowListeners[seriesType]) > 0):
            target.addAttribute('show', True)

        if (seriesType in self._seriesLegendItemClickListeners
                and len(self._seriesLegendItemClickListeners[seriesType]) > 0):
            target.addAttribute('legendItemClick', True)

        # Check for point events
        self.paintPointEvents(target, seriesType)
        target.endTag(tagName)


    def paintPointEvents(self, target, seriesType):
        target.startTag('pointEvents')

        if (seriesType in self._pointClickListeners
                and len(self._pointClickListeners[seriesType]) > 0):
            target.addAttribute('click', True)

        if (seriesType in self._pointRemoveListeners
                and len(self._pointRemoveListeners[seriesType]) > 0):
            target.addAttribute('remove', True)

        if (seriesType in self._pointSelectListeners
                and len(self._pointSelectListeners[seriesType]) > 0):
            target.addAttribute('select', True)

        if (seriesType in self._pointUnselectListeners
                and len(self._pointUnselectListeners[seriesType]) > 0):
            target.addAttribute('unselect', True)

        # Event applicable only for pie chart
        if (SeriesType.PIE == seriesType
                and len(self._pieChartLegendItemClickListener) > 0):
            target.addAttribute('legendItemClick', True)

        target.endTag('pointEvents')


    def changeVariables(self, source, variables):
        if 'event' in variables:
            eventData = variables.get('eventData')
            eventName = variables.get('event')
            if eventName.lower() == "addSeries".lower():
                self.fireAddSeries()
            elif eventName.lower() == "chartClick".lower():
                xAxisPos = float(eventData.get("xAxisPos"))
                yAxisPos = float(eventData.get("yAxisPos"))

                mousePosition = self.getClickPosition(eventData)
                self.fireChartClick(DecimalPoint(self, xAxisPos, yAxisPos),
                        mousePosition)
            elif eventName.lower() == "chartZoom".lower():
                xAxisMin = float(eventData.get("xAxisMin"))
                xAxisMax = float(eventData.get("xAxisMax"))
                yAxisMin = float(eventData.get("yAxisMin"))
                yAxisMax = float(eventData.get("yAxisMax"))
                self.fireChartZoom(ChartArea(xAxisMin, xAxisMax, yAxisMin,
                        yAxisMax))
            elif eventName.lower() == "chartResetZoom".lower():
                self.fireChartResetZoom()
            elif eventName.lower() == "chartSVGAvailable".lower():
                self.fireChartSVGAvailable(eventData.get("svg"))
            elif eventName.lower() == "seriesClick".lower():
                pointEventData = self.getPointEventData(eventData)

                mousePosition = self.getClickPosition(eventData)
                self.fireSeriesClick(
                        self.getSeriesFromEventData(
                                pointEventData.getSeriesName()),
                        self.getPointFromEventData(pointEventData),
                        mousePosition)
            elif eventName.lower() == "seriesHide".lower():
                seriesName = eventData.get("seriesName")
                self.fireSeriesHide(self.getSeriesFromEventData(seriesName))
            elif eventName.lower() == "seriesShow".lower():
                seriesName = eventData.get("seriesName")
                self.fireSeriesShow(self.getSeriesFromEventData(seriesName))
            elif eventName.lower() == "seriesLegendItemClick".lower():
                seriesName = eventData.get("seriesName")
                self.fireSeriesLegendItemClick(
                        self.getSeriesFromEventData(seriesName))
            elif eventName.lower() == "pieLegendItemClick".lower():
                pointEventData = self.getPointEventData(eventData)
                self.fireLegendItemClick(
                        self.getPointFromEventData(pointEventData))
            elif eventName.lower() == "pointClick".lower():
                mousePosition = self.getClickPosition(eventData)

                pointEventData = self.getPointEventData(eventData)
                self.firePointClick(pointEventData.getCategory(),
                        self.getPointFromEventData(pointEventData),
                        mousePosition)
            elif eventName.lower() == "pointSelect".lower():
                pointEventData = self.getPointEventData(eventData)
                self.firePointSelect(pointEventData.getCategory(),
                        self.getPointFromEventData(pointEventData))
            elif eventName.lower() == "pointUnselect".lower():
                pointEventData = self.getPointEventData(eventData)
                self.firePointUnselect(pointEventData.getCategory(),
                        self.getPointFromEventData(pointEventData))
            elif eventName.lower() == "pointRemove".lower():
                pointEventData = self.getPointEventData(eventData)
                self.firePointRemove(pointEventData.getCategory(),
                        self.getPointFromEventData(pointEventData))


    def getPointFromEventData(self, eventData):
        # First locate a series and then point
        series = self.getSeriesFromEventData(eventData.getSeriesName())
        if series is not None:
            if isinstance(series, XYSeries):
                for point in series.getPoints():
                    if (point.getY() is not None
                        and cmp(point.getY(), eventData.getPointY()) == 0
                        and point.getX() is not None
                        and cmp(point.getX(), eventData.getPointX()) == 0):
                        return point
            else:
                for point in series.getPoints():
                    if (point.getY() is not None
                        and cmp(point.getY(), eventData.getPointY()) == 0
                        and point.getX() is not None
                        and getDate(point.getX(),
                            series.isIncludeTime()) == eventData.getPointX()):
                        return point
        return None


    def getSeriesFromEventData(self, seriesName):
        for series in self._chartSeries:
            if series.getName() == seriesName:
                return series
        # should not happen
        return None


    def fireAddSeries(self):
        self.fireEvent(ChartAddSeriesEvent(self, self))


    def fireChartClick(self, point, mousePosition):
        self.fireEvent(ChartClickEvent(self, self, point, mousePosition))


    def fireChartZoom(self, selectedArea):
        self.fireEvent(ChartZoomEvent(self, self, selectedArea))


    def fireChartSVGAvailable(self, svg):
        self.fireEvent(ChartSVGAvailableEvent(self, self, svg))


    def fireChartResetZoom(self):
        self.fireEvent(ChartResetZoomEvent(self, self))


    def fireSeriesClick(self, series, point, mousePosition):
        self.fireEvent(SeriesClickEvent(self, self, series, point,
                mousePosition))


    def fireSeriesShow(self, series):
        self.fireEvent(SeriesShowEvent(self, self, series))


    def fireSeriesHide(self, series):
        self.fireEvent(SeriesHideEvent(self, self, series))


    def fireSeriesLegendItemClick(self, series):
        self.fireEvent(SeriesLegendItemClickEvent(self, self, series))


    def firePointClick(self, category, point, mousePosition):
        self.fireEvent(PointClickEvent(self, self, category, point,
                mousePosition))


    def firePointSelect(self, category, point):
        self.fireEvent(PointSelectEvent(self, self, category, point))


    def firePointUnselect(self, category, point):
        self.fireEvent(PointUnselectEvent(self, self, category, point))


    def firePointRemove(self, category, point):
        self.fireEvent(PointRemoveEvent(self, self, category, point))


    def fireLegendItemClick(self, point):
        self.fireEvent(PieChartLegendItemClickEvent(self, self, point))


    def getPointEventData(self, eventData):
        seriesName = eventData['seriesName']
        category = eventData['category']
        pointX = float(eventData['pointX'])
        pointY = float(eventData['pointY'])
        return PointEventData(seriesName, category, pointX, pointY)


    def getClickPosition(self, eventData):
        mouseX = None
        if isinstance(eventData['mouseX'], int):
            mouseX = eventData['mouseX']
        mouseY = None
        if isinstance(eventData['mouseY'], int):
            mouseY = eventData['mouseY']
        if mouseX is not None and mouseY is not None:
            return MousePosition(mouseX, mouseY)
        return None


    def addListener(self, listener, seriesTypes=None):
        """Adds the listener. If the argument seriesTypes is not specified
        then the listener will be added for all series type otherwise it will
        be added for a specific series type

        @param listener:
                   the L{IListener} to be added.
        """
        if seriesTypes is None:
            if isinstance(listener, ChartAddSeriesListener):
                self._chartAddSeriesListener.add(listener)
                self.registerListener(ChartAddSeriesEvent, listener,
                        _CHART_ADD_SERIES_METHOD)
            elif isinstance(listener, ChartClickListener):
                self._chartClickListener.add(listener)
                self.registerListener(ChartClickEvent, listener,
                        _CHART_CLICK_METHOD)
            elif isinstance(listener, ChartResetZoomListener):
                self._chartResetZoomListener.add(listener)
                self.registerListener(ChartResetZoomEvent, listener,
                        _CHART_RESET_ZOOM_METHOD)
            elif isinstance(listener, ChartSVGAvailableListener):
                if (self._svgAvailableListener is not None
                        and self._svgAvailableListener != listener):
                    # remove earlier listener
                    self.removeListener(self._svgAvailableListener)
                self._svgAvailableListener = listener
                self.registerListener(ChartSVGAvailableEvent,
                        self._svgAvailableListener,
                        _CHART_SVG_AVAILABLE_METHOD)
                self._isRetrieveSVG = True
                self.requestRepaint()
            elif isinstance(listener, ChartZoomListener):
                self._chartZoomListener.add(listener)
                self.registerListener(ChartZoomEvent, listener,
                        _CHART_ZOOM_METHOD)
            elif isinstance(listener, PieChartLegendItemClickListener):
                self._pieChartLegendItemClickListener.add(listener)
                self.registerListener(PieChartLegendItemClickEvent, listener,
                        _LEGENDITEM_CLICK_METHOD)
            else:
                super(InvientCharts, self).addListener(listener, seriesTypes)
        else:
            if isinstance(listener, PointClickListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointClickListeners:
                        self._pointClickListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._pointClickListeners[seriesType] = listeners
                self.registerListener(PointClickEvent, listener,
                        _POINT_CLICK_METHOD)
            elif isinstance(listener, PointRemoveListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointRemoveListeners:
                        self._pointRemoveListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._pointRemoveListeners[seriesType] = listeners
                self.registerListener(PointRemoveEvent, listener,
                        _POINT_REMOVE_METHOD)
            elif isinstance(listener, PointSelectListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointSelectListeners:
                        self._pointSelectListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._pointSelectListeners[seriesType] = listeners
                self.registerListener(PointSelectEvent, listener,
                        _POINT_SELECT_METHOD)
            elif isinstance(listener, PointUnselectListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointUnselectListeners:
                        self._pointUnselectListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._pointUnselectListeners[seriesType] = listeners
                self.registerListener(PointUnselectEvent, listener,
                        _POINT_UNSELECT_METHOD)
            elif isinstance(listener, SeriesClickListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesClickListeners:
                        self._seriesClickListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._seriesClickListeners[seriesType] = listeners
                self.registerListener(SeriesClickEvent, listener,
                        _SERIES_CLICK_METHOD)
            elif isinstance(listener, SeriesHideListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesHideListeners:
                        self._seriesHideListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._seriesHideListeners[seriesType] = listeners
                self.registerListener(SeriesHideEvent, listener,
                        _SERIES_HIDE_METHOD)
            elif isinstance(listener, SeriesLegendItemClickListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesLegendItemClickListeners:
                        self._seriesLegendItemClickListeners[seriesType].add(
                                listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._seriesLegendItemClickListeners[seriesType] = \
                                listeners
                self.registerListener(SeriesLegendItemClickEvent, listener,
                        _SERIES_LEGENDITEM_CLICK_METHOD)
            elif isinstance(listener, SeriesShowListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesShowListeners:
                        self._seriesShowListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._seriesShowListeners[seriesType] = listeners
                self.registerListener(SeriesShowEvent, listener,
                        _SERIES_SHOW_METHOD)
            else:
                iface = seriesTypes
                super(InvientCharts, self).addListener(listener, iface)


    def removeListener(self, listener, seriesTypes=None):
        """Removes the listener. If the argument seriesTypes is not specified
        then the listener will be removed only for a series type
        SeriesType.COMMONSERIES otherwise the listener will be removed for all
        specified series types.

        @param listener:
                   the listener to be removed
        @param seriesTypes:
                   one or more series types as defined by L{SeriesType}
        """
        if seriesTypes is None:
            if isinstance(listener, ChartAddSeriesListener):
                self._chartAddSeriesListener.remove(listener)
                self.withdrawListener(ChartAddSeriesEvent, listener,
                        _CHART_ADD_SERIES_METHOD)
            elif isinstance(listener, ChartClickListener):
                self._chartClickListener.remove(listener)
                self.withdrawListener(ChartClickEvent, listener,
                        _CHART_CLICK_METHOD)
            elif isinstance(listener, ChartResetZoomListener):
                self._chartResetZoomListener.remove(listener)
                self.withdrawListener(ChartResetZoomEvent, listener,
                        _CHART_RESET_ZOOM_METHOD)
            elif isinstance(listener, ChartSVGAvailableListener):
                if self._svgAvailableListener == listener:
                    self.withdrawListener(ChartSVGAvailableEvent, listener,
                            _CHART_SVG_AVAILABLE_METHOD)
                    self._isRetrieveSVG = False
                    self._svgAvailableListener = None
            elif isinstance(listener, ChartZoomListener):
                self._chartZoomListener.remove(listener)
                self.withdrawListener(ChartZoomEvent, listener,
                        _CHART_ZOOM_METHOD)
            elif isinstance(listener, PieChartLegendItemClickListener):
                self._pieChartLegendItemClickListener.remove(listener)
                self.withdrawListener(PieChartLegendItemClickEvent, listener,
                        _LEGENDITEM_CLICK_METHOD)
            else:
                super(InvientCharts, self).removeListener(listener, seriesTypes)
        else:
            if isinstance(listener, PointClickListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointClickListeners:
                        self._pointClickListeners[seriesType].remove(listener)
                self.withdrawListener(PointClickEvent, listener,
                        _POINT_CLICK_METHOD)
            elif isinstance(listener, PointRemoveListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointRemoveListeners:
                        self._pointRemoveListeners[seriesType].remove(listener)
                self._pointRemoveListeners.remove(listener)
                self.withdrawListener(PointRemoveEvent, listener,
                        _POINT_REMOVE_METHOD)
            elif isinstance(listener, PointSelectListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointSelectListeners:
                        self._pointSelectListeners[seriesType].remove(listener)
                self.withdrawListener(PointSelectEvent, listener,
                        _POINT_SELECT_METHOD)
            elif isinstance(listener, PointUnselectListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointUnselectListeners:
                        self._pointUnselectListeners[seriesType].remove(
                                listener)
                self.withdrawListener(PointUnselectEvent, listener,
                        _POINT_UNSELECT_METHOD)
            elif isinstance(listener, SeriesClickListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesClickListeners:
                        self._seriesClickListeners[seriesType].remove(listener)
                self.withdrawListener(SeriesClickEvent, listener,
                        _SERIES_CLICK_METHOD)
            elif isinstance(listener, SeriesHideListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesHideListeners:
                        self._seriesHideListeners[seriesType].remove(listener)
                self.withdrawListener(SeriesHideEvent, listener,
                        _SERIES_HIDE_METHOD)
            elif isinstance(listener, SeriesLegendItemClickListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesLegendItemClickListeners:
                        self._seriesLegendItemClickListeners[
                                seriesType].remove(listener)
                self.withdrawListener(SeriesLegendItemClickEvent, listener,
                        _SERIES_LEGENDITEM_CLICK_METHOD)
            elif isinstance(listener, SeriesShowListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesShowListeners:
                        self._seriesShowListeners[seriesType].remove(listener)
                self.withdrawListener(SeriesShowEvent, listener,
                        _SERIES_SHOW_METHOD)
            else:
                iface = seriesTypes
                super(InvientCharts, self).removeListener(listener, iface)


    def setSeries(self, series):
        """The data of a chart is defined in terms of L{Series}. This method
        removes all previously set series of this chart and adds the argument
        series. If the argument series is null then no actions are taken.

        @param series:
                   A collection of series to set as chart's data
        """
        if series is not None:
            self._reloadChartSeries = True
            self._chartSeries.clear()
            self._seriesCURMap.clear()
            for seriesData in series:
                self.addSeries(seriesData)


    def getSeries(self, name):
        """Returns a series whose name matches the argument name.

        @param name:
                   the name of the series
        @return: Returns a series with the given name
        """
        for series in self._chartSeries:
            if series.getName() == name:
                return series
        return None


    def getAllSeries(self):
        """Returns all series associated with this chart.
        @return: returns all series associated with this chart.
        """
        return self._chartSeries


    def addSeries(self, seriesData):
        """Adds the argument series to this chart.

        @param seriesData:
                   the series to be added
        """
        # Before sending data to the client, this method sets
        # axis in all series associated with the chart
        if self._chartSeries.add(seriesData):
            self.setAxisInSeriesIfNotSetAlready(seriesData)
            seriesData.setInvientCharts(self)
            self.addSeriesCUROperation(SeriesCUR(SeriesCURType.ADD,
                    seriesData.getName()))
            self.requestRepaint()


    def setAxisInAllSeriesIfNotSetAlready(self):
        for series in self._chartSeries:
            self.setAxisInSeriesIfNotSetAlready(series)


    def setAxisInSeriesIfNotSetAlready(self, series):
        if self.getConfig() is not None:
            if (series.getXAxis() is None
                    and self.getConfig().getXAxes() is not None
                    and len(self.getConfig().getXAxes()) > 0):
                series.setXAxis(iter(self.getConfig().getXAxes()).next())  # FIXME: iterator
            if (series.getYAxis() is None
                    and self.getConfig().getYAxes() is not None
                    and len(self.getConfig().getYAxes()) > 0):
                series.setYAxis(iter(self.getConfig().getYAxes()).next())  # FIXME: iterator


    def removeSeries(self, name_or_seriesData):
        """Removes a series whose name matches the argument name or the
        argument seriesData from this chart.

        @param seriesData:
                   the name of the series or the series object to be removed
        """
        if isinstance(name_or_seriesData, Series):
            seriesData = name_or_seriesData
            if self._chartSeries.remove(seriesData):
                seriesData.setInvientCharts(None)
                self.addSeriesCUROperation(SeriesCUR(SeriesCURType.REMOVE,
                        seriesData.getName()))
                self.requestRepaint()
        else:
            name = name_or_seriesData

            seriesItr = self._chartSeries.copy()
            for series in seriesItr:
                if series.getName() == name:
                    self._chartSeries.remove(series)
                    series.setInvientCharts(None)
                    self.addSeriesCUROperation(SeriesCUR(SeriesCURType.REMOVE,
                            series.getName()))
                    self.requestRepaint()


    def addSeriesCUROperation(self, newSeriesCUR):
        if newSeriesCUR.getName() in self._seriesCURMap:
            seriesCURSet = self._seriesCURMap.get(newSeriesCUR.getName())

            # If for a series, no operation is found
            if (seriesCURSet is None) or (len(seriesCURSet) == 0):
                seriesCURSet = OrderedSet()
                seriesCURSet.add(newSeriesCUR)
                self._seriesCURMap[newSeriesCUR.getName()] = seriesCURSet
            elif seriesCURSet.contains(newSeriesCUR):
                seriesCUR = self.getMatchedSeriesCUR(seriesCURSet,
                        newSeriesCUR)

                # In case of series update (due to series.show/hide or
                # series.setPoints or series.removeAllPoints)
                # we need to check if all points of a series are set afresh.
                # If so then set a flag to indicate that instead of adding and
                # removing points to and from series, set series data in full.
                if seriesCUR.getType() == SeriesCURType.UPDATE:
                    seriesCUR.setReloadPoints(newSeriesCUR.isReloadPoints())
                    if newSeriesCUR.isReloadPoints():
                        seriesCUR.clearTrackedPoints()
                    return True
                # Operation on a series has already been recorded
                return False
            else:
                seriesCURItr = seriesCURSet.copy()
                for seriesCUR in seriesCURItr:
                    if seriesCUR.getName() == newSeriesCUR.getName():
                        if (SeriesCURType.REMOVE == newSeriesCUR.getType()
                                and SeriesCURType.ADD == seriesCUR.getType()):
                            # Remove addition of a series as there is no reason
                            # to add a series and then remove it. E.g. If a new
                            # series is added and then removed then actually
                            # there is nothing to be done
                            seriesCURSet.remove(seriesCUR)
                            return False
                        if (SeriesCURType.UPDATE == newSeriesCUR.getType()
                                and SeriesCURType.ADD == seriesCUR.getType()):
                            # There is no need for update as adding a series
                            # will take care of applying any update to the
                            # series attributes specifically visibility
                            return False
                        if (SeriesCURType.REMOVE == newSeriesCUR.getType()
                            and SeriesCURType.UPDATE == seriesCUR.getType()):
                            # Remove update of a series as there is no reason
                            # to update a series  and then remove it. E.g. If
                            # an existing series was updated (for show/hide)
                            # and then removed then series need not be updated
                            # after all it is going to be removed. Hover, the
                            # remove operation must be captured.
                            seriesCURSet.remove(seriesCUR)
                            break
            seriesCURSet.add(newSeriesCUR)
            return True
        else:
            seriesCURSet = OrderedSet()
            seriesCURSet.add(newSeriesCUR)
            self._seriesCURMap[newSeriesCUR.getName()] = seriesCURSet
            return True


    def addSeriesPointAddedOperation(self, seriesName, point):
        seriesCURSet = self._seriesCURMap.get(seriesName)
        if (seriesCURSet is None) or (len(seriesCURSet) == 0):
            seriesCUR = SeriesCUR(SeriesCURType.UPDATE, seriesName)
            seriesCUR.trackPointAdded(point)
            seriesCURSet = OrderedSet()
            seriesCURSet.add(seriesCUR)
            self._seriesCURMap[seriesName] = seriesCURSet
        else:
            lastSeriesCur = self.getLastSeriesCUR(seriesCURSet)
            # Track points only if series is updated.
            # Tracking point is useless in following cases
            # 1. A new series is added : In this case, a series will be added
            # with all points so no need to track
            # 2. A series is removed : In this case, a series will be removed
            # and hence any point added to the series doesn't carry any
            # meaning.
            if (lastSeriesCur.getType() == SeriesCURType.UPDATE
                    and not lastSeriesCur.isReloadPoints()):
                lastSeriesCur.trackPointAdded(point)


    def getLastSeriesCUR(self, seriesCURSet):
        if (seriesCURSet is None) or (len(seriesCURSet) == 0):
            return None
        lastSeriesCur = None
        for seriesCur in seriesCURSet:
            lastSeriesCur = seriesCur
        return lastSeriesCur


    def getMatchedSeriesCUR(self, seriesCURSet, matchAgainstSeriesCUR):
        for seriesCur in seriesCURSet:
            if matchAgainstSeriesCUR == seriesCur:
                return seriesCur
        return None


    def addSeriesPointRemovedOperation(self, seriesName, point):
        seriesCURSet = self._seriesCURMap.get(seriesName)
        if (seriesCURSet is None) or (len(seriesCURSet) == 0):
            seriesCUR = SeriesCUR(SeriesCURType.UPDATE, seriesName)
            seriesCUR.trackPointRemoved(point)
            seriesCURSet = OrderedSet()
            seriesCURSet.add(seriesCUR)
            self._seriesCURMap[seriesName] = seriesCURSet
        else:
            lastSeriesCur = self.getLastSeriesCUR(seriesCURSet)
            # Track points only if series is updated.
            # Tracking point is useless in following cases
            # 1. A new series is added : In this case, a series will be added
            # with all points so no need to track
            # 2. A series is removed : In this case, a series will be removed
            # and hence any point removed from the series
            # doesn't carry any meaning.
            if (lastSeriesCur.getType() == SeriesCURType.UPDATE
                    and not lastSeriesCur.isReloadPoints()):
                lastSeriesCur.trackPointRemoved(point)


    def refresh(self):
        """After a series is added or removed, there is no need to call this
        method as it is handled implicitly. This method will send updates to
        the client. This method should be called after adding/removing
        plotbands and plotlines. This inconsistency will be fixed in next
        revision.
        """
        super(InvientCharts, self).requestRepaint()


    def print_(self):
        """Displays a Print dialog of the Webkit to print this chart. Invoking
        this method causes the Webkit to hide other widgets on the screen and
        only this chart widget will be visible. Also it prints this chart
        widget as it is displayed.
        """
        self._isPrint = True
        self.requestRepaint()


class MousePosition(object):
    """This class contain mouse coordinates when a click event occurs
    on a chart, a series or a point.

    The mouse coordinates are in pixels.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, mouseX, mouseY):
        """Creates this object with given arguments.

        @param mouseX:
                   x position of mouse when a click event occurred, in pixel
        @param mouseY:
                   y position of mouse when a click event occurred, in pixel
        """
        self._mouseX = mouseX
        self._mouseY = mouseY


    def getMouseX(self):
        """@return: Returns x position of mouse when a click event occurred,
        in pixel
        """
        return self._mouseX


    def getMouseY(self):
        """@return: Returns y position of mouse when a click event occurred,
        in pixel
        """
        return self._mouseY


    def __str__(self):
        return ('MousePosition [mouseX=' + str(self._mouseX)
                + ', mouseY=' + str(self._mouseY) + ']')


class PointEventData(object):

    def __init__(self, seriesName, category, pointX, pointY):
        self._seriesName = seriesName
        self._category = category
        self._pointX = pointX
        self._pointY = pointY

    def getSeriesName(self):
        return self._seriesName

    def getCategory(self):
        return self._category

    def getPointX(self):
        return self._pointX

    def getPointY(self):
        return self._pointY

    def __str__(self):
        return ('PointEventData [seriesName=' + self._seriesName
                + ', category=' + self._category
                + ', pointX=' + str(self._pointX)
                + ', pointY=' + str(self._pointY) + ']')


class PointClickEvent(ComponentEvent):
    """Click event. This event is thrown, when any point of this chart is
    clicked and the point marker is enabled. The point marker is enabled by
    default.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, category, point, mousePosition):
        """New instance of the point click event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param category:
                   a category to which point is associated in case of
                   categorized axis,
        @param point:
                   the point on which the click event occurred
        @param mousePosition:
                   the position of a mouse when the click event occurred
        """
        super(PointClickEvent, self).__init__(source)

        self._chart = chart
        self._category = category
        self._point = point
        self._mousePosition = mousePosition

    def getCategory(self):
        """@return: Returns a category to which point is associated in case
        of categorized axis only.
        """
        return self._category

    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart

    def getPoint(self):
        """@return: Returns the point on which the click event occurred"""
        return self._point

    def getMousePosition(self):
        """@return: Returns the position of a mouse when the click event
        occurred"""
        return self._mousePosition


class PointClickListener(object):
    """Interface for listening for a L{PointClickEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def pointClick(self, pointClickEvent):
        raise NotImplementedError


class PointRemoveEvent(ComponentEvent):
    """Point remove event. This event is thrown, when any point of this chart
    is removed from its series.

    This event is EXPERIMENTAL ONLY.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, category, point):
        """New instance of the point remove event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param category:
                   a category to which point is associated in case of
                   categorized axis,
        @param point:
                   the point removed
        """
        super(PointRemoveEvent, self).__init__(source)

        self._chart = chart
        self._category = category
        self._point = point


    def getCategory(self):
        """@return: Returns a category to which point is associated in case
        of categorized axis only.
        """
        return self._category


    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart


    def getPoint(self):
        """@return: Returns the point which has been removed"""
        return self._point


class PointRemoveListener(object):
    """Interface for listening for a L{PointRemoveEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def pointRemove(self, pointRemoveEvent):
        raise NotImplementedError


class PointUnselectEvent(ComponentEvent):
    """Point unselect event. This event is thrown, when any point of this
    chart is unselected and the point marker is enabled. The point marker
    is enabled by default.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, category, point):
        """New instance of the point unselect event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param category:
                   a category to which point is associated in case of
                   categorized axis,
        @param point:
                   the point unselected as a result of this event
        """
        super(PointUnselectEvent, self).__init__(source)

        self._chart = chart
        self._category = category
        self._point = point

    def getCategory(self):
        """@return: Returns a category to which point is associated in case
        of categorized axis only.
        """
        return self._category

    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart

    def getPoint(self):
        """@return: Returns the unselected point"""
        return self._point


class PointUnselectListener(object):
    """Interface for listening for a L{PointUnselectEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def pointUnSelect(self, pointUnSelectEvent):
        raise NotImplementedError


class PointSelectEvent(ComponentEvent):
    """Point select event. This event is thrown, when any point of this chart
    is selected and the point marker is enabled. The point marker is enabled
    by default.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, category, point):
        """New instance of the point select event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param category:
                   a category to which point is associated in case of
                   categorized axis,
        @param point:
                   the point selected as a result of this event
        """
        super(PointSelectEvent, self).__init__(source)

        self._chart = chart
        self._category = category
        self._point = point

    def getCategory(self):
        """@return: Returns a category to which point is associated in case
        of categorized axis only.
        """
        return self._category

    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart

    def getPoint(self):
        """@return: Returns the selected point"""
        return self._point


class PointSelectListener(object):
    """Interface for listening for a L{PointSelectListener} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def pointSelected(self, pointSelectEvent):
        raise NotImplementedError


_POINT_CLICK_METHOD = getattr(PointClickListener, 'pointClick')
_POINT_REMOVE_METHOD = getattr(PointRemoveListener, 'pointRemove')
_POINT_SELECT_METHOD = getattr(PointSelectListener, 'pointSelected')
_POINT_UNSELECT_METHOD = getattr(PointUnselectListener, 'pointUnSelect')




class SeriesClickEvent(ComponentEvent):
    """Series click event. This event is thrown, when any series of this
    chart is clicked.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, series, point, mousePosition):
        """New instance of the series click event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param series:
                   the series on which click event occurred
        @param point:
                   the closest point of a series
        @param mousePosition:
                   the position of a mouse when the click event occurred
        """
        super(SeriesClickEvent, self).__init__(source)

        self._chart = chart
        self._series = series
        self._point = point
        self._mousePosition = mousePosition

    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart

    def getSeries(self):
        """@return: Returns the series object on which the click event
        occurred"""
        return self._series

    def getNearestPoint(self):
        """@return: Returns the point of a series closest to the position
        where mouse click event occurred.
        """
        return self._point

    def getMousePosition(self):
        """@return: Returns the position of a mouse when the click event
        occurred"""
        return self._mousePosition


class SeriesClickListerner(object):
    """Interface for listening for a L{SeriesClickListerner} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def seriesClick(self, seriesClickEvent):
        raise NotImplementedError


class SeriesHideEvent(ComponentEvent):
    """Series Hide event. This event is thrown, when any series of this chart
    is hidden.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, series):
        """@param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param series:
                   the series which got hidden
        """
        super(SeriesHideEvent, self).__init__(source)
        self._chart = chart
        self._series = series

    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart

    def getSeries(self):
        """@return: Returns the series which got hidden"""
        return self._series


class SeriesHideListerner(object):
    """Interface for listening for a L{SeriesHideEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def seriesHide(self, seriesHideEvent):
        raise NotImplementedError


class SeriesShowEvent(ComponentEvent):
    """Series show event. This event is thrown, when any series of this
    chart is displayed after a chart is created.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, series):
        """New instance of the series show event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param series:
                   the series which got displayed
        """
        super(SeriesShowEvent, self).__init__(source)
        self._chart = chart
        self._series = series

    def getChart(self):
        """@return: Returns the chart object associated with the series"""
        return self._chart

    def getSeries(self):
        """@return: Returns the series which got displayed"""
        return self._series


class SeriesShowListerner(object):
    """Interface for listening for a L{SeriesShowEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def seriesShow(self, seriesShowEvent):
        raise NotImplementedError


class SeriesLegendItemClickEvent(ComponentEvent):
    """Series legend item click event. This event is thrown, when legend item
    is clicked. This event is not applicable for PieChart instead use
    L{LegendItemClickEvent}

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, series):
        """New instance of the point click event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param series:
                   the series associated with the legend item
        """
        super(SeriesLegendItemClickEvent, self).__init__(source)
        self._chart = chart
        self._series = series

    def getChart(self):
        """@return: Returns the chart object associated with the series"""
        return self._chart

    def getSeries(self):
        """@return: Returns the series associated with the legend item"""
        return self._series


class SeriesLegendItemClickListerner(object):
    """Interface for listening for a L{SeriesLegendItemClickEvent}
    triggered by L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def seriesLegendItemClick(self, seriesLegendItemClickEvent):
        raise NotImplementedError


_SERIES_CLICK_METHOD = getattr(SeriesClickListerner, 'seriesClick')
_SERIES_HIDE_METHOD = getattr(SeriesHideListerner, 'seriesHide')
_SERIES_SHOW_METHOD = getattr(SeriesShowListerner, 'seriesShow')
_SERIES_LEGENDITEM_CLICK_METHOD = getattr(SeriesLegendItemClickListerner,
        'seriesLegendItemClick')


class PieChartLegendItemClickEvent(ComponentEvent):
    """PieChart legend item click event. This event is thrown, when the
    legend item belonging to the pie point (slice) is clicked.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, point):
        """New instance of the piechart legend item click event

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param point:
                   the pie point (slice) associated with the legend item
        """
        super(PieChartLegendItemClickEvent, self).__init__(source)
        self._chart = chart
        self._point = point

    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart

    def getPoint(self):
        """@return: Returns the pie point (slice) associated with the legend
        item"""
        return self._point


class PieChartLegendItemClickListener(object):
    """Interface for listening for a L{PieChartLegendItemClickEvent}
    triggered by L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def legendItemClick(self, legendItemClickEvent):
        raise NotImplementedError


_LEGENDITEM_CLICK_METHOD = getattr(PieChartLegendItemClickListener,
        'legendItemClick')


class ChartClickEvent(ComponentEvent):
    """Chart Click event. This event is thrown, when this chart is clicked.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, point, mousePosition):
        """New instance of the chart click event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param point:
                   the position where the click event occurred in axes units
        @param mousePosition:
                   the coordinate of mouse where the click event occurred in
                   pixels
        """
        super(ChartClickEvent, self).__init__(source)

        self._chart = chart
        self._point = point
        self._mousePosition = mousePosition


    def getChart(self):
        """Returns the chart object on which the click event occurred

        @return: Returns the chart object on which the click event occurred
        @see: L{InvientCharts}
        """
        return self._chart


    def getPoint(self):
        """Returns the point representing the position where the click event
        occurred in axes units

        @return: Returns the point representing the position where the click
                 event occurred in axes units
        @see: L{Point}
        """
        return self._point


    def getMousePosition(self):
        """Returns the position of a mouse when the click event occurred

        @return: Returns the position of a mouse when the click event occurred
        @see: L{MousePosition}
        """
        return self._mousePosition


    def __str__(self):
        return ('ChartClickEvent [point=' + str(self._point)
                + ', mousePosition=' + str(self._mousePosition) + ']')


class ChartClickListener(object):
    """Interface for listening for a L{ChartClickEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def chartClick(self, chartClickEvent):
        raise NotImplementedError


class ChartAddSeriesEvent(ComponentEvent):
    """Add series event. This event is thrown, when a series is added to
    the chart.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart):
        """New instance of the chart add series event.

        @param source
        @param chart
        """
        super(ChartAddSeriesEvent, self).__init__(source)

        self._chart = chart

    def getChart(self):
        """Returns the chart object to which a series is added

        @return: Returns the chart object to which a series has been added.
        @see: L{InvientCharts}
        """
        return self._chart


class ChartAddSeriesListener(object):
    """Interface for listening for a L{ChartAddSeriesEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def chartAddSeries(self, chartAddSeriesEvent):
        raise NotImplementedError


class ChartArea(object):
    """Defines information on the selected area.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, xAxisMin, xAxisMax, yAxisMin, yAxisMax):
        self._xAxisMin = xAxisMin
        self._xAxisMax = xAxisMax
        self._yAxisMin = yAxisMin
        self._yAxisMax = yAxisMax

    def getxAxisMin(self):
        return self._xAxisMin

    def getxAxisMax(self):
        return self._xAxisMax

    def getyAxisMin(self):
        return self._yAxisMin

    def getyAxisMax(self):
        return self._yAxisMax

    def __str__(self):
        return ('ChartSelectedArea [xAxisMin=' + str(self._xAxisMin)
                + ', xAxisMax=' + str(self._xAxisMax)
                + ', yAxisMin=' + str(self._yAxisMin)
                + ', yAxisMax=' + str(self._yAxisMax) + ']')


class ChartZoomEvent(ComponentEvent):
    """Chart zoom event. This event is thrown, when an area of the chart has
    been selected.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, chartArea):
        """New instance of the chart zoom event.

        @param source
                   the chart object itself
        @param chart
                   the chart object itself
        @param chartArea
                   the chartArea object containing dimensions of zoomed area
                   of the chart
        """
        super(ChartZoomEvent, self).__init__(source)

        self._chart = chart
        self._chartArea = chartArea


    def getChart(self):
        """Returns the chart object for which the zoom event has occurred

        @return: Returns the chart object for which the zoom event has
                 occurred
        """
        return self._chart


    def getChartArea(self):
        """Returns the chartArea object containing dimensions of zoomed area
        of the chart

        @return: Returns the chartArea object containing dimensions of zoomed
                 area of the chart
        """
        return self._chartArea


class ChartZoomListener(object):
    """Interface for listening for a L{ChartZoomEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def chartZoom(self, chartZoomEvent):
        raise NotImplementedError


class ChartResetZoomEvent(ComponentEvent):
    """Chart reset zoom event. This event is thrown, when a chart is reset
    by setting its zoom level to normal.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart):
        """New instance of the chart reset zoom event

        @param source
                   the chart object itself
        @param chart
                   the chart object itself
        """
        super(ChartResetZoomEvent, self).__init__(source)
        self._chart = chart


    def getChart(self):
        """Returns the chart object for which zoom has been reset to normal

        @return: Returns the chart object for which zoom has been reset to
                 normal
        """
        return self._chart


class ChartResetZoomListener(object):
    """Interface for listening for a L{@link ChartResetZoomEvent} triggered
    by L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def chartResetZoom(self, chartResetZoomEvent):
        raise NotImplementedError


class ChartSVGAvailableEvent(ComponentEvent):
    """Chart SVG event. This event is thrown, when an SVG string representing
    the chart is received or ready.

    Note that this event is thrown only once after a
    L{ChartSVGAvailableListener} is registered.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, svg):
        """New instance of the chart svg available event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param svg:
                   an svg string representing the chart object
        """
        super(ChartSVGAvailableEvent, self).__init__(source)
        self._chart = chart
        self._svg = svg


    def getChart(self):
        """Returns the chart object for which an svg string representation
        is available

        @return: Returns the chart object for which an svg string
                 representation is available
        """
        return self._chart


    def getSVG(self):
        """@return: Returns an SVG string representing the chart"""
        return self._svg


class ChartSVGAvailableListener(object):
    """Interface for listening for a L{ChartSVGAvailableEvent} triggered by
    L{InvientCharts}.

    The chart can have only one listener of this type registered at any time.
    If a listener has already been registered and an attempt is made to
    register another listener then the previously registered listener will be
    unregistered and the new listener will be registered.

    A listener will be called only once after it has been registered though
    it will be called again if the same listener is registered again.

    @author: Invient
    @author: Richard Lincoln
    """

    def svgAvailable(self, chartSVGAvailableEvent):
        pass


_CHART_CLICK_METHOD = getattr(ChartClickListener, 'chartClick')
_CHART_ADD_SERIES_METHOD = getattr(ChartAddSeriesListener, 'chartAddSeries')
_CHART_ZOOM_METHOD = getattr(ChartZoomListener, 'chartZoom')
_CHART_RESET_ZOOM_METHOD = getattr(ChartResetZoomListener, 'chartResetZoom')
_CHART_SVG_AVAILABLE_METHOD = getattr(ChartSVGAvailableListener,
        'svgAvailable')


class Point(object):
    """This class represents a point of the chart's series. A series can have
    one or more points. A point has (X, Y) coordinates. None of the
    coordinates are mandatory. The name of a point can be displayed in a
    tooltip.

    To represent no activity or missing points in the chart, create a point
    with both X and Y as null or just Y as null.

    It is possible to specify custom configuration for each point. e.g. If a
    highest point can be marked in a chart with a different color using this
    configuration.

    A point cannot be created without a series. It must belong to a series.
    However, the point must be added to a series by calling Series.addPoint()
    or Series.setPoints() to permanently add point to the series.

    @author: Invient
    @author: Richard Lincoln

    @see: L{DecimalPoint}
    @see: L{DateTimePoint}
    @see: L{PointConfig}
    """

    def __init__(self, series, name_or_config=None, config=None):
        """Creates a point with given arguments.

        @param series:
                   The series to which the point must be associated.
        @param name_or_config:
                   The configuration for this point, or the name of this point
        @param config:
                   The configuration for this point, if any
        @exception ValueError:
                   If the argument series is null
        """
        self._id = None
        self._isAutosetX = None
        self._shift = False

        name = None
        if name_or_config is not None:
            if isinstance(name_or_config, PointConfig):
                config = name_or_config
                name = None
            else:
                name = name_or_config
                config = None

        self._series = series
        self._name = name
        self._config = config


    def getId(self):
        return self._id


    def getName(self):
        """@return: Returns name of this point"""
        return self._name


    def setName(self, name):
        """Sets name of this point

        @param name:
                   name of this point
        """
        self._name = name


    def getSeries(self):
        """@return: Returns L{Series} associated with this point"""
        return self._series


    def getConfig(self):
        """@return: Returns L{PointConfig} for this point"""
        return self._config


    def setConfig(self, config):
        """Sets L{PointConfig} for this point

        @param config:
                   configuration of this point
        @see: L{PointConfig}
        """
        self._config = config


    def isAutosetX(self):
        """@return: Returns true if X value of this point is set
        programmatically"""
        return self._isAutosetX


    def setAutosetX(self, isAutosetX):
        """If the argument is true it indicates that the X value of this point
        is set programmatically and user has not specified it.
        """
        self._isAutosetX = isAutosetX


    def isShift(self):
        """@return: Returns true if a point at the start of the series should
        beshifted off when this point is appended otherwise false.
        """
        return self._shift


    def setShift(self, shift):
        """A value of true means one point is shifted off the start of the
        series as one is appended to the end.
        """
        self._shift = shift


    def getX(self):
        """@return: Returns X value of this point"""
        raise NotImplementedError


    def getY(self):
        """@return: Returns Y value of this point"""
        raise NotImplementedError


    def __str__(self):
        return ('Point [id=' + self._id
                + ', name=' + self._name
                + ', series=' + self._series.getName()
                + ', config=' + str(self._config) + ']')


class DecimalPoint(Point):
    """This class represent a point with (X, Y) both as number. It should be
    used to add points to L{XYSeries}

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, *args):
        """@param invientCharts:
        @param args:
            tuple of the form:
                - (series)
                  - the series to which this belongs to
                - (series, y)
                  - the series to which this belongs to
                  - the y value of this point
                - (series, name, y)
                  - the series to which this belongs to
                  - the name of this point
                  - the y value of this point
                - (x, y)
                  - the x value of this point
                  - the y value of this point
                - (series, name, y, config)
                  - the series to which this belongs to
                  - the name of this point
                  - the y value of this point
                  - the configuration of this point
                - (series, y, config)
                  - the series to which this belongs to
                  - the y value of this point
                  - the configuration of this point
                - (series, x, y)
                  - the series to which this belongs to
                  - the x value of this point
                  - the y value of this point
                - (series, x, y, config)
                  - the series to which this belongs to
                  - the x value of this point
                  - the y value of this point
                  - the configuration of this point
        """
        self._x = None
        self._y = None

        nargs = len(args)
        if nargs == 1:
            series, = args
            super(DecimalPoint, self).__init__(series)
        elif nargs == 2:
            if isinstance(args[0], Series):
                series, y = args
                super(DecimalPoint, self).__init__(series)
                self._y = y
            else:
                x, y = args
                super(DecimalPoint, self).__init__(None)
                self._x = x
                self._y = y
        elif nargs == 3:
            if isinstance(args[1], (float, int)):
                if isinstance(args[2], PointConfig):
                    series, y, config = args
                    super(DecimalPoint, self).__init__(series, config)
                    self._y = y
                else:
                    series, x, y = args
                    self.__init__(series, x, y, None)
                    series, x, y = args
                    self.__init__(series, x, y, None)
            else:
                series, name, y = args
                super(DecimalPoint, self).__init__(series, name)
                self._y = y
        elif nargs == 4:
            if isinstance(args[1], (float, int)):
                series, x, y, config = args
                super(DecimalPoint, self).__init__(series, config)
                self._x = x
                self._y = y
            else:
                series, name, y, config = args
                super(DecimalPoint, self).__init__(series, name, config)
                self._y = y
        else:
            raise ValueError


    def getX(self):
        return self._x


    def setX(self, x):
        """Sets the x value of this point
        """
        self._x = x


    def getY(self):
        return self._y


    def setY(self, y):
        """Sets the y value of this point
        """
        self._y = y


    def __str__(self):
        return ('DecimalPoint [x=' + self._x
                + ', y=' + self._y
                + ', id=' + self.getId()
                + ', name=' + self.getName()
                + ', seriesName='
                + (self._series.getName()
                    if self._series is not None else '')
                + ']')


    def __hash__(self):
        prime = 31
        result = 1
        result = ((prime * result)
                + (0 if self._y is None else hash(self._y)))
        return result


    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None:
            return False
        if self.__class__ != obj.__class__:
            return False
        other = obj
        # If x is null then return always false as x is calculated
        # if not specified
        if (self._x is None) or (other._x is None):
            return False
        if not (self._x == other._x):
            return False
        if self._y is None:
            if other._y is not None:
                return False
        elif other._y is None:
            return False
        elif cmp(self._y, other._y) != 0:
            return False
        return True


class DateTimePoint(Point):
    """This class represent a point with (X, Y) both as number. It should
    be used to add points to L{DateTimeSeries}

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, *args):
        """@param args:
            tuple of the form:
              - (series)
                - the series to which this belongs to
              - (series, y)
                - the series to which this belongs to
                - the y value of this point
              - (series, name, y)
                - the series to which this belongs to
                - the name of this point
                - the y value of this point
              - (series, name, y, config)
                - the series to which this belongs to
                - the name of this point
                - the y value of this point
                - the configuration of this point
              - (series, x, y)
                - the series to which this belongs to
                - the x value of this point
                - the y value of this point
        """
        self._x = None
        self._y = None

        nargs = len(args)
        if nargs == 1:
            series, = args
            super(DateTimePoint, self).__init__(series)
        elif nargs == 2:
            series, y = args
            self.__init__(series, '', y)
        elif nargs == 3:
            if isinstance(args[1], datetime):
                series, x, y = args
                self.__init__(series, y)
                self._x = x
            else:
                series, name, y = args
                super(DateTimePoint, self).__init__(series, name)
                self._y = y
        elif nargs == 4:
            series, name, y, config = args
            super(DateTimePoint, self).__init__(series, name, config)
            self._y = y
        else:
            raise ValueError


    def getX(self):
        return self._x


    def setX(self, x):
        """Sets the x value of this point

        @param x
        """
        self._x = x


    def getY(self):
        return self._y


    def setY(self, y):
        """Sets the y value of this point

        @param y
        """
        self._y = y


    def __str__(self):
        return ('DateTimePoint [x='
            + getDate(self._x,
                    self._series.isIncludeTime()
                    if self._series is not None else False)
            + ', y=' + str(self._y) + ', id=' + self.getId()
            + ', name=' + self.getName()
            + ', seriesName=' + (self._series.getName()
                    if self._series is not None else '')
            + ']')


    def __hash__(self):
        prime = 31
        result = 1
        result = ((prime * result) + (0 if self._y is None else hash(self._y)))
        return result


    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None:
            return False
        if self.__class__ != obj.__class__:
            return False
        other = obj
        # If x is null then return always false as x is calculated if not
        # specified
        if (self._x is None) or (other._x is None):
            return False
        pointIncludeTime = (self.getSeries().isIncludeTime()
                if isinstance(self.getSeries(), DateTimeSeries) else False)
        pointOtherIncludeTime = (other.getSeries().isIncludeTime()
                if isinstance(other.getSeries(), DateTimeSeries) else False)
        pointX = getDate(self._x, pointIncludeTime)
        pointOtherX = getDate(other._x, pointOtherIncludeTime)
        if cmp(pointX, pointOtherX) != 0:
            return False
        if self._y is None:
            if other._y is not None:
                return False
        elif other._y is None:
            return False
        elif cmp(self._y, other._y) != 0:
            return False
        return True


class Series(object):
    """This class defines a series of the chart. A series contains a collection
    of points. Series can be one of types defined by L{SeriesType}.

    Each series must have unique name. If an attempt is made to add two
    series with same then only the first added series will be in effect.

    If the series type is not specified, it defaults to chart type and the
    default chart type is SeriesType.LINE. A series has unique xAxis and
    yAxis object associated with it. There is no need to set xAxis and yAxis
    unless the chart has more than one one axis of any type and the series
    must belong to any of the secondary axis.

    It is also possible to specify configuration for individual series and
    not just series type.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, name, seriesType_or_config=None, config=None):
        """Creates a series with given name, type and configuration

        @param name:
                   the name of this series
        @param seriesType_or_config:
                   the type of this series or the configuration for this series
        @param config:
                   the configuration for this series
        """
        self._points = OrderedSet()
        self._name = ''
        self._type = None
        self._stack = None
        self._xAxis = None
        self._yAxis = None
        self._config = None
        self._invientCharts = None

        seriesType = None
        if seriesType_or_config is not None:
            if isinstance(seriesType_or_config, SeriesType):
                seriesType = seriesType_or_config
            else:
                config = seriesType_or_config

        self._name = name
        self._type = seriesType
        self._config = config


    def getConfig(self):
        """@return: Returns the configuration object associated with this
        series"""
        return self._config


    def getName(self):
        """@return: Returns name of this series"""
        return self._name


    def setName(self, name):
        """Sets name of this series
        """
        self._name = name


    def getType(self):
        """@return"""
        return self._type


    def setType(self, typ):
        """Sets type of this series
        """
        self._type = typ


    def getStack(self):
        """@return: Returns stack of this series"""
        return self._stack


    def setStack(self, stack):
        """By using this stack property, it is possible to group series in a
        stacked chart. Sets stack for this series. If two series belongs to
        the same stack then the resultant chart will be stacked chart
        """
        self._stack = stack


    def getXAxis(self):
        """@return: Returns x-axis associated with this series.
        @see: L{Axis}
        """
        return self._xAxis


    def setXAxis(self, xAxis):
        """Sets x-axis of this series. A series can be associated with at most
        one x-axis.
        """
        self._xAxis = xAxis


    def getYAxis(self):
        """@return: Returns y-axis of this series."""
        return self._yAxis


    def setYAxis(self, yAxis):
        """Sets y-axis of this series. A series can be associated with at most
        one y-axis.
        """
        self._yAxis = yAxis


    def removePoint(self, *points):
        pointsRemovedList = list()
        for point in points:
            if point in self._points:
                self._points.remove(point)
                pointsRemovedList.append(point)

        self.updatePointXValuesIfNotPresent()

        for point in pointsRemovedList:
            if self._invientCharts is not None:
                self._invientCharts.addSeriesPointRemovedOperation(
                        point.getSeries().getName(), point)
                self._invientCharts.requestRepaint()


    def removeAllPoints(self):
        """Removes all points in this series"""
        self._points.clear()
        if self._invientCharts is not None:
            cur = SeriesCUR(SeriesCURType.UPDATE, self.getName(), True)
            self._invientCharts.addSeriesCUROperation(cur)
            self._invientCharts.requestRepaint()


    def addPoint(self, shift, points):
        """Adds one or more points into this series, specified as an argument
        to this method

        @return: Returns null if the argument is null otherwise returns a
                 collection of points which are added in this series. If a
                 point has same (x, y) value as any other point in the
                 argument points then it will not be added.
        """
        points = [points] if isinstance(points, Point) else points

        if shift:
            # Remove first point as other points gets appended at the end
            pointsItr = iter(self._points)
            try:
                p = pointsItr.next()
                self._points.remove(p)
            except StopIteration:
                pass

        pointsAddedList = list()

        for point in points:
            if point not in self._points:
                self._points.add(point)
                pointsAddedList.append(point)

        self.updatePointXValuesIfNotPresent()

        # Now record point add event as we need to know x value of a point
        for point in pointsAddedList:
            if self._invientCharts is not None:
                self._invientCharts.addSeriesPointAddedOperation(
                        point.getSeries().getName(), point)
                self._invientCharts.requestRepaint()

        return OrderedSet(pointsAddedList)


    def addPointsInternal(self, points):
        for point in points:
            self._points.add(point)


    def getPoints(self):
        """@return: Returns all points of this series. Adding or removing any
                point to or from the returned collection will not impact the
                chart. To add a point or points, use addPoint() or
                removePoint() method.
        """
        return OrderedSet(self._points)


    def setPoints(self, points):
        """Sets points into this series

        @return: Returns null if the argument is null otherwise returns a
                 collection of points which are set in this series. If a point
                 has same (x, y) value as any other point in the argument
                 points then it will not be added.
        """
        if points is not None:
            self._points.clear()
            self.addPointsInternal(points)
            self.updatePointXValuesIfNotPresent()
            if self._invientCharts is not None:
                cur = SeriesCUR(SeriesCURType.UPDATE, self.getName(), True)
                self._invientCharts.addSeriesCUROperation(cur)
                self._invientCharts.requestRepaint()
            return self.getPoints()
        return None


    def updatePointXValuesIfNotPresent(self):
        """Each of the subclass needs to implement this method to ensure that
        each point has appropriate X value even if it is not specified.
        """
        pass


    def show(self):
        """Show this series"""
        self._config = SeriesConfig() if self._config is None else self._config
        self._config.setVisible(True)
        if self._invientCharts is not None:
            cur = SeriesCUR(SeriesCURType.UPDATE, self.getName())
            self._invientCharts.addSeriesCUROperation(cur)
            self._invientCharts.requestRepaint()


    def hide(self):
        """Hide this series"""
        self._config = SeriesConfig() if self._config is None else self._config
        self._config.setVisible(False)
        if self._invientCharts is not None:
            cur = SeriesCUR(SeriesCURType.UPDATE, self.getName())
            self._invientCharts.addSeriesCUROperation(cur)
            self._invientCharts.requestRepaint()


    def setInvientCharts(self, invientCharts):
        self._invientCharts = invientCharts


    def __hash__(self):
        prime = 31
        result = 1
        result = ((prime * result)
                + (0 if self._name is None else hash(self._name)))
        return result


    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None:
            return False
        if self.__class__ != obj.__class__:
            return False
        other = obj
        if self._name is None:
            if other._name is not None:
                return False
        elif not (self._name == other._name):
            return False
        return True


    def __str__(self):
        return ('Series [points=' + self._points
                + ', name=' + self._name
                + ', type=' + str(self._type)
                + ', stack=' + self._stack
                + ', xAxis=' + str(self._xAxis)
                + ', yAxis=' + str(self._yAxis)
                + ', config=' + str(self._config) + ']')


class XYSeries(Series):
    """This class defines a number series. In this series both X and Y values
    must be number. To use date values, use L{DateTimeSeries}

    @author: Invient
    @author: Richard Lincoln

    @see: L{DateTimeSeries}
    """

    def __init__(self, name, seriesType_or_config=None, config=None):
        """Creates a series with given name, type and configuration

        @param name:
                   the name of this series
        @param seriesType_or_config:
                   the type of this series or the configuration for this series
        @param config:
                   the configuration for this series
        """
        seriesType = None
        if seriesType_or_config is not None:
            if isinstance(seriesType_or_config, SeriesType):
                seriesType = seriesType_or_config
            else:
                config = seriesType_or_config

        super(XYSeries, self).__init__(name, seriesType, config)


    def removePoint(self, *points):
        """Removes the specified point from the series
        """
        super(XYSeries, self).removePoint(*points)


    def removeAllPoints(self):
        super(XYSeries, self).removeAllPoints()


    def addPoint(self, point_or_points, shift=None):
        """Appends the specified point(s) into the series if they do not exists
        in this series. The points which already exists will not be appended. A
        collection of points appended to this series will be returned.

        @param point_or_points:
        @param shift:
                   If true then one point is shifted off the start of this
                   series as one is appended to the end.
        @return: Returns a collection of points which are added in this
                 series. If a point has same (x, y) value as any other point
                 in the input argument points then it will not be added in
                 this series.
        """
        if shift is None:
            points = point_or_points
            return super(XYSeries, self).addPoint(False, points)
        else:
            point = point_or_points
            point.setShift(shift)
            return super(XYSeries, self).addPoint(shift, point)


    def getPoints(self):
        return super(XYSeries, self).getPoints()


    def setSeriesPoints(self, points):
        """Sets points into this series. This method removes all of its points
        and then add points specified in the method argument. If the argument
        is null then no actions are taken.

        @param points:
                   the collection of points to set into this series.
        @return: Returns a collection of points which are set in this series.
                 If a point has same (x, y) value as any other point in the
                 argument points then it will not be added.
        """
        return super(XYSeries, self).setPoints(points)


    def updatePointXValuesIfNotPresent(self):
        pointStart = 0
        pointInterval = 1

        if isinstance(super(XYSeries, self).getConfig(), BaseLineConfig):
            config = super(XYSeries, self).getConfig()
            if config.getPointStart() is not None:
                pointStart = config.getPointStart()
            if config.getPointInterval() is not None:
                pointInterval = config.getPointInterval()

        count = 0

        for point in self.getPoints():
            if ((point.getX() is None)
                    or (point.getX() is not None and point.isAutosetX())):
                point.setAutosetX(True)
                if count == 0:
                    point.setX(pointStart)
                    count += 1
                else:
                    pointStart = pointStart + pointInterval
                    point.setX(pointStart)


class DateTimeSeries(Series):
    """This class defines a datetime series. In this series, the X value must
    be date and Y values must be number. To use number values, use L{XYSeries}

    By default, the time of a day is not included in the X value. In order to
    include time, use a constructor with argument isIncludeTime and pass true
    value for the argument.

    @author: Invient
    @author: Richard Lincoln

    @see: L{XYSeries}
    """

    def __init__(self, invientCharts, *args):
        """Creates a series with given name. This series will not consider time
        in the X property of L{DateTimePoint}.

        @param args:
            tuple of the form:
              - (name)
                - the name of this series
              - (name, isIncludeTime)
                - the name of this series
                - If true then the time in the X property of L{DateTimePoint}
                  will be considered when drawing the chart. Defaults to false.
              - (name, config)
                - the name of this series
                - the configuration for this series
              - (name, config, isIncludeTime)
                - the name of this series
                - the configuration for this series
                - If true then the time in the X property of L{DateTimePoint}
                  will be considered when drawing the chart. Defaults to false.
              - (name, seriesType, isIncludeTime)
                - the name of this series
                - the type of this series
                - If true then the time in the X property of L{DateTimePoint}
                  will be considered when drawing the chart. Defaults to false.
              - (name, seriesType, config)
                - the name of this series
                - the type of this series
                - the configuration for this series
              - (name, seriesType, config, isIncludeTime)
                - the name of this series
                - the type of this series
                - the configuration for this series
                - If true then the time in the X property of L{DateTimePoint}
                  will be considered when drawing the chart. Defaults to false.
        """
        self._invientCharts = invientCharts

        self._includeTime = None

        args = args
        nargs = len(args)
        if nargs == 1:
            name, = args
            self.__init__(invientCharts, name, False)
        elif nargs == 2:
            if isinstance(args[1], SeriesType):
                name, seriesType = args
                self.__init__(invientCharts, name, seriesType, False)
            elif isinstance(args[1], SeriesConfig):
                name, config = args
                self.__init__(invientCharts, name, config, False)
            else:
                name, isIncludeTime = args
                super(DateTimeSeries, self).__init__(name)
                self._includeTime = isIncludeTime
        elif nargs == 3:
            if isinstance(args[1], SeriesType):
                if isinstance(args[2], SeriesConfig):
                    name, seriesType, config = args
                    self.__init__(invientCharts, name, seriesType, config, False)
                else:
                    name, seriesType, isIncludeTime = args
                    super(DateTimeSeries, self).__init__(name, seriesType)
                    self._includeTime = isIncludeTime
            else:
                name, config, isIncludeTime = args
                super(DateTimeSeries, self).__init__(name, config)
                self._includeTime = isIncludeTime
        elif nargs == 4:
            name, seriesType, config, isIncludeTime = args
            super(DateTimeSeries, self).__init__(name, seriesType, config)
            self._includeTime = isIncludeTime
        else:
            raise ValueError


    def removePoint(self, *points):
        """Removes all points specified as method argument into this series
        """
        super(DateTimeSeries, self).removePoint(points)


    def removeAllPoints(self):
        super(DateTimeSeries, self).removeAllPoints()


    def addPoint(self, point_or_points, shift=None):
        """Appends the specified point(s) into the series if they do not exists in
        this series. The points which already exists will not be appended. A
        collection of points appended to this series will be returned.

        @param point_or_points:
        @param shift:
                   If true then one point is shifted off the start of this
                   series as one is appended to the end.
        @return Returns a collection of points which are added in this
                series. If a point has same (x, y) value as any other point
                in the input argument points then it will not be added in
                this series.
        """
        if shift is None:
            points = point_or_points
            return super(DateTimeSeries, self).addPoint(False, points)
        else:
            point = point_or_points
            point.setShift(shift)
            return super(DateTimeSeries, self).addPoint(shift, point)


    def isIncludeTime(self):
        """@return: Returns true if the time in the X property of
                L{DateTimePoint} will be considered when drawing the
                chart otherwise false.
        """
        return self._includeTime


    def getPoints(self):
        return super(DateTimeSeries, self).getPoints()


    def setSeriesPoints(self, points):
        """Sets points into this series. This method removes all of its points
        and then add points specified in the method argument. If the argument
        is null then no actions are taken.

        @param points:
                   the collection of points to set into this series.
        @return: Returns a collection of points which are added in this
                 series. If a point has same (x, y) value as any other point
                 in the input argument points then it will not be added in
                 this series.
        """
        return super(DateTimeSeries, self).setPoints(points)


    def updatePointXValuesIfNotPresent(self):
        pointStart = self.getDefPointStart()
        pointInterval = 3600000
        # 1 hour
        if isinstance(super(DateTimeSeries, self).getConfig(), BaseLineConfig):
            config = super(DateTimeSeries, self).getConfig()
            if config.getPointStart() is not None:
                pointStart = config.getPointStart()
            if config.getPointInterval() is not None:
                pointInterval = config.getPointInterval()
        prevDate = datetime.fromtimestamp(pointStart / 1e03)
        count = 0
        for point in self.getPoints():
            if ((point.getX() is None)
                    or (point.getX() is not None and point.isAutosetX())):
                point.setAutosetX(True)
                if count == 0:
                    point.setX(prevDate)
                    count += 1
                else:
                    point.setX(self.getUpdatedDate(prevDate, pointInterval))
                    prevDate = point.getX()


    @classmethod
    def getDefPointStart(cls):
#        dt = datetime(1970, 1, 1)
#        return long(totalseconds(dt - datetime(1970, 1, 1)) * 1e03)
        return -3600000.0


    @classmethod
    def getUpdatedDate(cls, dt, milliseconds):
        ts = getDate(dt) + milliseconds
        return datetime.fromtimestamp(ts / 1e03)


    def __str__(self):
        return ('DateTimeSeries [includeTime=' + self._includeTime
                + ', getConfig()=' + str(self._invientCharts.getConfig())
                + ', getName()=' + self.getName()
                + ', getType()=' + str(self.getType())
                + ', getStack()=' + self.getStack()
                + ', getXAxis()=' + str(self.getXAxis())
                + ', getYAxis()=' + str(self.getYAxis())
                + ']')


class SeriesType(object):
    COMMONSERIES = None
    LINE = None
    SPLINE = None
    SCATTER = None
    AREA = None
    AREASPLINE = None
    BAR = None
    COLUMN = None
    PIE = None

    def __init__(self, typ):
        self._typ = typ

    def getName(self):
        return self._typ

    @classmethod
    def values(cls):
        return [cls.COMMONSERIES, cls.LINE, cls.SPLINE, cls.SCATTER,
                cls.AREA, cls.AREASPLINE, cls.BAR, cls.COLUMN, cls.PIE]

SeriesType.COMMONSERIES = SeriesType('series')
SeriesType.LINE = SeriesType('line')
SeriesType.SPLINE = SeriesType('spline')
SeriesType.SCATTER = SeriesType('scatter')
SeriesType.AREA = SeriesType('area')
SeriesType.AREASPLINE = SeriesType('areaspline')
SeriesType.BAR = SeriesType('bar')
SeriesType.COLUMN = SeriesType('column')
SeriesType.PIE = SeriesType('pie')


class SeriesCUR(object):

    def getType(self):
        return self._type

    def getName(self):
        return self._name

    def __init__(self, typ, name, reloadPoints=False):
        self._type = typ
        self._name = name
        self._reloadPoints = reloadPoints
        self._pointsAdded = OrderedSet()
        self._pointsRemoved = OrderedSet()

        super(SeriesCUR, self).__init__()


    def isReloadPoints(self):
        """Indicates whether the client/terminal should update series by
        setting all data of a series instead of adding or removing individual
        points

        @return: Returns true if the data of the series must be reloaded
                 otherwise false.
        """
        return self._reloadPoints


    def setReloadPoints(self, reloadPoints):
        self._reloadPoints = reloadPoints


    def trackPointAdded(self, point):
        self._pointsAdded.add(point)


    def trackPointRemoved(self, point):
        # If the point was added earlier and now removed
        # then there is no need to record its add/remove operation
        # as add of a point is nullified by remove of a point
        if not self.removePointIfTrackedAlready(point):
            self._pointsRemoved.add(point)


    def removePointIfTrackedAlready(self, point):
        # Used to clear all points added/removed when
        # series data is set/cleared using series.setPoints() or
        # series.removeAllPoints()
        return self._pointsAdded.remove(point)


    def clearTrackedPoints(self):
        self._pointsAdded.clear()
        self._pointsRemoved.clear()


    def getPointsAdded(self):
        return self._pointsAdded


    def getPointsRemoved(self):
        return self._pointsRemoved


    def __hash__(self):
        prime = 31
        result = 1
        result = ((prime * result)
                + (0 if self._name is None else hash(self._name)))
        result = ((prime * result)
                + (0 if self._type is None else hash(self._type)))
        return result


    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None:
            return False
        if self.__class__ != obj.__class__:
            return False
        other = obj
        if self._name is None:
            if other._name is not None:
                return False
        elif not (self._name == other._name):
            return False
        if self._type is None:
            if other._type is not None:
                return False
        elif not (self._type == other._type):
            return False
        return True


    def __str__(self):
        return ('SeriesCUR [type=' + str(self._type)
                + ', name=' + self._name
                + ', reloadPoints=' + str(self._reloadPoints)
                + ', pointsAdded=' + str(self._pointsAdded)
                + ', pointsRemoved=' + str(self._pointsRemoved)
                + ']')


class SeriesCURType(object):

    ADD = None
    UPDATE = None
    REMOVE = None

    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    @classmethod
    def values(cls):
        return [cls.ADD, cls.UPDATE, cls.REMOVE]

SeriesCURType.ADD = SeriesCURType('Add')
SeriesCURType.UPDATE = SeriesCURType('Update')
SeriesCURType.REMOVE = SeriesCURType('Remove')
