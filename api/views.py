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
    df = pd.read_csv(file.doc)
    df['longitude'] = df['longitude'].replace(r'\s+', np.nan, regex=True)
    df['longitude'] = df['longitude'].replace(r'^$', np.nan, regex=True)
    df['longitude'] = df['longitude'].fillna(-0.99999)
    df['longitude'] = pd.to_numeric(df['longitude'])
    df['latitude'] = df['latitude'].replace(r'\s+', np.nan, regex=True)
    df['latitude'] = df['latitude'].replace(r'^$', np.nan, regex=True)
    df['latitude'] = df['latitude'].fillna(-0.99999)
    df['latitude'] = pd.to_numeric(df['latitude'])

    df = df.to_json(orient='index')
    d = json.loads(df)
    return Response(data={"coords": d}, status=status.HTTP_200_OK)

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data,  context={"request": request})

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


