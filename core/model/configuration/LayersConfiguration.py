from django.db import models
from picklefield import PickledObjectField

from core.model.files.IDataSource import IDataSource


class LayersConfiguration:

    ds_a = models.ForeignKey(IDataSource, on_delete=models.CASCADE, related_name='+', null=True)
    ds_b = models.ForeignKey(IDataSource, on_delete=models.CASCADE, related_name='+', null=True)
    popup_data = PickledObjectField(null=True)
    colours = PickledObjectField(null=True)

    def __init__(self):
        pass
