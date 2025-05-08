from __future__ import annotations
from typing import List, Union, Tuple, Optional
from dataclasses import dataclass
from itertools import groupby
from functools import reduce, partial
from decimal import Decimal

import pendulum
from rdflib import URIRef, Graph, Literal
from clojos_common.util import monad, tokeniser

from climate import model, repo, rdf


@dataclass
class MinMaxTemperatureRecord:
    subject: URIRef
    minimum: Decimal
    maximum: Decimal
    locale: model.locale.Locale
    recorded_for: pendulum.Date
    recorded_at: Optional[pendulum.DateTime] = None


def record(g: repo.GraphRepo,
           locale: Union[str, model.locale.Locale],
           minimum: Decimal,
           maximum: Decimal,
           for_date=None):
    temp_record = _to_model(g, locale, minimum, maximum, for_date)
    if result := repo.temperature.upsert(g, temp_record):
        return monad.Right(temp_record)
    breakpoint()


def get_all(g: repo.GraphRepo) -> groupby:
    return _fill_blanks(g, list(map(_from_dto, repo.temperature.get_all(g))))


def _from_dto(record):
    locale = model.locale._to_locale_result(name=record.locale_name, subject=record.locale_subject)
    return MinMaxTemperatureRecord(subject=record.subject,
                                   minimum=record.minimum,
                                   maximum=record.maximum,
                                   locale=locale.value,
                                   recorded_at=record.recorded_at,
                                   recorded_for=record.recorded_for)


def _to_model(g: repo.GraphRepo,
              locale: Union[str, model.locale.Locale],
              minimum: Decimal,
              maximum: Decimal,
              for_date: str = None):
    locale = model.locale.locale_from_name(g, locale)
    if locale.is_left():
        breakpoint()
    record_date = model.helpers.record_date(for_date)
    return MinMaxTemperatureRecord(subject=_record_sub(locale.value, record_date),
                                   minimum=minimum,
                                   maximum=maximum,
                                   locale=locale.value,
                                   recorded_at=pendulum.now(tz=model.TZ),
                                   recorded_for=record_date)


def _record_sub(locale: model.locale.Locale, date: pendulum.Date) -> URIRef:
    _, date_form = rdf.month_day_from_datetime(date)
    return rdf.plz_cl_ind_tem[locale.symbolised_name()] + "/" + date_form


def _fill_blanks(g, records):
    all_dates = sorted({rec.recorded_for for rec in records})
    period = set(pendulum.interval(all_dates[0], all_dates[-1]).range('days'))
    grouped = [(url, list(rec)) for url, rec in groupby(records, lambda rec: rec.locale.subject)]
    blanks = reduce(partial(_find_blanks, g, period), grouped, [])
    return blanks + records


def _find_blanks(g, period, acc, locale_temp_days):
    locale_sub, recordings = locale_temp_days
    locale = model.locale.locale_from_sub(g, sub=locale_sub)
    if locale.is_left():
        breakpoint()
    all_dates = {rec.recorded_for for rec in recordings}

    gaps = period - all_dates
    if not gaps:
        return acc
    return acc + [_create_blank_recording(locale.value, dt) for dt in gaps]


def _create_blank_recording(locale: model.locale.Locale, date):
    return MinMaxTemperatureRecord(_record_sub(locale, date),
                                   minimum=None,
                                   maximum=None,
                                   locale=locale,
                                   recorded_for=date)


## FIXES

def fix(g: repo.GraphRepo):
    return change_date_strategy(g)

def change_date_strategy(g: repo.GraphRepo):
    all_recs = repo.temperature.get_all_temperature_records(g)
    for s, _, _ in all_recs:
        triples = rdf.all_matching(g, (s, None, None))
        on_dt = rdf.triple_finder(rdf.isRecordedAtDateTime, triples, builder=rdf.literal_time_triple_parser)
        for_d = rdf.triple_finder(rdf.isRecordedForDate, triples)
        if not for_d:
            g.set((s, rdf.isRecordedForDate, Literal(on_dt.date())))
            g.set((s, rdf.isRecordedAtDateTime, Literal(on_dt.add(days=1, hours=8))))
    return monad.Right(g)