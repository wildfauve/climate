from pathlib import Path

from climate import repo

GRAPHS = {
    "climateGraph": (Path(__file__).parent.parent.parent.parent / "data" / "db" / "climate.ttl", "ttl")
}


def initialise_db():
    return repo.init(GRAPHS)
