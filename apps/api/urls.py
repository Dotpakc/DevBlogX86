from django.urls import path,include

from . import views

app_name = 'api'

urlpatterns = [
    path('catalog/', include('apps.api.catalog.urls')),
]           