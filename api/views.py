from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser


# This will return a list of books
@api_view(["GET"])
def file(request):
    files = ["Pro Python", "Fluent Python", "Speaking javascript", "The Go programming language"]
    return Response(status=status.HTTP_200_OK, data={"data": files})

class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)