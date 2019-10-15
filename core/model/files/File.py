from core.model.files.IDataSource import IDataSource
from django.db import models
from django.core.validators import FileExtensionValidator
import pandas as pd
import numpy as np


class File (IDataSource):
    doc = models.FileField(upload_to='files/', verbose_name='Archivo',
                           validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        dataset = pd.read_csv(self.doc, error_bad_lines=False)
        self.dataset = dataset
        self.clean_data()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    '''cleans the data and saves it again in the dataset field'''
    def clean_data(self):
        lat = self.lat_col
        lon = self.lon_col
        df = self.dataset
        df[lon] = df[lon].replace(r'\s+', np.nan, regex=True)
        df[lon] = df[lon].replace(r'^$', np.nan, regex=True)
        df[lon] = df[lon].fillna(-0.99999)
        df[lon] = pd.to_numeric(df[lon])
        df[lat] = df[lat].replace(r'\s+', np.nan, regex=True)
        df[lat] = df[lat].replace(r'^$', np.nan, regex=True)
        df[lat] = df[lat].fillna(-0.99999)
        df[lat] = pd.to_numeric(df[lat])
        self.dataset = df

    '''returns the dataset'''
    def get_data(self):
        return self.dataset
