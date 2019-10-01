
from picklefield.fields import PickledObjectField

from core.model.files.IFile import IFile


class LinkedFile(IFile):
    dataset = PickledObjectField(null=True)

    def set_data(self, data):
        self.dataset = data

    def get_data(self):
        pass
