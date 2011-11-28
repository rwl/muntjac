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

import re

import pygwt as GWT

from __pyjamas__ import JS

from pyjamas import DOM, Window

from pyjamas.Timer import Timer
from pyjamas.ui import Event
from pyjamas.ui import RootPanel
from pyjamas.ui.Widget import Widget

from muntjac.terminal.gwt.client.v_console import VConsole
from muntjac.terminal.gwt.client.container import Container
from muntjac.terminal.gwt.client.render_information import RenderInformation, FloatSize
from muntjac.terminal.gwt.client.application_connection import ApplicationConnection
from muntjac.terminal.gwt.client.v_caption import VCaption
from muntjac.terminal.gwt.client.uidl import UIDL
from muntjac.terminal.gwt.client.browser_info import BrowserInfo


class Util(object):

    _LAZY_SIZE_CHANGE_TIMEOUT = 400
    _latelyChangedWidgets = set()

    @classmethod
    def browserDebugger(cls):
        """Helper method for debugging purposes.

        Stops execution on firefox browsers on a breakpoint.
        """
        JS("""
            if($wnd.console)
                debugger;
        """)
        pass

    @classmethod
    def getElementFromPoint(cls, clientX, clientY):
        """Returns the topmost element of from given coordinates.

        TODO: fix crossplat issues clientX vs pageX. See quircksmode. Not
        critical for Muntjac as we scroll div istead of page.

        @return: the element at given coordinates
        """
        JS("""
            var el = $wnd.document.elementFromPoint(@{{clientX}}, @{{clientY}});
            if(el != null && el.nodeType == 3) {
                el = el.parentNode;
            }
            return el;
        """)
        pass

    class lazySizeChangeTimer(Timer):
        _lazySizeChangeTimerScheduled = False

        def run(self):
            Util_this.componentSizeUpdated(Util_this._latelyChangedWidgets)
            Util_this._latelyChangedWidgets.clear()
            self._lazySizeChangeTimerScheduled = False

        def schedule(self, delayMillis):
            if self._lazySizeChangeTimerScheduled:
                self.cancel()
            else:
                self._lazySizeChangeTimerScheduled = True
            super(_0_, self).schedule(delayMillis)


    @classmethod
    def notifyParentOfSizeChange(cls, widget, lazy):
        """This helper method can be called if components size have been changed
        outside rendering phase. It notifies components parent about the size
        change so it can react.

        When using this method, developer should consider if size changes could
        be notified lazily. If lazy flag is true, method will save widget and
        wait for a moment until it notifies parents in chunks. This may vastly
        optimize layout in various situation. Example: if component have a lot of
        images their onload events may fire "layout phase" many times in a short
        period.

        @param widget:
        @param lazy:
                   run componentSizeUpdated lazyly
        """
        if lazy:
            cls._latelyChangedWidgets.add(widget)
            cls.lazySizeChangeTimer.schedule(cls._LAZY_SIZE_CHANGE_TIMEOUT)
        else:
            widgets = set()
            widgets.add(widget)
            Util.componentSizeUpdated(widgets)


    @classmethod
    def componentSizeUpdated(cls, paintables):
        """Called when the size of one or more widgets have changed during
        rendering. Finds parent container and notifies them of the size change.

        @param paintables
        """
        if paintables.isEmpty():
            return

        childWidgets = dict()

        for paintable in paintables:
            widget = paintable
            if not widget.isAttached():
                continue

            # ApplicationConnection.getConsole().log(
            # "Widget " + Util.getSimpleName(widget) + " size updated");
            parent = widget.getParent()
            while parent is not None and not isinstance(parent, Container):
                parent = parent.getParent()

            if parent is not None:
                wset = childWidgets[parent]
                if wset is None:
                    wset = set()
                    childWidgets[parent] = wset
                wset.add(paintable)

        parentChanges = set()
        for parent in childWidgets.keys():
            if not parent.requestLayout(childWidgets[parent]):
                parentChanges.add(parent)
        cls.componentSizeUpdated(parentChanges)


    @classmethod
    def parseRelativeSize(cls, uidl_or_size=None):
        """Parses the UIDL parameter and fetches the relative size of the
        component. If a dimension is not specified as relative it will return
        -1. If the UIDL does not contain width or height specifications this
        will return null.
        """
        if isinstance(uidl_or_size, UIDL):
            uidl = uidl_or_size
            hasAttribute = False
            w = ''
            h = ''
            if uidl.hasAttribute('width'):
                hasAttribute = True
                w = uidl.getStringAttribute('width')
            if uidl.hasAttribute('height'):
                hasAttribute = True
                h = uidl.getStringAttribute('height')
            if not hasAttribute:
                return None
            relativeWidth = Util.parseRelativeSize(w)
            relativeHeight = Util.parseRelativeSize(h)
            relativeSize = FloatSize(relativeWidth, relativeHeight)
            return relativeSize
        else:
            size = uidl_or_size
            if (size is None) or (not size.endswith('%')):
                return -1
            try:
                return float(size[:-1])
            except Exception:
                VConsole.log('Unable to parse relative size')
                return -1


    @classmethod
    def getLayout(cls, component):
        """Returns closest parent Widget in hierarchy that implements
        Container interface.

        @return: closest parent Container
        """
        parent = component.getParent()
        while (parent is not None) and not isinstance(parent, Container):
            parent = parent.getParent()

        if parent is not None:
            assert parent.hasChildComponent(component)
            return parent

        return None


    @classmethod
    def isIE(cls):
        """Detects if current browser is IE.

        @deprecated: use BrowserInfo class instead

        @return: true if IE
        """
        return BrowserInfo.get().isIE()


    @classmethod
    def isIE6(cls):
        """Detects if current browser is IE6.

        @deprecated: use BrowserInfo class instead

        @return: true if IE6
        """
        return BrowserInfo.get().isIE6()


    @classmethod
    def isIE7(cls):
        """@deprecated: use BrowserInfo class instead
        """
        return BrowserInfo.get().isIE7()


    @classmethod
    def isFF2(cls):
        """@deprecated: use BrowserInfo class instead
        """
        return BrowserInfo.get().isFF2()


    _escapeHtmlHelper = DOM.createDiv()

    @classmethod
    def escapeHTML(cls, html):
        """Converts html entities to text.

        @return: escaped string presentation of given html
        """
        DOM.setInnerText(cls._escapeHtmlHelper, html)

        escapedText = DOM.getInnerHTML(cls._escapeHtmlHelper)
        if BrowserInfo.get().isIE() and (BrowserInfo.get().getIEVersion() < 9):
            # #7478 IE6-IE8 "incorrectly" returns "<br>" for newlines set using
            # setInnerText. The same for " " which is converted to "&nbsp;"
            escapedText = re.sub('<(BR|br)>', '\n', escapedText)
            escapedText = re.sub('&nbsp;', ' ', escapedText)

        return escapedText


    @classmethod
    def escapeAttribute(cls, attribute):
        """Escapes the string so it is safe to write inside an HTML attribute.

        @param attribute:
                   The string to escape
        @return: An escaped version of <literal>attribute</literal>.
        """
        attribute = attribute.replace('\"', '&quot;')
        attribute = attribute.replace('\'', '&#39;')
        attribute = attribute.replace('>', '&gt;')
        attribute = attribute.replace('<', '&lt;')
        attribute = attribute.replace('&', '&amp;')
        return attribute


    @classmethod
    def addPngFix(cls, el):
        """Adds transparent PNG fix to image element; only use for IE6.

        @param el: IMG element
        """
        JS("""
            @{{el}}.attachEvent("onload", function() {
                @com.vaadin.terminal.gwt.client.Util::doIE6PngFix(Lcom/google/gwt/user/client/Element;)(@{{el}});
            },false);
        """)
        pass


    @classmethod
    def doPngFix(cls, el, blankImageUrl):
        JS("""
            var src = @{{el}}.src;
            if (src.indexOf(".png") < 1) return;
            var w = @{{el}}.width || 16;
            var h = @{{el}}.height || 16;
            if(h==30 || w==28) {
                setTimeout(function(){
                    @{{el}}.style.height = @{{el}}.height + "px";
                    @{{el}}.style.width = @{{el}}.width + "px";
                    @{{el}}.src = @{{blankImageUrl}};
                },10);
            } else {
                @{{el}}.src = @{{blankImageUrl}};
                @{{el}}.style.height = h + "px";
                @{{el}}.style.width = w + "px";
            }
            @{{el}}.style.padding = "0";
            @{{el}}.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='"+src+"', sizingMethod='crop')";
        """)
        pass


    @classmethod
    def doIE6PngFix(cls, el):
        blankImageUrl = GWT.getModuleBaseURL() + 'ie6pngfix/blank.gif'
        src = el.getAttribute('src')
        if src is not None and not (src == blankImageUrl):
            cls.doPngFix(el, blankImageUrl)


    @classmethod
    def cloneNode(cls, element, deep):
        """Clones given element as in JavaScript.

        Deprecate this if there appears similar method into GWT someday.

        @param element:
        @param deep:
                   clone child tree also
        """
        JS("""
            return @{{element}}.cloneNode(@{{deep}});
        """)
        pass


    @classmethod
    def measureHorizontalPaddingAndBorder(cls, element, paddingGuess):
        originalWidth = DOM.getStyleAttribute(element, 'width')
        originalOverflow = ''
        if BrowserInfo.get().isIE6():
            originalOverflow = DOM.getStyleAttribute(element, 'overflow')
            DOM.setStyleAttribute(element, 'overflow', 'hidden')

        originalOffsetWidth = element.getOffsetWidth()
        widthGuess = originalOffsetWidth - paddingGuess
        if widthGuess < 1:
            widthGuess = 1

        DOM.setStyleAttribute(element, 'width', widthGuess + 'px')
        padding = element.getOffsetWidth() - widthGuess

        DOM.setStyleAttribute(element, 'width', originalWidth)
        if BrowserInfo.get().isIE6():
            DOM.setStyleAttribute(element, 'overflow', originalOverflow)

        return padding


    @classmethod
    def measureVerticalPaddingAndBorder(cls, element, paddingGuess):
        originalHeight = DOM.getStyleAttribute(element, 'height')
        originalOffsetHeight = element.getOffsetHeight()
        widthGuess = originalOffsetHeight - paddingGuess
        if widthGuess < 1:
            widthGuess = 1

        DOM.setStyleAttribute(element, 'height', widthGuess + 'px')
        padding = element.getOffsetHeight() - widthGuess

        DOM.setStyleAttribute(element, 'height', originalHeight)
        return padding


    @classmethod
    def measureHorizontalBorder(cls, element):
        if BrowserInfo.get().isIE():
            width = element.getStyle().getProperty('width')
            height = element.getStyle().getProperty('height')

            offsetWidth = element.getOffsetWidth()
            offsetHeight = element.getOffsetHeight()
            if not BrowserInfo.get().isIE7():
                if offsetHeight < 1:
                    offsetHeight = 1

                if offsetWidth < 1:
                    offsetWidth = 10

                element.getStyle().setPropertyPx('height', offsetHeight)

            element.getStyle().setPropertyPx('width', offsetWidth)

            borders = element.getOffsetWidth() - element.getClientWidth()

            element.getStyle().setProperty('width', width)
            if not BrowserInfo.get().isIE7():
                element.getStyle().setProperty('height', height)
        else:
            borders = (element.getOffsetWidth()
                    - element.getPropertyInt('clientWidth'))

        assert borders >= 0

        return borders


    @classmethod
    def measureVerticalBorder(cls, element):
        if BrowserInfo.get().isIE():
            width = element.getStyle().getProperty('width')
            height = element.getStyle().getProperty('height')

            offsetWidth = element.getOffsetWidth()
            offsetHeight = element.getOffsetHeight()
            # if (BrowserInfo.get().isIE6()) {
            if offsetHeight < 1:
                offsetHeight = 1

            if offsetWidth < 1:
                offsetWidth = 10

            element.getStyle().setPropertyPx('width', offsetWidth)
            # }
            element.getStyle().setPropertyPx('height', offsetHeight)
            borders = (element.getOffsetHeight()
                    - element.getPropertyInt('clientHeight'))
            element.getStyle().setProperty('height', height)
            # if (BrowserInfo.get().isIE6()) {
            element.getStyle().setProperty('width', width)
            # }
        else:
            borders = element.getOffsetHeight() - element.getPropertyInt('clientHeight')

        assert borders >= 0

        return borders


    @classmethod
    def measureMarginLeft(cls, element):
        return (element.getAbsoluteLeft()
                - element.getParentElement().getAbsoluteLeft())


    @classmethod
    def setHeightExcludingPaddingAndBorder(cls, *args):
        nargs = len(args)
        if nargs == 3:
            widget, height, paddingBorderGuess = args
            if height == '':
                cls.setHeight(widget, '')
                return paddingBorderGuess
            elif height.endswith('px'):
                pixelHeight = int(height[:-2])
                return cls.setHeightExcludingPaddingAndBorder(
                        widget.getElement(), pixelHeight,
                        paddingBorderGuess, False)
            else:
                # Set the height in unknown units
                cls.setHeight(widget, height)
                # Use the offsetWidth
                return cls.setHeightExcludingPaddingAndBorder(
                        widget.getElement(), widget.getOffsetHeight(),
                        paddingBorderGuess, True)
        elif nargs == 4:
            (element, requestedHeight, verticalPaddingBorderGuess,
             requestedHeightIncludesPaddingBorder) = args

            heightGuess = requestedHeight - verticalPaddingBorderGuess
            if heightGuess < 0:
                heightGuess = 0

            DOM.setStyleAttribute(element, 'height', heightGuess + 'px')
            captionOffsetHeight = DOM.getIntElemAttribute(element,
                    'offsetHeight')

            actualPadding = captionOffsetHeight - heightGuess

            if requestedHeightIncludesPaddingBorder:
                actualPadding += actualPadding

            if actualPadding != verticalPaddingBorderGuess:
                h = requestedHeight - actualPadding
                if h < 0:
                    # Cannot set negative height even if we would want to
                    h = 0
                DOM.setStyleAttribute(element, 'height', h + 'px')

            return actualPadding
        else:
            raise ValueError('nargs=%d - 3 or 4 allowed' % nargs)


    @classmethod
    def setWidth(cls, widget, width):
        DOM.setStyleAttribute(widget.getElement(), 'width', width)


    @classmethod
    def setHeight(cls, widget, height):
        DOM.setStyleAttribute(widget.getElement(), 'height', height)


    @classmethod
    def setWidthExcludingPaddingAndBorder(cls, *args):
        nargs = len(args)
        if nargs == 3:
            widget, width, paddingBorderGuess = args
            if width == '':
                cls.setWidth(widget, '')
                return paddingBorderGuess
            elif width.endswith('px'):
                pixelWidth = int(width[:-2])
                return cls.setWidthExcludingPaddingAndBorder(
                        widget.getElement(), pixelWidth,
                        paddingBorderGuess, False)
            else:
                cls.setWidth(widget, width)
                return cls.setWidthExcludingPaddingAndBorder(
                        widget.getElement(), widget.getOffsetWidth(),
                        paddingBorderGuess, True)
        elif nargs == 4:
            (element, requestedWidth, horizontalPaddingBorderGuess,
             requestedWidthIncludesPaddingBorder) = args

            widthGuess = requestedWidth - horizontalPaddingBorderGuess
            if widthGuess < 0:
                widthGuess = 0

            DOM.setStyleAttribute(element, 'width', widthGuess + 'px')
            captionOffsetWidth = DOM.getIntElemAttribute(element,
                    'offsetWidth')
            actualPadding = captionOffsetWidth - widthGuess
            if requestedWidthIncludesPaddingBorder:
                actualPadding += actualPadding

            if actualPadding != horizontalPaddingBorderGuess:
                w = requestedWidth - actualPadding
                if w < 0:
                    # Cannot set negative width even if we would want to
                    w = 0
                DOM.setStyleAttribute(element, 'width', w + 'px')

            return actualPadding
        else:
            raise ValueError('nargs=%d - 3 or 4 allowed' % nargs)


    @classmethod
    def getSimpleName(cls, widget):
        if widget is None:
            return '(null)'
        name = widget.__class__.__name__
        return name[name.rfind('.') + 1:]


    @classmethod
    def setFloat(cls, element, value):
        if BrowserInfo.get().isIE():
            DOM.setStyleAttribute(element, 'styleFloat', value)
        else:
            DOM.setStyleAttribute(element, 'cssFloat', value)

    _detectedScrollbarSize = -1


    @classmethod
    def getNativeScrollbarSize(cls):
        if cls._detectedScrollbarSize < 0:
            scroller = DOM.createDiv()
            scroller.getStyle().setProperty('width', '50px')
            scroller.getStyle().setProperty('height', '50px')
            scroller.getStyle().setProperty('overflow', 'scroll')
            scroller.getStyle().setProperty('position', 'absolute')
            scroller.getStyle().setProperty('marginLeft', '-5000px')
            RootPanel.getBodyElement().appendChild(scroller)
            cls._detectedScrollbarSize = (scroller.getOffsetWidth()
                    - scroller.getPropertyInt('clientWidth'))
            RootPanel.getBodyElement().removeChild(scroller)
        return cls._detectedScrollbarSize


    @classmethod
    def runWebkitOverflowAutoFix(cls, elem):
        """Run workaround for webkits overflow auto issue.

        See: our bug #2138 and https://bugs.webkit.org/show_bug.cgi?id=21462

        @param elem:
                   with overflow auto
        """
        # Add max version if fix lands sometime to Webkit
        # Starting from Opera 11.00, also a problem in Opera
        if ((BrowserInfo.get().getWebkitVersion() > 0)
                or (BrowserInfo.get().getOperaVersion() >= 11)
                and cls.getNativeScrollbarSize() > 0):

            originalOverflow = elem.getStyle().getProperty('overflow')
            if originalOverflow == 'hidden':
                return

            # check the scrolltop value before hiding the element
            scrolltop = elem.getScrollTop()
            scrollleft = elem.getScrollLeft()
            elem.getStyle().setProperty('overflow', 'hidden')

            class _1_(Command):

                def execute(self):
                    # Dough, Safari scroll auto means actually just a moped
                    self.elem.getStyle().setProperty('overflow',
                            self.originalOverflow)
                    if (self.scrolltop > 0) or (self.elem.getScrollTop() > 0):
                        scrollvalue = self.scrolltop
                        if scrollvalue == 0:
                            # mysterious are the ways of webkits scrollbar
                            # handling. In some cases webkit reports bad (0)
                            # scrolltop before hiding the element temporary,
                            # sometimes after.
                            scrollvalue = self.elem.getScrollTop()
                        # fix another bug where scrollbar remains in wrong
                        # position
                        self.elem.setScrollTop(scrollvalue - 1)
                        self.elem.setScrollTop(scrollvalue)
                    # fix for #6940 : Table horizontal scroll sometimes not
                    # updated when collapsing/expanding columns
                    # Also appeared in Safari 5.1 with webkit 534 (#7667)
                    if (BrowserInfo.get().isChrome()
                            or (BrowserInfo.get().isSafari() and BrowserInfo.get().getWebkitVersion() >= 534)
                            and (self.scrollleft > 0)
                            or (self.elem.getScrollLeft() > 0)):
                        scrollvalue = self.scrollleft
                        if scrollvalue == 0:
                            # mysterious are the ways of webkits scrollbar
                            # handling. In some cases webkit may report a bad
                            # (0) scrollleft before hiding the element
                            # temporary, sometimes after.
                            scrollvalue = self.elem.getScrollLeft()
                        # fix another bug where scrollbar remains in wrong
                        # position
                        self.elem.setScrollLeft(scrollvalue - 1)
                        self.elem.setScrollLeft(scrollvalue)

            _1_ = _1_()
            Scheduler.get().scheduleDeferred(_1_)


    @classmethod
    def isCached(cls, uidl):
        return uidl.getBooleanAttribute('cached')


    @classmethod
    def alert(cls, string):
        if True:
            Window.alert(string)


    @classmethod
    def equals(cls, a, b):
        if a is None:
            return b is None
        return a == b


    @classmethod
    def updateRelativeChildrenAndSendSizeUpdateEvent(cls, client,
                container, widget=None):
        # Relative sized children must be updated first so the component has
        # the correct outer dimensions when signaling a size change to the
        # parent.
        if widget is None:
            cls.updateRelativeChildrenAndSendSizeUpdateEvent(client,
                    container, container)
        else:
            childIterator = container
            for w in childIterator:
                client.handleComponentRelativeSize(w)
            widgets = set()
            widgets.add(widget)
            Util.componentSizeUpdated(widgets)


    @classmethod
    def getRequiredWidth(cls, widget_or_element):
        if isinstance(widget_or_element, Widget):
            widget = widget_or_element
            return cls.getRequiredWidth(widget.getElement())
        else:
            element = widget_or_element
            JS("""
                if (@{{element}}.getBoundingClientRect) {
                  var rect = @{{element}}.getBoundingClientRect();
                  return Math.ceil(rect.right - rect.left);
                } else {
                  return @{{element}}.offsetWidth;
                }
            """)

    @classmethod
    def getRequiredHeight(cls, widget_or_element):
        if isinstance(widget_or_element, Widget):
            widget = widget_or_element
            return cls.getRequiredHeight(widget.getElement())
        else:
            element = widget_or_element
            JS("""
                var height;
                if (@{{element}}.getBoundingClientRect != null) {
                  var rect = @{{element}}.getBoundingClientRect();
                  height = Math.ceil(rect.bottom - rect.top);
                } else {
                  height = @{{element}}.offsetHeight;
                }
                return height;
            """)

    @classmethod
    def mayHaveScrollBars(cls, pe):
        """Detects what is currently the overflow style attribute in given
        element.

        @param pe:
                   the element to detect
        @return: true if auto or scroll
        """
        overflow = cls.getComputedStyle(pe, 'overflow')
        if overflow is not None:
            if (overflow == 'auto') or (overflow == 'scroll'):
                return True
            else:
                return False
        else:
            return False


    @classmethod
    def getComputedStyle(cls, el, p):
        """A simple helper method to detect "computed style" (aka style
        sheets + element styles). Values returned differ a lot depending
        on browsers. Always be very careful when using this.

        @param el:
                   the element from which the style property is detected
        @param p:
                   the property to detect
        @return: String value of style property
        """
        JS("""
            try {

            if (@{{el}}.currentStyle) {
                // IE
                return @{{el}}.currentStyle[@{{p}}];
            } else if (window.getComputedStyle) {
                // Sa, FF, Opera
                var view = @{{el}}.ownerDocument.defaultView;
                return view.getComputedStyle(@{{el}},null).getPropertyValue(@{{p}});
            } else {
                // fall back for non IE, Sa, FF, Opera
                return "";
            }
            } catch (e) {
                return "";
            }
        """)
        pass


    @classmethod
    def runIE7ZeroSizedBodyFix(cls):
        """IE7 sometimes "forgets" to render content. This function runs a
        hack to workaround the bug if needed. This happens easily in framset.
        See #3295.
        """
        if BrowserInfo.get().isIE7():
            offsetWidth = RootPanel.getBodyElement().getOffsetWidth()
            if offsetWidth == 0:
                cls.shakeBodyElement()


    @classmethod
    def shakeBodyElement(cls):
        """Does some very small adjustments to body element. We need this
        just to overcome some IE bugs.
        """
        shaker = DOM.createDiv()
        RootPanel.getBodyElement().insertBefore(shaker,
                RootPanel.getBodyElement().getFirstChildElement())
        shaker.getStyle().setPropertyPx('height', 0)
        shaker.setInnerHTML('&nbsp;')
        RootPanel.getBodyElement().removeChild(shaker)


    @classmethod
    def getChildPaintableForElement(cls, client, parent, element):
        """Locates the child component of <literal>parent</literal> which
        contains the element <literal>element</literal>. The child component
        is also returned if "element" is part of its caption. If
        <literal>element</literal> is not part of any child component, null is
        returned.

        This method returns the immediate child of the parent that contains the
        element. See L{getPaintableForElement} for the deepest nested paintable
        of parent that contains the element.

        @param client:
                   A reference to ApplicationConnection
        @param parent:
                   The widget that contains <literal>element</literal>.
        @param element:
                   An element that is a sub element of the parent
        @return: The Paintable which the element is a part of. Null if the
                 element does not belong to a child.
        """
        rootElement = parent.getElement()
        while (element is not None) and (element != rootElement):
            paintable = client.getPaintable(element)
            if paintable is None:
                ownerPid = VCaption.getCaptionOwnerPid(element)
                if ownerPid is not None:
                    paintable = client.getPaintable(ownerPid)
            if paintable is not None:
                # We assume everything is a widget however there is no need
                # to crash everything if there is a paintable that is not.
                try:
                    if parent.hasChildComponent(paintable):
                        return paintable
                except Exception:#ClassCastException:
                    pass
            element = element.getParentElement()
        return None


    @classmethod
    def getPaintableForElement(cls, client, parent, element):
        """Locates the nested child component of <literal>parent</literal>
        which contains the element <literal>element</literal>. The child
        component is also returned if "element" is part of its caption. If
        <literal>element</literal> is not part of any child component, null
        is returned.

        This method returns the deepest nested Paintable. See
        L{getChildPaintableForElement} for the immediate child component of
        parent that contains the element.

        @param client:
                   A reference to ApplicationConnection
        @param parent:
                   The widget that contains <literal>element</literal>.
        @param element:
                   An element that is a sub element of the parent
        @return: The Paintable which the element is a part of. Null if the
                 element does not belong to a child.
        """
        rootElement = parent.getElement()
        while (element is not None) and (element != rootElement):
            paintable = client.getPaintable(element)
            if paintable is None:
                ownerPid = VCaption.getCaptionOwnerPid(element)
                if ownerPid is not None:
                    paintable = client.getPaintable(ownerPid)
            if paintable is not None:
                # check that inside the rootElement
                while (element is not None) and (element != rootElement):
                    element = element.getParentElement()
                if element != rootElement:
                    return None
                else:
                    return paintable
            element = element.getParentElement()
        return None


    @classmethod
    def focus(cls, el):
        """Will (attempt) to focus the given DOM Element.

        @param el: the element to focus
        """
        JS("""
            try {
                @{{el}}.focus();
            } catch (e) {

            }
        """)
        pass


    @classmethod
    def findWidget(cls, element, class1):
        """Helper method to find first instance of given Widget type found
        by traversing DOM upwards from given element.

        @param element:
                   the element where to start seeking of Widget
        @param class1:
                   the Widget type to seek for
        """
        if element is not None:
            # First seek for the first EventListener (~Widget) from dom
            eventListener = None
            while eventListener is None and element is not None:
                eventListener = Event.getEventListener(element)
                if eventListener is None:
                    element = element.getParentElement()

            if eventListener is not None:
                # Then find the first widget of type class1 from widget
                # hierarchy
                w = eventListener
                while w is not None:
                    if (class1 is None) or (w.getClass() == class1):
                        return w
                    w = w.getParent()
        return None


    @classmethod
    def forceWebkitRedraw(cls, element):
        """Force webkit to redraw an element

        @param element:
                   The element that should be redrawn
        """
        style = element.getStyle()
        s = style.getProperty('webkitTransform')
        if (s is None) or (len(s) == 0):
            style.setProperty('webkitTransform', 'scale(1)')
        else:
            style.setProperty('webkitTransform', '')


    @classmethod
    def detachAttach(cls, element):
        """Detaches and re-attaches the element from its parent. The element
        is reattached at the same position in the DOM as it was before.

        Does nothing if the element is not attached to the DOM.

        @param element:
                   The element to detach and re-attach
        """
        if element is None:
            return
        nextSibling = element.getNextSibling()
        parent = element.getParentNode()
        if parent is None:
            return
        parent.removeChild(element)
        if nextSibling is None:
            parent.appendChild(element)
        else:
            parent.insertBefore(element, nextSibling)


    @classmethod
    def sinkOnloadForImages(cls, element):
        imgElements = element.getElementsByTagName('img')
        for img in imgElements:
            DOM.sinkEvents(img, Event.ONLOAD)


    @classmethod
    def getChildElementIndex(cls, childElement):
        """Returns the index of the childElement within its parent.
        """
        idx = 0
        n = childElement.getPreviousSibling()
        while n is not None:
            idx += 1
            n = n.getPreviousSibling()
        return idx


    @classmethod
    def printPaintablesVariables(cls, variables, Id, c):
        paintable = c.getPaintable(Id)
        if paintable is not None:
            VConsole.log('\t' + Id + ' (' + paintable.getClass() + ') :')
            for var in variables:
                VConsole.log('\t\t' + var[1] + ' (' + var[2] + ')'
                        + ' : ' + var[0])


    @classmethod
    def logVariableBurst(cls, c, loggedBurst):
        try:
            VConsole.log('Variable burst to be sent to server:')
            curId = None
            variables = list()
            i = 0
            while i < len(loggedBurst):
                value = loggedBurst[i]
                i += 1
                sep = ApplicationConnection.VAR_FIELD_SEPARATOR
                split = loggedBurst[i].split(sep)
                Id = split[0]
                if curId is None:
                    curId = Id
                elif not (curId == Id):
                    cls.printPaintablesVariables(variables, curId, c)
                    variables.clear()
                    curId = Id
                split[0] = value
                variables.add(split)
                i += 1
            if len(variables) > 0:
                cls.printPaintablesVariables(variables, curId, c)
        except Exception, e:
            VConsole.error(e)


    @classmethod
    def setStyleTemporarily(cls, element, styleProperty, tempValue):
        """Temporarily sets the C{styleProperty} to C{tempValue} and then
        resets it to its current value. Used mainly to work around rendering
        issues in IE (and possibly in other browsers)

        @param element:
                   The target element
        @param styleProperty:
                   The name of the property to set
        @param tempValue:
                   The temporary value
        """
        style = element.getStyle()
        currentValue = style.getProperty(styleProperty)
        style.setProperty(styleProperty, tempValue)
        element.getOffsetWidth()
        style.setProperty(styleProperty, currentValue)


    @classmethod
    def getTouchOrMouseClientX(cls, event):
        """A helper method to return the client position from an event. Returns
        position from either first changed touch (if touch event) or from the
        event itself.

        @see: L{getTouchOrMouseClientX}
        """
        if cls.isTouchEvent(event):
            return event.getChangedTouches().get(0).getClientX()
        else:
            return event.getClientX()


    @classmethod
    def getTouchOrMouseClientY(cls, event):
        """A helper method to return the client position from an event. Returns
        position from either first changed touch (if touch event) or from the
        event itself.

        @see: L{getTouchOrMouseClientY}
        """
        if cls.isTouchEvent(event):
            return event.getChangedTouches().get(0).getClientY()
        else:
            return event.getClientY()


    @classmethod
    def isTouchEvent(cls, event):
        return event.getType().contains('touch')


    @classmethod
    def simulateClickFromTouchEvent(cls, touchevent, widget):
        touch = touchevent.getChangedTouches().get(0)
        createMouseUpEvent = DOM.createMouseUpEvent(0, touch.getScreenX(), touch.getScreenY(), touch.getClientX(), touch.getClientY(), False, False, False, False, NativeEvent.BUTTON_LEFT)
        createMouseDownEvent = DOM.createMouseDownEvent(0, touch.getScreenX(), touch.getScreenY(), touch.getClientX(), touch.getClientY(), False, False, False, False, NativeEvent.BUTTON_LEFT)
        createMouseClickEvent = DOM.createClickEvent(0, touch.getScreenX(), touch.getScreenY(), touch.getClientX(), touch.getClientY(), False, False, False, False)
        # Get target with element from point as we want the actual element, not
        # the one that sunk the event.

        target = cls.getElementFromPoint(touch.getClientX(), touch.getClientY())

        class _2_(ScheduledCommand):

            def execute(self):
                try:
                    self.target.dispatchEvent(self.createMouseDownEvent)
                    self.target.dispatchEvent(self.createMouseUpEvent)
                    self.target.dispatchEvent(self.createMouseClickEvent)
                except Exception, e:
                    pass # astStmt: [Stmt([]), None]

        _2_ = _2_()
        Scheduler.get().scheduleDeferred(_2_)

    @classmethod
    def getIEFocusedElement(cls):
        """Gets the currently focused element for Internet Explorer.

        @return The currently focused element
        """
        JS("""
            if ($wnd.document.activeElement) {
                return $wnd.document.activeElement;
            }

            return null;
        """)
        pass


    @classmethod
    def isAttachedAndDisplayed(cls, widget):
        """Kind of stronger version of isAttached(). In addition to std
        isAttached, this method checks that this widget nor any of its parents
        is hidden. Can be e.g used to check whether component should react to
        some events or not.

        @return: true if attached and displayed
        """
        if widget.isAttached():
            # Failfast using offset size, then by iterating the widget tree
            notZeroSized = ((widget.getOffsetHeight() > 0)
                    or (widget.getOffsetWidth() > 0))
            return notZeroSized or cls.checkVisibilityRecursively(widget)
        else:
            return False


    @classmethod
    def checkVisibilityRecursively(cls, widget):
        if widget.isVisible():
            parent = widget.getParent()
            if parent is None:
                return True  # root panel
            else:
                return cls.checkVisibilityRecursively(parent)
        else:
            return False


    @classmethod
    def scrollIntoViewVertically(cls, elem):
        """Scrolls an element into view vertically only. Modified version of
        Element.scrollIntoView.

        @param elem
                   The element to scroll into view
        """
        JS("""
            var top = @{{elem}}.offsetTop;
            var height = @{{elem}}.offsetHeight;

            if (@{{elem}}.parentNode != @{{elem}}.offsetParent) {
              top -= @{{elem}}.parentNode.offsetTop;
            }

            var cur = @{{elem}}.parentNode;
            while (cur && (cur.nodeType == 1)) {
              if (top < cur.scrollTop) {
                cur.scrollTop = top;
              }
              if (top + height > cur.scrollTop + cur.clientHeight) {
                cur.scrollTop = (top + height) - cur.clientHeight;
              }

              var offsetTop = cur.offsetTop;
              if (cur.parentNode != cur.offsetParent) {
                offsetTop -= cur.parentNode.offsetTop;
              }

              top += offsetTop - cur.scrollTop;
              cur = cur.parentNode;
            }
        """)
        pass
