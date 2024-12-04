from django.urls import path

from query.views import *


app_name = 'query'

urlpatterns = [
    path('entities/', list_entities),
    path('entities/<str:filter>', get_entity),
]