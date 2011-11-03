
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

from muntjac.ui.html5_file import Html5File
from muntjac.event.dd.drop_handler import IDropHandler

from muntjac.ui.drag_and_drop_wrapper import \
    DragAndDropWrapper, WrapperTransferable


class DragDropHtml5FromDesktop(Feature):

    def getSinceVersion(self):
        return Version.V63


    def getDescription(self):
        return ('On browsers supporting HTML5 style drag and drop several '
            'data flovours can be dropped from desktop applications to '
            'Muntjac application. Firefox from version 3.6 even support '
            'dragging files from the client file system to a Muntjac '
            'application. With Firefox, try dropping an image file from '
            'the desktop to the drop box, else you must retain to dragging '
            'text from your favorite word processor. ')


    def getName(self):
        return 'Drag from desktop applications'


    def getRelatedAPI(self):
        return [
            APIResource(DragAndDropWrapper),
            APIResource(WrapperTransferable),
            APIResource(Html5File),
            APIResource(IDropHandler)
        ]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.dragndrop.DragDropTreeSorting import \
            DragDropTreeSorting

        from muntjac.demo.sampler.features.dragndrop.DragDropTableTree import \
            DragDropTableTree

        from muntjac.demo.sampler.features.dragndrop.DragDropServerValidation import \
            DragDropServerValidation

        from muntjac.demo.sampler.features.dragndrop.DragDropRearrangeComponents \
            import DragDropRearrangeComponents

        return [
            DragDropTreeSorting,
            DragDropTableTree,
            DragDropServerValidation,
            DragDropRearrangeComponents
        ]


    def getRelatedResources(self):
        return None
