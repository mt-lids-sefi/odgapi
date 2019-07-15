from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
import numpy as np
from core.models import File
from .serializers import FileSerializer
from django.shortcuts import get_object_or_404
import json

# This will return a list of files
@api_view(["GET"])
def file(request):
    # files = ["Pro Python", "Fluent Python", "Speaking javascript", "The Go programming language"]
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    return JsonResponse(serializer.data, safe=False)
    # return Response(status=status.HTTP_200_OK, data={"data": files})

@api_view(["GET"])
def file_data(request, pk):
    file = get_object_or_404(File, document_id=pk)
    print(file.name)
    lat = file.lat_col
    lon = file.lon_col
    df = pd.read_csv(file.doc)
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
    return Response(data={"rows": d, "lat_col": file.lat_col, "lon_col": file.lon_col, "name": file.name, "desc":file.description}, status=status.HTTP_200_OK)

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data,  context={"request": request})

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


