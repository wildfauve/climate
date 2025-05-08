from climate import model


def test_create_narrative(climate_repo, locale_for_testing):
    terms = [
        "rain[heavy:early_morning;showers:late_afternoon,early_evening]",
        "wind[still:morning;strong:afternoon]"
    ]
    result = model.weather_narrative.record(climate_repo, "Palazzo Bronzino", terms)

    assert result.is_right()

