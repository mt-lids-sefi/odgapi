from django.db import models
from picklefield import PickledObjectField

from core.model.files.GeoDataSource import GeoDataSource
from core.model.files.IDataSource import IDataSource


class GeoLinkedFile(GeoDataSource):
    source_a = models.ForeignKey(IDataSource, on_delete=models.CASCADE, related_name='+', null=True)
    source_b = models.ForeignKey(IDataSource, on_delete=models.CASCADE, related_name='+', null=True)
    link_strategy = PickledObjectField(null=True)

    def set_def_name(self):
        self.name = self.source_a.get_name() + self.source_b.get_name()

    def set_lstrategy(self, strategy):
        self.link_strategy = strategy

    def set_sources(self, sa, sb):
        self.source_a = sa
        self.source_b = sb

    def link(self):
        self.dataset = self.link_strategy.link(self.source_a, self.source_b)
