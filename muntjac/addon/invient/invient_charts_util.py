# @INVIENT_COPYRIGHT@
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

"""Utility functions used by L{InvientCharts} to write its state to
the UIDL stream. The state includes properties of L{InvientCharts} such
as L{InvientChartsConfig}, L{Series}, L{Point} and various chart events.

In general, only non-null properties/attributes of a chart are written to
the UIDL stream.

@author: Invient
@author: Richard Lincoln
"""

from datetime \
    import datetime

from muntjac.util \
    import totalseconds

from muntjac.addon.invient.invient_charts_config \
    import AreaConfig, AreaSplineConfig, DateTimeRange, DateTimeValue, \
    Grid, NumberRange, NumberValue, Tick, BarConfig, CategoryAxis, \
    ColumnConfig, DateTimeAxis, ImageMarker, LineConfig, \
    NonLinearSeriesState, NumberAxis, NumberXAxis, NumberYAxis, PieConfig, \
    PieDataLabel, ScatterConfig, SplineConfig, SymbolMarker, XAxisDataLabel


def writeTitleBaseOptions(target, titleBaseOptions):
    """Writes configuration attributes common to chart title and subtitle.

    @param target
    @param titleBaseOptions
    @throws PaintException
    """
    if titleBaseOptions.getText() is not None:
        target.addAttribute('text', titleBaseOptions.getText())
    if titleBaseOptions.getX() is not None:
        target.addAttribute('x', titleBaseOptions.getX())
    if titleBaseOptions.getY() is not None:
        target.addAttribute('y', titleBaseOptions.getY())
    if titleBaseOptions.getFloating() is not None:
        target.addAttribute('floating', titleBaseOptions.getFloating())
    if titleBaseOptions.getAlign() is not None:
        target.addAttribute('align', titleBaseOptions.getAlign().getName())
    if titleBaseOptions.getVertAlign() is not None:
        target.addAttribute('verticalAlign',
                titleBaseOptions.getVertAlign().getName())
    if titleBaseOptions.getStyle() is not None:
        target.addAttribute('style', titleBaseOptions.getStyle())


def writeTitleConfig(target, titleOptions):
    """Writes configuration attributes of the chart title.

    @param target
    @param titleOptions
    @throws PaintException
    """
    target.startTag('title')
    writeTitleBaseOptions(target, titleOptions)
    if titleOptions.getMargin() is not None:
        target.addAttribute('margin', titleOptions.getMargin())
    target.endTag('title')


def writeSubtitleConfig(target, subtitleOptions):
    """Writes configuration attributes of the chart subtitle. Only those
    attributes are written who have got non-null values.

    @param target
    @param subtitleOptions
    @throws PaintException
    """
    target.startTag('subtitle')
    writeTitleBaseOptions(target, subtitleOptions)
    target.endTag('subtitle')


def writeCreditConfig(target, creditOptions):
    """Writes configuration attributes of the chart subtitle.

    @param target
    @param creditOptions
    @throws PaintException
    """
    target.startTag('credit')

    if creditOptions.getEnabled() is not None:
        target.addAttribute('enabled', creditOptions.getEnabled())

    target.startTag('position')

    if creditOptions.getPosition() is not None:
        if creditOptions.getPosition().getAlign() is not None:
            target.addAttribute('align',
                    creditOptions.getPosition().getAlign().getName())
        if creditOptions.getPosition().getVertAlign() is not None:
            target.addAttribute('verticalAlign',
                    creditOptions.getPosition().getVertAlign().getName())
        if creditOptions.getPosition().getX() is not None:
            target.addAttribute('x', creditOptions.getPosition().getX())
        if creditOptions.getPosition().getY() is not None:
            target.addAttribute('y', creditOptions.getPosition().getY())

    target.endTag('position')

    if creditOptions.getLink() is not None:
        target.addAttribute('href', creditOptions.getLink())
    if creditOptions.getStyle() is not None:
        target.addAttribute('style', creditOptions.getStyle())
    if creditOptions.getText() is not None:
        target.addAttribute('text', creditOptions.getText())

    target.endTag('credit')


def writeLegendConfig(target, legendOptions):
    """Writes configuration attributes of the chart legend.

    @param target
    @param legendOptions
    @throws PaintException
    """
    target.startTag('legend')
    if legendOptions.getBackgroundColor() is not None:
        target.addAttribute('backgroundColor',
                legendOptions.getBackgroundColor().getString())
    if legendOptions.getBorderColor() is not None:
        target.addAttribute('borderColor',
                legendOptions.getBorderColor().getString())
    if legendOptions.getBorderRadius() is not None:
        target.addAttribute('borderRadius',
                legendOptions.getBorderRadius())
    if legendOptions.getBorderWidth() is not None:
        target.addAttribute('borderWidth', legendOptions.getBorderWidth())
    if legendOptions.getEnabled() is not None:
        target.addAttribute('enabled', legendOptions.getEnabled())
    if legendOptions.getFloating() is not None:
        target.addAttribute('floating', legendOptions.getFloating())
    if legendOptions.getItemHiddenStyle() is not None:
        target.addAttribute('itemHiddenStyle',
                legendOptions.getItemHiddenStyle())
    if legendOptions.getItemHoverStyle() is not None:
        target.addAttribute('itemHoverStyle',
                legendOptions.getItemHoverStyle())
    if legendOptions.getItemStyle() is not None:
        target.addAttribute('itemStyle', legendOptions.getItemStyle())
    if legendOptions.getItemWidth() is not None:
        target.addAttribute('itemWidth', legendOptions.getItemWidth())
    if legendOptions.getLayout() is not None:
        target.addAttribute('layout', legendOptions.getLayout().getName())
    if legendOptions.getLabelFormatterJsFunc() is not None:
        target.addAttribute('labelFormatter',
                legendOptions.getLabelFormatterJsFunc())
    if legendOptions.getMargin() is not None:
        target.addAttribute('margin', legendOptions.getMargin())
    if legendOptions.getReversed() is not None:
        target.addAttribute('reversed', legendOptions.getReversed())
    if legendOptions.getShadow() is not None:
        target.addAttribute('shadow', legendOptions.getShadow())
    if legendOptions.getSymbolPadding() is not None:
        target.addAttribute('symbolPadding',
                legendOptions.getSymbolPadding())
    if legendOptions.getSymbolWidth() is not None:
        target.addAttribute('symbolWidth', legendOptions.getSymbolWidth())
    if legendOptions.getWidth() is not None:
        target.addAttribute('width', legendOptions.getWidth())
    if legendOptions.getPosition() is not None:
        if legendOptions.getPosition().getAlign() is not None:
            target.addAttribute('align',
                    legendOptions.getPosition().getAlign().getName())
        if legendOptions.getPosition().getVertAlign() is not None:
            target.addAttribute('verticalAlign',
                    legendOptions.getPosition().getVertAlign().getName())
        if legendOptions.getPosition().getX() is not None:
            target.addAttribute('x', legendOptions.getPosition().getX())
        if legendOptions.getPosition().getY() is not None:
            target.addAttribute('y', legendOptions.getPosition().getY())
    target.endTag('legend')


