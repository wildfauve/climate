import pytest
from pathlib import Path

from climate import repo
from climate import triples

TEST_DB_MAP = {
    'climate_graph': (Path(__file__).parent.parent.parent / "fixtures" / "climate_test.ttl")
}


@pytest.fixture
def configure_repo():
    triples.RepoContext().configure(graphs=TEST_DB_MAP)
    triples.init()
    yield triples
    triples.drop(name='climate_graph')



@pytest.fixture
def empty_graph():
    return repo.triples.graph()

