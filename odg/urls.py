"""odg URL configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import file, file_data, link_closest_point, link_polygon, link_closest_point_preview, \
    link_polygon_preview, link_closest_point_filter_preview, link_closest_point_filter
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include('api.urls')),
    path("file/", file, name="file"),
    path("map/<int:pk>", file_data, name="file_data"),
    #path("join/<int:pkA>/<int:pkB>/<int:max_distance>", files_join, name="files_join"),
    path("link_closest_point/<int:pk_a>/<int:pk_b>/<str:name>/<str:description>", link_closest_point, name="link_closest_point"),
    path("link_closest_point_filter/<int:pk_a>/<int:pk_b>/<int:max_distance>/<str:name>/<str:description>", link_closest_point_filter, name="link_closest_point_filter"),
    path("link_polygon/<int:pk_a>/<int:pk_b>/<int:max_distance>", link_polygon, name="link_polygon"),
    path("link_closest_point_preview/<int:pk_a>/<int:pk_b>", link_closest_point_preview, name="link_closest_point_preview"),
    path("link_closest_point_filter_preview/<int:pk_a>/<int:pk_b>/<int:max_distance>", link_closest_point_filter_preview, name="link_closest_point_filter_preview"),
    path("link_polygon_preview/<int:pk_a>/<int:pk_b>/<int:max_distance>", link_polygon_preview, name="link_polygon_preview")
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)