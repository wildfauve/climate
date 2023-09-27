from typing import Tuple
from rdflib import Graph


class GraphRepo:

    def __init__(self, graph: Graph, name: str):
        self.name = name
        self.graph = graph

    def add(self, triples: Tuple):
        """
        Proxy for RDFLIB add
        :param triples:
        :return:
        """
        return self.graph.add(triples)

    def triples(self, triples: Tuple):
        """
        Proxy for RDFLIB triples
        :param triples:
        :return:
        """
        return self.graph.triples(triples)

    def set(self, triples: Tuple):
        """
        Proxy for RDFLIB set
        :param sparql:
        :return:
        """
        return self.graph.set(triples)


    def query(self, sparql: str):
        """
        Proxy for RDFLIB sparql query
        :param sparql:
        :return:
        """
        return self.graph.query(sparql)


    def p(self):
        print(self.graph.serialize(format="ttl"))
        pass

    def write(self, file, fmt="ttl"):
        with open(file, 'w') as f:
            f.write(self.graph.serialize(format=fmt))
