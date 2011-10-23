
from muntjac.ui.drag_and_drop_wrapper import DragAndDropWrapper
from muntjac.event.dd.drop_handler import IDropHandler

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class DragDropRearrangeComponents(Feature):

    def getSinceVersion(self):
        return Version.V63


    def getDescription(self):
        return ('In addition to arbitrary data items, whole components can '
            'also be dragged. ' + 'Here, the order of various components in '
            'a layout can be rearranged by dragging the components.')


    def getName(self):
        return 'Drag components'


    def getRelatedAPI(self):
        return [APIResource(DragAndDropWrapper), APIResource(IDropHandler)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.dragndrop.DragDropHtml5FromDesktop import \
            DragDropHtml5FromDesktop

        from muntjac.demo.sampler.features.dragndrop.DragDropTreeSorting import \
            DragDropTreeSorting

        from muntjac.demo.sampler.features.dragndrop.DragDropTableTree import \
            DragDropTableTree

        from muntjac.demo.sampler.features.dragndrop.DragDropServerValidation import \
            DragDropServerValidation

        return [
            DragDropTreeSorting,
            DragDropTableTree,
            DragDropServerValidation,
            DragDropHtml5FromDesktop
        ]


    def getRelatedResources(self):
        return None
