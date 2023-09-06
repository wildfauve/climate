from climate import model

def narrative_term_names():
    return [m.name for m in model.weather_narrative.WeatherNarrativeTerm]