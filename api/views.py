from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from api import utils
import pandas as pd
import numpy as np
from core.models import File
from .serializers import FileSerializer
from django.shortcuts import get_object_or_404
import json


# This will return a list of files
@api_view(["GET"])
def file(request):
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(["GET"])
def file_data(request, pk):
    file = get_object_or_404(File, document_id=pk)
    print(file.name)
    lat = file.lat_col
    lon = file.lon_col
    df = pd.read_csv(file.doc, error_bad_lines=False)

    cols =  list(df.columns.values)
    df[lon] = df[lon].replace(r'\s+', np.nan, regex=True)
    df[lon] = df[lon].replace(r'^$', np.nan, regex=True)
    df[lon] = df[lon].fillna(-0.99999)
    df[lon] = pd.to_numeric(df[lon])
    df[lat] = df[lat].replace(r'\s+', np.nan, regex=True)
    df[lat] = df[lat].replace(r'^$', np.nan, regex=True)
    df[lat] = df[lat].fillna(-0.99999)
    df[lat] = pd.to_numeric(df[lat])

    df = df.to_json(orient='index')
    d = json.loads(df)
    
    return Response(data={"rows": d, "lat_col": file.lat_col, "lon_col": file.lon_col, "name": file.name, "desc":file.description, "cols": cols}, status=status.HTTP_200_OK)

@api_view(["GET"])
def files_join(request, pkA, pkB, max_distance):
    fileA =  get_object_or_404(File, document_id=pkA)
    fileB =  get_object_or_404(File, document_id=pkB)
    fileA_df = pd.read_csv(fileA.doc, error_bad_lines=False)
    fileB_df = pd.read_csv(fileB.doc, error_bad_lines=False)

    fileA_df = fileA_df[np.isfinite(fileA_df[fileA.lat_col])]
    fileA_df = fileA_df[np.isfinite(fileA_df[fileA.lon_col])]

    fileB_df = fileB_df[np.isfinite(fileB_df[fileB.lat_col])]
    fileB_df = fileB_df[np.isfinite(fileB_df[fileB.lon_col])]

    fileA_df['pointA'] = [(x, y) for x, y in zip(fileA_df[fileA.lat_col], fileA_df[fileA.lon_col])]
    fileB_df['pointB'] = [(x, y) for x, y in zip(fileB_df[fileB.lat_col], fileB_df[fileB.lon_col])]

    fileA_df['distances'] = [utils.haversine_np(x,y, list(fileB_df[fileB.lat_col]), list(fileB_df[fileB.lon_col])) for x, y in
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


class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data,  context={"request": request})

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


