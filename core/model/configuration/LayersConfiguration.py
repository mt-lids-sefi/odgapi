from django.db import models
from picklefield import PickledObjectField

from core.model.configuration.Configuration import Configuration
from core.model.files.GeoDataSource import GeoDataSource


class LayersConfiguration(Configuration):

    ds_a = models.ForeignKey(GeoDataSource, on_delete=models.CASCADE, related_name='+', null=True)
    ds_b = models.ForeignKey(GeoDataSource, on_delete=models.CASCADE, related_name='+', null=True)
    popup_data = PickledObjectField(null=True)
    colours = PickledObjectField(null=True)


    def __init__(self, name, description, pk_a, pk_b, popup, colours):
        super().__init__()
        self.ds_a = pk_a
        self.ds_b = pk_b
        self.set_colours(colours)
        self.set_popup_data(popup)
        self.set_name(name)
        self.set_description(description)

    def set_colours(self, colours):
        self.colours = colours

    def set_popup_data(self, popup_data):
        self.popup_data = popup_data

