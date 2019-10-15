from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from api import utils
import pandas as pd
import numpy as np

from core.model.App import App
from core.model.files.File import File
from core.model.files.IDataSource import IDataSource
from core.model.linker.ClosestPoint import ClosestPoint
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



@api_view(["GET"])
def files_join(request, pkA, pkB, max_distance):
    fileA = get_object_or_404(File, document_id=pkA)
    fileB = get_object_or_404(File, document_id=pkB)
    fileA_df = pd.read_csv(fileA.doc, error_bad_lines=False)
    fileB_df = pd.read_csv(fileB.doc, error_bad_lines=False)

    fileA_df = fileA_df[np.isfinite(fileA_df[fileA.lat_col])]
    fileA_df = fileA_df[np.isfinite(fileA_df[fileA.lon_col])]

    fileB_df = fileB_df[np.isfinite(fileB_df[fileB.lat_col])]
    fileB_df = fileB_df[np.isfinite(fileB_df[fileB.lon_col])]

    fileA_df['pointA'] = [(x, y) for x, y in zip(fileA_df[fileA.lat_col], fileA_df[fileA.lon_col])]
    fileB_df['pointB'] = [(x, y) for x, y in zip(fileB_df[fileB.lat_col], fileB_df[fileB.lon_col])]

    fileA_df['distances'] = [utils.haversine_np(x, y, list(fileB_df[fileB.lat_col]), list(fileB_df[fileB.lon_col])) for
                             x, y in
                             zip(fileA_df[fileA.lat_col], fileA_df[fileA.lon_col])]
    fileA_df['closest_point'] = [fileB_df.iloc[x.argmin()]['pointB'] for x in fileA_df['distances']]
    fileA_df['closest_dist'] = [min(x) for x in fileA_df['distances']]
    fileA_df['nearby_points'] = [utils.nearby_points(x, max_distance) for x in fileA_df['distances']]
    fileA_df['count'] = [len(x) for x in fileA_df['nearby_points']]
    unrolled = utils.unroll(fileA_df)
    joined = utils.join_dfs(unrolled, fileA_df, fileB_df)
    print(len(joined.index))
    joined = joined.drop(columns=['distances'])
    joined = joined.to_json(orient='index')
    d = json.loads(joined)
    return Response(data={"PEPE": d}, status=status.HTTP_200_OK)


#save FILE endpoint.
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
def link_closest_point(request, pk_a, pk_b, max_distance):
    #create the strategy
    params = {'distance': max_distance}
    link_strategy = ClosestPoint(params)

    #create & save the linkedfile
    linked_file = App.link_files(pk_a, pk_b, link_strategy)

    #api specific
    data = linked_file.get_data().to_json(orient='index')
    data = json.loads(data)
    return Response(data={"data": data}, status=status.HTTP_200_OK)
