from csv import reader
from io import StringIO

from django.test import TestCase


# Create your tests here.
from core.model.files.GeoFile import GeoFile


class GeoFileTest(TestCase):

    def setUp(self):

        self.geofile = GeoFile.objects.create(name='geofile test', description='description', lat_col='latitude', lon_col='longitude', doc='files/GeoVin_sample.csv')
        self.geofile.save()

    def tearDown(self):
        self.geofile.delete()

    def test_name_desc(self):
        self.assertEqual(self.geofile.name, 'geofile test')
