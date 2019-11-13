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
from api.views import geo_files, geo_file, link_closest_point, link_polygon, link_closest_point_preview, \
    link_polygon_preview, link_closest_point_filter_preview, link_closest_point_filter, clusterize_kmeans_preview, \
    clusterize_meanshift_preview, data_files, data_file, get_configurations, clusterize_kmeans, clusterize_meanshift
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include('api.urls')),
    path("geofiles/", geo_files, name="file"),
    path("datafiles/", data_files, name="datafiles"),
    path("geo_file/<int:pk>", geo_file, name="file_data"),
    path("data_file/<int:pk>", data_file, name="file_data"),
    path("configurations/", get_configurations, name="configurations"),
    path("link_closest_point/<int:pk_a>/<int:pk_b>/<str:name>/<str:description>", link_closest_point, name="link_closest_point"),
    path("link_closest_point_filter/<int:pk_a>/<int:pk_b>/<int:max_distance>/<str:name>/<str:description>", link_closest_point_filter, name="link_closest_point_filter"),
    path("link_polygon/<int:pk_a>/<int:pk_b>/<int:max_distance>/<str:name>/<str:description>", link_polygon, name="link_polygon"),
    path("link_closest_point_preview/<int:pk_a>/<int:pk_b>", link_closest_point_preview, name="link_closest_point_preview"),
    path("link_closest_point_filter_preview/<int:pk_a>/<int:pk_b>/<int:max_distance>", link_closest_point_filter_preview, name="link_closest_point_filter_preview"),
    path("link_polygon_preview/<int:pk_a>/<int:pk_b>/<int:max_distance>", link_polygon_preview, name="link_polygon_preview"),
    path("clusterize_kmeans_preview/<int:pk_ids>/<str:col_a>/<str:col_b>", clusterize_kmeans_preview, name="clusterize_kmeans_preview"),
    path("clusterize_kmeans/<int:pk_ids>/<str:name>/<str:description>/<str:col_a>/<str:col_b>/<int:k>", clusterize_kmeans, name="clusterize_kmeans"),
    path("clusterize_meanshift/<int:pk_ids>/<str:name>/<str:description>/<str:col_a>/<str:col_b>", clusterize_meanshift, name="clusterize_meanshift"),
    path("clusterize_meanshift_preview/<int:pk_ids>/<str:col_a>/<str:col_b>", clusterize_meanshift_preview, name="clusterize_meanshift_preview")
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)