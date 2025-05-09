from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rdflib import Graph, URIRef, Namespace
from returns.maybe import Maybe

from climate.util import fn, singleton

@dataclass
class Prefix:
    prefix: str
    uri: URIRef | Namespace

    def to_q(self):
        return f"prefix {self.prefix}: <{str(self.uri)}>"


@dataclass
class G:
    name: str
    path: Path
    rdf_form: str
    graph: Graph
    loaded: bool = False

    @classmethod
    def find_by_name(cls, name, graphs: list[G]):
        return fn.find(lambda g: g.name == name, graphs)

    def load(self):
        if self.loaded:
            return self
        self.graph.parse(self.path, format=self.rdf_form)
        self.loaded = True
        return self

    def serialize_and_write(self, format: str = None, indent: int = None):
        return self.write(self.serialize(format=format, indent=indent))

    def serialize(self, format: str = None, indent: int = None):
        return self.graph.serialize(format=format, indent=indent)

    def write(self, serialised_graph):
        with open(self.path, 'w') as f:
            f.write(serialised_graph)



@singleton.singleton
class GraphRepo:
    def __init__(self, graphs: dict[tuple[Path, str]]):
        self.graphs = [G(name=k, path=path, rdf_form=form, graph=Graph()) for k,(path, form) in graphs.items()]
        self._g = None

    # def __init__(self, graph: Graph, name: str, context: dict = None):
    #     self.name = name
    #     self.graph = graph
    #     self.context = context if context else {}

    def with_bindings(self, prefixes: list[Prefix]):
        for binding in prefixes:
            self._g.graph.bind(binding.prefix, binding.uri)
        return self

    def load(self, name: str):
        g = G.find_by_name(name, self.graphs).load()
        self._g = g
        return self
    
    def save(self, graph_name: str = None):
        self._write_to_ttl(self._g)
        
    def _write_to_ttl(self, g: G):
        if g.rdf_form == "ttl":
            g.serialize_and_write(format=g.rdf_form)
        else:
            g.serialize_and_write(format="json-ld", indent=4)

    @property
    def namespace_manager(self):
        return self._g.graph.namespace_manager

    def uri_for_prefix(self, prefix: str) -> Maybe[tuple[str, URIRef]]:
        return fn.maybe_find(lambda p: p[0] == prefix, self.namespaces)

    def namespace_for_prefix(self, prefix: str) -> Maybe[tuple[str, Namespace]]:
        return (fn.maybe_find(lambda p: p[0] == prefix, self.namespaces)
                .bind_optional(lambda prefix_tuple: (prefix_tuple[0], Namespace(prefix_tuple[1]))))

    @property
    def namespaces(self):
        return self._g.graph.namespaces()

    def add(self, triples: tuple):
        """
        Proxy for RDFLIB add
        :param triples:
        :return:
        """
        return self._g.graph.add(triples)

    def triples(self, triples: tuple):
        """
        Proxy for RDFLIB triples
        :param triples:
        :return:
        """
        return self._g.graph.triples(triples)

    def set(self, triples: tuple):
        """
        Proxy for RDFLIB set
        :param sparql:
        :return:
        """
        return self._g.graph.set(triples)

    def query(self, sparql: str):
        """
        Proxy for RDFLIB sparql query
        :param sparql:
        :return:
        """
        return self._g.graph.query(sparql)

    def p(self):
        print(self.serialise(fmt="ttl"))
        pass

    @property
    def context_obj(self):
        return dict((k, str(v)) for k, v in self.context.items())

    def serialise(self, fmt: str = "ttl", with_context: bool = False, **kwargs):
        additional_args = {}
        if with_context:
            additional_args['context'] = self.context_obj
        return self._g.graph.serialize(format=fmt, **{**kwargs, **additional_args})

    def write(self, file, fmt="ttl"):
        with open(file, 'w') as f:
            f.write(self.serialise(fmt=fmt))


# from typing import Tuple
# from rdflib import Graph
#
#
# class GraphRepo:
#
#     def __init__(self, graph: Graph, name: str):
#         self.name = name
#         self.graph = graph
#
#     def add(self, triples: Tuple):
#         """
#         Proxy for RDFLIB add
#         :param triples:
#         :return:
#         """
#         return self._g.graph.add(triples)
#
#     def triples(self, triples: Tuple):
#         """
#         Proxy for RDFLIB triples
#         :param triples:
#         :return:
#         """
#         return self._g.graph.triples(triples)
#
#     def set(self, triples: Tuple):
#         """
#         Proxy for RDFLIB set
#         :param sparql:
#         :return:
#         """
#         return self._g.graph.set(triples)
#
#
#     def query(self, sparql: str):
#         """
#         Proxy for RDFLIB sparql query
#         :param sparql:
#         :return:
#         """
#         return self._g.graph.query(sparql)
#
#
#     def p(self):
#         print(self._g.graph.serialize(format="ttl"))
#         pass
#
#     def write(self, file, fmt="ttl"):
#         with open(file, 'w') as f:
#             f.write(self._g.graph.serialize(format=fmt))
