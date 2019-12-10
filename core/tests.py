import pandas as pd
from django.test import TestCase
import numpy as np

# Create your tests here.
from core.model.files.GeoFile import GeoFile


class GeoFileTest(TestCase):

    def setUp(self):
        self.gf = GeoFile.objects.create(name='geofile test', description='description', lat_col='latitude', lon_col='longitude', doc='files/GeoVin_sample.csv')

    def tearDown(self):
        self.gf.delete()

    def test_name_desc(self):
        self.assertEqual(self.gf.name, 'geofile test')
        self.assertEqual(self.gf.description, 'description')

    def test_dataset(self):
        lat = self.gf.lat_col
        lon = self.gf.lon_col
        df = pd.read_csv('media/files/GeoVin_sample.csv', error_bad_lines=False)
        df[lon] = df[lon].replace(r'\s+', np.nan, regex=True)
        df[lon] = df[lon].replace(r'^$', np.nan, regex=True)
        df[lon] = df[lon].fillna(-0.99999)
        df[lon] = pd.to_numeric(df[lon])
        df[lat] = df[lat].replace(r'\s+', np.nan, regex=True)
        df[lat] = df[lat].replace(r'^$', np.nan, regex=True)
        df[lat] = df[lat].fillna(-0.99999)
        df[lat] = pd.to_numeric(df[lat])
        self.assertEqual(self.gf.dataset, df)