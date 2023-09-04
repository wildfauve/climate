from __future__ import annotations
from typing import List, Union
from dataclasses import dataclass
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
    date: pendulum.Date


def record(g: repo.GraphRepo, locale: str, minimum: Decimal, maximum: Decimal, date=None):
    temp_record = _to_model(g, locale, minimum, maximum, date)
    if result := repo.temperature.upsert(g, temp_record):
        return monad.Right(temp_record)
    breakpoint()


def _to_model(g: repo.GraphRepo, locale_name: str, minimum: float, maximum: float, date: str = None):
    locale = model.locale.locale_from_name(g, locale_name)
    if locale.is_left():
        breakpoint()
    record_date = _record_date(date)
    return MinMaxTemperatureRecord(subject=_record_sub(locale.value, record_date),
                                   minimum=minimum,
                                   maximum=maximum,
                                   locale=locale.value,
                                   date=record_date)


def _record_sub(locale: model.locale.Locale, date) -> URIRef:
    _, date_form = rdf.month_day_from_datetime(date)
    return rdf.plz_cl_ind_tem[locale.symbolised_name()] + "/" + date_form


def _record_date(date: str = None):
    if not date:
        return pendulum.now(tz=model.TZ)
    try_parse = rdf.safe_date_convert(date)
    if not try_parse.is_right():
        breakpoint()
    return try_parse.value
