from __future__ import annotations
from typing import List, Union
from dataclasses import dataclass
from enum import Enum

import pendulum
from rdflib import URIRef, Graph
from clojos_common.util import monad, tokeniser

from climate import model, repo, rdf


class WeatherNarrativeTerm(Enum):
    MILD = rdf.plz_cl_nar.Mild
    FROST = rdf.plz_cl_nar.Frost
    SUNNY = rdf.plz_cl_nar.Sunny
    COLD = rdf.plz_cl_nar.Cold
    OVERCAST = rdf.plz_cl_nar.OverCast
    WILD_LIGHT = rdf.plz_cl_nar.WildLight
    WILD_MODERATE = rdf.plz_cl_nar.WildModerate
    WILD_STRONG = rdf.plz_cl_nar.WildStrong
    WILD_GALE = rdf.plz_cl_nar.WildGale
    RAIN_LIGHT_SPARSE = rdf.plz_cl_nar.RainLightSparse


@dataclass
class WeatherNarrativeRecord:
    subject: URIRef
    locale: model.locale.Locale
    terms: List[WeatherNarrativeTerm]
    recorded_at: pendulum.Date


def record(g: repo.GraphRepo, locale: str, terms: List[str], date=None):
    narrative_record = _to_model(g, locale, terms, date)
    if result := repo.narrative.upsert(g, narrative_record):
        return monad.Right(narrative_record)
    breakpoint()


def _to_model(g: repo.GraphRepo, locale_name: str, terms: List[str], date: str = None):
    locale = model.locale.locale_from_name(g, locale_name)
    if locale.is_left():
        breakpoint()
    record_date = model.helpers.record_date(date)
    return WeatherNarrativeRecord(subject=_record_sub(locale.value, record_date),
                                  locale=locale.value,
                                  terms=_to_terms(terms),
                                  recorded_at=record_date)



def _record_sub(locale: model.locale.Locale, date) -> URIRef:
    _, date_form = rdf.month_day_from_datetime(date)
    return rdf.plz_cl_ind_nar[locale.symbolised_name()] + "/" + date_form


def _to_terms(terms: List[str]) -> List[WeatherNarrativeTerm]:
    return [WeatherNarrativeTerm[t] for t in terms if t in WeatherNarrativeTerm.__members__]