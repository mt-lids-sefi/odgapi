from django.shortcuts import get_object_or_404

from core.model.clusterizer.KMeansStrategy import KMeansStrategy
from core.model.clusterizer.MeanShiftStrategy import MeanShiftStrategy
from core.model.configuration.ClusterConfiguration import ClusterConfiguration
from core.model.files.IDataSource import IDataSource
from core.model.files.GeoLinkedFile import GeoLinkedFile
from core.model.linker.ClosestPoint import ClosestPoint
from core.model.linker.Polygon import Polygon


class App:

    @staticmethod
    def get_files():
        return IDataSource.objects.all()

    #TBA para visualizaciones!
    def get_configurations(self):
        pass

    '''return a datasource as object to be used'''
    @staticmethod
    def get_ds(pk):
        return get_object_or_404(IDataSource, id=pk)

    @staticmethod
    def save_linked_file(pk_a, pk_b, link_strategy, name, description):
        ds_a = App.get_ds(pk_a)
        ds_b = App.get_ds(pk_b)
        linked_file = GeoLinkedFile()
        linked_file.set_lstrategy(link_strategy)
        linked_file.set_latlng_cols(ds_a.lat_col, ds_a.lon_col)
        linked_file.set_sources(ds_a, ds_b)
        linked_file.set_name(name)
        linked_file.set_description(description)
        linked_file.link()

        # save the linkedfile
        linked_file.save()

        return linked_file

    @staticmethod
    def link_closest_points(pk_a, pk_b,  name, description, params):
        link_strategy = ClosestPoint(params)
        return App.save_linked_file(pk_a, pk_b, link_strategy, name, description)

    @staticmethod
    def link_polygon(pk_a, pk_b,  name, description, params):
        link_strategy = Polygon(params)
        return App.save_linked_file(pk_a, pk_b, link_strategy, name, description)

    @staticmethod
    def link_files_closest_point_preview(pk_a, pk_b, params):
        link_strategy = ClosestPoint(params)
        ds_a = App.get_ds(pk_a)
        ds_b = App.get_ds(pk_b)
        dataset = link_strategy.link(ds_a, ds_b)
        return dataset

    @staticmethod
    def link_files_polygon_preview(pk_a, pk_b, params):
        link_strategy = Polygon(params)
        ds_a = App.get_ds(pk_a)
        ds_b = App.get_ds(pk_b)
        dataset = link_strategy.link(ds_a, ds_b)
        return dataset

    @staticmethod
    def clusterize(name, description, ids_pk, cluster_strategy, col_a, col_b):
        ids = App.get_ds(ids_pk)
        conf = ClusterConfiguration()
        conf.set_name(name)
        conf.set_description(description)
        conf.set_cols(col_a, col_b)
        conf.set_strategy(cluster_strategy)
        conf.set_ds(ids)
        conf.clusterize()

        conf.save()

        return conf


    @staticmethod
    def clusterize_meanshift_preview(ids, col_a, col_b):
        meanshift_strategy = MeanShiftStrategy()
        source = App.get_ds(ids)
        results = meanshift_strategy.clusterize(source, col_a, col_b)
        return results

    @staticmethod
    def clusterize_kmeans_preview(ids, col_a, col_b, k):
        params = {'k': k}
        kmeans_strategy = KMeansStrategy(params)
        source = App.get_ds(ids)
        results = kmeans_strategy.clusterize(source, col_a, col_b)
        return results
