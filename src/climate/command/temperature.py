from typing import Dict, Union

from clojos_common.util import monad

from climate import initialiser, model, dataframe, plot, presenter, adapter
from climate.command import helpers, commanda

@commanda.command(graph_name='climateGraph')
def add_temperature(locale: str | model.locale.Locale, minimum, maximum, date=None) -> monad.EitherMonad[Dict]:
    g = helpers.climate_graph()
    result = model.temperature.record(g=g,
                                      locale=locale,
                                      minimum=minimum,
                                      maximum=maximum,
                                      for_date=date)
    return result



@commanda.command(graph_name='climateGraph')
def temperature_fix() -> monad.EitherMonad[Dict]:
    g = helpers.climate_graph()
    result = model.temperature.fix(g=g)
    return result



def plot_temperatures(channel: str):
    g = helpers.climate_graph()
    result = plot.temperature_plot.locale_temperatures(df=dataframe.temperature.locale_temperatures(g))
    if result.is_left():
        return result
    presenter.plot_to_channel(result.value,
                              channel=adapter.Channel[channel.upper()],
                              title="Daily Temperature Plot",
                              description="Daily min/max temperatures at each locale")
    return result
