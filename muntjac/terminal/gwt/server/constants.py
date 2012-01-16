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
    DEFAULT_WIDGETSET = 'org.muntiacus.MuntjacWidgetSet'

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
