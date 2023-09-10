from climate import model, adapter

def narrative_term_names():
    return [m.name.lower() for m in model.weather_narrative.WeatherNarrativeTerm]

def channels():
    return [c.name.lower() for c in adapter.Channel]