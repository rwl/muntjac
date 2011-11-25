# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)


class VOverlay(PopupPanel, CloseHandler):
    """In Vaadin UI this Overlay should always be used for all elements that
    temporary float over other components like context menus etc. This is to deal
    stacking order correctly with VWindow objects.
    """
    # The z-index value from where all overlays live. This can be overridden in
    # any extending class.

    Z_INDEX = 20000
    _leftFix = -1
    _topFix = -1
    # Shadow element style. If an extending class wishes to use a different
    # style of shadow, it can use setShadowStyle(String) to give the shadow
    # element a new style name.

    CLASSNAME_SHADOW = 'v-shadow'
    # The shadow element for this overlay.
    _shadow = None
    # The HTML snippet that is used to render the actual shadow. In consists of
    # nine different DIV-elements with the following class names:
    # 
    # <pre>
    #   .v-shadow[-stylename]
    #   ----------------------------------------------
    #   | .top-left     |   .top    |     .top-right |
    #   |---------------|-----------|----------------|
    #   |               |           |                |
    #   | .left         |  .center  |         .right |
    #   |               |           |                |
    #   |---------------|-----------|----------------|
    #   | .bottom-left  |  .bottom  |  .bottom-right |
    #   ----------------------------------------------
    # </pre>
    # 
    # See default theme 'shadow.css' for implementation example.

    _SHADOW_HTML = '<div class=\"top-left\"></div><div class=\"top\"></div><div class=\"top-right\"></div><div class=\"left\"></div><div class=\"center\"></div><div class=\"right\"></div><div class=\"bottom-left\"></div><div class=\"bottom\"></div><div class=\"bottom-right\"></div>'
    _sinkShadowEvents = False

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(VOverlay, self)()
            self.adjustZIndex()
        elif _1 == 1:
            autoHide, = _0
            super(VOverlay, self)(autoHide)
            self.adjustZIndex()
        elif _1 == 2:
            autoHide, modal = _0
            super(VOverlay, self)(autoHide, modal)
            self.adjustZIndex()
        elif _1 == 3:
            autoHide, modal, showShadow = _0
            super(VOverlay, self)(autoHide, modal)
            self.setShadowEnabled(showShadow)
            self.adjustZIndex()
        else:
            raise ARGERROR(0, 3)

    def setShadowEnabled(self, enabled):
        """Method to controle whether DOM elements for shadow are added. With this
        method subclasses can control displaying of shadow also after the
        constructor.

        @param enabled
                   true if shadow should be displayed
        """
        if enabled != self.isShadowEnabled():
            if enabled:
                self._shadow = DOM.createDiv()
                self._shadow.setClassName(self.CLASSNAME_SHADOW)
                self._shadow.setInnerHTML(self._SHADOW_HTML)
                DOM.setStyleAttribute(self._shadow, 'position', 'absolute')
                self.addCloseHandler(self)
            else:
                self.removeShadowIfPresent()
                self._shadow = None

    def isShadowEnabled(self):
        return self._shadow is not None

    def removeShadowIfPresent(self):
        if self.isShadowAttached():
            self._shadow.getParentElement().removeChild(self._shadow)
            # Remove event listener from the shadow
            self.unsinkShadowEvents()

    def isShadowAttached(self):
        return self.isShadowEnabled() and self._shadow.getParentElement() is not None

    def adjustZIndex(self):
        self.setZIndex(self.Z_INDEX)

    def setZIndex(self, zIndex):
        """Set the z-index (visual stack position) for this overlay.

        @param zIndex
                   The new z-index
        """
        DOM.setStyleAttribute(self.getElement(), 'zIndex', '' + zIndex)
        if self.isShadowEnabled():
            DOM.setStyleAttribute(self._shadow, 'zIndex', '' + zIndex)

    def setPopupPosition(self, left, top):
        # TODO, this should in fact be part of
        # Document.get().getBodyOffsetLeft/Top(). Would require overriding DOM
        # for all permutations. Now adding fix as margin instead of fixing
        # left/top because parent class saves the position.
        style = self.getElement().getStyle()
        style.setMarginLeft(-self.adjustByRelativeLeftBodyMargin(), Unit.PX)
        style.setMarginTop(-self.adjustByRelativeTopBodyMargin(), Unit.PX)
        super(VOverlay, self).setPopupPosition(left, top)
        self.updateShadowSizeAndPosition(0 if self.isAnimationEnabled() else 1)

    @classmethod
    def adjustByRelativeTopBodyMargin(cls):
        if cls._topFix == -1:
            ie6OrIe7 = BrowserInfo.get().isIE() and BrowserInfo.get().getIEVersion() <= 7
            cls._topFix = cls.detectRelativeBodyFixes('top', ie6OrIe7)
        return cls._topFix

    @classmethod
    def detectRelativeBodyFixes(cls, axis, removeClientLeftOrTop):
        JS("""
        try {
            var b = $wnd.document.body;
            var cstyle = b.currentStyle ? b.currentStyle : getComputedStyle(b);
            if(cstyle && cstyle.position == 'relative') {
                var offset = b.getBoundingClientRect()[@{{axis}}];
                if (@{{removeClientLeftOrTop}}) {
                    // IE6 and IE7 include the top left border of the client area into the boundingClientRect
                    var clientTopOrLeft = 0;
                    if (@{{axis}} == "top")
                        clientTopOrLeft = $wnd.document.documentElement.clientTop;
                    else
                        clientTopOrLeft = $wnd.document.documentElement.clientLeft;

                    offset -= clientTopOrLeft;
                }
                return offset;
            }
        } catch(e){}
        return 0;
    """)
        pass

    @classmethod
    def adjustByRelativeLeftBodyMargin(cls):
        if cls._leftFix == -1:
            ie6OrIe7 = BrowserInfo.get().isIE() and BrowserInfo.get().getIEVersion() <= 7
            cls._leftFix = cls.detectRelativeBodyFixes('left', ie6OrIe7)
        return cls._leftFix

    def show(self):
        super(VOverlay, self).show()
        if self.isShadowEnabled():
            if self.isAnimationEnabled():
                sa = self.ShadowAnimation()
                sa.run(200)
            else:
                self.updateShadowSizeAndPosition(1.0)
        Util.runIE7ZeroSizedBodyFix()

    def hide(self, autoClosed):
        super(VOverlay, self).hide(autoClosed)
        Util.runIE7ZeroSizedBodyFix()

    def onDetach(self):
        super(VOverlay, self).onDetach()
        # Always ensure shadow is removed when the overlay is removed.
        self.removeShadowIfPresent()

    def setVisible(self, visible):
        super(VOverlay, self).setVisible(visible)
        if self.isShadowEnabled():
            self._shadow.getStyle().setProperty('visibility', 'visible' if visible else 'hidden')

    def setWidth(self, width):
        super(VOverlay, self).setWidth(width)
        self.updateShadowSizeAndPosition(1.0)

    def setHeight(self, height):
        super(VOverlay, self).setHeight(height)
        self.updateShadowSizeAndPosition(1.0)

    def setShadowStyle(self, style):
        """Sets the shadow style for this overlay. Will override any previous style
        for the shadow. The default style name is defined by CLASSNAME_SHADOW.
        The given style will be prefixed with CLASSNAME_SHADOW.

        @param style
                   The new style name for the shadow element. Will be prefixed by
                   CLASSNAME_SHADOW, e.g. style=='foobar' -> actual style
                   name=='v-shadow-foobar'.
        """
        # Extending classes should always call this method after they change the
        # size of overlay without using normal 'setWidth(String)' and
        # 'setHeight(String)' methods (if not calling super.setWidth/Height).

        if self.isShadowEnabled():
            self._shadow.setClassName(self.CLASSNAME_SHADOW + '-' + style)

    def updateShadowSizeAndPosition(self, *args):
        """None
        ---
        Recalculates proper position and dimensions for the shadow element. Can
        be used to animate the shadow, using the 'progress' parameter (used to
        animate the shadow in sync with GWT PopupPanel's default animation
        'PopupPanel.AnimationType.CENTER').

        @param progress
                   A value between 0.0 and 1.0, indicating the progress of the
                   animation (0=start, 1=end).
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.updateShadowSizeAndPosition(1.0)
        elif _1 == 1:
            progress, = _0
            if (not self.isAttached()) or (self._shadow is None):
                return
            # Calculate proper z-index
            zIndex = None
            # Odd behaviour with Windows Hosted Mode forces us to use
            # this redundant try/catch block (See dev.vaadin.com #2011)
            # Ignored, will cause no harm
            try:
                zIndex = DOM.getStyleAttribute(self.getElement(), 'zIndex')
            except Exception, ignore:
                zIndex = '1000'
            if zIndex is None:
                zIndex = '' + self.Z_INDEX
            # Calculate position and size
            if BrowserInfo.get().isIE():
                # Shake IE
                self.getOffsetHeight()
                self.getOffsetWidth()
            x = self.getAbsoluteLeft()
            y = self.getAbsoluteTop()
            # This is needed for IE7 at least
            # Account for the difference between absolute position and the
            # body's positioning context.
            x -= Document.get().getBodyOffsetLeft()
            y -= Document.get().getBodyOffsetTop()
            x -= self.adjustByRelativeLeftBodyMargin()
            y -= self.adjustByRelativeTopBodyMargin()
            width = self.getOffsetWidth()
            height = self.getOffsetHeight()
            if width < 0:
                width = 0
            if height < 0:
                height = 0
            # Animate the shadow size
            x += (width * (1.0 - progress)) / 2.0
            y += (height * (1.0 - progress)) / 2.0
            width = width * progress
            height = height * progress
            # Opera needs some shaking to get parts of the shadow showing
            # properly
            # (ticket #2704)
            if BrowserInfo.get().isOpera():
                # Clear the height of all middle elements
                DOM.getChild(self._shadow, 3).getStyle().setProperty('height', 'auto')
                DOM.getChild(self._shadow, 4).getStyle().setProperty('height', 'auto')
                DOM.getChild(self._shadow, 5).getStyle().setProperty('height', 'auto')
            # Update correct values
            DOM.setStyleAttribute(self._shadow, 'zIndex', zIndex)
            DOM.setStyleAttribute(self._shadow, 'width', width + 'px')
            DOM.setStyleAttribute(self._shadow, 'height', height + 'px')
            DOM.setStyleAttribute(self._shadow, 'top', y + 'px')
            DOM.setStyleAttribute(self._shadow, 'left', x + 'px')
            DOM.setStyleAttribute(self._shadow, 'display', 'none' if progress < 0.9 else '')
            # Opera fix, part 2 (ticket #2704)
            if BrowserInfo.get().isOpera():
                # We'll fix the height of all the middle elements
                DOM.getChild(self._shadow, 3).getStyle().setPropertyPx('height', DOM.getChild(self._shadow, 3).getOffsetHeight())
                DOM.getChild(self._shadow, 4).getStyle().setPropertyPx('height', DOM.getChild(self._shadow, 4).getOffsetHeight())
                DOM.getChild(self._shadow, 5).getStyle().setPropertyPx('height', DOM.getChild(self._shadow, 5).getOffsetHeight())
            # Attach to dom if not there already
            if not self.isShadowAttached():
                RootPanel.get().getElement().insertBefore(self._shadow, self.getElement())
                self.sinkShadowEvents()
        else:
            raise ARGERROR(0, 1)

    # Don't do anything if overlay element is not attached

    def ShadowAnimation(VOverlay_this, *args, **kwargs):

        class ShadowAnimation(Animation):

            def onUpdate(self, progress):
                VOverlay_this.updateShadowSizeAndPosition(progress)

        return ShadowAnimation(*args, **kwargs)

    def onClose(self, event):
        self.removeShadowIfPresent()

    def sinkEvents(self, eventBitsToAdd):
        super(VOverlay, self).sinkEvents(eventBitsToAdd)
        # Also sink events on the shadow if present
        self.sinkShadowEvents()

    def sinkShadowEvents(self):
        if self.isSinkShadowEvents() and self.isShadowAttached():
            # Sink the same events as the actual overlay has sunk
            DOM.sinkEvents(self._shadow, DOM.getEventsSunk(self.getElement()))
            # Send events to VOverlay.onBrowserEvent
            DOM.setEventListener(self._shadow, self)

    def unsinkShadowEvents(self):
        if self.isShadowAttached():
            DOM.setEventListener(self._shadow, None)
            DOM.sinkEvents(self._shadow, 0)

    def setSinkShadowEvents(self, sinkShadowEvents):
        """Enables or disables sinking the events of the shadow to the same
        onBrowserEvent as events to the actual overlay goes.

        Please note, that if you enable this, you can't assume that e.g.
        event.getEventTarget returns an element inside the DOM structure of the
        overlay

        @param sinkShadowEvents
        """
        self._sinkShadowEvents = sinkShadowEvents
        if sinkShadowEvents:
            sinkShadowEvents()
        else:
            self.unsinkShadowEvents()

    def isSinkShadowEvents(self):
        return self._sinkShadowEvents
