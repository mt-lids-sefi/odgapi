from django.db import models
from core.model.files.IDataSource import IDataSource


class LinkedFile(IDataSource):
    sourceA = models.ForeignKey(IDataSource, on_delete=models.CASCADE, related_name='+', null=True)
    sourceB = models.ForeignKey(IDataSource, on_delete=models.CASCADE, related_name='+', null=True)

    def set_data(self, data):
        self.dataset = data

    def get_data(self):
        pass