def writeTooltipConfig(target, tooltipOptions):
    """Writes configuration attributes of the chart tooltip.

    @param target
    @param tooltipOptions
    @throws PaintException
    """
    target.startTag('tooltip')
    if tooltipOptions.getBackgroundColor() is not None:
        target.addAttribute('backgroundColor',
                tooltipOptions.getBackgroundColor().getString())
    if tooltipOptions.getBorderColor() is not None:
        target.addAttribute('borderColor',
                tooltipOptions.getBorderColor().getString())
    if tooltipOptions.getBorderRadius() is not None:
        target.addAttribute('borderRadius',
                tooltipOptions.getBorderRadius())
    if tooltipOptions.getBorderWidth() is not None:
        target.addAttribute('borderWidth', tooltipOptions.getBorderWidth())
    if tooltipOptions.getCrosshairs() is not None:
        target.addAttribute('crosshairs', tooltipOptions.getCrosshairs())
    if tooltipOptions.getEnabled() is not None:
        target.addAttribute('enabled', tooltipOptions.getEnabled())
    if tooltipOptions.getFormatterJsFunc() is not None:
        target.addAttribute('formatter',
                tooltipOptions.getFormatterJsFunc())
    if tooltipOptions.getShadow() is not None:
        target.addAttribute('shadow', tooltipOptions.getShadow())
    if tooltipOptions.getShared() is not None:
        target.addAttribute('shared', tooltipOptions.getShared())
    if tooltipOptions.getSnap() is not None:
        target.addAttribute('snap', tooltipOptions.getSnap())
    if tooltipOptions.getStyle() is not None:
        target.addAttribute('style', tooltipOptions.getStyle())
    target.endTag('tooltip')


def writeGeneralChartConfig(target, chartOptions):
    """Writes configuration attributes of the chart itself.

    @param target
    @param chartOptions
    @throws PaintException
    """
    target.startTag('chart')
    if chartOptions.getType() is not None:
        target.addAttribute('type', chartOptions.getType().getName())
    if chartOptions.getWidth() is not None:
        target.addAttribute('width', chartOptions.getWidth())
    if chartOptions.getHeight() is not None:
        target.addAttribute('height', chartOptions.getHeight())
    if chartOptions.getBackgroundColor() is not None:
        target.addAttribute('backgroundColor',
                chartOptions.getBackgroundColor().getString())
    if chartOptions.getBorderColor() is not None:
        target.addAttribute('borderColor',
                chartOptions.getBorderColor().getString())
    if chartOptions.getBorderRadius() is not None:
        target.addAttribute('borderRadius', chartOptions.getBorderRadius())
    if chartOptions.getBorderWidth() is not None:
        target.addAttribute('borderWidth', chartOptions.getBorderWidth())
    if chartOptions.getIgnoreHiddenSeries() is not None:
        target.addAttribute('ignoreHiddenSeries',
                chartOptions.getIgnoreHiddenSeries())
    if chartOptions.getInverted() is not None:
        target.addAttribute('inverted', chartOptions.getInverted())
    if chartOptions.getMargin() is not None:
        if chartOptions.getMargin().getTop() is not None:
            target.addAttribute('marginTop',
                    chartOptions.getMargin().getTop())
        if chartOptions.getMargin().getLeft() is not None:
            target.addAttribute('marginLeft',
                    chartOptions.getMargin().getLeft())
        if chartOptions.getMargin().getBottom() is not None:
            target.addAttribute('marginBottom',
                    chartOptions.getMargin().getBottom())
        if chartOptions.getMargin().getRight() is not None:
            target.addAttribute('marginRight',
                    chartOptions.getMargin().getRight())
    if chartOptions.getSpacing() is not None:
        if chartOptions.getSpacing().getTop() is not None:
            target.addAttribute('spacingTop',
                    chartOptions.getSpacing().getTop())
        if chartOptions.getSpacing().getLeft() is not None:
            target.addAttribute('spacingLeft',
                    chartOptions.getSpacing().getLeft())
        if chartOptions.getSpacing().getBottom() is not None:
            target.addAttribute('spacingBottom',
                    chartOptions.getSpacing().getBottom())
        if chartOptions.getSpacing().getRight() is not None:
            target.addAttribute('spacingRight',
                    chartOptions.getSpacing().getRight())
    if chartOptions.getShowAxes() is not None:
        target.addAttribute('showAxes', chartOptions.getShowAxes())
    if chartOptions.getZoomType() is not None:
        target.addAttribute('zoomType',
                chartOptions.getZoomType().getName())
    target.addAttribute('clientZoom', chartOptions.isClientZoom())
    if chartOptions.getAlignTicks() is not None:
        target.addAttribute('alignTicks', chartOptions.getAlignTicks())
    if chartOptions.getAnimation() is not None:
        target.addAttribute('animation', chartOptions.getAnimation())
    if chartOptions.getClassName() is not None:
        target.addAttribute('className', chartOptions.getClassName())
    if chartOptions.getPlot() is not None:
        if chartOptions.getPlot().getBackgroundColor() is not None:
            target.addAttribute('plotBackgroundColor',
                chartOptions.getPlot().getBackgroundColor().getString())
        if chartOptions.getPlot().getBorderColor() is not None:
            target.addAttribute('plotBorderColor',
                chartOptions.getPlot().getBorderColor().getString())
        if chartOptions.getPlot().getBackgroundImage() is not None:
            target.addAttribute('plotBackgroundImage',
                chartOptions.getPlot().getBackgroundImage())
        if chartOptions.getPlot().getBorderWidth() is not None:
            target.addAttribute('plotBorderWidth',
                chartOptions.getPlot().getBorderWidth())
        if chartOptions.getPlot().getShadow() is not None:
            target.addAttribute('plotShadow',
                chartOptions.getPlot().getShadow())
    if chartOptions.getReflow() is not None:
        target.addAttribute('reflow', chartOptions.getReflow())
    if chartOptions.getShadow() is not None:
        target.addAttribute('shadow', chartOptions.getShadow())
    if chartOptions.getStyle() is not None:
        target.addAttribute('style', chartOptions.getStyle())
    target.endTag('chart')


