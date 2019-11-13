from rest_framework import serializers

from core.model.configuration.Configuration import Configuration
from core.model.files.DataFile import DataFile
from core.model.files.GeoFile import GeoFile
from core.model.files.GeoLinkedFile import GeoLinkedFile


class GeoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoFile
        fields = ['id', 'name', 'description', 'lat_col', 'lon_col', 'doc']


class DataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFile
        fields = ['id', 'name', 'description', 'doc']


class GeoLinkedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLinkedFile
        fields = ['id', 'name', 'description', 'lat_col', 'lon_col']


class IDataSourceSerializer(serializers.Serializer):
    @classmethod
    def get_serializer(cls, model):
        if model == GeoFile:
            return GeoFileSerializer
        elif model == DataFile:
            return DataFileSerializer
        elif model == GeoLinkedFile:
            return GeoLinkedFileSerializer

    def to_representation(self, instance):
        serializer = self.get_serializer(instance.__class__)
        return serializer(instance, context=self.context).data


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ['id', 'name', 'description']

