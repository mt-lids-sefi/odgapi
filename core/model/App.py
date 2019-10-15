from django.shortcuts import get_object_or_404

from core.model.files.IDataSource import IDataSource
from core.model.files.LinkedFile import LinkedFile


class App:

    @staticmethod
    def get_files():
        return IDataSource.objects.all()

    #TBA
    def get_configurations(self):
        pass

    '''return a datasource to be used'''
    @staticmethod
    def get_ds(pk):
        return get_object_or_404(IDataSource, id=pk)

    @staticmethod
    def link_files(pk_a, pk_b, link_strategy):
        ds_a = App.get_ds(pk_a)
        ds_b = App.get_ds(pk_b)
        linked_file = LinkedFile()
        linked_file.set_lstrategy(link_strategy)
        linked_file.set_latlng_cols(ds_a.lat_col, ds_a.lon_col)
        linked_file.set_sources(ds_a, ds_b)
        linked_file.link()

        # save the linkedfile
        linked_file.save()

        return linked_file
