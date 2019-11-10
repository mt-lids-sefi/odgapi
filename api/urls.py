from django.urls import path
from .views import *

urlpatterns = [
    path('', FileUploadView.as_view()),
    path('datafile', DataFileUploadView.as_view())
]