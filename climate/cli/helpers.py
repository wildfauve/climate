import pendulum

from climate import model, adapter


def channels():
    return [c.name.lower() for c in adapter.Channel]

def default_record_date():
    return model.helpers.default_day(format_as_date_str=True)