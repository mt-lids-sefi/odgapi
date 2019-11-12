from django.db import models
from picklefield import PickledObjectField

from core.model.configuration.Configuration import Configuration
from core.model.files.GeoDataSource import GeoDataSource


class LayersConfiguration(Configuration):

    ds_a = models.ForeignKey(GeoDataSource, on_delete=models.CASCADE, related_name='+', null=True)
    ds_b = models.ForeignKey(GeoDataSource, on_delete=models.CASCADE, related_name='+', null=True)
    popup_data = PickledObjectField(null=True)
    colours = PickledObjectField(null=True)

    def set_colours(self, colours):
        self.colours = colours
