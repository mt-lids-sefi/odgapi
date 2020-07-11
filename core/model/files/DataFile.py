from django.core.validators import FileExtensionValidator
from django.db import models
from core.model.files.IDataSource import IDataSource
import pandas as pd

class DataFile(IDataSource):
    doc = models.FileField(upload_to='files/', verbose_name='Archivo',
                           validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        dataset = pd.read_csv(self.doc, error_bad_lines=False)
        self.dataset = dataset
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def set_doc(self, doc):
        self.doc = doc

    def get_details(self):
        details = {'doc': self.doc.name, 'uploaded_at': self.uploaded_at.ctime()}
        details.update(super().get_details())
        return details
