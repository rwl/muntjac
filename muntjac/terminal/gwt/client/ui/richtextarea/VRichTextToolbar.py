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

# Copyright 2007 Google Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# from com.google.gwt.core.client.GWT import (GWT,)
# from com.google.gwt.event.dom.client.ChangeEvent import (ChangeEvent,)
# from com.google.gwt.event.dom.client.ChangeHandler import (ChangeHandler,)
# from com.google.gwt.event.dom.client.ClickEvent import (ClickEvent,)
# from com.google.gwt.event.dom.client.ClickHandler import (ClickHandler,)
# from com.google.gwt.event.dom.client.KeyUpEvent import (KeyUpEvent,)
# from com.google.gwt.event.dom.client.KeyUpHandler import (KeyUpHandler,)
# from com.google.gwt.i18n.client.Constants import (Constants,)
# from com.google.gwt.resources.client.ClientBundle import (ClientBundle,)
# from com.google.gwt.resources.client.ImageResource import (ImageResource,)
# from com.google.gwt.user.client.Window import (Window,)
# from com.google.gwt.user.client.ui.Composite import (Composite,)
# from com.google.gwt.user.client.ui.FlowPanel import (FlowPanel,)
# from com.google.gwt.user.client.ui.Image import (Image,)
# from com.google.gwt.user.client.ui.ListBox import (ListBox,)
# from com.google.gwt.user.client.ui.PushButton import (PushButton,)
# from com.google.gwt.user.client.ui.RichTextArea import (RichTextArea,)
# from com.google.gwt.user.client.ui.ToggleButton import (ToggleButton,)


