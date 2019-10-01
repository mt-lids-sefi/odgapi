
from picklefield.fields import PickledObjectField

from core.model.files.IDataSource import IDataSource


class LinkedFile(IDataSource):
    dataset = PickledObjectField(null=True)

    def set_data(self, data):
        self.dataset = data

    def get_data(self):
        pass

    def get_cols(self):
        return list(self.dataset.columns.values)