def writeSeriesConfigPerSeriesType(target, seriesOptions):
    """Writes configuration attributes of every series type. The series
    type can be one of the line, spline, scatter, area, areaspline, bar,
    column and pie.

    @param target
    @param seriesOptions
    @throws PaintException
    """
    target.startTag('seriesOptionsPerSeriesType')
    # For each SeriesType have separate tag
    for k, seriesEntryOptions in seriesOptions.iteritems():
        tagName = k.getName()
        target.startTag(tagName)
        # Write options for appropriate series type
        writeSeriesConfig(target, seriesEntryOptions)
        target.endTag(tagName)
    target.endTag('seriesOptionsPerSeriesType')


def writeSeriesConfig(target, series):
    """Writes configuration attributes of a single series.

    @param target
    @param series
    @raise PaintException:
    """
    # Write options for appropriate series type
    if isinstance(series, LineConfig):
        writeLineOptions(target, series)
    elif isinstance(series, ScatterConfig):
        writeScatterOptions(target, series)
    elif isinstance(series, SplineConfig):
        writeSplineOptions(target, series)
    elif isinstance(series, AreaConfig):
        writeAreaOptions(target, series)
    elif isinstance(series, AreaSplineConfig):
        writeAreaSplineOptions(target, series)
    elif isinstance(series, ColumnConfig):
        writeColumnOptions(target, series)
    elif isinstance(series, BarConfig):
        writeBarOptions(target, series)
    elif isinstance(series, PieConfig):
        writePieOptions(target, series)
    else:
        # Common series attributes
        writeCommonSeriesOptions(target, series)


def writeCommonSeriesOptions(target, seriesOptions):
    """Writes configuration attributes common to all types of series.

    @param target
    @param seriesOptions
    @throws PaintException
    """
    if seriesOptions.getAllowPointSelect() is not None:
        target.addAttribute('allowPointSelect',
                seriesOptions.getAllowPointSelect())
    if seriesOptions.getAnimation() is not None:
        target.addAttribute('animation',
                seriesOptions.getAnimation())
    if seriesOptions.getCursor() is not None:
        target.addAttribute('cursor', seriesOptions.getCursor())
    if seriesOptions.getColor() is not None:
        target.addAttribute('color', seriesOptions.getColor().getString())
    if seriesOptions.getEnableMouseTracking() is not None:
        target.addAttribute('enableMouseTracking',
                seriesOptions.getEnableMouseTracking())
    # if (seriesOptions.getSelected() != null) {
    # target.addAttribute("selected", seriesOptions.getSelected());
    # }
    if seriesOptions.getShowCheckbox() is not None:
        target.addAttribute('showCheckbox',
                seriesOptions.getShowCheckbox())
    if seriesOptions.getShowInLegend() is not None:
        target.addAttribute('showInLegend',
                seriesOptions.getShowInLegend())
    if seriesOptions.getStacking() is not None:
        target.addAttribute('stacking',
                seriesOptions.getStacking().getName())
    if seriesOptions.getShadow() is not None:
        target.addAttribute('shadow', seriesOptions.getShadow())
    if seriesOptions.getVisible() is not None:
        target.addAttribute('visible', seriesOptions.getVisible())
    # Data Label
    writeSeriesDataLabel(target, seriesOptions.getDataLabel())
    # State
    writeSeriesState(target, seriesOptions.getHoverState())


def writeSeriesState(target, seriesState):
    """Writes configuration attributes of a series hover state.

    @param target
    @param seriesState
    @throws PaintException
    """
    target.startTag('state')
    if seriesState is not None:
        target.startTag('hover')
        if seriesState.getEnabled() is not None:
            target.addAttribute('enabled', seriesState.getEnabled())
        if seriesState.getLineWidth() is not None:
            target.addAttribute('lineWidth', seriesState.getLineWidth())
        if (isinstance(seriesState, NonLinearSeriesState)
                and seriesState.getBrightness() is not None):
            target.addAttribute('brightness', seriesState.getBrightness())
        target.endTag('hover')
    target.endTag('state')


def writeSeriesDataLabel(target, dataLabel):
    """Writes configuration attributes common to all types of series. It
    takes care of specific data labels in case of pie.

    @param target
    @param dataLabel
    @raise PaintException
    """
    target.startTag('dataLabel')
    if dataLabel is not None:
        if isinstance(dataLabel, PieDataLabel):
            writePieDataLabel(target, dataLabel)
        else:
            writeDataLabel(target, dataLabel)
    target.endTag('dataLabel')


def writeDataLabel(target, dataLabel):
    """Writes configuration attributes of a series data labels.

    @param target
    @param dataLabel
    @raise PaintException
    """
    if dataLabel.getAlign() is not None:
        target.addAttribute('align', dataLabel.getAlign().getName())
    if dataLabel.getEnabled() is not None:
        target.addAttribute('enabled', dataLabel.getEnabled())
    if dataLabel.getFormatterJsFunc() is not None:
        target.addAttribute('formatter', dataLabel.getFormatterJsFunc())
    if dataLabel.getRotation() is not None:
        target.addAttribute('rotation', dataLabel.getRotation())
    if dataLabel.getStyle() is not None:
        target.addAttribute('style', dataLabel.getStyle())
    if dataLabel.getX() is not None:
        target.addAttribute('x', dataLabel.getX())
    if dataLabel.getY() is not None:
        target.addAttribute('y', dataLabel.getY())
    if dataLabel.getColor() is not None:
        target.addAttribute('color', dataLabel.getColor().getString())


def writePieDataLabel(target, dataLabel):
    """Writes configuration attributes of a pie chart's data label.

    @param target
    @param dataLabel
    @raise PaintException
    """
    writeDataLabel(target, dataLabel)
    if dataLabel.getConnectorWidth() is not None:
        target.addAttribute('connectorWidth',
                dataLabel.getConnectorWidth())
    if dataLabel.getConnectorPadding() is not None:
        target.addAttribute('connectorPadding',
                dataLabel.getConnectorPadding())
    if dataLabel.getConnectorColor() is not None:
        target.addAttribute('connectorColor',
                dataLabel.getConnectorColor().getString())
    if dataLabel.getDistance() is not None:
        target.addAttribute('distance', dataLabel.getDistance())


