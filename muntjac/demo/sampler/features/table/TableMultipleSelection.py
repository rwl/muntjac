# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.table.TableMainFeaturesExample import (TableMainFeaturesExample,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TableMultipleSelection(Feature):

    def getDescription(self):
        return 'When the table is in multiselect mode you can use the Ctrl (or Meta key) to select or unselect multiple items.' + 'You can also use the Shift key to select a range of items and Ctrl+Shift key to select multiple ranges.'

    def getName(self):
        return 'Table, multiple selection'

    def getRelatedAPI(self):
        return [APIResource(Table)]

    def getRelatedFeatures(self):
        return [FeatureSet.Tables]

    def getRelatedResources(self):
        return None

    def getSinceVersion(self):
        return Version.V64

    def getExample(self):
        return TableMainFeaturesExample()
