from django.db import models
from polymorphic.models import PolymorphicModel
from picklefield.fields import PickledObjectField


class IDataSource(PolymorphicModel):
    description = models.TextField(max_length=255, blank=True, verbose_name='Descripción')
    name = models.CharField(max_length=128, blank=True, verbose_name='Nombre')
    dataset = PickledObjectField(null=True)

    def get_data(self):
        return self.dataset

    def get_cols(self):
        return list(self.dataset.columns.values)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_data(self, data):
        self.dataset = data

    def get_id(self):
        return self.id

    def get_details(self):
        return {'name': self.name, 'description': self.description}
