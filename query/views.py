import json

from django.http import (
    HttpResponse, HttpResponseNotFound
)

from query.sparql import SPARQL


def list_entities(request):
    if request.method == 'GET':
        q = SPARQL()
        query = q.prefix + f'''
SELECT ?entity ?entType ?entLabel
WHERE {{
    ?entity a ?entType \.
    ?entity rdfs:label ?entLabel .
}}
'''
    # FILTER (CONTAINS(LCASE(?entLabel), "{filter.lower()}"))
        resp = q.execute(query)
        return HttpResponse(
            json.dumps(resp),
            content_type='application/json'
        )
    return HttpResponseNotFound

def get_entity(request, filter):
    if request.method == 'GET':
        q = SPARQL()
        query = q.prefix + f'''
SELECT ?p ?o
WHERE {{
    :{filter} ?p ?o 
}}
'''
        resp = q.execute(query)
        return HttpResponse(
            json.dumps(resp),
            content_type='application/json'
        )
    return HttpResponseNotFound
