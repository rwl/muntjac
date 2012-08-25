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

"""The foundation for all Muntjac themes."""


class BaseTheme(object):
    """The Base theme is the foundation for all Muntjac themes. Although
    it is not necessary to use it as the starting point for all other
    themes, it is heavily encouraged, since it abstracts and hides away
    many necessary style properties that the Muntjac terminal expects and
    needs.

    When creating your own theme, either extend this class and specify
    the styles implemented in your theme here, or extend some other theme
    that has a class file specified (e.g. Reindeer or Runo).

    All theme class files should follow the convention of specifying the
    theme name as a string constant C{THEME_NAME}.
    """

    THEME_NAME = 'base'

    #: Creates a button that looks like a regular hypertext link but still
    #  acts like a normal button.
    BUTTON_LINK = 'link'

    #: Removes extra decorations from the panel.
    #
    # @deprecated: Base theme does not implement this style, but it is defined
    #              here since it has been a part of the framework before
    #              multiple themes were available. Use the constant provided
    #              by the theme you're using instead, e.g.
    #              L{Reindeer.PANEL_LIGHT} or L{Runo.PANEL_LIGHT}.
    PANEL_LIGHT = 'light'
