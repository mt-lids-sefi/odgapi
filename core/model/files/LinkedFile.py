from django.db import models
from picklefield import PickledObjectField

from core.model.files.IDataSource import IDataSource


class LinkedFile(IDataSource):
    sourceA = models.ForeignKey(IDataSource, on_delete=models.CASCADE, related_name='+', null=True)
    sourceB = models.ForeignKey(IDataSource, on_delete=models.CASCADE, related_name='+', null=True)
    link_strategy = PickledObjectField(null=True)
    #dataset es el linkeddata

    # def __init__(self):
    #     super().__init__()
    #     self.set_name()

    def set_data(self, data):
        self.dataset = data

    def get_data(self):
        return self.dataset

    def set_latlng_cols(self, lat, lon):
        self.lat_col = lat
        self.lon_col = lon

    def set_name(self):
        self.name = self.sourceA.get_name()+self.sourceB.get_name()

    def set_lstrategy(self, strategy):
        self.link_strategy = strategy

    def set_sources(self, sa, sb):
        self.sourceA = sa
        self.sourceB = sb
        self.set_name()

    def link(self):
        self.dataset = self.link_strategy.link(self.sourceA, self.sourceB)
