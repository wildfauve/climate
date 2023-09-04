from typing import List, Tuple
from climate import repo

def save(graph_names: List = None, val: Tuple = None) -> Tuple:
    repo.save(graph_names)
    return val


def climate_graph():
    return repo.graph('climate_graph')