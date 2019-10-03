from abc import abstractmethod
from django.db import models
from polymorphic.models import PolymorphicModel
from picklefield.fields import PickledObjectField


class IDataSource(PolymorphicModel):
    description = models.TextField(max_length=255, blank=True, verbose_name='Descripción')
    name = models.CharField(max_length=128, blank=True, verbose_name='Nombre')
    lat_col = models.CharField(max_length=50, null=True)
    lon_col = models.CharField(max_length=50, null=True)
    dataset = PickledObjectField(null=True)


    @abstractmethod
    def get_data(self):
        pass

    def get_cols(self):
        return list(self.dataset.columns.values)
