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

    '''return a datasource as object to be used'''
    @staticmethod
    def get_ds(pk):
        return get_object_or_404(IDataSource, id=pk)

    @staticmethod
    def link_files(pk_a, pk_b, link_strategy):
        ds_a = App.get_ds(pk_a)
        ds_b = App.get_ds(pk_b)
        linked_file = LinkedFile(ds_a, ds_b, link_strategy)
        linked_file.link()

        # save the linkedfile
        linked_file.save()

        return linked_file
