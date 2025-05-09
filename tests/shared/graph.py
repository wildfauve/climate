import pytest
from pathlib import Path

from climate import repo

TEST_DB_MAP = {
    'climateGraph': (Path(__file__).parent.parent.parent / "fixtures" / "climate_test.ttl")
}


@pytest.fixture
def climate_repo():
    repo.RepoContext().configure(graphs=TEST_DB_MAP)
    repo.init()
    yield repo.graph('climateGraph')
    repo.drop(name='climateGraph')



@pytest.fixture
def empty_graph():
    return repo.triples.graph()

