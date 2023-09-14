import pytest

from climate import model

@pytest.fixture
def locale_for_testing(climate_repo):
    model.locale.create(g=climate_repo, name="Palazzo Bronzino")