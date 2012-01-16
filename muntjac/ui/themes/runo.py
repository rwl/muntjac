# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
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

from muntjac.ui.themes.base_theme import BaseTheme


class Runo(BaseTheme):

    THEME_NAME = 'runo'

    @classmethod
    def themeName(cls):
        return cls.THEME_NAME.lower()

    # Button styles
    #
    #      ********************************************************************

    # Small sized button, use for context specific actions for example
    BUTTON_SMALL = 'small'

    # Big sized button, use to gather much attention for some particular action
    BUTTON_BIG = 'big'

    # Default action style for buttons (the button that should get activated
    # when the user presses 'enter' in a form). Use sparingly, only one default
    # button per view should be visible.
    BUTTON_DEFAULT = 'default'

    # Panel styles
    #
    #      ********************************************************************

    # Removes borders and background color from the panel
    PANEL_LIGHT = 'light'

    # TabSheet styles
    #
    #      ********************************************************************

    # Smaller tabs, no border and background for content area
    TABSHEET_SMALL = 'light'

    # SplitPanel styles
    #
    #      ********************************************************************

    # Reduces the width/height of the split handle. Useful when you don't want
    # the split handle to touch the sides of the containing layout.
    SPLITPANEL_REDUCED = 'rounded'

    # Reduces the visual size of the split handle to one pixel (the active drag
    # size is still larger).
    SPLITPANEL_SMALL = 'small'

    # Label styles
    #
    #      ********************************************************************

    # Largest title/header size. Use for main sections in your application.
    LABEL_H1 = 'h1'

    # Similar style as in panel captions. Useful for sub-sections within a
    # view.
    LABEL_H2 = 'h2'

    # Small font size. Useful for contextual help texts and similar less
    # frequently needed information. Use with modesty, since this style will be
    # more harder to read due to its smaller size and contrast.
    LABEL_SMALL = 'small'

    # Layout styles
    #
    #      ********************************************************************

    # An alternative background color for layouts. Use on top of white
    # background (e.g. inside Panels, TabSheets and sub-windows).
    LAYOUT_DARKER = 'darker'

    # Add a drop shadow around the layout and its contained components.
    # Produces a rectangular shadow, even if the contained component would have
    # a different shape.
    # <p>
    # Note: does not work in Internet Explorer 6
    CSSLAYOUT_SHADOW = 'box-shadow'

    # Adds necessary styles to the layout to make it look selectable (i.e.
    # clickable). Add a click listener for the layout, and toggle the
    # L{#CSSLAYOUT_SELECTABLE_SELECTED} style for the same layout to make
    # it look selected or not.
    CSSLAYOUT_SELECTABLE = 'selectable'
    CSSLAYOUT_SELECTABLE_SELECTED = 'selectable-selected'

    # TextField styles
    #
    #      ********************************************************************

    # Small sized text field with small font
    TEXTFIELD_SMALL = 'small'

    # Table styles
    #
    #      ********************************************************************

    # Smaller header and item fonts.
    TABLE_SMALL = 'small'

    # Removes the border and background color from the table. Removes
    # alternating row background colors as well.
    TABLE_BORDERLESS = 'borderless'

    # Accordion styles
    #
    #      ********************************************************************

    # A detached looking accordion, providing space around its captions and
    # content. Doesn't necessarily need a Panel or other container to wrap it
    # in order to make it look right.
    ACCORDION_LIGHT = 'light'

    # Window styles
    #
    #      ********************************************************************

    # Smaller header and a darker background color for the window. Useful for
    # smaller dialog-like windows.
    WINDOW_DIALOG = 'dialog'