def writeAxisDataLabel(target, dataLabel):
    """Writes configuration attributes of an axis data labels.

    @param target
    @param dataLabel
    @raise PaintException
    """
    writeDataLabel(target, dataLabel)
    if dataLabel.getStep() is not None:
        target.addAttribute('step', dataLabel.getStep())


def writeXAxisDataLabel(target, dataLabel):
    """Writes configuration attributes of an x-axis data labels.

    @param target
    @param dataLabel
    @raise PaintException
    """
    target.startTag('label')
    if dataLabel is not None:
        writeAxisDataLabel(target, dataLabel)
        if dataLabel.getStaggerLines() is not None:
            target.addAttribute('staggerLines',
                    dataLabel.getStaggerLines())
    target.endTag('label')


def writeYAxisDataLabel(target, dataLabel):
    """Writes configuration attributes of y-axis data labels.

    @param target
    @param dataLabel
    @raise PaintException
    """
    target.startTag('label')
    if dataLabel is not None:
        writeAxisDataLabel(target, dataLabel)
    target.endTag('label')


def writeMarkerOptions(target, markerOptions):
    """Writes configuration attributes of a marker. It takes care of
    handling image or symbol marker.

    @param target
    @param markerOptions
    @raise PaintException
    """
    target.startTag('marker')
    if markerOptions is not None:
        if markerOptions.getEnabled() is not None:
            target.addAttribute('enabled', markerOptions.getEnabled())
        if isinstance(markerOptions, ImageMarker):
            target.addAttribute('markerType', 'image')
            writeImageMarkerOptions(target, markerOptions)
        elif isinstance(markerOptions, SymbolMarker):
            target.addAttribute('markerType', 'symbol')
            writeSymbolMarkerOptions(target, markerOptions)
            writeMarkerStates(target, markerOptions)
    target.endTag('marker')


def writeMarkerStates(target, marker):
    """Writes configuration attributes of a marker states hover and select

    @param target
    @param marker
    @raise PaintException
    """
    target.startTag('states')
    target.startTag('hover')
    if marker.getHoverState() is not None:
        writeMarkerState(target, marker.getHoverState())
    target.endTag('hover')
    target.startTag('select')
    if marker.getSelectState() is not None:
        writeMarkerState(target, marker.getSelectState())
    target.endTag('select')
    target.endTag('states')


def writeImageMarkerOptions(target, imgMarker):
    """Writes configuration attributes of an image marker

    @param target
    @param imgMarker
    @raise PaintException
    """
    if imgMarker.getImageURL() is not None:
        target.addAttribute('symbol', imgMarker.getImageURL())


def writeSymbolMarkerOptions(target, symbolMarker):
    """Writes configuration attributes of a symbol marker

    @param target
    @param symbolMarker
    @raise PaintException
    """
    if symbolMarker.getFillColor() is not None:
        target.addAttribute('fillColor',
                symbolMarker.getFillColor().getString())
    if symbolMarker.getLineColor() is not None:
        target.addAttribute('lineColor',
                symbolMarker.getLineColor().getString())
    if symbolMarker.getLineWidth() is not None:
        target.addAttribute('lineWidth',
                symbolMarker.getLineWidth())
    if symbolMarker.getRadius() is not None:
        target.addAttribute('radius',
                symbolMarker.getRadius())
    if symbolMarker.getSymbol() is not None:
        target.addAttribute('symbol',
                symbolMarker.getSymbol().getName())


def writeMarkerState(target, markerState):
    """Writes configuration attributes of a marker

    @param target
    @param markerState
    @raise PaintException
    """
    if markerState.getEnabled() is not None:
        target.addAttribute('enabled', markerState.getEnabled())
    if markerState.getFillColor() is not None:
        target.addAttribute('fillColor',
                markerState.getFillColor().getString())
    if markerState.getLineColor() is not None:
        target.addAttribute('lineColor',
                markerState.getLineColor().getString())
    if markerState.getLineWidth() is not None:
        target.addAttribute('lineWidth', markerState.getLineWidth())
    if markerState.getRadius() is not None:
        target.addAttribute('radius', markerState.getRadius())


def writeBaseLineOptions(target, baseLineOptions):
    """Writes configuration attributes common to all lines series such
    as line, spline and area.

    @param target
    @param baseLineOptions
    @raise PaintException
    """
    writeCommonSeriesOptions(target, baseLineOptions)
    if baseLineOptions.getDashStyle() is not None:
        target.addAttribute('dashStyle',
                baseLineOptions.getDashStyle().getName())
    if baseLineOptions.getLineWidth() is not None:
        target.addAttribute('lineWidth', baseLineOptions.getLineWidth())
    if baseLineOptions.getPointInterval() is not None:
        target.addAttribute('pointInterval',
                baseLineOptions.getPointInterval())
    if baseLineOptions.getPointStart() is not None:
        target.addAttribute('pointStart', baseLineOptions.getPointStart())
    if baseLineOptions.getStickyTracking() is not None:
        target.addAttribute('stickyTracking',
                baseLineOptions.getStickyTracking())
    writeMarkerOptions(target, baseLineOptions.getMarker())


def writeSplineOptions(target, splineOptions):
    """Writes configuration attributes of a spline series

    @param target
    @param splineOptions
    @raise PaintException
    """
    writeBaseLineOptions(target, splineOptions)


def writeScatterOptions(target, scatterOptions):
    """Writes configuration attributes of s scatter series

    @param target
    @param scatterOptions
    @raise PaintException
    """
    writeBaseLineOptions(target, scatterOptions)


def writeLineOptions(target, lineOptions):
    """Writes configuration attributes of a line series

    @param target
    @param lineOptions
    @raise PaintException
    """
    writeBaseLineOptions(target, lineOptions)
    if lineOptions.getStep() is not None:
        target.addAttribute('step', lineOptions.getStep())


def writeAreaOptions(target, areaOptions):
    """Writes configuration attributes of an area series

    @param target
    @param areaOptions
    @raise PaintException
    """
    writeBaseLineOptions(target, areaOptions)
    if areaOptions.getFillColor() is not None:
        target.addAttribute('fillColor',
                areaOptions.getFillColor().getString())
    if areaOptions.getFillOpacity() is not None:
        target.addAttribute('fillOpacity', areaOptions.getFillOpacity())
    if areaOptions.getLineColor() is not None:
        target.addAttribute('lineColor',
                areaOptions.getLineColor().getString())
    if areaOptions.getThreshold() is not None:
        target.addAttribute('threshold', areaOptions.getThreshold())


