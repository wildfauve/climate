import pendulum

from climate import model, rdf

def record_date(date: str = None):
    if not date:
        return pendulum.now(tz=model.TZ)
    try_parse = rdf.safe_date_convert(date)
    if not try_parse.is_right():
        breakpoint()
    return try_parse.value
