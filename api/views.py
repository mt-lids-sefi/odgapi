from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.model.App import App
from core.model.files.IDataSource import IDataSource
from core.model.linker.ClosestPoint import ClosestPoint
from core.model.linker.Polygon import Polygon
from .serializers import FileSerializer, IDataSourceSerializer
from django.shortcuts import get_object_or_404
import json


# This will return a list of files
@api_view(["GET"])
def file(request):
    files = IDataSource.objects.all()
    serializer = IDataSourceSerializer(files, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def file_data(request, pk):
    source = get_object_or_404(IDataSource, id=pk)
    d = source.get_data()
    d = d.to_json(orient='index')
    cols = source.get_cols()
    return Response(
        data={"rows": json.loads(d), "lat_col": source.lat_col, "lon_col": source.lon_col, "name": source.name,
              "desc": source.description, "cols": cols}, status=status.HTTP_200_OK)


# save FILE endpoint.
class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data, context={"request": request})

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def link_closest_point(request, pk_a, pk_b, name, description):
    # create the strategy
    params = {'distance': 0, 'filter': False}
    link_strategy = ClosestPoint(params)

    # create & save the linkedfile
    linked_file = App.link_files(pk_a, pk_b, link_strategy, name, description)

    # api specific
    data = linked_file.get_data().to_json(orient='index')
    data = json.loads(data)
    return Response(data={"data": data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def link_closest_point_filter(request, pk_a, pk_b, max_distance, name, description):
    # create the strategy
    params = {'distance': max_distance, 'filter': True}
    link_strategy = ClosestPoint(params)

    # create & save the linkedfile
    linked_file = App.link_files(pk_a, pk_b, link_strategy, name, description)

    # api specific
    data = linked_file.get_data().to_json(orient='index')
    data = json.loads(data)
    return Response(data={"data": data, "id": linked_file.id}, status=status.HTTP_200_OK)


@api_view(["GET"])
def link_polygon(request, pk_a, pk_b, max_distance, name, description):
    # create the strategy
    params = {'distance': max_distance}
    link_strategy = Polygon(params)

    # create & save the linkedfile
    linked_file = App.link_files(pk_a, pk_b, link_strategy, name, description)

    # api specific
    data = linked_file.get_data().to_json(orient='index')
    data = json.loads(data)
    return Response(data={"data": data, "id": linked_file.id}, status=status.HTTP_200_OK)


@api_view(["GET"])
def link_closest_point_preview(request, pk_a, pk_b):
    params = {'distance': 0, 'filter': False}
    link_strategy = ClosestPoint(params)
    data_preview = App.link_files_preview(pk_a, pk_b, link_strategy)
    cols = data_preview.columns.values
    data_preview = data_preview.to_json(orient='index')
    data = json.loads(data_preview)
    return Response(data={"data": data, "cols": cols}, status=status.HTTP_200_OK)


@api_view(["GET"])
def link_closest_point_filter_preview(request, pk_a, pk_b, max_distance):
    params = {'distance': max_distance, 'filter': True}
    link_strategy = ClosestPoint(params)
    data_preview = App.link_files_preview(pk_a, pk_b, link_strategy)
    cols = data_preview.columns.values
    data_preview = data_preview.to_json(orient='index')
    data = json.loads(data_preview)
    return Response(data={"data": data, "cols": cols}, status=status.HTTP_200_OK)


@api_view(["GET"])
def link_polygon_preview(request, pk_a, pk_b, max_distance):
    params = {'distance': max_distance}
    link_strategy = Polygon(params)
    data_preview = App.link_files_preview(pk_a, pk_b, link_strategy)
    cols = data_preview.columns.values
    data_preview = data_preview.to_json(orient='index')
    data = json.loads(data_preview)
    return Response(data={"data": data, "cols": cols}, status=status.HTTP_200_OK)

