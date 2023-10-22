from climate import model


def test_noun_adjective_temporal_narrative():
    rain_narrative = "rain[showers:late_afternoon,early_evening]"

    result = model.narrative_parser.parse(rain_narrative)

    assert result.is_right()

    statement = result.value

    assert statement.noun == model.narrative_parser.NarrativeNoun.RAIN.value[0]

    adjs = statement.temporal_adjectives

    assert len(adjs) == 1
    assert adjs[0].adjective == model.narrative_parser.RainTerms.SHOWERS

    expected_temporality = {model.narrative_parser.TemporalTerm.LATE_AFTERNOON,
                            model.narrative_parser.TemporalTerm.EARLY_EVENING}
    assert set(adjs[0].temporal_statements) == expected_temporality


def test_noun_adjective_multiple_temporal_narrative():
    rain_narrative = "rain[heavy:early_morning;showers:late_afternoon,early_evening]"

    result = model.narrative_parser.parse(rain_narrative)

    assert result.is_right()

    statement = result.value


    adjs = statement.temporal_adjectives

    assert len(adjs) == 2
    assert adjs[0].adjective == model.narrative_parser.RainTerms.HEAVY

    expected_temporality = {model.narrative_parser.TemporalTerm.EARLY_MORNING}
    assert set(adjs[0].temporal_statements) == expected_temporality


def test_with_spaces():
    rain_narrative = "rain [ heavy : early_morning; showers : late_afternoon, early_evening ]"

    result = model.narrative_parser.parse(rain_narrative)

    assert result.is_right()

    statement = result.value

    adjs = statement.temporal_adjectives

    assert len(adjs) == 2
    assert adjs[0].adjective == model.narrative_parser.RainTerms.HEAVY

    expected_temporality = {model.narrative_parser.TemporalTerm.EARLY_MORNING}
    assert set(adjs[0].temporal_statements) == expected_temporality


def test_using_temporal_shortcuts(climate_repo, locale_for_testing):
    narrative = "rain[heavy:em;showers:ea,ee]"

    result = model.narrative_parser.parse(narrative)

    assert result.is_right()

    statement = result.value

    adjs = statement.temporal_adjectives

    assert len(adjs) == 2
    assert adjs[0].adjective == model.narrative_parser.RainTerms.HEAVY

    expected_temporality = {model.narrative_parser.TemporalTerm.EARLY_MORNING}
    assert set(adjs[0].temporal_statements) == expected_temporality


