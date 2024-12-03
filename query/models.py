from string import Template
from typing import Self

from django.db import models


# Create your models here.
class QueryBuilder:
    def __init__(self):
        self.query = Template(
            """
            PREFIX : <http://project.org/data/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> .
            PREFIX rdfs: <http://www.w3.org/2000/rdf-schema#> .
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
            PREFIX v: <http://project.org/vocab#> .
            """
        )

    def select(self, columns: dict) -> Self:
        """TODO: append select with columns to query template."""
        return self
    
    def where(self, clause: str) -> Self:
        """TODO: append where clauses to query template."""
        return self

    def limit(self, count: int) -> Self:
        """TODO: append limit clause to end of query."""
        return self
    
    def group_by(self, column: str) -> Self:
        """TODO: append group_by clause to end of query."""
        return self
