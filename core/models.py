from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class File(models.Model):
    description = models.TextField(max_length=255, blank=True, verbose_name='Descripción')
    name = models.CharField(max_length=128, blank=True, verbose_name='Nombre')
    file = models.FileField(upload_to='files/', verbose_name='Archivo',  validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    document_id = models.AutoField(primary_key=True)
    lat_col= models.CharField(max_length=50, null=True, choices={})
    lon_col = models.CharField(max_length=50, null=True, choices={})