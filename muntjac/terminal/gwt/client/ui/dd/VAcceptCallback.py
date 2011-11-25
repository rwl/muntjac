# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class VAcceptCallback(object):

    def accepted(self, event):
        """This method is called by {@link VDragAndDropManager} if the
        {@link VDragEvent} is still active. Developer can update for example drag
        icon or empahsis the target if the target accepts the transferable. If
        the drag and drop operation ends or the {@link VAbstractDropHandler} has
        changed before response arrives, the method is never called.
        """
        pass
