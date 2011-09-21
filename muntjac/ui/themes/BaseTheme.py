# Copyright (C) 2011 Vaadin Ltd
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


class BaseTheme(object):
    """<p>
    The Base theme is the foundation for all Vaadin themes. Although it is not
    necessary to use it as the starting point for all other themes, it is heavily
    encouraged, since it abstracts and hides away many necessary style properties
    that the Vaadin terminal expects and needs.
    </p>
    <p>
    When creating your own theme, either extend this class and specify the styles
    implemented in your theme here, or extend some other theme that has a class
    file specified (e.g. Reindeer or Runo).
    </p>
    <p>
    All theme class files should follow the convention of specifying the theme
    name as a string constant <code>THEME_NAME</code>.

    @since 6.3.0
    """
    THEME_NAME = 'base'

    # Creates a button that looks like a regular hypertext link but still acts
    # like a normal button.
    BUTTON_LINK = 'link'

    # Removes extra decorations from the panel.
    #
    # @deprecated Base theme does not implement this style, but it is defined
    #             here since it has been a part of the framework before
    #             multiple themes were available. Use the constant provided by
    #             the theme you're using instead, e.g.
    #             {@link Reindeer#PANEL_LIGHT} or {@link Runo#PANEL_LIGHT}.
    PANEL_LIGHT = 'light'
