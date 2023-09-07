from climate import model, adapter

def narrative_term_names():
    return [m.name for m in model.weather_narrative.WeatherNarrativeTerm]

def channels():
    return [c.name for c in adapter.Channel]