from django.db import models
from django.core.validators import FileExtensionValidator
from picklefield.fields import PickledObjectField


# Create your models here.
# class IFile(models.Model):
#     description = models.TextField(max_length=255, blank=True, verbose_name='Descripción')
#     name = models.CharField(max_length=128, blank=True, verbose_name='Nombre')
#     document_id = models.AutoField(primary_key=True)
#     lat_col= models.CharField(max_length=50, null=True)
#     lon_col = models.CharField(max_length=50, null=True)
#
#     class Meta:
#         abstract = True
#
#
# class File (IFile):
#     doc = models.FileField(upload_to='files/', verbose_name='Archivo',
#                            validators=[FileExtensionValidator(allowed_extensions=['csv'])])
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#
#
# class LinkedFile(IFile):
#     dataframe = PickledObjectField(null=True)
#
#     def setData(self, data):
#         self.dataframe = data

