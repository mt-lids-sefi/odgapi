from django.shortcuts import get_object_or_404
from core.model.clusterizer.KMeansStrategy import KMeansStrategy
from core.model.clusterizer.MeanShiftStrategy import MeanShiftStrategy
from core.model.configuration.LayersConfiguration import LayersConfiguration
from core.model.configuration.ClusterConfiguration import ClusterConfiguration
from core.model.configuration.Configuration import Configuration
from core.model.files.DataFile import DataFile
from core.model.files.GeoDataSource import GeoDataSource
from core.model.files.IDataSource import IDataSource
from core.model.files.GeoLinkedFile import GeoLinkedFile
from core.model.linker.ClosestPoint import ClosestPoint
from core.model.linker.Polygon import Polygon
from core.model.linker.Rule import Rule
from core.model.linker.Similarity import Similarity
import json

class App:

    @staticmethod
    def get_files():
        return IDataSource.objects.all()

    @staticmethod
    def get_geo_files():
        return GeoDataSource.objects.all()

    @staticmethod
    def get_data_files():
        return DataFile.objects.all()

    @staticmethod
    def get_configurations():
        return Configuration.objects.all()

    '''return a datasource as object to be used'''
    @staticmethod
    def get_ds(pk):
        return get_object_or_404(IDataSource, id=pk)

    @staticmethod
    def get_data_file(pk):
        return get_object_or_404(DataFile, id=pk)

    @staticmethod
    def get_geo_file(pk):
        return get_object_or_404(GeoDataSource, id=pk)

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
    def link_similarity(pk_a, pk_b, name, description, params):
        rules = App.make_rules(params)
        prms = {'rules': rules}
        link_strategy = Similarity(prms)
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
    def link_files_similarity_preview(ids_a, ids_b, params):
        rules = App.make_rules(params)
        ds_a = App.get_ds(ids_a)
        ds_b = App.get_ds(ids_b)
        prms = {'rules': rules}
        link_strategy = Similarity(prms)
        dataset = link_strategy.link(ds_a, ds_b)
        return dataset

    @staticmethod
    def save_cluster_configuration(name, description, ids_pk, col_a, col_b, cluster_startegy):
        ids = App.get_ds(ids_pk)
        conf = ClusterConfiguration()
        conf.set_name(name)
        conf.set_description(description)
        conf.set_cols(col_a, col_b)
        conf.set_strategy(cluster_startegy)
        conf.set_ds(ids)
        conf.clusterize()

        conf.save()

        return conf

    @staticmethod
    def clusterize_meanshift(name, description, ids_pk,  col_a, col_b):
        meanshift_strategy = MeanShiftStrategy()
        conf = App.save_cluster_configuration(name, description, ids_pk, col_a, col_b, meanshift_strategy)
        return conf

    @staticmethod
    def clusterize_kmeans(name, description, ids_pk, col_a, col_b, k):
        params = {'k': k}
        kmeans_strategy = KMeansStrategy(params)
        conf = App.save_cluster_configuration(name, description, ids_pk, col_a, col_b, kmeans_strategy)
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

    @staticmethod
    def make_rules(json_rules):
        rules = []
        for r in json_rules['rules']:
            matches = []
            for m in r['matches']:
                matches.append(m)
            rule = Rule(r['col_a'], r['col_b'], matches)
            rules.append(rule)
        return rules

    @staticmethod
    def make_response_link(results):
        cols = results.columns.values
        data_preview = results.to_json(orient='index')
        data = json.loads(data_preview)
        return [data, cols]

    @staticmethod
    def make_response_cluster(results):
        [centroids, labels, dataset, cats] = results
        cluster_size = len(centroids)
        data = dataset.to_json(orient='index')
        data = json.loads(data)
        return [centroids, labels, data, cluster_size, cats]

    @staticmethod
    def save_layers_configuration(pk_a, pk_b, popup_data, colours, name, description):
        id_a = App.get_ds(pk_a)
        id_b = App.get_ds(pk_b)
        conf = LayersConfiguration(name, description, id_a, id_b, popup_data,colours)
        conf.save()
        pass


