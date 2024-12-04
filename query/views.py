from django.http import (
    HttpResponse, HttpResponseNotFound
)

from query.sparql import SPARQL


def list_characters(request):
    if request.method == 'GET':
        q = SPARQL()
        query = q.prefix + """
SELECT ?entity 
WHERE {
    ?entity a :Character .
}
LIMIT 10
"""
        print(query)
        resp = q.execute(query)
        return HttpResponse(resp)

def get_character(request):
    if request.method == 'GET':
        pass

def list_episodes(request):
    if request.method == 'GET':
        pass

def get_episode(request):
    if request.method == 'GET':
        pass
