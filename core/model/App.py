from django.shortcuts import get_object_or_404

from core.model.configuration.ClusterConfiguration import ClusterConfiguration
from core.model.files.IDataSource import IDataSource
from core.model.files.GeoLinkedFile import GeoLinkedFile


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
    def link_files(pk_a, pk_b, link_strategy, name, description):
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
    def link_files_preview(pk_a, pk_b, link_strategy):
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

        conf.save()

        return conf


    @staticmethod
    def clusterize_preview(ids, cluster_strategy, col_a, col_b):
        source = App.get_ds(ids)
        results = cluster_strategy.clusterize(source, col_a, col_b)
        return results
