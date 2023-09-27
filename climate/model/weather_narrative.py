from __future__ import annotations
from typing import List, Union
from dataclasses import dataclass

import pendulum
from rdflib import URIRef, Literal
from clojos_common.util import monad

from climate import model, repo, rdf


@dataclass
class WeatherNarrativeRecord:
    subject: URIRef
    locale: model.locale.Locale
    narrative_statements: List[model.narrative_parser.TemporalAdjectiveCollection]
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
                                  narrative_statements=_to_statements(terms),
                                  recorded_at=record_date)


def _record_sub(locale: model.locale.Locale, date) -> URIRef:
    _, date_form = rdf.month_day_from_datetime(date)
    return rdf.plz_cl_ind_nar[locale.symbolised_name()] + "/" + date_form


def _to_statements(terms: List[str]) -> List[model.narrative_parser.TemporalAdjectiveCollection]:
    return [model.narrative_parser.parse(term) for term in terms]


def fix(g: repo.GraphRepo):
    return change_date_strategy(g)

def change_date_strategy(g: repo.GraphRepo):
    all_recs = repo.narrative.get_all_narratives(g)
    for s, _, _ in all_recs:
        triples = rdf.all_matching(g, (s, None, None))
        on_dt = rdf.triple_finder(rdf.isRecordedAtDateTime, triples, builder=rdf.literal_time_triple_parser)
        for_d = rdf.triple_finder(rdf.isRecordedForDate, triples)
        if not for_d:
            g.set((s, rdf.isRecordedForDate, Literal(on_dt.date())))
            g.set((s, rdf.isRecordedAtDateTime, Literal(on_dt.add(days=1, hours=8))))
    return monad.Right(g)