def writeAreaSplineOptions(target, areaSplineOptions):
    """Writes configuration attributes of an area-spline

    @param target
    @param areaSplineOptions
    @raise PaintException
    """
    writeAreaOptions(target, areaSplineOptions)


def writePieOptions(target, pieOptions):
    """Writes configuration attributes of a pie series

    @param target
    @param pieOptions
    @raise PaintException
    """
    writeCommonSeriesOptions(target, pieOptions)
    if pieOptions.getBorderColor() is not None:
        target.addAttribute('borderColor',
                pieOptions.getBorderColor().getString())
    if pieOptions.getBorderWidth() is not None:
        target.addAttribute('borderWidth', pieOptions.getBorderWidth())
    if pieOptions.getCenterX() is not None:
        target.addAttribute('centerX', pieOptions.getCenterX())
    if pieOptions.getCenterY() is not None:
        target.addAttribute('centerY', pieOptions.getCenterY())
    if pieOptions.getInnerSize() is not None:
        target.addAttribute('innerSize', pieOptions.getInnerSize())
    if pieOptions.getSize() is not None:
        target.addAttribute('size', pieOptions.getSize())
    if pieOptions.getSlicedOffset() is not None:
        target.addAttribute('slicedOffset', pieOptions.getSlicedOffset())


def writeBaseBarOptions(target, baseBarOptions):
    """Writes configuration attributes common to columnar series such as
    bar and column

    @param target
    @param baseBarOptions
    @raise PaintException
    """
    writeCommonSeriesOptions(target, baseBarOptions)
    if baseBarOptions.getBorderColor() is not None:
        target.addAttribute('borderColor',
                baseBarOptions.getBorderColor().getString())
    if baseBarOptions.getBorderRadius() is not None:
        target.addAttribute('borderRadius',
                baseBarOptions.getBorderRadius())
    if baseBarOptions.getBorderWidth() is not None:
        target.addAttribute('borderWidth',
                baseBarOptions.getBorderWidth())
    if baseBarOptions.getColorByPoint() is not None:
        target.addAttribute('colorByPoint',
                baseBarOptions.getColorByPoint())
    if baseBarOptions.getGroupPadding() is not None:
        target.addAttribute('groupPadding',
                baseBarOptions.getGroupPadding())
    if baseBarOptions.getMinPointLength() is not None:
        target.addAttribute('minPointLength',
                baseBarOptions.getMinPointLength())
    if baseBarOptions.getPointPadding() is not None:
        target.addAttribute('pointPadding',
                baseBarOptions.getPointPadding())
    if baseBarOptions.getPointWidth() is not None:
        target.addAttribute('pointWidth',
                baseBarOptions.getPointWidth())


def writeBarOptions(target, barOptions):
    """Writes configuration attributes of a bar series

    @param target
    @param barOptions
    @raise PaintException
    """
    writeBaseBarOptions(target, barOptions)


def writeColumnOptions(target, columnOptions):
    """Writes configuration attributes of a column series

    @param target
    @param columnOptions
    @raise PaintException
    """
    writeBaseBarOptions(target, columnOptions)


def writeSeries(target, chartSeriesType, data, xAxes, yAxes):
    """Writes data of each series of the chart. It transforms data into
    a form which is usable by the Muntjac terminal class. It also writes
    configuration attributes specific to each series, if any.

    @param target
    @param chartSeriesType
    @param data
    @param xAxes
    @param yAxes
    @throws PaintException
    """
    if data is None:
        return
    for series in data:
        target.startTag('series')
        if series.getName() is not None and len(series.getName()) > 0:
            target.addAttribute('name', series.getName())
        if series.getType() is not None:
            target.addAttribute('type', series.getType().getName())
        if series.getStack() is not None and len(series.getStack()) > 0:
            target.addAttribute('stack', series.getStack())
        target.addAttribute('xAxis', getXAxisIndex(series.getXAxis(),
                xAxes))
        target.addAttribute('yAxis', getYAxisIndex(series.getYAxis(),
                yAxes))
        seriesOptionsTagName = chartSeriesType.getName()
        if series.getType() is not None:
            seriesOptionsTagName = series.getType().getName()
        target.startTag(seriesOptionsTagName)
        if series.getConfig() is not None:
            writeSeriesConfig(target, series.getConfig())
        target.endTag(seriesOptionsTagName)
        target.startTag('points')
        if series.getPoints() is not None:
            writePoints(target, series.getPoints())
        target.endTag('points')
        target.endTag('series')


def writePoints(target, points):
    """Writes point data (x, y) and its configuration attributes, if any.
    If a point does not have x and y values then the point is skipped.
    However, for such points empty tags is created without any attributes
    or children.

    @param target
    @param points
    @throws PaintException
    """
    from muntjac.addon.invient.invient_charts import DecimalPoint

    if points is None:
        return
    for point in points:
        target.startTag('point')
        if (point.getX() is not None) or (point.getY() is not None):
            if point.getId() is not None and len(point.getId()) > 0:
                target.addAttribute('id', point.getId())
            if point.getName() is not None and len(point.getName()) > 0:
                target.addAttribute('name', point.getName())
            if point.getX() is not None:
                if isinstance(point, DecimalPoint):
                    target.addAttribute('x', float(point.getX()))
                else:
                    target.addAttribute('x', getDate(point.getX(),
                            point.getSeries().isIncludeTime()))

            if point.getY() is not None:
                target.addAttribute('y', float(point.getY()))

            target.addAttribute('isShift', point.isShift())

            # Point config
            if point.getConfig() is not None:
                if point.getConfig().getSliced() is not None:
                    target.addAttribute('sliced',
                            point.getConfig().getSliced())
                if point.getConfig().getSelected() is not None:
                    target.addAttribute('selected',
                            point.getConfig().getSelected())
                if point.getConfig().getColor() is not None:
                    target.addAttribute('color',
                            point.getConfig().getColor().getString())
                if point.getConfig().getMarker() is not None:
                    writeMarkerOptions(target,
                            point.getConfig().getMarker())
        target.endTag('point')


