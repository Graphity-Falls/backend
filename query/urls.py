from django.urls import path

from query.views import *


app_name = 'query'

urlpatterns = [
    path('entities/<str:filter>', list_entities),
    path('entity/<str:filter>', get_entity),
]