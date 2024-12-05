import json

from django.http import (
    HttpResponse, HttpResponseNotFound
)

from query.sparql import SPARQL, SPARQL_WIKIDATA


def list_entities(request, filter):
    if request.method == 'GET':
        # Get pagination parameters from request, with default values
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 5))
        
        # Calculate the OFFSET for the SPARQL query based on page and page_size
        offset = (page - 1) * page_size

        q = SPARQL()
        query = q.prefix + f'''
        SELECT ?entity ?entType ?entLabel
        WHERE {{
            ?entity a ?entType .
            ?entity rdfs:label ?entLabel .
            FILTER (CONTAINS(LCASE(?entLabel), "{filter.lower()}"))
        }}
        LIMIT {page_size}
        OFFSET {offset}
        '''
        
        # Execute the query
        resp = q.execute(query)
        
        # Include pagination metadata (total count and page info)
        total_count_query = q.prefix + f'''
        SELECT (COUNT(?entity) AS ?totalCount)
        WHERE {{
            ?entity a ?entType .
            ?entity rdfs:label ?entLabel .
            FILTER (CONTAINS(LCASE(?entLabel), "{filter.lower()}"))
        }}
        '''
        
        total_count_result = q.execute(total_count_query)

        # Extract the total count from the nested dictionary structure
        if total_count_result and isinstance(total_count_result[0], dict):
            # Extract the 'value' of 'totalCount' from the nested dictionary
            total_count_str = total_count_result[0].get('totalCount', {}).get('value', '0')
        else:
            total_count_str = '0'

        # Ensure total count is an integer
        try:
            total_count = int(total_count_str)
        except (ValueError, TypeError):
            total_count = 0

        total_pages = (total_count // page_size) + (1 if total_count % page_size > 0 else 0)

        # Prepare the response with the data and pagination info
        response_data = {
            "entities": resp,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": total_pages,
            }
        }

        # Return the JSON response
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
    
    return HttpResponseNotFound

# Define a list of predicates that are associated with human persons
PERSON_PREDICATES = [
    "http://project.org/vocab#hasWriters",
    "http://project.org/vocab#hasAnimators",
    "http://project.org/vocab#hasStoryboard",
    "http://project.org/vocab#hasStoryboardArtists",
    "http://project.org/vocab#hasSupervisors",
    "http://project.org/vocab#hasLineProducer",
    "http://project.org/vocab#hasMain",
    "http://project.org/vocab#hasTechnical",
    "http://project.org/vocab#hasSupervisingProducers",
    "http://project.org/vocab#hasAnimationSupervisors",
    "http://project.org/vocab#hasGuests",
    "http://project.org/vocab#hasCreators",
    "http://project.org/vocab#hasVoiceActors",
    "http://project.org/vocab#hasCreative",
    "http://project.org/vocab#hasPortrayer",
    # Add any other predicates you think should map to people
]

def get_entity(request, filter):
    if request.method == 'GET':
        q = SPARQL()
        query = q.prefix + f'''
        SELECT ?p ?o ?oLabel
        WHERE {{
            :{filter} ?p ?o .
            OPTIONAL {{ ?o rdfs:label ?oLabel }}
        }}
        '''
        resp = q.execute(query)

        # Grouping by predicate
        grouped_resp = {}

        for item in resp:
            predicate = item["p"]["value"]
            object_value = item["o"]
            object_label = item.get("oLabel", None)

            # If the predicate refers to a person, handle accordingly
            if predicate in PERSON_PREDICATES:
                # Check if the object is a literal (person's name)
                if isinstance(object_value, dict) and object_value.get("type") == "literal":
                    person_name = object_value.get("value")
                    escaped_person_name = escape_sparql_string(person_name)

                    # Query Wikidata to find the person URI by name
                    qw = SPARQL_WIKIDATA()

                    query_test = qw.prefix + f'''
                    SELECT ?person ?personLabel WHERE {{
                    # Search for the person by their name
                    ?person rdfs:label "{escaped_person_name}"@en.

                    # Check if the notable work is "SpongeBob SquarePants" (P800)
                    {{
                        ?person wdt:P800 ?work.
                        ?work rdfs:label "SpongeBob SquarePants"@en.
                    }}

                    # Alternatively, check if the person is the creator of SpongeBob SquarePants (P1056)
                    UNION {{
                        ?person wdt:P1056 ?creator.
                        ?creator rdfs:label "SpongeBob SquarePants"@en.
                    }}

                    # Alternatively, check if the person has an occupation related to animation or storyboarding
                    UNION {{
                        ?person wdt:P106 ?occupation.
                        FILTER(?occupation IN (wd:Q1068227, wd:Q33999, wd:Q5762300, wd:Q715301, wd:Q2059704, wd:Q2405480, wd:Q245068, wd:Q10798782)) # Occupations (Animator, Storyboard Artist, etc.)
                    }}
                    
                    # Retrieve labels for the person
                    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
                    }}
                    LIMIT 1
                    '''

                    print(query_test)
                    
                    resp2 = qw.execute(query_test)

                    # If we found a matching person, get their URI and label
                    if resp2:
                        person_data = resp2[0]
                        person_uri = person_data.get("person", {}).get("value")
                        person_label = person_data.get("personLabel", {}).get("value")

                        # Add the person URI and label to the object
                        object_value["person_uri"] = person_uri
                        object_value["person_label"] = person_label

            # Group the predicate and its objects
            if predicate not in grouped_resp:
                grouped_resp[predicate] = []

            object_entry = {
                "object": object_value
            }

            if object_label:
                object_entry["label"] = object_label

            # Append the object entry under the current predicate
            grouped_resp[predicate].append(object_entry)

        # Prepare the response in the desired format
        formatted_resp = [{"predicate": p, "objects": objs} for p, objs in grouped_resp.items()]

        return HttpResponse(
            json.dumps(formatted_resp, indent=2),
            content_type='application/json'
        )
    
    return HttpResponseNotFound


def escape_sparql_string(value):
    # Escape both single and double quotes by backslash
    value = value.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")  
    return value