class VRichTextToolbar(Composite):
    """A modified version of sample toolbar for use with {@link RichTextArea}. It
    provides a simple UI for all rich text formatting, dynamically displayed only
    for the available functionality.
    """

    class Images(ClientBundle):
        """This {@link ClientBundle} is used for all the button icons. Using a
        bundle allows all of these images to be packed into a single image, which
        saves a lot of HTTP requests, drastically improving startup time.
        """

        def bold(self):
            pass

        def createLink(self):
            pass

        def hr(self):
            pass

        def indent(self):
            pass

        def insertImage(self):
            pass

        def italic(self):
            pass

        def justifyCenter(self):
            pass

        def justifyLeft(self):
            pass

        def justifyRight(self):
            pass

        def ol(self):
            pass

        def outdent(self):
            pass

        def removeFormat(self):
            pass

        def removeLink(self):
            pass

        def strikeThrough(self):
            pass

        def subscript(self):
            pass

        def superscript(self):
            pass

        def ul(self):
            pass

        def underline(self):
            pass

    class Strings(Constants):
        """This {@link Constants} interface is used to make the toolbar's strings
        internationalizable.
        """
        # We use an inner EventHandler class to avoid exposing event methods on the
        # RichTextToolbar itself.

        # private class EventHandler implements ClickHandler, ChangeHandler,
        # KeyUpHandler {
        # @SuppressWarnings("deprecation")
        # public void onChange(ChangeEvent event) {
        # Object sender = event.getSource();
        # if (sender == backColors) {
        # basic.setBackColor(backColors.getValue(backColors
        # .getSelectedIndex()));
        # backColors.setSelectedIndex(0);
        # } else if (sender == foreColors) {
        # basic.setForeColor(foreColors.getValue(foreColors
        # .getSelectedIndex()));
        # foreColors.setSelectedIndex(0);
        # } else if (sender == fonts) {
        # basic.setFontName(fonts.getValue(fonts.getSelectedIndex()));
        # fonts.setSelectedIndex(0);
        # } else if (sender == fontSizes) {
        # basic.setFontSize(fontSizesConstants[fontSizes
        # .getSelectedIndex() - 1]);
        # fontSizes.setSelectedIndex(0);
        # }
        # }
        # @SuppressWarnings("deprecation")
        # public void onClick(ClickEvent event) {
        # Object sender = event.getSource();
        # if (sender == bold) {
        # basic.toggleBold();
        # } else if (sender == italic) {
        # basic.toggleItalic();
        # } else if (sender == underline) {
        # basic.toggleUnderline();
        # } else if (sender == subscript) {
        # basic.toggleSubscript();
        # } else if (sender == superscript) {
        # basic.toggleSuperscript();
        # } else if (sender == strikethrough) {
        # extended.toggleStrikethrough();
        # } else if (sender == indent) {
        # extended.rightIndent();
        # } else if (sender == outdent) {
        # extended.leftIndent();
        # } else if (sender == justifyLeft) {
        # basic.setJustification(RichTextArea.Justification.LEFT);
        # } else if (sender == justifyCenter) {
        # basic.setJustification(RichTextArea.Justification.CENTER);
        # } else if (sender == justifyRight) {
        # basic.setJustification(RichTextArea.Justification.RIGHT);
        # } else if (sender == insertImage) {
        # final String url = Window.prompt("Enter an image URL:",
        # "http://");
        # if (url != null) {
        # extended.insertImage(url);
        # }
        # } else if (sender == createLink) {
        # final String url = Window
        # .prompt("Enter a link URL:", "http://");
        # if (url != null) {
        # extended.createLink(url);
        # }
        # } else if (sender == removeLink) {
        # extended.removeLink();
        # } else if (sender == hr) {
        # extended.insertHorizontalRule();
        # } else if (sender == ol) {
        # extended.insertOrderedList();
        # } else if (sender == ul) {
        # extended.insertUnorderedList();
        # } else if (sender == removeFormat) {
        # extended.removeFormat();
        # } else if (sender == richText) {
        # // We use the RichTextArea's onKeyUp event to update the toolbar
        # // status. This will catch any cases where the user moves the
        # // cursur using the keyboard, or uses one of the browser's
        # // built-in keyboard shortcuts.
        # updateStatus();
        # }
        # }
        # public void onKeyUp(KeyUpEvent event) {
        # if (event.getSource() == richText) {
        # // We use the RichTextArea's onKeyUp event to update the toolbar
        # // status. This will catch any cases where the user moves the
        # // cursor using the keyboard, or uses one of the browser's
        # // built-in keyboard shortcuts.
        # updateStatus();
        # }
        # }
        # }

        def black(self):
            pass

        def blue(self):
            pass

        def bold(self):
            pass

        def color(self):
            pass

        def createLink(self):
            pass

        def font(self):
            pass

        def green(self):
            pass

        def hr(self):
            pass

        def indent(self):
            pass

        def insertImage(self):
            pass

        def italic(self):
            pass

        def justifyCenter(self):
            pass

        def justifyLeft(self):
            pass

        def justifyRight(self):
            pass

        def large(self):
            pass

        def medium(self):
            pass

        def normal(self):
            pass

        def ol(self):
            pass

        def outdent(self):
            pass

        def red(self):
            pass

        def removeFormat(self):
            pass

        def removeLink(self):
            pass

        def size(self):
            pass

        def small(self):
            pass

        def strikeThrough(self):
            pass

        def subscript(self):
            pass

        def superscript(self):
            pass

        def ul(self):
            pass

        def underline(self):
            pass

        def white(self):
            pass

        def xlarge(self):
            pass

        def xsmall(self):
            pass

        def xxlarge(self):
            pass

        def xxsmall(self):
            pass

        def yellow(self):
            pass

    _fontSizesConstants = [RichTextArea.FontSize.XX_SMALL, RichTextArea.FontSize.X_SMALL, RichTextArea.FontSize.SMALL, RichTextArea.FontSize.MEDIUM, RichTextArea.FontSize.LARGE, RichTextArea.FontSize.X_LARGE, RichTextArea.FontSize.XX_LARGE]
    _images = GWT.create(Images)
    _strings = GWT.create(Strings)
    _handler = Composite.EventHandler()
    _richText = None
    _basic = None
    _extended = None
    _outer = FlowPanel()
    _topPanel = FlowPanel()
    _bottomPanel = FlowPanel()
    _bold = None
    _italic = None
    _underline = None
    _subscript = None
    _superscript = None
    _strikethrough = None
    _indent = None
    _outdent = None
    _justifyLeft = None
    _justifyCenter = None
    _justifyRight = None
    _hr = None
    _ol = None
    _ul = None
    _insertImage = None
    _createLink = None
    _removeLink = None
    _removeFormat = None
    _backColors = None
    _foreColors = None
    _fonts = None
    _fontSizes = None

    def __init__(self, richText):
        """Creates a new toolbar that drives the given rich text area.

        @param richText
                   the rich text area to be controlled
        """
        self._richText = richText
        self._basic = richText.getBasicFormatter()
        self._extended = richText.getExtendedFormatter()
        self._outer.add(self._topPanel)
        self._outer.add(self._bottomPanel)
        self._topPanel.setStyleName('gwt-RichTextToolbar-top')
        self._bottomPanel.setStyleName('gwt-RichTextToolbar-bottom')
        self.initWidget(self._outer)
        self.setStyleName('gwt-RichTextToolbar')
        if self._basic is not None:
            self._topPanel.add(self._bold = self.createToggleButton(self._images.bold(), self._strings.bold()))
            self._topPanel.add(self._italic = self.createToggleButton(self._images.italic(), self._strings.italic()))
            self._topPanel.add(self._underline = self.createToggleButton(self._images.underline(), self._strings.underline()))
            self._topPanel.add(self._subscript = self.createToggleButton(self._images.subscript(), self._strings.subscript()))
            self._topPanel.add(self._superscript = self.createToggleButton(self._images.superscript(), self._strings.superscript()))
            self._topPanel.add(self._justifyLeft = self.createPushButton(self._images.justifyLeft(), self._strings.justifyLeft()))
            self._topPanel.add(self._justifyCenter = self.createPushButton(self._images.justifyCenter(), self._strings.justifyCenter()))
            self._topPanel.add(self._justifyRight = self.createPushButton(self._images.justifyRight(), self._strings.justifyRight()))
        if self._extended is not None:
            self._topPanel.add(self._strikethrough = self.createToggleButton(self._images.strikeThrough(), self._strings.strikeThrough()))
            self._topPanel.add(self._indent = self.createPushButton(self._images.indent(), self._strings.indent()))
            self._topPanel.add(self._outdent = self.createPushButton(self._images.outdent(), self._strings.outdent()))
            self._topPanel.add(self._hr = self.createPushButton(self._images.hr(), self._strings.hr()))
            self._topPanel.add(self._ol = self.createPushButton(self._images.ol(), self._strings.ol()))
            self._topPanel.add(self._ul = self.createPushButton(self._images.ul(), self._strings.ul()))
            self._topPanel.add(self._insertImage = self.createPushButton(self._images.insertImage(), self._strings.insertImage()))
            self._topPanel.add(self._createLink = self.createPushButton(self._images.createLink(), self._strings.createLink()))
            self._topPanel.add(self._removeLink = self.createPushButton(self._images.removeLink(), self._strings.removeLink()))
            self._topPanel.add(self._removeFormat = self.createPushButton(self._images.removeFormat(), self._strings.removeFormat()))
        if self._basic is not None:
            self._bottomPanel.add(self._backColors = self.createColorList('Background'))
            self._bottomPanel.add(self._foreColors = self.createColorList('Foreground'))
            self._bottomPanel.add(self._fonts = self.createFontList())
            self._bottomPanel.add(self._fontSizes = self.createFontSizes())
            # We only use these handlers for updating status, so don't hook
            # them up unless at least basic editing is supported.
            # richText.addKeyUpHandler(handler);
            # richText.addClickHandler(handler);

    def createColorList(self, caption):
        lb = ListBox()
        lb.addChangeHandler(self._handler)
        lb.setVisibleItemCount(1)
        lb.addItem(caption)
        lb.addItem(self._strings.white(), 'white')
        lb.addItem(self._strings.black(), 'black')
        lb.addItem(self._strings.red(), 'red')
        lb.addItem(self._strings.green(), 'green')
        lb.addItem(self._strings.yellow(), 'yellow')
        lb.addItem(self._strings.blue(), 'blue')
        lb.setTabIndex(-1)
        return lb

    def createFontList(self):
        lb = ListBox()
        lb.addChangeHandler(self._handler)
        lb.setVisibleItemCount(1)
        lb.addItem(self._strings.font(), '')
        lb.addItem(self._strings.normal(), 'inherit')
        lb.addItem('Times New Roman', 'Times New Roman')
        lb.addItem('Arial', 'Arial')
        lb.addItem('Courier New', 'Courier New')
        lb.addItem('Georgia', 'Georgia')
        lb.addItem('Trebuchet', 'Trebuchet')
        lb.addItem('Verdana', 'Verdana')
        lb.setTabIndex(-1)
        return lb

    def createFontSizes(self):
        lb = ListBox()
        lb.addChangeHandler(self._handler)
        lb.setVisibleItemCount(1)
        lb.addItem(len(self._strings))
        lb.addItem(self._strings.xxsmall())
        lb.addItem(self._strings.xsmall())
        lb.addItem(self._strings.small())
        lb.addItem(self._strings.medium())
        lb.addItem(self._strings.large())
        lb.addItem(self._strings.xlarge())
        lb.addItem(self._strings.xxlarge())
        lb.setTabIndex(-1)
        return lb

    def createPushButton(self, img, tip):
        pb = PushButton(Image(img))
        pb.addClickHandler(self._handler)
        pb.setTitle(tip)
        pb.setTabIndex(-1)
        return pb

    def createToggleButton(self, img, tip):
        tb = ToggleButton(Image(img))
        tb.addClickHandler(self._handler)
        tb.setTitle(tip)
        tb.setTabIndex(-1)
        return tb

    def updateStatus(self):
        """Updates the status of all the stateful buttons."""
        if self._basic is not None:
            self._bold.setDown(self._basic.isBold())
            self._italic.setDown(self._basic.isItalic())
            self._underline.setDown(self._basic.isUnderlined())
            self._subscript.setDown(self._basic.isSubscript())
            self._superscript.setDown(self._basic.isSuperscript())
        if self._extended is not None:
            self._strikethrough.setDown(self._extended.isStrikethrough())
