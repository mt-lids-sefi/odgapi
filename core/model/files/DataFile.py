from django.core.validators import FileExtensionValidator
from django.db import models
from core.model.files.IDataSource import IDataSource


class DataFile(IDataSource):
    doc = models.FileField(upload_to='files/', verbose_name='Archivo',
                           validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def set_doc(self, doc):
        self.doc = doc

