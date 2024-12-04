import os
from string import Template
from typing import Any

from dotenv import load_dotenv
from django.db import models
from SPARQLWrapper import SPARQLWrapper, JSON


load_dotenv()

# Create your models here.
class SPARQL:
    def __init__(self):
        self.graphdb_url = os.environ['GRAPHDB_URL']
        self.sparql = SPARQLWrapper(self.graphdb_url)
        self.sparql.setReturnFormat(JSON)
        self.prefix = """
PREFIX : <http://project.org/data/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX v: <http://project.org/vocab#>
"""

    def execute(self, query: str) -> Any:
        """Executes given query to GraphDB."""
        print(query)
        self.sparql.setQuery(query)
        try:
            ret = self.sparql.queryAndConvert()
            return ret['results']['bindings']
        except Exception as e:
            return str(e)

class SPARQL_WIKIDATA:
    def __init__(self):
        self.graphdb_url = "https://query.wikidata.org/sparql"
        self.sparql = SPARQLWrapper(self.graphdb_url)
        self.sparql.setReturnFormat(JSON)
        self.prefix = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wds: <http://www.wikidata.org/prop/statement/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
"""

    def execute(self, query: str) -> Any:
        """Executes given query to GraphDB."""
        self.sparql.setQuery(query)
        try:
            ret = self.sparql.queryAndConvert()
            return ret['results']['bindings']
        except Exception as e:
            return str(e)

    # def select(self, columns: dict) -> Self:
    #     """TODO: append select with columns to query template."""
    #     return self
    
    # def where(self, clause: str) -> Self:
    #     """TODO: append where clauses to query template."""
    #     return self

    # def limit(self, count: int) -> Self:
    #     """TODO: append limit clause to end of query."""
    #     return self
    
    # def group_by(self, column: str) -> Self:
    #     """TODO: append group_by clause to end of query."""
    #     return self
