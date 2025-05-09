from typing import List, Tuple
from climate import repo

def save(graph_name: str) -> Tuple:
    return repo.save(graph_name)


def climate_graph():
    return repo.graph('climateGraph')