from core.model.files.IFile import IFile
from django.db import models
from django.core.validators import FileExtensionValidator


class File (IFile):
    doc = models.FileField(upload_to='files/', verbose_name='Archivo',
                           validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)


def get_data():
    pass


