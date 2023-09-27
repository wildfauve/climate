from __future__ import annotations
from typing import List, Union, Tuple
from dataclasses import dataclass
from itertools import groupby
from functools import reduce, partial
from decimal import Decimal

import pendulum
from rdflib import URIRef, Graph
from clojos_common.util import monad, tokeniser

from climate import model, repo, rdf


@dataclass
class MinMaxTemperatureRecord:
    subject: URIRef
    minimum: Decimal
    maximum: Decimal
    locale: model.locale.Locale
    recorded_at: pendulum.DateTime
    recorded_for: pendulum.Date


def record(g: repo.GraphRepo, locale: str, minimum: Decimal, maximum: Decimal, for_date=None):
    temp_record = _to_model(g, locale, minimum, maximum, for_date)
    if result := repo.temperature.upsert(g, temp_record):
        return monad.Right(temp_record)
    breakpoint()


def get_all(g: repo.GraphRepo) -> groupby:
    return _fill_blanks(list(map(_from_dto, repo.temperature.get_all(g))))


def _from_dto(record):
    locale = model.locale.to_locale(name=record.locale_name, subject=record.locale_subject)
    return MinMaxTemperatureRecord(subject=record.subject,
                                   minimum=record.minimum,
                                   maximum=record.maximum,
                                   locale=locale.value,
                                   recorded_at=record.recorded_at)


def _to_model(g: repo.GraphRepo,
              locale_name: str,
              minimum: Decimal,
              maximum: Decimal,
              for_date: str = None):
    locale = model.locale.locale_from_name(g, locale_name)
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


def _fill_blanks(records):
    all_dates = sorted({rec.recorded_at for rec in records})
    period = set(pendulum.period(all_dates[0], all_dates[-1]).range('days'))
    grouped = [(url, list(rec)) for url, rec in groupby(records, lambda rec: rec.locale.subject)]
    blanks = reduce(partial(_find_blanks, period), grouped, [])
    return blanks + records


def _find_blanks(period, acc, locale_groups):
    _, recordings = locale_groups
    all_dates = {rec.recorded_at for rec in recordings}

    gaps = period - all_dates
    if not gaps:
        return acc
    return acc + [_create_blank_recording(recordings[0].locale, dt) for dt in gaps]


def _create_blank_recording(locale, datetime):
    return MinMaxTemperatureRecord(_record_sub(locale, datetime),
                                   minimum=None,
                                   maximum=None,
                                   locale=locale,
                                   recorded_at=datetime)