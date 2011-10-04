# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.vaadin.Application import (Application,)
# from com.vaadin.terminal.SystemError import (SystemError,)
# from com.vaadin.ui.Label import (Label,)
# from com.vaadin.ui.Panel import (Panel,)
# from java.io.File import (File,)


class SampleDirectory(object):
    """Provides sample directory based on application directory. If this fails then
    sampleDirectory property is read. If no sample directory is resolved, then a
    panel displaying error message is added to main window.

    @author IT Mill Ltd.
    """

    @classmethod
    def getDirectory(cls, application):
        """Get sample directory.

        @param application
        @return file pointing to sample directory
        """
        errorMessage = 'Access to application ' + 'context base directory failed, ' + 'possible security constraint with Application ' + 'Server or Servlet Container.<br />'
        file = application.getContext().getBaseDirectory()
        if (
            ((file is None) or (not file.canRead())) or (file.getAbsolutePath() is None)
        ):
            # cannot access example directory, possible security issue with
            # Application Server or Servlet Container
            # Try to read sample directory from web.xml parameter
            if application.getProperty('sampleDirectory') is not None:
                file = File(application.getProperty('sampleDirectory'))
                if file is not None and file.canRead() and file.getAbsolutePath() is not None:
                    # Success using property
                    return file
                # Failure using property
                errorMessage += 'Failed also to access sample directory <b>[' + application.getProperty('sampleDirectory') + ']</b> defined in <b>sampleDirectory property</b>.'
            else:
                # Failure using application context base dir, no property set
                errorMessage += '<b>Note: </b>You can set this manually in ' + 'web.xml by defining ' + 'sampleDirectory property.'
        else:
            # Success using application context base dir
            return file
        # Add failure notification as an Panel to main window
        errorPanel = Panel('Demo application error')
        errorPanel.setStyleName('strong')
        errorPanel.setComponentError(SystemError('Cannot provide sample directory'))
        errorPanel.addComponent(Label(errorMessage, Label.CONTENT_XHTML))
        # Remove all components from applications main window
        application.getMainWindow().getContent().removeAllComponents()
        # Add error panel
        application.getMainWindow().getContent().addComponent(errorPanel)
        return None
