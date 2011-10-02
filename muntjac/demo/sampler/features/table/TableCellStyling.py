# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.table.TableStylingExample import (TableStylingExample,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TableCellStyling(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Table, styling cells'

    def getExample(self):
        return TableStylingExample()

    def getDescription(self):
        return 'Individual cells can be styled in a Table by using a' + ' CellStyleGenerator. Regular CSS is used to create the' + ' actual style.<br/>Double click a first or last name to' + ' mark/unmark that cell.'

    def getRelatedAPI(self):
        return [APIResource(Table)]

    def getRelatedFeatures(self):
        return [FeatureSet.Tables]

    def getRelatedResources(self):
        return None
