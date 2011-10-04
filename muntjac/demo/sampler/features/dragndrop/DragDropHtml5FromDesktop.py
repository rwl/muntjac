# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.dragndrop.DragDropTreeSorting import (DragDropTreeSorting,)
from muntjac.demo.sampler.features.dragndrop.DragDropTableTree import (DragDropTableTree,)
from muntjac.demo.sampler.features.dragndrop.DragDropServerValidation import (DragDropServerValidation,)
from muntjac.demo.sampler.features.dragndrop.DragDropRearrangeComponents import (DragDropRearrangeComponents,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
# from com.vaadin.ui.DragAndDropWrapper import (DragAndDropWrapper,)
# from com.vaadin.ui.DragAndDropWrapper.WrapperTransferable import (WrapperTransferable,)
# from com.vaadin.ui.Html5File import (Html5File,)
Version = Feature.Version


class DragDropHtml5FromDesktop(Feature):

    def getSinceVersion(self):
        return Version.V63

    def getDescription(self):
        return 'On browsers supporting HTML5 style drag and drop several data flovours can ' + 'be dropped from desktop applications to Vaadin application. Firefox from version 3.6 even ' + 'support dragging files from the client file system to a Vaadin application. ' + 'With Firefox, try dropping an image file from the desktop to the drop box, else you ' + 'must retain to dragging text from your favorite word processor. '

    def getName(self):
        return 'Drag from desktop applications'

    def getRelatedAPI(self):
        return [APIResource(DragAndDropWrapper), APIResource(WrapperTransferable), APIResource(Html5File), APIResource(DropHandler)]

    def getRelatedFeatures(self):
        return [DragDropTreeSorting, DragDropTableTree, DragDropServerValidation, DragDropRearrangeComponents]

    def getRelatedResources(self):
        return None
