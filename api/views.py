from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import File
from .serializers import FileSerializer


# This will return a list of books
@api_view(["GET"])
def file(request):
    # files = ["Pro Python", "Fluent Python", "Speaking javascript", "The Go programming language"]
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    return JsonResponse(serializer.data, safe=False)
    # return Response(status=status.HTTP_200_OK, data={"data": files})


class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
