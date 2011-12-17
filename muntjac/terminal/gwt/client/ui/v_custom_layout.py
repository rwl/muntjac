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

from __pyjamas__ import JS

from pyjamas import DOM

from pyjamas.ui import Event

from pyjamas.ui.ComplexPanel import ComplexPanel

from muntjac.terminal.gwt.client.paintable import IPaintable
from muntjac.terminal.gwt.client.container import IContainer
from muntjac.terminal.gwt.client.render_space import RenderSpace
from muntjac.terminal.gwt.client.container_resized_listener import IContainerResizedListener
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.v_caption import VCaption
from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.v_caption_wrapper import VCaptionWrapper
from muntjac.terminal.gwt.client.render_information import FloatSize


class VCustomLayout(ComplexPanel, IPaintable, IContainer,
            IContainerResizedListener):
    """Custom Layout implements complex layout defined with HTML template.

    @author: IT Mill
    @author: Richard Lincoln
    """

    CLASSNAME = 'v-customlayout'

    def __init__(self):
        # Location-name to containing element in DOM map
        self._locationToElement = dict()

        # Location-name to contained widget map
        self._locationToWidget = dict()

        # Widget to captionwrapper map
        self._widgetToCaptionWrapper = dict()

        # Name of the currently rendered style
        self._currentTemplateName = None

        # Unexecuted scripts loaded from the template
        self._scripts = ''

        # Paintable ID of this paintable
        self._pid = None
        self._client = None

        # Has the template been loaded from contents passed in UIDL *
        self._hasTemplateContents = False
        self._elementWithNativeResizeFunction = None
        self._height = ''
        self._width = ''
        self._locationToExtraSize = dict()

        self.setElement(DOM.createDiv())

        # Clear any unwanted styling
        DOM.setStyleAttribute(self.getElement(), 'border', 'none')
        DOM.setStyleAttribute(self.getElement(), 'margin', '0')
        DOM.setStyleAttribute(self.getElement(), 'padding', '0')

        if BrowserInfo.get().isIE():
            DOM.setStyleAttribute(self.getElement(), 'position', 'relative')

        self.setStyleName(self.CLASSNAME)


    def setWidget(self, widget, location):
        """Sets widget to given location.

        If location already contains a widget it will be removed.

        @param widget:
                   Widget to be set into location.
        @param location:
                   location name where widget will be added

        @raise ValueError:
                    if no such location is found in the layout.
        """
        if widget is None:
            return

        # If no given location is found in the layout, and exception is throws
        elem = self._locationToElement[location]
        if elem is None and self.hasTemplate():
            raise ValueError('No location ' + location + ' found')

        # Get previous widget
        previous = self._locationToWidget[location]

        # NOP if given widget already exists in this location
        if previous == widget:
            return

        if previous is not None:
            self.remove(previous)

        # if template is missing add element in order
        if not self.hasTemplate():
            elem = self.getElement()

        # Add widget to location
        super(VCustomLayout, self).add(widget, elem)

        self._locationToWidget.put(location, widget)


    def updateFromUIDL(self, uidl, client):
        """Update the layout from UIDL"""
        self._client = client

        # ApplicationConnection manages generic component features
        if client.updateComponent(self, uidl, True):
            return

        self._pid = uidl.getId()

        if not self.hasTemplate():
            # Update HTML template only once
            self.initializeHTML(uidl, client)

        # Evaluate scripts
        self.eval(self._scripts)
        self._scripts = None
        self.iLayout()

        # TODO: Check if this is needed
        client.runDescendentsLayout(self)
        oldWidgets = set()
        oldWidgets.addAll(self._locationToWidget.values())

        # For all contained widgets
        i = uidl.getChildIterator()
        while i.hasNext():
            uidlForChild = i.next()
            if uidlForChild.getTag() == 'location':
                location = uidlForChild.getStringAttribute('name')
                child = client.getPaintable(uidlForChild.getChildUIDL(0))
                # If no location is found, this component is not visible
                try:
                    self.setWidget(child, location)
                    child.updateFromUIDL(uidlForChild.getChildUIDL(0), client)
                except ValueError:
                    pass
                oldWidgets.remove(child)

        iterator = oldWidgets
        while iterator.hasNext():
            oldWidget = iterator.next()
            if oldWidget.isAttached():
                # slot of this widget is emptied, remove it
                self.remove(oldWidget)

        self.iLayout()

        # TODO: Check if this is needed
        client.runDescendentsLayout(self)


    def initializeHTML(self, uidl, client):
        """Initialize HTML-layout."""
        newTemplateContents = uidl.getStringAttribute('templateContents')
        newTemplate = uidl.getStringAttribute('template')
        self._currentTemplateName = None
        self._hasTemplateContents = False
        template = ''
        if newTemplate is not None:
            # Get the HTML-template from client
            template = client.getResource('layouts/' + newTemplate + '.html')
            if template is None:
                template = ('<em>Layout file layouts/' + newTemplate
                        + '.html is missing. Components will be drawn for debug purposes.</em>')
            else:
                self._currentTemplateName = newTemplate
        else:
            self._hasTemplateContents = True
            template = newTemplateContents

        # Connect body of the template to DOM
        template = self.extractBodyAndScriptsFromTemplate(template)

        # TODO: prefix img src:s here with a regeps, cannot work further with IE
        themeUri = client.getThemeUri()
        relImgPrefix = themeUri + '/layouts/'

        # prefix all relative image elements to point to theme dir with a
        # regexp search
        template = template.replaceAll('<((?:img)|(?:IMG))\\s([^>]*)src=\"((?![a-z]+:)[^/][^\"]+)\"', '<$1 $2src=\"' + relImgPrefix + '$3\"')

        # also support src attributes without quotes
        template = template.replaceAll('<((?:img)|(?:IMG))\\s([^>]*)src=[^\"]((?![a-z]+:)[^/][^ />]+)[ />]', '<$1 $2src=\"' + relImgPrefix + '$3\"')

        # also prefix relative style="...url(...)..."
        template = template.replaceAll('(<[^>]+style=\"[^\"]*url\\()((?![a-z]+:)[^/][^\"]+)(\\)[^>]*>)', '$1 ' + relImgPrefix + '$2 $3')
        self.getElement().setInnerHTML(template)

        # Remap locations to elements
        self._locationToElement.clear()
        self.scanForLocations(self.getElement())
        self.initImgElements()
        self._elementWithNativeResizeFunction = DOM.getFirstChild(self.getElement())

        if self._elementWithNativeResizeFunction is None:
            self._elementWithNativeResizeFunction = self.getElement()

        self.publishResizedFunction(self._elementWithNativeResizeFunction)


    def uriEndsWithSlash(self):
        JS("""
            var path =  $wnd.location.pathname;
            if(path.charAt(path.length - 1) == "/")
                return true;
            return false;
        """)
        pass


    def hasTemplate(self):
        if self._currentTemplateName is None and not self._hasTemplateContents:
            return False
        else:
            return True

    def scanForLocations(self, elem):
        """Collect locations from template"""
        location = elem.getAttribute('location')
        if not ('' == location):
            self._locationToElement.put(location, elem)
            elem.setInnerHTML('')
            x = Util.measureHorizontalPaddingAndBorder(elem, 0)
            y = Util.measureVerticalPaddingAndBorder(elem, 0)
            fs = FloatSize(x, y)
            self._locationToExtraSize.put(location, fs)
        else:
            len = DOM.getChildCount(elem)
            for i in range(len):
                self.scanForLocations(DOM.getChild(elem, i))


    @classmethod
    def eval(cls, script):
        """Evaluate given script in browser document"""
        JS("""
          try {
         	 if (@{{script}} != null)
          eval("{ var document = $doc; var window = $wnd; "+ @{{script}} + "}");
          } catch (e) {
          }
        """)
        pass


    def initImgElements(self):
        """Img elements needs some special handling in custom layout. Img
        elements will get their onload events sunk. This way custom layout
        can notify parent about possible size change.
        """
        nodeList = self.getElement().getElementsByTagName('IMG')
        for i in range(nodeList.getLength()):
            img = nodeList.getItem(i)
            DOM.sinkEvents(img, Event.ONLOAD)


    def extractBodyAndScriptsFromTemplate(self, html):
        """Extract body part and script tags from raw html-template.

        Saves contents of all script-tags to private property: scripts.
        Returns contents of the body part for the html without script-tags.
        Also replaces all _UID_ tags with an unique id-string.

        @param html:
                   Original HTML-template received from server
        @return: html that is used to create the HTMLPanel.
        """
        # Replace UID:s
        html = html.replaceAll('_UID_', self._pid + '__')

        # Exctract script-tags
        self._scripts = ''
        endOfPrevScript = 0
        nextPosToCheck = 0
        lc = html.toLowerCase()
        res = ''
        scriptStart = lc.find('<script', nextPosToCheck)
        while scriptStart > 0:
            res += html[endOfPrevScript:scriptStart]
            scriptStart = lc.find('>', scriptStart)
            j = lc.find('</script>', scriptStart)
            self._scripts += (html[scriptStart + 1:j]) + ';'
            nextPosToCheck = endOfPrevScript = j + len('</script>')
            scriptStart = lc.find('<script', nextPosToCheck)
        res += html[endOfPrevScript:]

        # Extract body
        html = res
        lc = html.lower()
        startOfBody = lc.find('<body')
        if startOfBody < 0:
            res = html
        else:
            res = ''
            startOfBody = lc.find('>', startOfBody) + 1
            endOfBody = lc.find('</body>', startOfBody)
            if endOfBody > startOfBody:
                res = html[startOfBody:endOfBody]
            else:
                res = html[startOfBody:]
        return res


    def replaceChildComponent(self, from_, to):
        """Replace child components"""
        location = self.getLocation(from_)
        if location is None:
            raise ValueError()
        self.setWidget(to, location)


    def hasChildComponent(self, component):
        """Does this layout contain given child"""
        return self._locationToWidget.containsValue(component)


    def updateCaption(self, component, uidl):
        """Update caption for given widget"""
        wrapper = self._widgetToCaptionWrapper[component]
        if VCaption.isNeeded(uidl):
            if wrapper is None:
                loc = self.getLocation(component)
                super(VCustomLayout, self).remove(component)
                wrapper = VCaptionWrapper(component, self._client)
                super(VCustomLayout, self).add(wrapper,
                        self._locationToElement[loc])
                self._widgetToCaptionWrapper.put(component, wrapper)
            wrapper.updateCaption(uidl)
        elif wrapper is not None:
            loc = self.getLocation(component)
            super(VCustomLayout, self).remove(wrapper)
            super(VCustomLayout, self).add(wrapper.getPaintable(),
                    self._locationToElement[loc])
            self._widgetToCaptionWrapper.remove(component)


    def getLocation(self, w):
        """Get the location of an widget"""
        for location in self._locationToWidget:
            if self._locationToWidget[location] == w:
                return location
        return None


    def remove(self, w):
        """Removes given widget from the layout"""
        self._client.unregisterPaintable(w)
        location = self.getLocation(w)
        if location is not None:
            del self._locationToWidget[location]

        cw = self._widgetToCaptionWrapper[w]
        if cw is not None:
            del self._widgetToCaptionWrapper[w]
            return super(VCustomLayout, self).remove(cw)
        elif w is not None:
            return super(VCustomLayout, self).remove(w)

        return False


    def add(self, w):
        """Adding widget without specifying location is not supported"""
        raise NotImplementedError


    def clear(self):
        """Clear all widgets from the layout"""
        super(VCustomLayout, self).clear()
        self._locationToWidget.clear()
        self._widgetToCaptionWrapper.clear()


    def iLayout(self):
        self.iLayoutJS(DOM.getFirstChild(self.getElement()))


    def notifyChildrenOfSizeChange(self):
        """This method is published to JS side with the same name into first
        DOM node of custom layout. This way if one implements some resizeable
        containers in custom layout he/she can notify children after resize.
        """
        self._client.runDescendentsLayout(self)


    def onDetach(self):
        super(VCustomLayout, self).onDetach()
        if self._elementWithNativeResizeFunction is not None:
            self.detachResizedFunction(self._elementWithNativeResizeFunction)


    def detachResizedFunction(self, element):
        JS("""
        	@{{element}}.notifyChildrenOfSizeChange = null;
        """)
        pass


    def publishResizedFunction(self, element):
        JS("""
        	var self = @{{self}};
        	@{{element}}.notifyChildrenOfSizeChange = function() {
        		self.@com.vaadin.terminal.gwt.client.ui.VCustomLayout::notifyChildrenOfSizeChange()();
        	};
        """)
        pass


    def iLayoutJS(self, el):
        """In custom layout one may want to run layout functions made with
        JavaScript. This function tests if one exists (with name "iLayoutJS"
        in layouts first DOM node) and runs et. Return value is used to
        determine if children needs to be notified of size changes.

        Note! When implementing a JS layout function you most likely want to
        call notifyChildrenOfSizeChange() function on your custom layouts main
        element. That method is used to control whether child components layout
        functions are to be run.

        @return: true if layout function exists and was run successfully, else
                 false.
        """
        JS("""
        	if(@{{el}} && @{{el}}.iLayoutJS) {
        		try {
        			@{{el}}.iLayoutJS();
        			return true;
        		} catch (e) {
        			return false;
        		}
        	} else {
        		return false;
        	}
        """)
        pass


    def requestLayout(self, child):
        self.updateRelativeSizedComponents(True, True)
        if (self._width == '') or (self._height == ''):
            # Automatically propagated upwards if the size can change
            return False
        return True


    def getAllocatedSpace(self, child):
        pe = child.getElement().getParentElement()
        extra = self._locationToExtraSize[self.getLocation(child)]
        return RenderSpace(pe.getOffsetWidth() - extra.getWidth(),
                pe.getOffsetHeight() - extra.getHeight(),
                Util.mayHaveScrollBars(pe))


    def onBrowserEvent(self, event):
        super(VCustomLayout, self).onBrowserEvent(event)
        if event.getTypeInt() == Event.ONLOAD:
            Util.notifyParentOfSizeChange(self, True)
            event.cancelBubble(True)


    def setHeight(self, height):
        if self._height == height:
            return

        shrinking = True
        if self.isLarger(height, self._height):
            shrinking = False

        self._height = height

        super(VCustomLayout, self).setHeight(height)

        # If the height shrinks we must remove all components with relative
        # height from the DOM, update their height when they do not affect the
        # available space and finally restore them to the original state
        if shrinking:
            self.updateRelativeSizedComponents(False, True)


    def setWidth(self, width):
        if self._width == width:
            return

        shrinking = True

        if self.isLarger(width, self._width):
            shrinking = False

        super(VCustomLayout, self).setWidth(width)

        self._width = width
        # If the width shrinks we must remove all components with relative
        # width from the DOM, update their width when they do not affect the
        # available space and finally restore them to the original state
        if shrinking:
            self.updateRelativeSizedComponents(True, False)


    def updateRelativeSizedComponents(self, relativeWidth, relativeHeight):
        relativeSizeWidgets = set()
        for widget in self._locationToWidget.values():
            relativeSize = self._client.getRelativeSize(widget)
            if relativeSize is not None:
                if ((relativeWidth and relativeSize.getWidth() >= 0.0)
                    or (relativeHeight and relativeSize.getHeight() >= 0.0)):
                    relativeSizeWidgets.add(widget)
                    widget.getElement().getStyle().setProperty('position',
                            'absolute')

        for widget in relativeSizeWidgets:
            self._client.handleComponentRelativeSize(widget)
            widget.getElement().getStyle().setProperty('position', '')


    def isLarger(self, newSize, currentSize):
        """Compares newSize with currentSize and returns true if it is clear
        that newSize is larger than currentSize. Returns false if newSize is
        smaller or if it is unclear which one is smaller.
        """
        if (newSize == '') or (currentSize == ''):
            return False

        if (not newSize.endswith('px')) or (not currentSize.endswith('px')):
            return False

        newSizePx = int(newSize[:-2])
        currentSizePx = int(currentSize[:-2])
        larger = newSizePx > currentSizePx
        return larger
