from typing import Dict

from clojos_common.util import monad

from climate import initialiser, model, dataframe, plot, presenter, adapter
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
    result = plot.temperature_plot.locale_temperatures(df=dataframe.temperature.locale_temperatures(g))
    if result.is_left():
        return result
    presenter.plot_to_channel(result.value,
                              channel=adapter.Channel.DISCORD,
                              title="Daily Temperature Plot",
                              description="Daily min/max temperatures at each locale")
    return result