def writeBaseAxis(target, axis, axes):
    """Writes configuration attributes common to all types of axis.

    @param target
    @param axis
    @param axes
    @throws PaintException
    """
    if axis.getAlternateGridColor() is not None:
        target.addAttribute('alternateGridColor',
                axis.getAlternateGridColor().getString())
    if axis.getEndOnTick() is not None:
        target.addAttribute('endOnTick', axis.getEndOnTick())
    if axis.getGrid() is not None:
        writeAxisGrid(target, axis.getGrid())
    if axis.getId() is not None and len(axis.getId()) > 0:
        target.addAttribute('id', axis.getId())
    if axis.getLineColor() is not None:
        target.addAttribute('lineColor', axis.getLineColor().getString())
    if axis.getLineWidth() is not None:
        target.addAttribute('lineWidth', axis.getLineWidth())
    if axis.getLinkedTo() is not None:
        target.addAttribute('linkedTo',
                getAxisIndex(axis.getLinkedTo(), axes))
    if axis.getMaxPadding() is not None:
        target.addAttribute('maxPadding', axis.getMaxPadding())
    if axis.getMaxZoom() is not None:
        target.addAttribute('maxZoom', axis.getMaxZoom())
    if axis.getMinPadding() is not None:
        target.addAttribute('minPadding', axis.getMinPadding())
    if axis.getMinorGrid() is not None:
        writeAxisMinorGrid(target, axis.getMinorGrid())
    if axis.getMinorTick() is not None:
        writeAxisMinorTick(target, axis.getMinorTick())
    if axis.getOffset() is not None:
        target.addAttribute('offset', axis.getOffset())
    if axis.getOpposite() is not None:
        target.addAttribute('opposite', axis.getOpposite())
    if axis.getReversed() is not None:
        target.addAttribute('reversed', axis.getReversed())
    if axis.getShowFirstLabel() is not None:
        target.addAttribute('showFirstLabel', axis.getShowFirstLabel())
    if axis.getShowLastLabel() is not None:
        target.addAttribute('showLastLabel', axis.getShowLastLabel())
    if axis.getStartOfWeek() is not None:
        target.addAttribute('startOfWeek', axis.getStartOfWeek().ordinal())
    if axis.getStartOnTick() is not None:
        target.addAttribute('startOnTick', axis.getStartOnTick())
    if axis.getTick() is not None:
        writeAxisTick(target, axis.getTick())
    if axis.getType() is not None:
        target.addAttribute('type', axis.getType().getName())

    # Title
    writeAxisTitle(target, axis.getTitle())

    # Labels
    if isinstance(axis.getLabel(), XAxisDataLabel):
        writeXAxisDataLabel(target, axis.getLabel())
    else:
        writeYAxisDataLabel(target, axis.getLabel())

    if isinstance(axis, NumberAxis):
        writePlotBands(target, axis.getPlotBands())
        writePlotLines(target, axis.getPlotLines())
    elif isinstance(axis, DateTimeAxis):
        writePlotBands(target, axis.getPlotBands())
        writePlotLines(target, axis.getPlotLines())
    elif isinstance(axis, CategoryAxis):
        writePlotBands(target, axis.getPlotBands())
        writePlotLines(target, axis.getPlotLines())


def getXAxisIndex(indexOfXAxis, xAxes):
    """Returns an index of an x-axis in a list of x-axis only if the
    x-axis exists otherwise null

    @param indexOfXAxis
    @param xAxes
    @return: Retrieves Retrieves an index of an x-axis in a list of x-axis
             only if the x-axis exists otherwise null
    """
    return getAxisIndex(indexOfXAxis, xAxes)


def getYAxisIndex(indexOfYAxis, yAxes):
    """Returns an index of a y-axis in a list of y-axis only if the y-axis
    exists otherwise null

    @param indexOfYAxis
    @param yAxes
    @return: Returns index of a y-axis in a list of y-axis only if the
             y-axis exists otherwise null
    """
    return getAxisIndex(indexOfYAxis, yAxes)


def getAxisIndex(indexOfAxis, axes):
    """Returns an index of an axis in a list of axis only if the axis
    exists otherwise null

    @param indexOfAxis
    @param axes
    @return: Returns an index of an axis in a list of axis only if the
             axis exists otherwise null
    """
    if ((indexOfAxis is None) or (axes is None)) or (len(axes) == 0):
        return 0

    index = 0
    for axis in axes:
        if axis == indexOfAxis:
            return index
        index += 1

    return None


def writePlotBands(target, plotBands):
    """Writes configuration attributes of the plotbands associated with
    an axis.

    @param target
    @param plotBands
    @throws PaintException
    """
    target.startTag('plotBands')
    if plotBands is not None:
        for plotBand in plotBands:
            target.startTag('plotBand')
            if plotBand.getColor() is not None:
                target.addAttribute('color',
                        plotBand.getColor().getString())
            if plotBand.getId() is not None:
                target.addAttribute('id', plotBand.getId())
            if plotBand.getZIndex() is not None:
                target.addAttribute('zIndex', plotBand.getZIndex())
            writePlotLabel(target, plotBand.getLabel())
            writePlotBandRange(target, plotBand.getRange())
            target.endTag('plotBand')
    target.endTag('plotBands')


def writePlotLabel(target, plotLabel):
    """Writes configuration attributes of a plotlabel.

    @param target
    @param plotLabel
    @throws PaintException
    """
    target.startTag('label')
    if plotLabel is not None:
        if plotLabel.getAlign() is not None:
            target.addAttribute('align', plotLabel.getAlign().getName())
        if plotLabel.getRotation() is not None:
            target.addAttribute('rotation', plotLabel.getRotation())
        if plotLabel.getStyle() is not None:
            target.addAttribute('style', plotLabel.getStyle())
        if plotLabel.getText() is not None:
            target.addAttribute('text', plotLabel.getText())
        if plotLabel.getTextAlign() is not None:
            target.addAttribute('textAlign',
                    plotLabel.getTextAlign().getName())
        if plotLabel.getVertAlign() is not None:
            target.addAttribute('verticalAlign',
                    plotLabel.getVertAlign().getName())
        if plotLabel.getX() is not None:
            target.addAttribute('x', plotLabel.getX())
        if plotLabel.getY() is not None:
            target.addAttribute('y', plotLabel.getY())
    target.endTag('label')


