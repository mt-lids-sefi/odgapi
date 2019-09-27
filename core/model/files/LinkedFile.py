
from picklefield.fields import PickledObjectField

from core.model.files.IFile import IFile

class LinkedFile(IFile):
    dataframe = PickledObjectField(null=True)

    def setData(self, data):
        self.dataframe = data
