from django.urls import path

from query.views import *


app_name = 'query'

urlpatterns = [
    path('character/', query_character1)
]