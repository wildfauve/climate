import pendulum

from climate import model, rdf

def record_date(date: str = None):
    if not date:
        return now_date_in_tz()
    try_parse = rdf.safe_date_convert(date)
    if not try_parse.is_right():
        breakpoint()
    return try_parse.value.date()


def now_date_in_tz():
    return now_in_tz().date()

def now_in_tz():
    return pendulum.now(tz=model.TZ)

def default_day(format_as_date_str: bool = True):
    now = now_in_tz().subtract(days=1)
    if not format_as_date_str:
        return now
    return now.to_date_string()
