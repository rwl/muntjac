
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

from muntjac.ui.table import Table
from muntjac.event.dd.drop_handler import IDropHandler

from muntjac.event.dd.acceptcriteria.server_side_criterion import \
    ServerSideCriterion


class DragDropServerValidation(Feature):

    def getSinceVersion(self):
        return Version.V63


    def getDescription(self):
        return ('In more complex cases, the browser might not have enough '
            'information to decide whether something can be dropped at a '
            'given location. In these cases, the drag mechanism can ask the '
            'server whether dropping an item at a particular location is '
            'allowed. Drag persons onto others with the same last name.')


    def getName(self):
        return 'Drop validation, server'


    def getRelatedAPI(self):
        return [
            APIResource(ServerSideCriterion),
            APIResource(Table),
            APIResource(IDropHandler)
        ]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.dragndrop.DragDropHtml5FromDesktop \
            import DragDropHtml5FromDesktop

        from muntjac.demo.sampler.features.dragndrop.DragDropTreeSorting import \
            DragDropTreeSorting

        from muntjac.demo.sampler.features.dragndrop.DragDropTableTree import \
            DragDropTableTree

        from muntjac.demo.sampler.features.dragndrop.DragDropRearrangeComponents \
            import DragDropRearrangeComponents

        return [
            DragDropTreeSorting,
            DragDropTableTree,
            DragDropRearrangeComponents,
            DragDropHtml5FromDesktop
        ]


    def getRelatedResources(self):
        return None
