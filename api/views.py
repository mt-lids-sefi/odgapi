from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import DataFileSerializer, ConfigurationSerializer
from core.model.App import App
from core.model.files.DataFile import DataFile
from core.model.files.GeoDataSource import GeoDataSource
from .serializers import GeoFileSerializer, IDataSourceSerializer
from django.shortcuts import get_object_or_404
import json


# This will return a list of files
@api_view(["GET"])
def geo_files(request):
    files = App.get_geo_files()
    serializer = IDataSourceSerializer(files, many=True)
    return JsonResponse(serializer.data, safe=False)


# This will return a list of configurations
@api_view(["GET"])
def get_configurations(request):
    confs = App.get_configurations()
    serializer = ConfigurationSerializer(confs, many=True)
    return JsonResponse(serializer.data, safe=False)


# This will return a list of files
@api_view(["GET"])
def data_files(request):
    files = App.get_data_files()
    serializer = IDataSourceSerializer(files, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def data_file(request, pk):
    source = get_object_or_404(DataFile, id=pk)
    d = source.get_data()
    d = d.to_json(orient='index')
    cols = source.get_cols()
    return Response(
        data={"rows": json.loads(d), "name": source.name,
              "desc": source.description, "cols": cols}, status=status.HTTP_200_OK)


@api_view(["GET"])
def geo_file(request, pk):
    source = get_object_or_404(GeoDataSource, id=pk)
    d = source.get_data()
    d = d.to_json(orient='index')
    cols = source.get_cols()
    return Response(
        data={"rows": json.loads(d), "lat_col": source.lat_col, "lon_col": source.lon_col, "name": source.name,
              "desc": source.   description, "cols": cols}, status=status.HTTP_200_OK)


# save FILE endpoint.
class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = GeoFileSerializer(data=request.data, context={"request": request})

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# save FILE endpoint.
class DataFileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = DataFileSerializer(data=request.data, context={"request": request})

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def link_closest_point(request, pk_a, pk_b, name, description):
    params = {'distance': 0, 'filter': False}
    linked_file = App.link_closest_points(pk_a, pk_b,  name, description, params)
    [data, cols] = App.make_response_link(linked_file.get_data())
    return Response(data={"data": data, "id": linked_file.get_id(), "cols": cols}, status=status.HTTP_200_OK)


@api_view(["GET"])
def link_closest_point_filter(request, pk_a, pk_b, max_distance, name, description):
    # create the strategy
    params = {'distance': max_distance, 'filter': True}
    linked_file = App.link_closest_points(pk_a, pk_b, name, description, params)
    [data, cols] = App.make_response_link(linked_file.get_data())
    return Response(data={"data": data, "id": linked_file.get_id(), "cols": cols}, status=status.HTTP_200_OK)


@api_view(["GET"])
def link_polygon(request, pk_a, pk_b, max_distance, name, description):
    params = {'distance': max_distance}
    linked_file = App.link_polygon(pk_a, pk_b, name, description, params)
    [data, cols] = App.make_response_link(linked_file.get_data())
    return Response(data={"data": data, "id": linked_file.get_id(), "cols": cols}, status=status.HTTP_200_OK)


@api_view(["GET"])
def link_closest_point_preview(request, pk_a, pk_b):
    params = {'distance': 0, 'filter': False}
    results = App.link_files_closest_point_preview(pk_a, pk_b, params)
    [data, cols] = App.make_response_link(results)
    return Response(data={"data": data, "cols": cols}, status=status.HTTP_200_OK)


@api_view(["GET"])
def link_closest_point_filter_preview(request, pk_a, pk_b, max_distance):
    params = {'distance': max_distance, 'filter': True}
    results = App.link_files_closest_point_preview(pk_a, pk_b, params)
    [data, cols] = App.make_response_link(results)
    return Response(data={"data": data, "cols": cols}, status=status.HTTP_200_OK)


@api_view(["GET"])
def link_polygon_preview(request, pk_a, pk_b, max_distance):
    params = {'distance': max_distance}
    results = App.link_files_polygon_preview(pk_a, pk_b, params)
    [data, cols] = App.make_response_link(results)
    return Response(data={"data": data, "cols": cols}, status=status.HTTP_200_OK)


@api_view(["GET"])
def clusterize_kmeans_preview(request, pk_ids, col_a, col_b, k=3):
    results = App.clusterize_kmeans_preview(pk_ids, col_a, col_b, k)
    [centroids, labels, data, cluster_size] = App.make_response_cluster(results)
    return Response(data={"centroids": centroids, "labels": labels, "data": data, "cluster_size": cluster_size}, status=status.HTTP_200_OK)


@api_view(["GET"])
def clusterize_meanshift_preview(request, pk_ids, col_a, col_b):
    results = App.clusterize_meanshift_preview(pk_ids,  col_a, col_b)
    [centroids, labels, data, cluster_size] = App.make_response_cluster(results)
    return Response(data={"centroids": centroids, "labels": labels, "data": data, "cluster_size": cluster_size}, status=status.HTTP_200_OK)


@api_view(["GET"])
def clusterize_meanshift(request, pk_ids, name, description, col_a, col_b):
    results = App.clusterize_meanshift(name, description, pk_ids,  col_a, col_b)
    return Response(data={"results": results}, status=status.HTTP_200_OK)


@api_view(["GET"])
def clusterize_kmeans(request, pk_ids, name,  description, col_a, col_b, k=3):
    results = App.clusterize_kmeans(name, description, pk_ids, col_a, col_b, k)
    return Response(data={"results": results}, status=status.HTTP_200_OK)


@api_view(["POST"])
def link_similarity_preview(request, pk_a, pk_b):
    rules = request.data['rules']
    results = App.link_files_similarity_preview(pk_a, pk_b, {'rules': rules})
    [data, cols] = App.make_response_link(results)
    return Response(data={"data": data, "cols": cols}, status=status.HTTP_200_OK)


@api_view(["POST"])
def link_similarity(request, pk_a, pk_b, name, description):
    rules = request.data['rules']
    linked_file = App.link_similarity(pk_a, pk_b, name, description, {'rules': rules})
    [data, cols] = App.make_response_link(linked_file.get_data())
    return Response(data={"data": data, "id": linked_file.get_id(), "cols": cols}, status=status.HTTP_200_OK)