def writePlotBandRange(target, plotBandRange):
    """Writes from/to value for a plotband. It considers date and number
    values separately.

    @param target
    @param plotBandRange
    @throws PaintException
    """
    target.startTag('rangeValue')
    if plotBandRange is not None:
        if isinstance(plotBandRange, NumberRange):
            target.addAttribute('valueType', 'number')
            numberRange = plotBandRange
            if numberRange.getFrom() is not None:
                target.addAttribute('from', numberRange.getFrom())
            if numberRange.getTo() is not None:
                target.addAttribute('to', numberRange.getTo())
        elif isinstance(plotBandRange, DateTimeRange):
            target.addAttribute('valueType', 'date')
            dateRange = plotBandRange
            target.startTag('from')
            if dateRange.getFrom() is not None:
                target.addAttribute('year',
                        getYearFromDate(dateRange.getFrom()))
                target.addAttribute('month',
                        getMonthFromDate(dateRange.getFrom()))
                target.addAttribute('day',
                        getDayFromDate(dateRange.getFrom()))
            target.endTag('from')
            target.startTag('to')
            if dateRange.getTo() is not None:
                target.addAttribute('year',
                        getYearFromDate(dateRange.getTo()))
                target.addAttribute('month',
                        getMonthFromDate(dateRange.getTo()))
                target.addAttribute('day',
                        getDayFromDate(dateRange.getTo()))
            target.endTag('to')
    target.endTag('rangeValue')


def writePlotLines(target, plotLines):
    """Writes configuration attributes of the plotlines

    @param target
    @param plotLines
    @throws PaintException
    """
    target.startTag('plotLines')
    if plotLines is not None:
        for plotLine in plotLines:
            target.startTag('plotLine')
            if plotLine.getColor() is not None:
                target.addAttribute('color',
                        plotLine.getColor().getString())
            if plotLine.getDashStyle() is not None:
                target.addAttribute('dashStyle',
                        plotLine.getDashStyle().getName())
            if plotLine.getId() is not None:
                target.addAttribute('id', plotLine.getId())
            if plotLine.getWidth() is not None:
                target.addAttribute('width', plotLine.getWidth())
            if plotLine.getZIndex() is not None:
                target.addAttribute('zIndex', plotLine.getZIndex())
            writePlotLabel(target, plotLine.getLabel())
            writePlotLineValue(target, plotLine.getValue())
            target.endTag('plotLine')
    target.endTag('plotLines')


def writePlotLineValue(target, plotLineValue):
    """Writes value of a plotline. It considers date and number value
    separately.

    @param target
    @param plotLineValue
    @throws PaintException
    """
    target.startTag('lineValue')
    if plotLineValue is not None:
        if (isinstance(plotLineValue, NumberValue)
                and plotLineValue.getValue() is not None):
            target.addAttribute('valueType', 'number')
            target.addAttribute('value', plotLineValue.getValue())
        elif (isinstance(plotLineValue, DateTimeValue)
                and plotLineValue.getValue() is not None):
            target.addAttribute('valueType', 'date')
            date = plotLineValue.getValue()
            target.addAttribute('year', getYearFromDate(date))
            target.addAttribute('month', getMonthFromDate(date))
            target.addAttribute('day', getDayFromDate(date))
    target.endTag('lineValue')


def writeAxisTick(target, tick):
    writeAxisMinorTick(target, tick)
    if tick.getPixelInterval() is not None:
        target.addAttribute('tickPixelInterval', tick.getPixelInterval())
    if tick.getPlacement() is not None:
        target.addAttribute('tickmarkPlacement',
                tick.getPlacement().getName())


def writeAxisMinorTick(target, tick):
    """Writes configuration attributes of an axis. Depending on type of
    the argument tick, it either writes attributes for L{MinorTick} or
    L{Tick}

    @param target
    @param tick
    @raise PaintException
    """
    attNameColor = 'minorTickColor'
    attNameInterval = 'minorTickInterval'
    attNameLength = 'minorTickLength'
    attNamePosition = 'minorTickPosition'
    attNameWidth = 'minorTickWidth'
    if isinstance(tick, Tick):
        attNameColor = 'tickColor'
        attNameInterval = 'tickInterval'
        attNameLength = 'tickLength'
        attNamePosition = 'tickPosition'
        attNameWidth = 'tickWidth'
    if tick.getColor() is not None:
        target.addAttribute(attNameColor, tick.getColor().getString())
    if tick.getInterval() is not None:
        target.addAttribute(attNameInterval, tick.getInterval())
    if tick.getLength() is not None:
        target.addAttribute(attNameLength, tick.getLength())
    if tick.getPosition() is not None:
        target.addAttribute(attNamePosition, tick.getPosition().getName())
    if tick.getWidth() is not None:
        target.addAttribute(attNameWidth, tick.getWidth())


def writeAxisGrid(target, grid):
    writeAxisMinorGrid(target, grid)


def writeAxisMinorGrid(target, grid):
    """Writes configuration attributes of an axis. Depending on type of
    the argument tick, it either writes attributes for L{MinorGrid} or
    L{Grid}

    @param target
    @param grid
    @raise PaintException
    """
    attNameLineColor = 'minorGridLineColor'
    attNameLineWidth = 'minorGridLineWidth'
    attNameLineDashStyle = 'minorGridLineDashStyle'
    if isinstance(grid, Grid):
        attNameLineColor = 'gridLineColor'
        attNameLineWidth = 'gridLineWidth'
        attNameLineDashStyle = 'gridLineDashStyle'
    if grid.getLineColor() is not None:
        target.addAttribute(attNameLineColor,
                grid.getLineColor().getString())
    if grid.getLineWidth() is not None:
        target.addAttribute(attNameLineWidth, grid.getLineWidth())
    if grid.getLineDashStyle() is not None:
        target.addAttribute(attNameLineDashStyle,
                grid.getLineDashStyle().getName())


def writeAxisTitle(target, title):
    target.startTag('title')
    if title is not None:
        if title.getAlign() is not None:
            target.addAttribute('align', title.getAlign().getName())
        if title.getMargin() is not None:
            target.addAttribute('margin', title.getMargin())
        if title.getRotation() is not None:
            target.addAttribute('rotation', title.getRotation())
        if title.getStyle() is not None:
            target.addAttribute('style', title.getStyle())
        if title.getText() is not None:
            target.addAttribute('text', title.getText())
    target.endTag('title')


def writeXAxes(target, axes, config):
    """Iteratively processes each x-axis and writes configuration
    attributes of each axis based on type of the axis e.g. L{NumberAxis},
    L{DateTimeAxis} and L{CategoryAxis}

    @param target
    @param axes
    @raise PaintException
    """
    target.startTag('xAxes')
    if axes is not None:
        for xAxis in axes:
            target.startTag('xAxis')
            writeBaseAxis(target, xAxis, axes)
            if isinstance(xAxis, NumberXAxis):
                writeNumberAxis(target, xAxis)
            elif isinstance(xAxis, CategoryAxis):
                writeCategoryAxis(target, xAxis)
            elif isinstance(xAxis, DateTimeAxis):
                # Check if time should be included as part of a date value.
                # If any of the datetime series
                writeDateTimeAxis(target, xAxis,
                        isIncludeTime(xAxis,
                                config.getInvientCharts().getAllSeries()))
            target.endTag('xAxis')
    target.endTag('xAxes')


