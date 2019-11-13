from django.db import models

from core.model.files.IDataSource import IDataSource


class GeoDataSource(IDataSource):
    lat_col = models.CharField(max_length=50, null=True)
    lon_col = models.CharField(max_length=50, null=True)

    def set_lat(self, lat):
        self.lat_col = lat

    def set_lon(self, lon):
        self.lon_col = lon

    def set_latlng_cols(self, lat, lon):
        self.lat_col = lat
        self.lon_col = lon

    def get_lat_col(self):
        return self.lat_col

    def get_lon_col(self):
        return self.lon_col
