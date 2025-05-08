from functools import reduce, partial

import polars as pl

from climate import model, repo

schema = {'Locale': pl.Utf8,
          'RecordedAt': pl.Datetime(time_zone=model.TZ),
          'RecordedFor': pl.Date,
          'Min': pl.Decimal,
          'Max': pl.Decimal}


def locale_temperatures(g: repo.GraphRepo):
    records = model.temperature.get_all(g)
    return pl.DataFrame(_build_series_2(records), schema=schema)


def _build_series_2(all_records):
    return [list(row) for row in zip(*[_build_rec(rec) for rec in all_records])]


def _build_rec(record):
    return [record.locale.name,
            record.recorded_at,
            record.recorded_for,
            float(record.minimum) if record.minimum else None,
            float(record.maximum) if record.maximum else None]


def _build_series(records):
    date_series = sorted({rec.recorded_at.to_date_string() for rec in records})
    series = reduce(_max_min_series, sorted(records, key=lambda rec: rec.recorded_at), {})
    return {**{"Locale": [loc for loc in series.keys()]}, **_generate_temp_series(series, date_series)}


def _generate_temp_series(temp_series, date_series):
    return reduce(partial(_temps_dict, date_series), _transpose_temps_to_series(temp_series), {})


def _transpose_temps_to_series(recordings):
    return enumerate(list(zip(*[temp for temp in recordings.values()])))


def _temps_dict(date_series, acc, temp_column):
    date_indx, temp = temp_column
    return {**acc, **{date_series[date_indx]: list(temp)}}


def _max_min_series(acc, record):
    _min(acc, record)
    _max(acc, record)
    return acc


def _min(acc, record):
    if (key := _min_key(record)) in acc:
        acc[key].append(record.minimum)
    else:
        acc[key] = [record.minimum]
    return acc


def _max(acc, record):
    if (key := _max_key(record)) in acc:
        acc[key].append(record.maximum)
    else:
        acc[key] = [record.maximum]
    return acc


def _min_key(record) -> str:
    return f"{record.locale.name}-MIN"


def _max_key(record) -> str:
    return f"{record.locale.name}-MAX"
