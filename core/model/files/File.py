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

    def get_data(self):
        lat = self.lat_col
        lon = self.lon_col
        df = pd.read_csv(self.doc, error_bad_lines=False)
        df[lon] = df[lon].replace(r'\s+', np.nan, regex=True)
        df[lon] = df[lon].replace(r'^$', np.nan, regex=True)
        df[lon] = df[lon].fillna(-0.99999)
        df[lon] = pd.to_numeric(df[lon])
        df[lat] = df[lat].replace(r'\s+', np.nan, regex=True)
        df[lat] = df[lat].replace(r'^$', np.nan, regex=True)
        df[lat] = df[lat].fillna(-0.99999)
        df[lat] = pd.to_numeric(df[lat])

        df = df.to_json(orient='index')
        return json.loads(df)

    def get_cols(self):
        df = pd.read_csv(self.doc, error_bad_lines=False)
        return list(df.columns.values)
