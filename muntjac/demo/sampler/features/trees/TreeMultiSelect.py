
from muntjac.ui.tree import Tree

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TreeMultiSelect(Feature):

    def getSinceVersion(self):
        return Version.V64


    def getName(self):
        return 'Tree, multiple selection'


    def getDescription(self):
        return ('In this example, you can select multiple tree nodes'
            ' and delete the selected items.<br/>'
            'You can select multiple nodes by holding down the Ctrl(or Meta) '
            'key and selecting the items.<br/> A range of items can be '
            'selected by first selecting a start item for the range and then,'
            ' by holding down the shift key, selecting the end item for the '
            'range.<br/>'
            'Finally, several ranges can be selected by first selecting one '
            'range as described previously and then select a new starting '
            'point using the ctrl key and the new ending point using '
            'ctrl+shift key combination.')


    def getRelatedAPI(self):
        return [APIResource(Tree)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.trees.TreeMouseEvents import TreeMouseEvents
        from muntjac.demo.sampler.features.trees.TreeSingleSelect import TreeSingleSelect
        from muntjac.demo.sampler.features.trees.TreeActions import TreeActions

        return [TreeSingleSelect, TreeActions, TreeMouseEvents]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
