from django.db import models


class IFile(models.Model):
    description = models.TextField(max_length=255, blank=True, verbose_name='Descripción')
    name = models.CharField(max_length=128, blank=True, verbose_name='Nombre')
    document_id = models.AutoField(primary_key=True)
    lat_col = models.CharField(max_length=50, null=True)
    lon_col = models.CharField(max_length=50, null=True)

    class Meta:
        abstract = True
