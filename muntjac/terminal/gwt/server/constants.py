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


class Constants(object):

    NOT_PRODUCTION_MODE_INFO = ('\n'
        '=================================================================\n'
        'Muntjac is running in DEBUG MODE.\nAdd productionMode=true to INI '
        'to disable debug features.\nTo show debug window, add ?debug to '
        'your application URL.\n'
        '=================================================================')

    WARNING_XSRF_PROTECTION_DISABLED = ('\n'
        '===========================================================\n'
        'WARNING: Cross-site request forgery protection is disabled!\n'
        '===========================================================')

    WARNING_RESOURCE_CACHING_TIME_NOT_NUMERIC = ('\n'
        '===========================================================\n'
        'WARNING: resourceCacheTime has been set to a non integer value '
        'in INI. The default of 1h will be used.\n'
        '===========================================================')

    WIDGETSET_MISMATCH_INFO = ('\n'
        '=================================================================\n'
        'The widgetset in use does not seem to be built for the Muntjac\n'
        'version in use. This might cause strange problems - a\n'
        'recompile/deploy is strongly recommended.\n'
        ' Muntjac version: %s\n'
        ' Widgetset version: %s\n'
        '=================================================================')

    URL_PARAMETER_RESTART_APPLICATION = 'restartApplication'
    URL_PARAMETER_CLOSE_APPLICATION = 'closeApplication'
    URL_PARAMETER_REPAINT_ALL = 'repaintAll'
    URL_PARAMETER_THEME = 'theme'

    SERVLET_PARAMETER_DEBUG = 'Debug'
    SERVLET_PARAMETER_PRODUCTION_MODE = 'productionMode'
    SERVLET_PARAMETER_DISABLE_XSRF_PROTECTION = 'disable-xsrf-protection'
    SERVLET_PARAMETER_RESOURCE_CACHE_TIME = 'resourceCacheTime'

    # Configurable parameter names
    PARAMETER_VAADIN_RESOURCES = 'Resources'
    DEFAULT_BUFFER_SIZE = 32 * 1024
    MAX_BUFFER_SIZE = 64 * 1024
    AJAX_UIDL_URI = '/UIDL'
    THEME_DIRECTORY_PATH = 'VAADIN/themes/'
    DEFAULT_THEME_CACHETIME = 1000 * 60 * 60 * 24
    WIDGETSET_DIRECTORY_PATH = 'VAADIN/widgetsets/'

    # Name of the default widget set, used if not specified in INI
    DEFAULT_WIDGETSET = 'com.vaadin.terminal.gwt.DefaultWidgetSet'

    # Widget set parameter name
    PARAMETER_WIDGETSET = 'widgetset'
    ERROR_NO_WINDOW_FOUND = ('No window found. '
            'Did you remember to setMainWindow()?')
    DEFAULT_THEME_NAME = 'reindeer'
    INVALID_SECURITY_KEY_MSG = 'Invalid security key.'

    # portal configuration parameters
    PORTAL_PARAMETER_VAADIN_WIDGETSET = 'vaadin.widgetset'
    PORTAL_PARAMETER_VAADIN_RESOURCE_PATH = 'vaadin.resources.path'
    PORTAL_PARAMETER_VAADIN_THEME = 'vaadin.theme'
