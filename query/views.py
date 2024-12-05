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
        SELECT ?person ?personLabel ?wikipedia WHERE {
            ?person rdfs:label "Tom Kenny"@en.
            ?person wdt:P800 ?work.  # Get the notable work
            ?work rdfs:label "SpongeBob SquarePants"@en.
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }
        """
        print(query)
        resp = q.execute(query)
        
        # Extract the Wikipedia URL and person label from the response
        if resp:
            person_label = resp[0]['personLabel']['value']
            wikipedia_url = resp[0]['person']['value']
            response_data = f"Name: {person_label}, Wikipedia: {wikipedia_url}"
            return HttpResponse(response_data)
        else:
            return HttpResponse("No data found.")



def list_episodes(request):
    if request.method == 'GET':
        pass

def get_episode(request):
    if request.method == 'GET':
        pass
