import pytest
from pathlib import Path

from climate import repo

TEST_DB_MAP = {
    'climate_graph': (Path(__file__).parent.parent.parent / "fixtures" / "climate_test.ttl")
}


@pytest.fixture
def climate_repo():
    repo.RepoContext().configure(graphs=TEST_DB_MAP)
    repo.init()
    yield repo.graph('climate_graph')
    repo.drop(name='climate_graph')



@pytest.fixture
def empty_graph():
    return repo.triples.graph()

