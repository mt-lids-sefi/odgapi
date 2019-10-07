from core.model.files.IDataSource import IDataSource
from django.db import models
from django.core.validators import FileExtensionValidator
import pandas as pd
import numpy as np
import json


class File (IDataSource):
    doc = models.FileField(upload_to='files/', verbose_name='Archivo',
                           validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # def create(cls, name, description, lat_col, lon_col, doc):
    #     dataset = pd.read_csv(doc, error_bad_lines=False)
    #     print(dataset)
    #     file = cls(name=name, description=description, lat_col=lat_col, lon_col=lon_col, doc=doc, dataset=dataset)
    #     return file

    def save(self, *args, **kwargs):
        dataset = pd.read_csv(self.doc, error_bad_lines=False)
        self.dataset = dataset
        super().save(*args, **kwargs)  # Call the "real" save() method.

    '''cleans the data and returns the dataset'''
    def get_data(self):
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
        return df
        # df = df.to_json(orient='index')
        # return json.loads(df)