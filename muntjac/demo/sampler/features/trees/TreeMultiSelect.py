# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.trees.TreeMouseEvents import (TreeMouseEvents,)
from com.vaadin.demo.sampler.features.trees.TreeSingleSelect import (TreeSingleSelect,)
from com.vaadin.demo.sampler.features.trees.TreeActions import (TreeActions,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TreeMultiSelect(Feature):

    def getSinceVersion(self):
        return Version.V64

    def getName(self):
        return 'Tree, multiple selection'

    def getDescription(self):
        return 'In this example, you can select multiple tree nodes' + ' and delete the selected items. <br/>You can select multiple nodes by holding down the Ctrl(or Meta) key' + ' and selecting the items.<br/> A range of items can be selected by first selecting a start item for the range and then,' + ' by holding down the shift key, selecting the end item for the range. <br/>Finally, several ranges can be selected' + ' by first selecting one range as described previously and then select a new starting point using the ctrl key' + ' and the new ending point using ctrl+shift key combination.'

    def getRelatedAPI(self):
        return [APIResource(Tree)]

    def getRelatedFeatures(self):
        return [TreeSingleSelect, TreeActions, TreeMouseEvents]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None