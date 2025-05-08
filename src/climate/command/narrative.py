from typing import Dict, List

from clojos_common.util import monad

from climate import initialiser, model
from climate.command import helpers, commanda


@commanda.command(graph_names=['climate_graph'])
def add_narrative(locale: model.locale, terms: List[str], date=None) -> monad.EitherMonad[Dict]:
    g = helpers.climate_graph()
    result = model.weather_narrative.record(g=g,
                                            locale=locale,
                                            terms=terms,
                                            date=date)
    return result


@commanda.command(graph_names=['climate_graph'])
def narrative_fix() -> monad.EitherMonad[Dict]:
    g = helpers.climate_graph()
    result = model.weather_narrative.fix(g=g)
    return result
