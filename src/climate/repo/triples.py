from pathlib import Path

from rdflib import Graph

from . import graphdb

from climate import rdf

def empty_graph():
    return initgraph()


def init(graphs: dict[str, tuple[Path, str]]):
    graphdb.GraphRepo(graphs=graphs)



def graph(graph_name):
    return graphdb.GraphRepo().load(graph_name)


def save(graph_name: str):
    return graphdb.GraphRepo().save(graph_name)


def reload():
    breakpoint()
    return init()


def drop(name: str = None):
    breakpoint()
    if not name:
        return RepoContext().db.drop(all_graphs=True)
    return RepoContext().db.drop(name=name)


def initgraph() -> Graph:
    return rdf.bind(rdf_graph())


def rdf_graph():
    return Graph()
