from typing import Dict

from clojos_common.util import monad

from climate import initialiser, model, dataframe, plot
from climate.command import helpers, commanda

@commanda.command(graph_names=['climate_graph'])
def add_temperature(locale, minimum, maximum, date=None) -> monad.EitherMonad[Dict]:
    g = helpers.climate_graph()
    result = model.temperature.record(g=g,
                                      locale=locale,
                                      minimum=minimum,
                                      maximum=maximum,
                                      date=date)
    return result


def plot_temperatures():
    g = helpers.climate_graph()
    plot.temperature_plot.locale_temperatures(df=dataframe.temperature.locale_temperatures(g))
    return monad.Right(None)