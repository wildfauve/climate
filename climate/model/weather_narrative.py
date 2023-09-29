from __future__ import annotations
from typing import List, Union
from functools import partial
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


def record(g: repo.GraphRepo, locale: model.locale.Locale, terms: List[str], date=None):
    result = (_to_model(locale, terms, date) >>
              partial(repo.narrative.upsert, g))

    if result.is_right():
        return result
    breakpoint()


def _to_model(locale: model.locale.Locale,
              terms: List[str],
              date: str = None) -> monad.EitherMonad[WeatherNarrativeRecord]:
    record_date = model.helpers.record_date(date)
    stmt_results = _to_statements(terms)
    if any(map(monad.maybe_value_fail, stmt_results)):
        return monad.Left(stmt_results)
    return monad.Right(WeatherNarrativeRecord(subject=_record_sub(locale, record_date),
                                              locale=locale,
                                              narrative_statements=[statement.value for statement in stmt_results],
                                              recorded_at=record_date))


def _record_sub(locale: model.locale.Locale, date) -> URIRef:
    _, date_form = rdf.month_day_from_datetime(date)
    return rdf.plz_cl_ind_nar[locale.symbolised_name()] + "/" + date_form


def _to_statements(terms: List[str]) -> List[monad.EitherMonad[model.narrative_parser.TemporalAdjectiveCollection]]:
    return [model.narrative_parser.parse(term) for term in terms]


# Data FIXes below.
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
