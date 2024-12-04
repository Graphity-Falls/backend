from django.urls import path

from query.views import *


app_name = 'query'

urlpatterns = [
    path('characters/', list_characters),
    path('characters/<str:label>', get_character),
    path('episodes/', list_episodes),
    path('episodes/<str:label>', get_episode),
    path('wikidata/', get_wiki),
]