def isIncludeTime(axis, chartSeries):
    from muntjac.addon.invient.invient_charts import DateTimeSeries

    for series in chartSeries:
        if (isinstance(series, DateTimeSeries)
                and series.getXAxis() == axis):
            return series.isIncludeTime()

    return False


def writeNumberAxis(target, numberAxis):
    if numberAxis.getAllowDecimals() is not None:
        target.addAttribute('allowDecimals', numberAxis.getAllowDecimals())
    if numberAxis.getMax() is not None:
        target.addAttribute('max', numberAxis.getMax())
    if numberAxis.getMin() is not None:
        target.addAttribute('min', numberAxis.getMin())


def getDate(dt, isIncludeTime=False):
    """Returns milliseconds of the date argument dt. If the argument
    isIncludeTime is false then the returned milliseconds does not include
    time.
    """
    if not isIncludeTime:
        dt2 = datetime(dt.year, dt.month, dt.day)
        dt = dt2
    return long(totalseconds(dt - datetime(1970, 1, 1)) * 1e03)


def writeDateTimeAxis(target, dateTimeAxis, isIncludeTime):
    """@param target
    @param dateTimeAxis
    @raise PaintException
    """
    if dateTimeAxis.getMax() is not None:
        target.addAttribute('max', getDate(dateTimeAxis.getMax(),
                isIncludeTime))
    if dateTimeAxis.getMin() is not None:
        target.addAttribute('min', getDate(dateTimeAxis.getMin(),
                isIncludeTime))
    if dateTimeAxis.getDateTimeLabelFormat() is not None:
        target.startTag('dateTimeLabelFormats')
        dateTimeLabelFormat = dateTimeAxis.getDateTimeLabelFormat()
        if dateTimeLabelFormat.getSecond() is not None:
            target.addAttribute('second',
                    dateTimeAxis.getDateTimeLabelFormat().getSecond())
        if dateTimeLabelFormat.getMinute() is not None:
            target.addAttribute('minute',
                    dateTimeAxis.getDateTimeLabelFormat().getMinute())
        if dateTimeLabelFormat.getHour() is not None:
            target.addAttribute('hour',
                    dateTimeAxis.getDateTimeLabelFormat().getHour())
        if dateTimeLabelFormat.getDay() is not None:
            target.addAttribute('day',
                    dateTimeAxis.getDateTimeLabelFormat().getDay())
        if dateTimeLabelFormat.getWeek() is not None:
            target.addAttribute('week',
                    dateTimeAxis.getDateTimeLabelFormat().getWeek())
        if dateTimeLabelFormat.getMonth() is not None:
            target.addAttribute('month',
                    dateTimeAxis.getDateTimeLabelFormat().getMonth())
        if dateTimeLabelFormat.getYear() is not None:
            target.addAttribute('year',
                    dateTimeAxis.getDateTimeLabelFormat().getYear())
        target.endTag('dateTimeLabelFormats')


def writeCategoryAxis(target, categoryAxis):
    target.startTag('categories')
    if (categoryAxis.getCategories() is not None
            and len(categoryAxis.getCategories()) > 0):
        for category in categoryAxis.getCategories():
            target.startTag('category')
            target.addAttribute('name', category)
            target.endTag('category')
    target.endTag('categories')


def writeYAxes(target, axes, config):
    target.startTag('yAxes')
    if axes is not None:
        for yAxis in axes:
            target.startTag('yAxis')
            writeBaseAxis(target, yAxis, axes)
            if isinstance(yAxis, NumberYAxis):
                writeNumberAxis(target, yAxis)
            target.endTag('yAxis')
    target.endTag('yAxes')


def writeChartLabelConfig(target, chartLabel):
    """Writes configuration attributes of the chart labels.
    """
    target.startTag('labels')
    if (chartLabel is not None and chartLabel.getLabels() is not None
            and len(chartLabel.getLabels()) > 0):
        if chartLabel.getStyle() is not None:
            target.addAttribute('style', chartLabel.getStyle())
        target.startTag('items')
        for label in chartLabel.getLabels():
            if ((label.getHtml() is not None)
                    or (label.getStyle() is not None)):
                target.startTag('item')
                if label.getHtml() is not None:
                    target.addAttribute('html', label.getHtml())
                if label.getStyle() is not None:
                    target.addAttribute('style', label.getStyle())
                target.endTag('item')
        target.endTag('items')
    target.endTag('labels')


def getYearFromDate(date):
    """@return: Returns year of the argument date."""
    if date is None:
        return None
    return str(date.year)


def getMonthFromDate(date):
    """@return: Returns month of the argument date. The returned values
            is based on zero-index i.e. for month January, the values
            returned is "0"
    """
    if date is None:
        return None
    return str(date.month - 1)


def getDayFromDate(date):
    if date is None:
        return None
    return str(date.day)


def writeChartDataUpdates(target, seriesCURMap):
    """Writes information about which series were added, removed or
    updated. This information is used by Muntjac terminal class to decide
    whether to add a new series or remove/delete an existing series.
    Basically, this information helps client to update only a portion of
    the chart instead of full chart.
    """
    for seriesName in seriesCURMap.keys():
        seriesCURSet = seriesCURMap.get(seriesName)
        if seriesCURSet is not None and len(seriesCURSet) > 0:
            for seriesCUR in seriesCURSet:
                target.startTag('seriesDataUpdate')
                target.addAttribute('seriesName', seriesCUR.getName())
                target.addAttribute('operation',
                        seriesCUR.getType().getName())
                target.addAttribute('isReloadPoints',
                        seriesCUR.isReloadPoints())
                target.startTag('pointsAdded')
                if len(seriesCUR.getPointsAdded()) > 0:
                    writePoints(target, seriesCUR.getPointsAdded())
                target.endTag('pointsAdded')
                target.startTag('pointsRemoved')
                if len(seriesCUR.getPointsRemoved()) > 0:
                    writePoints(target, seriesCUR.getPointsRemoved())
                target.endTag('pointsRemoved')
                target.endTag('seriesDataUpdate')
