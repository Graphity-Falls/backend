from django.http import (
    HttpResponse, HttpResponseNotFound
)

from query.sparql import SPARQL, SPARQL_WIKIDATA


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

def get_wiki(request):
    if request.method == 'GET':
        q = SPARQL_WIKIDATA()
        query = q.prefix + """
SELECT ?person ?personLabel WHERE {
  ?person rdfs:label "Tom Kenny"@en.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""
        print(query)
        resp = q.execute(query)
        return HttpResponse(resp)


def list_episodes(request):
    if request.method == 'GET':
        pass

def get_episode(request):
    if request.method == 'GET':
        pass
