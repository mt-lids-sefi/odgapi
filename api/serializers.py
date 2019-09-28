from rest_framework import serializers
from core.model.files.File import File
from core.model.files.LinkedFile import LinkedFile


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'description', 'lat_col', 'lon_col']


class LinkedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedFile
        fields = ['id', 'name', 'description', 'lat_col', 'lon_col']


class IFileSerializer(serializers.Serializer):
    @classmethod
    def get_serializer(cls, model):
        if model == File:
            return FileSerializer
        elif model == LinkedFile:
            return LinkedFileSerializer

    def to_representation(self, instance):
        serializer = self.get_serializer(instance.__class__)
        return serializer(instance, context=self.context).data
