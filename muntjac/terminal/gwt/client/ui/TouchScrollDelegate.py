# -*- coding: utf-8 -*-
from __pyjamas__ import (POSTINC,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
# from com.google.gwt.dom.client.Element import (Element,)
# from com.google.gwt.dom.client.Node import (Node,)
# from com.google.gwt.dom.client.NodeList import (NodeList,)
# from com.google.gwt.dom.client.Touch import (Touch,)
# from com.google.gwt.event.dom.client.TouchStartEvent import (TouchStartEvent,)
# from com.google.gwt.user.client.Event.NativePreviewEvent import (NativePreviewEvent,)
# from com.google.gwt.user.client.Event.NativePreviewHandler import (NativePreviewHandler,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Date import (Date,)


class TouchScrollDelegate(NativePreviewHandler):
    """Provides one finger touch scrolling for elements with once scrollable
    elements inside. One widget can have several of these scrollable elements.
    Scrollable elements are provided in the constructor. Users must pass
    touchStart events to this delegate, from there on the delegate takes over
    with an event preview. Other touch events needs to be sunken though.
    <p>
    This is bit similar as Scroller class in GWT expenses example, but ideas
    drawn from iscroll.js project:
    <ul>
    <li>uses GWT event mechanism.
    <li>uses modern CSS trick during scrolling for smoother experience:
    translate3d and transitions
    </ul>
    <p>
    Scroll event should only happen when the "touch scrolling actually ends".
    Later we might also tune this so that a scroll event happens if user stalls
    her finger long enought.

    TODO static getter for active touch scroll delegate. Components might need to
    prevent scrolling in some cases. Consider Table with drag and drop, or drag
    and drop in scrollable area. Optimal implementation might be to start the
    drag and drop only if user keeps finger down for a moment, otherwise do the
    scroll. In this case, the draggable component would need to cancel scrolling
    in a timer after touchstart event and take over from there.

    TODO support scrolling horizontally

    TODO cancel if user add second finger to the screen (user expects a gesture).

    TODO "scrollbars", see e.g. iscroll.js

    TODO write an email to sjobs √§t apple dot com and beg for this feature to be
    built into webkit. Seriously, we should try to lobbying this to webkit folks.
    This sure ain't our business to implement this with javascript.

    TODO collect all general touch related constant to better place.

    @author Matti Tahvonen, Vaadin Ltd
    """
    _FRICTION = 0.002
    _DECELERATION = 0.002
    _MAX_DURATION = 1500
    _origX = None
    _origY = None
    _scrollableElements = None
    _scrolledElement = None
    _origScrollTop = None
    _handlerRegistration = None
    _lastClientY = None
    _pixxelsPerMs = None
    _transitionPending = False
    _deltaScrollPos = None
    _transitionOn = False
    _finalScrollTop = None
    _layers = None
    _moved = None
    _activeScrollDelegate = None

    def __init__(self, *elements):
        self._scrollableElements = elements

    @classmethod
    def getActiveScrollDelegate(cls):
        return cls._activeScrollDelegate

    def isMoved(self):
        """Has user moved the touch.

        @return
        """
        return self._moved

    def stopScrolling(self):
        """Forces the scroll delegate to cancels scrolling process. Can be called by
        users if they e.g. decide to handle touch event by themselves after all
        (e.g. a pause after touch start before moving touch -> interpreted as
        long touch/click or drag start).
        """
        self._handlerRegistration.removeHandler()
        self._handlerRegistration = None
        if self._moved:
            self.moveTransformationToScrolloffset()
        else:
            self._activeScrollDelegate = None

    def onTouchStart(self, event):
        if self._activeScrollDelegate is None and len(event.getTouches()) == 1:
            touch = event.getTouches().get(0)
            if self.detectScrolledElement(touch):
                VConsole.log('TouchDelegate takes over')
                event.stopPropagation()
                self._handlerRegistration = self.Event.addNativePreviewHandler(self)
                self._activeScrollDelegate = self
                self.hookTransitionEndListener(self._scrolledElement.getFirstChildElement())
                self._origX = touch.getClientX()
                self._origY = touch.getClientY()
                self._yPositions[0] = self._origY
                self._eventTimeStamps[0] = Date()
                self._nextEvent = 1
                if self._transitionOn:
                    # TODO calculate current position of ongoing transition,
                    # fix to that and start scroll from there. Another option
                    # is to investigate if we can get even close the same
                    # framerate with scheduler based impl instead of using
                    # transitions (GWT examples has impl of this, with jsni
                    # though). This is very smooth on native ipad, now we
                    # ignore touch starts during animation.
                    self._origScrollTop = self._scrolledElement.getScrollTop()
                else:
                    self._origScrollTop = self._scrolledElement.getScrollTop()
                self._moved = False
                # event.preventDefault();
                # event.stopPropagation();
        else:
            # Touch scroll is currenly on (possibly bouncing). Ignore.
            pass

    def hookTransitionEndListener(self, element):
        # -{
        #         if(!element.hasTransitionEndListener) {
        #             var that = this;
        #             element.addEventListener("webkitTransitionEnd",function(event){
        #                 that.@com.vaadin.terminal.gwt.client.ui.TouchScrollDelegate::onTransitionEnd()();
        #             },false);
        #             element.hasTransitionEndListener = true;
        #         }
        #     }-

        pass

    def onTransitionEnd(self):
        if self._finalScrollTop < 0:
            self.animateToScrollPosition(0, self._finalScrollTop)
            self._finalScrollTop = 0
        elif self._finalScrollTop > self.getMaxFinalY():
            self.animateToScrollPosition(self.getMaxFinalY(), self._finalScrollTop)
            self._finalScrollTop = self.getMaxFinalY()
        else:
            self.moveTransformationToScrolloffset()
        self._transitionOn = False

    def animateToScrollPosition(self, to, from_):
        dist = self.Math.abs(to - from_)
        time = self.getAnimationTimeForDistance(dist)
        if time <= 0:
            time = 1
            # get animation and transition end event
        self.translateTo(time, -to + self._origScrollTop)

    def getAnimationTimeForDistance(self, dist):
        return 350
        # 350ms seems to work quite fine for all distances
        # if (dist < 0) {
        # dist = -dist;
        # }
        # return MAX_DURATION * dist / (scrolledElement.getClientHeight() * 3);

    def moveTransformationToScrolloffset(self):
        """Called at the end of scrolling. Moves possible translate values to
        scrolltop, causing onscroll event.
        """
        for el in self._layers:
            style = el.getStyle()
            style.setProperty('webkitTransitionProperty', 'none')
            style.setProperty('webkitTransform', 'translate3d(0,0,0)')
        self._scrolledElement.setScrollTop(self._finalScrollTop)
        self._activeScrollDelegate = None
        self._handlerRegistration.removeHandler()
        self._handlerRegistration = None

    def detectScrolledElement(self, touch):
        """Detects if a touch happens on a predefined element and the element has
        something to scroll.

        @param touch
        @return
        """
        target = touch.getTarget()
        for el in self._scrollableElements:
            if el.isOrHasChild(target) and el.getScrollHeight() > el.getClientHeight():
                self._scrolledElement = el
                childNodes = self._scrolledElement.getChildNodes()
                self._layers = list()
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < childNodes.getLength()):
                        break
                    item = childNodes.getItem(i)
                    if item.getNodeType() == Node.ELEMENT_NODE:
                        self._layers.add(item)
                return True
        return False

    def onTouchMove(self, event):
        if not self._moved:
            date = Date()
            l = date.getTime() - self._eventTimeStamps[0].getTime()
            VConsole.log(l + ' ms from start to move')
        handleMove = self.readPositionAndSpeed(event)
        if handleMove:
            deltaScrollTop = self._origY - self._lastClientY
            finalPos = self._origScrollTop + deltaScrollTop
            if finalPos > self.getMaxFinalY():
                # spring effect at the end
                overscroll = (deltaScrollTop + self._origScrollTop) - self.getMaxFinalY()
                overscroll = overscroll / 2
                if overscroll > self._scrolledElement.getClientHeight() / 2:
                    overscroll = self._scrolledElement.getClientHeight() / 2
                deltaScrollTop = (self.getMaxFinalY() + overscroll) - self._origScrollTop
            elif finalPos < 0:
                # spring effect at the beginning
                overscroll = finalPos / 2
                if -overscroll > self._scrolledElement.getClientHeight() / 2:
                    overscroll = -self._scrolledElement.getClientHeight() / 2
                deltaScrollTop = overscroll - self._origScrollTop
            self.quickSetScrollPosition(0, deltaScrollTop)
            self._moved = True
            event.preventDefault()
            event.stopPropagation()

    def quickSetScrollPosition(self, deltaX, deltaY):
        self._deltaScrollPos = deltaY
        self.translateTo(0, -self._deltaScrollPos)

    _EVENTS_FOR_SPEED_CALC = 3
    SIGNIFICANT_MOVE_THRESHOLD = 3
    _yPositions = [None] * _EVENTS_FOR_SPEED_CALC
    _eventTimeStamps = [None] * _EVENTS_FOR_SPEED_CALC
    _nextEvent = 0
    _transitionStart = None
    _transitionDuration = None

    def readPositionAndSpeed(self, event):
        """@param event
        @return
        """
        now = Date()
        touch = event.getChangedTouches().get(0)
        self._lastClientY = touch.getClientY()
        eventIndx = POSTINC(globals(), locals(), 'self._nextEvent')
        eventIndx = eventIndx % self._EVENTS_FOR_SPEED_CALC
        self._eventTimeStamps[eventIndx] = now
        self._yPositions[eventIndx] = self._lastClientY
        return self.isMovedSignificantly()

    def isMovedSignificantly(self):
        return self._moved if self._moved else self.Math.abs(self._origY - self._lastClientY) >= self.SIGNIFICANT_MOVE_THRESHOLD

    def onTouchEnd(self, event):
        if not self._moved:
            self._activeScrollDelegate = None
            self._handlerRegistration.removeHandler()
            self._handlerRegistration = None
            return
        currentY = self._origScrollTop + self._deltaScrollPos
        maxFinalY = self.getMaxFinalY()
        duration = -1
        if currentY > maxFinalY:
            # we are over the max final pos, animate to end
            pixelsToMove = maxFinalY - currentY
            finalY = maxFinalY
        elif currentY < 0:
            # we are below the max final pos, animate to beginning
            pixelsToMove = -currentY
            finalY = 0
        else:
            pixelsPerMs = self.calculateSpeed()
            # we are currently within scrollable area, calculate pixels that
            # we'll move due to momentum
            VConsole.log('pxPerMs' + pixelsPerMs)
            pixelsToMove = (0.5 * pixelsPerMs * pixelsPerMs) / self._FRICTION
            if pixelsPerMs < 0:
                pixelsToMove = -pixelsToMove
            # VConsole.log("pixels to move" + pixelsToMove);
            finalY = currentY + pixelsToMove
            if finalY > maxFinalY + self.getMaxOverScroll():
                # VConsole.log("To max overscroll");
                finalY = self.getMaxFinalY() + self.getMaxOverScroll()
                fixedPixelsToMove = finalY - currentY
                pixelsPerMs = (pixelsPerMs * pixelsToMove) / fixedPixelsToMove / self._FRICTION
                pixelsToMove = fixedPixelsToMove
            elif finalY < 0 - self.getMaxOverScroll():
                # VConsole.log("to min overscroll");
                finalY = -self.getMaxOverScroll()
                fixedPixelsToMove = finalY - currentY
                pixelsPerMs = (pixelsPerMs * pixelsToMove) / fixedPixelsToMove / self._FRICTION
                pixelsToMove = fixedPixelsToMove
            else:
                duration = self.Math.abs(pixelsPerMs / self._DECELERATION)
        if duration == -1:
            # did not keep in side borders or was outside borders, calculate
            # a good enough duration based on pixelsToBeMoved.
            duration = self.getAnimationTimeForDistance(pixelsToMove)
        if duration > self._MAX_DURATION:
            VConsole.log('Max animation time. ' + duration)
            duration = self._MAX_DURATION
        self._finalScrollTop = finalY
        if (self.Math.abs(pixelsToMove) < 3) or (duration < 20):
            VConsole.log('Small \'momentum\' ' + pixelsToMove + ' |  ' + duration + ' Skipping animation,')
            self.moveTransformationToScrolloffset()
            return
        translateY = -finalY + self._origScrollTop
        self.translateTo(duration, translateY)

    def calculateSpeed(self):
        if self._nextEvent < self._EVENTS_FOR_SPEED_CALC:
            VConsole.log('Not enough data for speed calculation')
            # not enough data for decent speed calculation, no momentum :-(
            return 0
        idx = self._nextEvent % self._EVENTS_FOR_SPEED_CALC
        firstPos = self._yPositions[idx]
        firstTs = self._eventTimeStamps[idx]
        idx += self._EVENTS_FOR_SPEED_CALC
        idx -= 1
        idx = idx % self._EVENTS_FOR_SPEED_CALC
        lastPos = self._yPositions[idx]
        lastTs = self._eventTimeStamps[idx]
        # speed as in change of scrolltop == -speedOfTouchPos
        return (firstPos - lastPos) / (lastTs.getTime() - firstTs.getTime())

    def translateTo(self, duration, translateY):
        """Note positive scrolltop moves layer up, positive translate moves layer
        down.

        @param duration
        @param translateY
        """
        for el in self._layers:
            style = el.getStyle()
            if duration > 0:
                style.setProperty('webkitTransitionDuration', duration + 'ms')
                style.setProperty('webkitTransitionTimingFunction', 'cubic-bezier(0,0,0.25,1)')
                style.setProperty('webkitTransitionProperty', '-webkit-transform')
                self._transitionOn = True
                self._transitionStart = Date()
                self._transitionDuration = Date()
            else:
                style.setProperty('webkitTransitionProperty', 'none')
            style.setProperty('webkitTransform', 'translate3d(0px,' + translateY + 'px,0px)')

    def getMaxOverScroll(self):
        return self._scrolledElement.getClientHeight() / 4

    def getMaxFinalY(self):
        return self._scrolledElement.getScrollHeight() - self._scrolledElement.getClientHeight()

    def onPreviewNativeEvent(self, event):
        if self._transitionOn:
            # TODO allow starting new events. See issue in onTouchStart
            event.cancel()
            return
        typeInt = event.getTypeInt()
        _0 = typeInt
        _1 = False
        while True:
            if _0 == self.Event.ONTOUCHMOVE:
                _1 = True
                if not event.isCanceled():
                    self.onTouchMove(event.getNativeEvent())
                    if self._moved:
                        event.cancel()
                break
            if (_1 is True) or (_0 == self.Event.ONTOUCHEND):
                _1 = True
            if (_1 is True) or (_0 == self.Event.ONTOUCHCANCEL):
                _1 = True
                if not event.isCanceled():
                    if self._moved:
                        event.cancel()
                    self.onTouchEnd(event.getNativeEvent())
                break
            if (_1 is True) or (_0 == self.Event.ONMOUSEMOVE):
                _1 = True
                if self._moved:
                    # no debug message, mobile safari generates these for some
                    # compatibility purposes.
                    event.cancel()
                break
            if True:
                _1 = True
                VConsole.log('Non touch event:' + event.getNativeEvent().getType())
                event.cancel()
                break
            break

    def setElements(self, elements):
        self._scrollableElements = elements
