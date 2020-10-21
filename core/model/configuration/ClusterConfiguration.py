from django.db import models
from picklefield import PickledObjectField

from core.model.configuration.Configuration import Configuration
from core.model.files.GeoDataSource import GeoDataSource


class ClusterConfiguration(Configuration):
    cluster_strategy = PickledObjectField(null=True)
    ds = models.ForeignKey(GeoDataSource, on_delete=models.CASCADE, related_name='+', null=True)
    col_a = models.CharField(max_length=50, null=True)
    col_b = models.CharField(max_length=50, null=True)
    centroids = PickledObjectField(null=True)
    labels = PickledObjectField(null=True)

    def set_strategy(self, strategy):
        self.cluster_strategy = strategy

    def set_ds(self, ds):
        self.ds = ds

    def set_cols(self, col_a, col_b):
        self.col_a = col_a
        self.col_b = col_b

    def get_col_a(self):
        return self.col_a

    def get_col_b(self):
        return self.col_b

    def get_strategy(self):
        return self.cluster_strategy.get_details()

    def get_ds(self):
        return self.ds

    def get_centroids(self):
        return self.centroids

    def get_labels(self):
        return self.labels

# en este caso, el resultado de apply será el de aplicar el algoritmo elegido sobre el ds
# guardado y devolver la info para mostrar los datos en el front --> visualización
    def apply(self):
        pass

    def clusterize(self):
        results = self.cluster_strategy.clusterize(self.ds, self.col_a, self.col_b)
        self.centroids = results[0]
        self.labels = results[1]




