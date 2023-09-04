from typing import Dict

from clojos_common.util import monad

from climate import initialiser, model
from climate.command import helpers, commanda


@commanda.command(graph_names=['climate_graph'])
def add_locale(name) -> monad.EitherMonad[Dict]:
    g = helpers.climate_graph()
    result = model.locale.create(g=g,
                                 name=name,
)
    return result
