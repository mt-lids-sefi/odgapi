import pandas as pd
from django.test import TestCase
import numpy as np

# Create your tests here.
from core.model.App import App
from core.model.clusterizer.Categorizer import Categorizer
from core.model.clusterizer.MeanShiftStrategy import MeanShiftStrategy
from core.model.files.DataFile import DataFile
from core.model.files.GeoFile import GeoFile
from core.model.linker.ClosestPoint import ClosestPoint
from core.model.linker.Polygon import Polygon


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

    def test_closest_point(self):
        params = {'distance': 0, 'filter': False}
        link_strategy = ClosestPoint(params)
        ds_a = App.get_ds(self.gf1.get_id())
        ds_b = App.get_ds(self.gf2.get_id())
        dataset = link_strategy.link(ds_a, ds_b)
        linked_file = App.link_closest_points(self.gf1.get_id(), self.gf2.get_id(), "name", "description", params)
        dataset_linked = linked_file.get_data()
        pd.testing.assert_frame_equal(dataset, dataset_linked)

    def test_polygon(self):
        params = {'distance': 3000}
        link_strategy = Polygon(params)
        ds_a = App.get_ds(self.gf1.get_id())
        ds_b = App.get_ds(self.gf2.get_id())
        dataset = link_strategy.link(ds_a, ds_b)
        linked_file = App.link_polygon(self.gf1.get_id(), self.gf2.get_id(), "name", "description", params)
        dataset_linked = linked_file.get_data()
        pd.testing.assert_frame_equal(dataset, dataset_linked)


class PolygonTest(TestCase):

    def setUp(self):
        self.gf1 = GeoFile.objects.create(name='geofile test', description='description', lat_col='latitude', lon_col='longitude', doc='test_files/GeoVin_sample.csv')
        self.gf2 = GeoFile.objects.create(name='dataunq test', description='description', lat_col='lat', lon_col='lon', doc='test_files/data_unq_sample.csv')

    def tearDown(self):
        self.gf1.delete()
        self.gf2.delete()

    def test_empty_polygon(self):
        params = {'distance': 3}
        link_strategy = Polygon(params)
        ds_a = App.get_ds(self.gf1.get_id())
        ds_b = App.get_ds(self.gf2.get_id())
        dataset = link_strategy.link(ds_a, ds_b)
        self.assertEqual(dataset.size, 0)

    def test_polygon_lenght(self):
        params = {'distance': 3000}
        link_strategy = Polygon(params)
        ds_a = App.get_ds(self.gf1.get_id())
        ds_b = App.get_ds(self.gf2.get_id())
        dataset = link_strategy.link(ds_a, ds_b)
        self.assertEqual(len(dataset.index), 9)


class ClosestPointTest(TestCase):

    def setUp(self):
        self.gf1 = GeoFile.objects.create(name='geofile test', description='description', lat_col='latitude', lon_col='longitude', doc='test_files/GeoVin_sample.csv')
        self.gf2 = GeoFile.objects.create(name='dataunq test', description='description', lat_col='lat', lon_col='lon', doc='test_files/data_unq_sample.csv')

    def tearDown(self):
        self.gf1.delete()
        self.gf2.delete()

    def test_empty_closest_point(self):
        params = {'filter': True, 'distance': 3}
        link_strategy = ClosestPoint(params)
        ds_a = App.get_ds(self.gf1.get_id())
        ds_b = App.get_ds(self.gf2.get_id())
        dataset = link_strategy.link(ds_a, ds_b)
        self.assertEqual(dataset.size, 0)

    def test_closest_point_lenght_filter(self):
        params = {'filter': True, 'distance': 3000}
        link_strategy = ClosestPoint(params)
        ds_a = App.get_ds(self.gf1.get_id())
        ds_b = App.get_ds(self.gf2.get_id())
        dataset = link_strategy.link(ds_a, ds_b)
        self.assertEqual(len(dataset.index), 3)

    def test_closest_point_lenght_no_filter(self):
        params = {'filter': False, 'distance': 0}
        link_strategy = ClosestPoint(params)
        ds_a = App.get_ds(self.gf1.get_id())
        ds_b = App.get_ds(self.gf2.get_id())
        dataset = link_strategy.link(ds_a, ds_b)
        self.assertEqual(len(dataset.index), 3)

class CategorizerTest(TestCase):
    def setUp(self):
        self.gf2 = GeoFile.objects.create(name='dataunq test', description='description', lat_col='lat', lon_col='lon', doc='test_files/data_unq_sample.csv')

    def tearDown(self):
        self.gf2.delete()

    def test_categorize_column_long(self):
        dataset = App.get_ds(self.gf2.get_id()).get_data()
        cat_col = Categorizer.categorize_column(dataset, 'p1')
        uncat_col = dataset[['p1']]
        self.assertEqual(len(cat_col), len(uncat_col))

    def test_categorize_uncategorize_values(self):
        dataset = App.get_ds(self.gf2.get_id()).get_data()
        cat_col = Categorizer.categorize_column(dataset, 'p1')
        dataset['p1_cat'] = cat_col
        cat_value = dataset.iloc[0]['p1_cat']
        real_value = dataset.iloc[0]['p1']
        uncat_value = Categorizer.uncategorize_value(dataset, 'p1', cat_value)
        self.assertEqual(real_value, uncat_value)
