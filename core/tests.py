import pandas as pd
from django.test import TestCase
import numpy as np

# Create your tests here.
from core.model.files.DataFile import DataFile
from core.model.files.GeoFile import GeoFile


class GeoFileTest(TestCase):

    def setUp(self):
        self.gf = GeoFile.objects.create(name='geofile test', description='description', lat_col='latitude', lon_col='longitude', doc='test_files/GeoVin_sample.csv')

    def tearDown(self):
        self.gf.delete()

    def test_atts(self):
        self.assertEqual(self.gf.name, 'geofile test')
        self.assertEqual(self.gf.description, 'description')

    def test_clean_dataset(self):
        lat = self.gf.lat_col
        lon = self.gf.lon_col
        df = pd.read_csv('media/test_files/GeoVin_sample.csv', error_bad_lines=False)
        df[lon] = df[lon].replace(r'\s+', np.nan, regex=True)
        df[lon] = df[lon].replace(r'^$', np.nan, regex=True)
        df[lon] = df[lon].fillna(-0.99999)
        df[lon] = pd.to_numeric(df[lon])
        df[lat] = df[lat].replace(r'\s+', np.nan, regex=True)
        df[lat] = df[lat].replace(r'^$', np.nan, regex=True)
        df[lat] = df[lat].fillna(-0.99999)
        df[lat] = pd.to_numeric(df[lat])
        pd.testing.assert_frame_equal(self.gf.dataset, df)

    def test_get_cols(self):
        df = pd.read_csv('media/test_files/GeoVin_sample.csv', error_bad_lines=False)
        cols = list(df.columns.values)
        self.assertEqual(self.gf.get_cols(), cols)


class DataFileTest(TestCase):

    def setUp(self):
        self.df = DataFile.objects.create(name='geofile test', description='description', doc='test_files/GeoVin_sample.csv')

    def tearDown(self):
        self.df.delete()

    def test_set_dataset(self):
        df = pd.read_csv('media/test_files/GeoVin_sample.csv', error_bad_lines=False)
        pd.testing.assert_frame_equal(self.df.get_data(), df)


class GeoDataSourceTest(TestCase):

    def setUp(self):
        self.gf = GeoFile.objects.create(name='geofile test', description='description', lat_col='latitude', lon_col='longitude', doc='test_files/GeoVin_sample.csv')

    def tearDown(self):
        self.gf.delete()

    def test_lat_lon_cols(self):
        self.assertEqual(self.gf.lat_col, 'latitude')
        self.assertEqual(self.gf.lon_col, 'longitude')


class GeoLinkedFileTest(TestCase):

    def setUp(self):
        self.gf1 = GeoFile.objects.create(name='geofile test', description='description', lat_col='latitude', lon_col='longitude', doc='test_files/GeoVin_sample.csv')
        self.gf2 = GeoFile.objects.create(name='dataunq test', description='description', lat_col='lat', lon_col='lon', doc='test_files/data_unq_sample.csv')

    def tearDown(self):
        self.gf1.delete()
        self.gf2.delete()

